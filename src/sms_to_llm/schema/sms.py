from pydantic import BaseModel, ConfigDict, Field


class SmsIncomingMessage(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    from_: str = Field(alias="from")
    body: str
    messageId: str
    timestamp: str


class SmsHookResponse(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    accepted: bool
    from_: str = Field(alias="from")
    body: str
    messageId: str
    timestamp: str
