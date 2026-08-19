from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.schema.conversation import ConversationMessage, FeedbackValue


class MongoDatabase(BaseDatabase):
    """In-memory Mongo-like database placeholder for conversation persistence."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._store: dict[str, list[ConversationMessage]] = {}

    def store_message(self, message: ConversationMessage) -> ConversationMessage:
        conversation = self._store.setdefault(message.phoneNumber, [])
        conversation.append(message)
        return message

    def get_last_message(self, phone_number: str) -> ConversationMessage | None:
        conversation = self._store.get(phone_number, [])
        if not conversation:
            return None
        return conversation[-1]

    def update_message_feedback(
        self, message_id: str, feedback: FeedbackValue | None
    ) -> ConversationMessage | None:
        for conversation in self._store.values():
            for index, message in enumerate(conversation):
                if message.id == message_id:
                    updated_message = message.model_copy(update={"feedback": feedback})
                    conversation[index] = updated_message
                    return updated_message
        return None

    def get_conversation(self, phone_number: str) -> list[ConversationMessage]:
        return list(self._store.get(phone_number, []))

    def list_messages(self, phone_number: str) -> list[ConversationMessage]:
        return self.get_conversation(phone_number)
