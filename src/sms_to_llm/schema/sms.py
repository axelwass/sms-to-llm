from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SmsIncomingMessage(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    from_: str = Field(validation_alias=AliasChoices("from", "From"), alias="from")
    body: str = Field(validation_alias=AliasChoices("body", "Body"))
    messageId: str = Field(
        validation_alias=AliasChoices("messageId", "MessageSid", "SmsMessageSid")
    )
    timestamp: str | None = Field(
        default=None,
        validation_alias=AliasChoices("timestamp", "Timestamp", "DateCreated"),
    )


class SmsHookResponse(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    accepted: bool
    from_: str = Field(alias="from")
    body: str
    messageId: str
    timestamp: str | None = None
