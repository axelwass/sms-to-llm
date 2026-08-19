from pytest import MonkeyPatch

from sms_to_llm.config import SettingsWithoutEnv


def test_settings_loads_from_environment(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("PORT", "4000")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "auth_123")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OLLAMA_MAX_TOKENS", "64")
    monkeypatch.setenv("SYSTEM_PROMPT_PATH", "prompts/system_prompt.md")
    monkeypatch.setenv("ADMIN_USERNAME", "ops")
    monkeypatch.setenv("ADMIN_PASSWORD", "super-secret")
    monkeypatch.setenv("DATABASE_URL", "mongodb://localhost:27017/sms_to_llm")

    settings = SettingsWithoutEnv()

    assert settings.port == 4000
    assert settings.twilio_auth_token == "auth_123"
    assert settings.llm_provider == "openai"
    assert settings.openai_api_key == "sk-test"
    assert settings.ollama_max_tokens == 64
    assert settings.system_prompt_path == "prompts/system_prompt.md"
    assert settings.admin_username == "ops"
    assert settings.admin_password == "super-secret"
    assert settings.database_url == "mongodb://localhost:27017/sms_to_llm"


def test_settings_uses_safe_defaults_when_env_missing(monkeypatch: MonkeyPatch) -> None:
    for key in [
        "PORT",
        "TWILIO_AUTH_TOKEN",
        "LLM_PROVIDER",
        "OPENAI_API_KEY",
        "OLLAMA_MAX_TOKENS",
        "SYSTEM_PROMPT_PATH",
        "ADMIN_USERNAME",
        "ADMIN_PASSWORD",
        "DATABASE_URL",
    ]:
        monkeypatch.delenv(key, raising=False)

    settings = SettingsWithoutEnv()

    assert settings.port == 3000
    assert settings.llm_provider == "mock"
    assert settings.ollama_max_tokens == 80
    assert settings.system_prompt_path == "prompts/system_prompt.md"
    assert settings.admin_username == "admin"
    assert settings.admin_password == "password"
    assert settings.twilio_auth_token is None
    assert settings.database_url == "mongodb://localhost:27017/sms_to_llm"
