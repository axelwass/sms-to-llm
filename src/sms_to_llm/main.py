from fastapi import FastAPI

from sms_to_llm.config import Settings
from sms_to_llm.endpoints import sms_router
from sms_to_llm.endpoints.health import router as health_router
from sms_to_llm.endpoints.version import router as version_router

settings = Settings()
app = FastAPI(title="sms-to-llm")
app.include_router(version_router)
app.include_router(health_router)
app.include_router(sms_router)


def run() -> None:
    import uvicorn

    uvicorn.run("sms_to_llm.main:app", host="0.0.0.0", port=settings.port)


if __name__ == "__main__":
    run()
