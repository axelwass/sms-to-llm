from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.mock import MockLLM


def test_mock_llm_implements_base_contract() -> None:
    llm: BaseLLM = MockLLM()

    response = llm.generate_response("Help me draft a text reply")

    assert response == "Hello, I'm your LLM assistant."
