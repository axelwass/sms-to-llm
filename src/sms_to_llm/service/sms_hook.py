from sms_to_llm.schema.sms import SmsHookResponse, SmsIncomingMessage


class SmsHookService:
    def accept_message(self, payload: SmsIncomingMessage) -> SmsHookResponse:
        return SmsHookResponse.model_validate(
            {
                "accepted": True,
                "from": payload.from_,
                "body": payload.body,
                "messageId": payload.messageId,
                "timestamp": payload.timestamp,
            }
        )
