from typing import Annotated

from fastapi import Depends

from sms_to_llm.config import Settings
from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.factory import create_database
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.llm.factory import create_llm
from sms_to_llm.service.feedback_loop import FeedbackLoopService
from sms_to_llm.service.sms_hook import SmsHookService


def get_settings() -> Settings:
    return Settings()


def get_llm(settings: Annotated[Settings, Depends(get_settings)]) -> BaseLLM:
    return create_llm(settings)


def get_database(settings: Annotated[Settings, Depends(get_settings)]) -> BaseDatabase:
    return create_database(settings)


def get_feedback_loop(
    database: Annotated[BaseDatabase, Depends(get_database)],
) -> FeedbackLoopService:
    return FeedbackLoopService(database=database)


def get_sms_hook_service(
    settings: Annotated[Settings, Depends(get_settings)],
    llm: Annotated[BaseLLM, Depends(get_llm)],
    database: Annotated[BaseDatabase, Depends(get_database)],
    feedback_loop: Annotated[FeedbackLoopService, Depends(get_feedback_loop)],
) -> SmsHookService:
    return SmsHookService(
        llm=llm,
        database=database,
        settings=settings,
        feedback_loop=feedback_loop,
    )
