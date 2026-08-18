from abc import ABC, abstractmethod


class BaseSmsProvider(ABC):
    """Base interface for SMS delivery providers."""

    @abstractmethod
    def send_message(self, phone_number: str, message: str) -> str:
        """Send a text message to the given number and return a provider message id."""
        raise NotImplementedError
