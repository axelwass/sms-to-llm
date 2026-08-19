import httpx

from sms_to_llm.llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    """LLM provider backed by a local or remote Ollama server."""

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: float = 30.0,
        max_tokens: int = 80,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens

    def generate_response(self, message: str) -> str:
        payload: dict[str, object] = {
            "model": self.model,
            "prompt": message,
            "stream": False,
        }

        if self.max_tokens > 0:
            payload["options"] = {"num_predict": self.max_tokens}

        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise RuntimeError("Ollama request failed") from exc

        data = response.json()
        generated_text = data.get("response")
        if not isinstance(generated_text, str) or not generated_text.strip():
            raise RuntimeError("Ollama returned an invalid response payload")

        return generated_text.strip()
