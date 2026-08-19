import httpx
import pytest

from sms_to_llm.llm.ollama import OllamaLLM

pytestmark = pytest.mark.integration


def _ollama_available(base_url: str) -> bool:
    try:
        response = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=2.0)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def test_ollama_llm_generate_response_integration(monkeypatch: pytest.MonkeyPatch) -> None:
    base_url = "http://localhost:11434"
    model = "tinyllama:1.1b"

    monkeypatch.setenv("OLLAMA_BASE_URL", base_url)
    monkeypatch.setenv("OLLAMA_MODEL", model)

    if not _ollama_available(base_url):
        pytest.skip("Ollama is not reachable at the configured base URL")

    llm = OllamaLLM(base_url=base_url, model=model)
    response = llm.generate_response("Reply with exactly: ok")

    assert isinstance(response, str)
    assert response.strip() != ""
