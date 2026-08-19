from datetime import UTC, datetime
from pathlib import Path

from sms_to_llm.config import Settings
from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.factory import create_database
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.factory import create_llm
from sms_to_llm.schema.conversation import ConversationMessage
from sms_to_llm.schema.sms import SmsHookResponse, SmsIncomingMessage
from sms_to_llm.service.feedback_loop import FeedbackLoopService


class SmsHookService:
    def __init__(
        self,
        llm: BaseLLM | None = None,
        database: BaseDatabase | None = None,
        history_limit: int = 5,
    ) -> None:
        settings = Settings()
        self.llm = llm or create_llm(settings)
        self.database = database or create_database(settings)
        self.history_limit = history_limit
        self.feedback_loop = FeedbackLoopService(database=self.database)
        self.system_prompt = self._load_system_prompt(settings.system_prompt_path)

    def _load_system_prompt(self, prompt_path: str) -> str:
        path = Path(prompt_path)
        if not path.is_absolute():
            repo_root = Path(__file__).resolve().parents[3]
            path = repo_root / path

        try:
            return path.read_text(encoding="utf-8").strip()
        except OSError:
            return ""

    def _build_history_prompt(self, phone_number: str, incoming_message: str) -> str:
        history = self.database.get_conversation(phone_number)
        recent = history[-self.history_limit :] if self.history_limit > 0 else history

        parts: list[str] = []
        if self.system_prompt:
            parts.append("System:")
            parts.append(self.system_prompt)
            parts.append("")

        for item in recent:
            parts.append(f"User: {item.incomingMessage}")
            parts.append(f"Assistant: {item.llmResponse}")

        parts.append(f"User: {incoming_message}")
        parts.append("Assistant:")
        return "\n".join(parts)

    def accept_message(self, payload: SmsIncomingMessage) -> SmsHookResponse:
        timestamp = payload.timestamp or datetime.now(UTC).isoformat()

        if self.feedback_loop.handle_feedback(payload.from_, payload.body):
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

        return SmsHookResponse.model_validate(
            {
                "accepted": True,
                "from": payload.from_,
                "body": generated_response,
                "messageId": payload.messageId,
                "timestamp": timestamp,
            }
        )
