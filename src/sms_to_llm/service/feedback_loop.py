from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.schema.conversation import FeedbackValue


class FeedbackLoopService:
    """Handle feedback responses before the normal LLM conversation flow."""

    def __init__(self, database: BaseDatabase) -> None:
        self.database = database

    def _normalize_feedback(self, value: str) -> FeedbackValue | None:
        normalized = value.strip().lower()
        if normalized == "1":
            return "positive"
        if normalized == "0":
            return "negative"
        return None

    def handle_feedback(self, phone_number: str, incoming_message: str) -> bool:
        feedback = self._normalize_feedback(incoming_message)
        if feedback is None:
            return False

        last_message = self.database.get_last_message(phone_number)
        if last_message is None:
            return False

        self.database.update_message_feedback(last_message.id, feedback)
        return True
