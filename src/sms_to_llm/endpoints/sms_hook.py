from typing import Any

from fastapi import APIRouter, HTTPException, Request
from twilio.request_validator import RequestValidator

from sms_to_llm.config import Settings
from sms_to_llm.schema.sms import SmsHookResponse, SmsIncomingMessage
from sms_to_llm.service.sms_hook import SmsHookService

router = APIRouter(prefix="/sms", tags=["sms"])


async def _extract_sms_payload(request: Request) -> SmsIncomingMessage:
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("application/x-www-form-urlencoded"):
        form_data = await request.form()
        raw_payload: dict[str, Any] = dict(form_data)
    else:
        raw_payload = await request.json()

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
    return SmsIncomingMessage.model_validate(normalized_payload)


@router.post("/hook", response_model=SmsHookResponse)
async def receive_sms_hook(request: Request) -> SmsHookResponse:
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

    service = SmsHookService()
    response = service.accept_message(payload)
    if payload.timestamp is None:
        return response.model_copy(update={"timestamp": None})
    return response
