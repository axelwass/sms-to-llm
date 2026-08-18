from pydantic import BaseModel, ConfigDict


class VersionResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    version: str


class HealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: str
