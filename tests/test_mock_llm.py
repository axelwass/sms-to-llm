from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.mock import MockLLM


def test_mock_llm_returns_fixed_assistant_message() -> None:
    llm: BaseLLM = MockLLM()

    response = llm.generate_response("Hi.")

    assert response == "Hello, I'm your LLM assistant."


def test_mock_llm_ignores_input_and_returns_same_response() -> None:
    llm: BaseLLM = MockLLM()

    response = llm.generate_response("Other.")

    assert response == "Hello, I'm your LLM assistant."
