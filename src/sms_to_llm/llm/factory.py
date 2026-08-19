from sms_to_llm.config import Settings
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.mock import MockLLM
from sms_to_llm.llm.ollama import OllamaLLM


def create_llm(settings: Settings | None = None) -> BaseLLM:
    resolved_settings = settings or Settings()
    provider_name = resolved_settings.llm_provider.lower()

    if provider_name == "mock":
        return MockLLM()

    if provider_name == "ollama":
        return OllamaLLM(
            base_url=resolved_settings.ollama_base_url,
            model=resolved_settings.ollama_model,
            timeout_seconds=resolved_settings.ollama_timeout_seconds,
            max_tokens=resolved_settings.ollama_max_tokens,
        )

    raise ValueError(f"Unsupported LLM provider: {resolved_settings.llm_provider}")
