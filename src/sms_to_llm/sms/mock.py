from sms_to_llm.sms.base import BaseSmsProvider


class MockSmsProvider(BaseSmsProvider):
    """Local SMS mock used when no real provider credentials are configured."""

    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, str]] = []

    def send_message(self, phone_number: str, message: str) -> str:
        self.sent_messages.append((phone_number, message))
        return "mock-sms-message-id"
