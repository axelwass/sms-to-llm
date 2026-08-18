from pytest import MonkeyPatch

from sms_to_llm.config import SettingsWithoutEnv
from sms_to_llm.sms.factory import create_sms_provider


def test_sms_provider_factory_uses_twilio_when_configured(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("SMS_PROVIDER", "twilio")
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "acct_123")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "auth_123")
    monkeypatch.setenv("TWILIO_PHONE_NUMBER", "+15551234567")

    provider = create_sms_provider(SettingsWithoutEnv())

    assert provider.__class__.__name__ == "TwilioSmsProvider"


def test_sms_provider_factory_falls_back_to_mock_when_credentials_missing(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("SMS_PROVIDER", "twilio")
    monkeypatch.delenv("TWILIO_ACCOUNT_SID", raising=False)
    monkeypatch.delenv("TWILIO_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("TWILIO_PHONE_NUMBER", raising=False)

    provider = create_sms_provider(SettingsWithoutEnv())

    assert provider.__class__.__name__ == "MockSmsProvider"
