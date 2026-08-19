import json
from typing import Annotated, Any
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from sms_to_llm.auth.authorization import require_user_key
from sms_to_llm.config import Settings
from sms_to_llm.dependencies import get_sms_hook_service
from sms_to_llm.schema.sms import SmsHookResponse, SmsIncomingMessage
from sms_to_llm.service.sms_hook import SmsHookService

router = APIRouter(prefix="/sms", tags=["sms"])
test_router = APIRouter(prefix="/test", tags=["test"])


async def _extract_sms_payload(request: Request) -> SmsIncomingMessage:
    content_type = request.headers.get("content-type", "").lower()
    body = await request.body()

    if not body:
        raise HTTPException(status_code=400, detail="Missing SMS payload")

    if content_type.startswith("application/x-www-form-urlencoded"):
        raw_payload: dict[str, Any] = dict(await request.form())
    elif content_type.startswith("application/json"):
        try:
            raw_payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc
    else:
        try:
            raw_payload = json.loads(body)
        except json.JSONDecodeError:
            parsed = parse_qs(body.decode("utf-8"), keep_blank_values=True)
            raw_payload = {key: values[0] if values else "" for key, values in parsed.items()}

    normalized_payload = {
        "from": raw_payload.get("from") or raw_payload.get("From"),
        "body": raw_payload.get("body") or raw_payload.get("Body"),
        "messageId": raw_payload.get("messageId")
        or raw_payload.get("MessageSid")
        or raw_payload.get("SmsMessageSid"),
        "timestamp": raw_payload.get("timestamp")
        or raw_payload.get("Timestamp")
        or raw_payload.get("DateCreated"),
    }

    try:
        return SmsIncomingMessage.model_validate(normalized_payload)
    except Exception as exc:  # pragma: no cover - endpoint validation guard
        raise HTTPException(status_code=400, detail="Invalid SMS payload") from exc


@router.post("/hook")
async def receive_sms_hook(
    request: Request,
    service: Annotated[SmsHookService, Depends(get_sms_hook_service)],
) -> Response:
    settings = Settings()
    payload = await _extract_sms_payload(request)

    signature = request.headers.get("X-Twilio-Signature")
    if settings.twilio_auth_token and signature:
        content_type = request.headers.get("content-type", "")
        form_data = (
            dict(await request.form())
            if content_type.startswith("application/x-www-form-urlencoded")
            else {}
        )
        validator: Any = RequestValidator(settings.twilio_auth_token)
        valid = bool(validator.validate(str(request.url), form_data, signature))
        if not valid:
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")

    response = service.accept_message(payload)

    twiml = MessagingResponse()
    twiml.message(response.body)  # type: ignore[reportUnknownMemberType]
    return Response(content=str(twiml), media_type="application/xml")


@test_router.post(
    "/sms/hook",
    response_model=SmsHookResponse,
    dependencies=[Depends(require_user_key)],
)
async def receive_test_sms_hook(
    payload: SmsIncomingMessage,
    service: Annotated[SmsHookService, Depends(get_sms_hook_service)],
) -> SmsHookResponse:
    response = service.accept_message(payload)
    if payload.timestamp is None:
        return response.model_copy(update={"timestamp": None})
    return response
