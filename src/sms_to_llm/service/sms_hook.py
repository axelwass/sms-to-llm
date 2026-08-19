from datetime import UTC, datetime

from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.factory import create_database
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.factory import create_llm
from sms_to_llm.schema.conversation import ConversationMessage
from sms_to_llm.schema.sms import SmsHookResponse, SmsIncomingMessage
from sms_to_llm.service.feedback_loop import FeedbackLoopService
from sms_to_llm.sms.base import BaseSmsProvider
from sms_to_llm.sms.factory import create_sms_provider


class SmsHookService:
    def __init__(
        self,
        llm: BaseLLM | None = None,
        database: BaseDatabase | None = None,
        sms_provider: BaseSmsProvider | None = None,
        history_limit: int = 5,
    ) -> None:
        self.llm = llm or create_llm()
        self.database = database or create_database()
        self.sms_provider = sms_provider or create_sms_provider()
        self.history_limit = history_limit
        self.feedback_loop = FeedbackLoopService(database=self.database)

    def _build_history_prompt(self, phone_number: str, incoming_message: str) -> str:
        history = self.database.get_conversation(phone_number)
        recent = history[-self.history_limit :] if self.history_limit > 0 else history

        parts: list[str] = []
        for item in recent:
            parts.append(f"User: {item.incomingMessage}")
            parts.append(f"Assistant: {item.llmResponse}")

        parts.append(f"User: {incoming_message}")
        return "\n".join(parts)

    def accept_message(self, payload: SmsIncomingMessage) -> SmsHookResponse:
        timestamp = payload.timestamp or datetime.now(UTC).isoformat()

        if self.feedback_loop.handle_feedback(payload.from_, payload.body):
            self.sms_provider.send_message(payload.from_, "Thanks for the feedback.")
            return SmsHookResponse.model_validate(
                {
                    "accepted": True,
                    "from": payload.from_,
                    "body": "Thanks for the feedback.",
                    "messageId": payload.messageId,
                    "timestamp": timestamp,
                }
            )

        prompt = self._build_history_prompt(payload.from_, payload.body)
        generated_response = self.llm.generate_response(prompt)

        message_record = ConversationMessage(
            id=f"conv_{payload.from_.replace('+', '')}_{payload.messageId}",
            phoneNumber=payload.from_,
            incomingMessage=payload.body,
            llmResponse=generated_response,
            providerMessageId=payload.messageId,
            status="completed",
            createdAt=timestamp,
        )
        self.database.store_message(message_record)
        self.sms_provider.send_message(payload.from_, generated_response)

        return SmsHookResponse.model_validate(
            {
                "accepted": True,
                "from": payload.from_,
                "body": generated_response,
                "messageId": payload.messageId,
                "timestamp": timestamp,
            }
        )
