from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    port: int = Field(default=3000, alias="PORT")
    twilio_auth_token: str | None = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1", alias="OLLAMA_MODEL")
    ollama_timeout_seconds: float = Field(default=90.0, alias="OLLAMA_TIMEOUT_SECONDS")
    ollama_max_tokens: int = Field(default=80, alias="OLLAMA_MAX_TOKENS")
    system_prompt_path: str = Field(
        default="prompts/system_prompt.md",
        alias="SYSTEM_PROMPT_PATH",
    )
    admin_username: str = Field(default="admin", alias="ADMIN_USERNAME")
    admin_password: str = Field(default="password", alias="ADMIN_PASSWORD")
    database_type: str = Field(default="mongo", alias="DATABASE_TYPE")
    database_url: str = Field(
        default="mongodb://localhost:27017/sms_to_llm",
        alias="DATABASE_URL",
    )


class SettingsWithoutEnv(Settings):
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
