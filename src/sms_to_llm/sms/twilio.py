from twilio.rest import Client

from sms_to_llm.config import Settings
from sms_to_llm.sms.base import BaseSmsProvider


class TwilioSmsProvider(BaseSmsProvider):
    """Twilio-backed SMS provider."""

    def __init__(self, client: Client | None = None, settings: Settings | None = None) -> None:
        resolved_settings = settings or Settings()
        account_sid = resolved_settings.twilio_account_sid
        auth_token = resolved_settings.twilio_auth_token
        if account_sid is None or auth_token is None:
            raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be configured")

        self.client = client or Client(account_sid, auth_token)
        self.from_number = resolved_settings.twilio_phone_number

    def send_message(self, phone_number: str, message: str) -> str:
        if self.from_number is None:
            raise ValueError("TWILIO_PHONE_NUMBER is not configured")

        sent_message = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=phone_number,
        )
        message_sid = sent_message.sid
        if message_sid is None:
            raise ValueError("Twilio message was created without a message id")
        return message_sid
