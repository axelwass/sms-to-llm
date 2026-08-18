from sms_to_llm.config import Settings
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.mock import MockLLM


def create_llm(settings: Settings | None = None) -> BaseLLM:
    resolved_settings = settings or Settings()
    provider_name = resolved_settings.llm_provider.lower()

    if provider_name == "mock":
        return MockLLM()

    raise ValueError(f"Unsupported LLM provider: {resolved_settings.llm_provider}")
