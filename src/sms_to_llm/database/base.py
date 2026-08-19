from abc import ABC, abstractmethod

from sms_to_llm.schema.conversation import ConversationMessage, FeedbackValue


class BaseDatabase(ABC):
    """Persistence interface for SMS conversations."""

    @abstractmethod
    def store_message(self, message: ConversationMessage) -> ConversationMessage:
        """Persist a completed conversation record keyed by phone number."""
        raise NotImplementedError

    @abstractmethod
    def get_last_message(self, phone_number: str) -> ConversationMessage | None:
        """Return the most recent message in a phone conversation."""
        raise NotImplementedError

    @abstractmethod
    def update_message_feedback(
        self, message_id: str, feedback: FeedbackValue | None
    ) -> ConversationMessage | None:
        """Update the feedback for a stored message by its unique message id."""
        raise NotImplementedError

    @abstractmethod
    def get_conversation(self, phone_number: str) -> list[ConversationMessage]:
        """Return the full conversation history for a phone number."""
        raise NotImplementedError

    @abstractmethod
    def list_messages(self, phone_number: str) -> list[ConversationMessage]:
        """Return the list of stored records for a conversation, in order."""
        raise NotImplementedError
