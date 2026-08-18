from sms_to_llm.config import Settings
from sms_to_llm.sms.base import BaseSmsProvider
from sms_to_llm.sms.mock import MockSmsProvider
from sms_to_llm.sms.twilio import TwilioSmsProvider


def create_sms_provider(settings: Settings | None = None) -> BaseSmsProvider:
    resolved_settings = settings or Settings()
    provider_name = resolved_settings.sms_provider.lower()

    if provider_name == "mock":
        return MockSmsProvider()

    if provider_name == "twilio":
        has_credentials = bool(
            resolved_settings.twilio_account_sid
            and resolved_settings.twilio_auth_token
            and resolved_settings.twilio_phone_number
        )
        if has_credentials:
            return TwilioSmsProvider(settings=resolved_settings)
        return MockSmsProvider()

    raise ValueError(f"Unsupported SMS provider: {resolved_settings.sms_provider}")
