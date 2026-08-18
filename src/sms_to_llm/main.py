from fastapi import FastAPI

from sms_to_llm.endpoints import sms_router
from sms_to_llm.endpoints.health import router as health_router
from sms_to_llm.endpoints.version import router as version_router

app = FastAPI(title="sms-to-llm")
app.include_router(version_router)
app.include_router(health_router)
app.include_router(sms_router)
