from pydantic import BaseModel, ConfigDict


class ConversationMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    phoneNumber: str
    incomingMessage: str
    llmResponse: str
    providerMessageId: str
    status: str
    createdAt: str
