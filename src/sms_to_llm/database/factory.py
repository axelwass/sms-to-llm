from sms_to_llm.config import Settings
from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.mongo import MongoDatabase


def create_database(settings: Settings | None = None) -> BaseDatabase:
    resolved_settings = settings or Settings()
    database_type = resolved_settings.database_type.lower()

    if database_type == "mongo":
        return MongoDatabase(resolved_settings.database_url)

    raise ValueError(f"Unsupported database provider: {resolved_settings.database_type}")
