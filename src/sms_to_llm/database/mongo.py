from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.schema.conversation import ConversationMessage


class MongoDatabase(BaseDatabase):
    """In-memory Mongo-like database placeholder for conversation persistence."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._store: dict[str, list[ConversationMessage]] = {}

    def store_message(self, message: ConversationMessage) -> ConversationMessage:
        conversation = self._store.setdefault(message.phoneNumber, [])
        conversation.append(message)
        return message

    def get_conversation(self, phone_number: str) -> list[ConversationMessage]:
        return list(self._store.get(phone_number, []))

    def list_messages(self, phone_number: str) -> list[ConversationMessage]:
        return self.get_conversation(phone_number)
