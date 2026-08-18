from abc import ABC, abstractmethod

from sms_to_llm.schema.conversation import ConversationMessage


class BaseDatabase(ABC):
    """Persistence interface for SMS conversations."""

    @abstractmethod
    def store_message(self, message: ConversationMessage) -> ConversationMessage:
        """Persist a completed conversation record keyed by phone number."""
        raise NotImplementedError

    @abstractmethod
    def get_conversation(self, phone_number: str) -> list[ConversationMessage]:
        """Return the full conversation history for a phone number."""
        raise NotImplementedError

    @abstractmethod
    def list_messages(self, phone_number: str) -> list[ConversationMessage]:
        """Return the list of stored records for a conversation, in order."""
        raise NotImplementedError
