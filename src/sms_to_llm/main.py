from fastapi import FastAPI

from sms_to_llm.__about__ import __version__
from sms_to_llm.schemas import HealthResponse, VersionResponse

app = FastAPI(title="sms-to-llm")


@app.get("/version", response_model=VersionResponse)
def get_version() -> VersionResponse:
    return VersionResponse(version=__version__)


@app.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
