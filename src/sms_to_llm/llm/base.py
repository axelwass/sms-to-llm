from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Base interface for any LLM provider used by the SMS service."""

    @abstractmethod
    def generate_response(self, message: str) -> str:
        """Return a text answer for the provided incoming message."""
        raise NotImplementedError
