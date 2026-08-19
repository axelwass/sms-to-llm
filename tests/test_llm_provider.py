from sms_to_llm.config import SettingsWithoutEnv
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.factory import create_llm
from sms_to_llm.llm.mock import MockLLM
from sms_to_llm.llm.ollama import OllamaLLM


def test_mock_llm_implements_base_contract() -> None:
    llm: BaseLLM = MockLLM()

    response = llm.generate_response("Help me draft a text reply")

    assert response == "Hello, I'm your LLM assistant."


def test_factory_creates_ollama_provider() -> None:
    settings = SettingsWithoutEnv.model_validate(
        {
            "LLM_PROVIDER": "ollama",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_MODEL": "llama3.1",
            "OLLAMA_MAX_TOKENS": 55,
        }
    )

    llm = create_llm(settings)

    assert isinstance(llm, OllamaLLM)
    assert llm.max_tokens == 55
