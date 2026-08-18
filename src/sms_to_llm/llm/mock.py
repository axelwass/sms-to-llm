from sms_to_llm.llm.base import BaseLLM


class MockLLM(BaseLLM):
    """Simple mock provider that always returns the same assistant greeting."""

    def generate_response(self, message: str) -> str:
        _ = message
        return "Hello, I'm your LLM assistant."
