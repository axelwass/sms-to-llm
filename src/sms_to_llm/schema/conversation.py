from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

FeedbackValue = Literal["positive", "negative"]


class ConversationMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    phoneNumber: str
    incomingMessage: str
    llmResponse: str
    providerMessageId: str
    status: str
    createdAt: str
    feedback: FeedbackValue | None = Field(default=None)
