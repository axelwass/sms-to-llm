from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from sms_to_llm.config import Settings

router = APIRouter(prefix="/llm", tags=["llm"])


class LlmRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    prompt: str


class LlmResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    response: str
    provider: str


@router.post("/generate", response_model=LlmResponse)
def generate_response(payload: LlmRequest) -> LlmResponse:
    settings = Settings()
    prompt = payload.prompt.strip()

    if not prompt:
        return LlmResponse(
            response="I need a prompt before I can help with that.",
            provider=settings.llm_provider,
        )

    normalized = prompt.lower()
    if any(
        keyword in normalized
        for keyword in ["phish", "steal password", "reveal a password", "trick user"]
    ):
        response = (
            "I can’t help with that request. I can help with a safe alternative such as "
            "a phishing awareness tip or a legitimate email security example."
        )
    else:
        response = (
            "This is a mock LLM response. For a safe, useful example, I can help you summarize "
            "password manager security best practices, phishing awareness, or other legitimate "
            "security guidance."
        )

    return LlmResponse(response=response, provider=settings.llm_provider)
