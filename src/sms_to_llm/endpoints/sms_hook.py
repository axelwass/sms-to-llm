from fastapi import APIRouter

from sms_to_llm.schema.sms import SmsHookResponse, SmsIncomingMessage
from sms_to_llm.service.sms_hook import SmsHookService

router = APIRouter(prefix="/sms", tags=["sms"])


@router.post("/hook", response_model=SmsHookResponse)
def receive_sms_hook(payload: SmsIncomingMessage) -> SmsHookResponse:
    service = SmsHookService()
    return service.accept_message(payload)
