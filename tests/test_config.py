from pytest import MonkeyPatch

from sms_to_llm.config import SettingsWithoutEnv


def test_settings_loads_from_environment(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("PORT", "4000")
    monkeypatch.setenv("SMS_PROVIDER", "twilio")
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "acct_123")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "auth_123")
    monkeypatch.setenv("TWILIO_PHONE_NUMBER", "+15551234567")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("ADMIN_USERNAME", "ops")
    monkeypatch.setenv("ADMIN_PASSWORD", "super-secret")
    monkeypatch.setenv("DATABASE_URL", "mongodb://localhost:27017/sms_to_llm")

    settings = SettingsWithoutEnv()

    assert settings.port == 4000
    assert settings.sms_provider == "twilio"
    assert settings.twilio_account_sid == "acct_123"
    assert settings.twilio_auth_token == "auth_123"
    assert settings.twilio_phone_number == "+15551234567"
    assert settings.llm_provider == "openai"
    assert settings.openai_api_key == "sk-test"
    assert settings.admin_username == "ops"
    assert settings.admin_password == "super-secret"
    assert settings.database_url == "mongodb://localhost:27017/sms_to_llm"


def test_settings_uses_safe_defaults_when_env_missing(monkeypatch: MonkeyPatch) -> None:
    for key in [
        "PORT",
        "SMS_PROVIDER",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER",
        "LLM_PROVIDER",
        "OPENAI_API_KEY",
        "ADMIN_USERNAME",
        "ADMIN_PASSWORD",
        "DATABASE_URL",
    ]:
        monkeypatch.delenv(key, raising=False)

    settings = SettingsWithoutEnv()

    assert settings.port == 3000
    assert settings.sms_provider == "mock"
    assert settings.llm_provider == "mock"
    assert settings.admin_username == "admin"
    assert settings.admin_password == "password"
    assert settings.twilio_account_sid is None
    assert settings.database_url == "mongodb://localhost:27017/sms_to_llm"
