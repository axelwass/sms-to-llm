from sms_to_llm.config import Settings
from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.mongo import MongoDatabase

_MONGO_INSTANCES: dict[str, MongoDatabase] = {}


def create_database(settings: Settings | None = None) -> BaseDatabase:
    resolved_settings = settings or Settings()
    database_type = resolved_settings.database_type.lower()

    if database_type == "mongo":
        database_url = resolved_settings.database_url
        if database_url not in _MONGO_INSTANCES:
            _MONGO_INSTANCES[database_url] = MongoDatabase(database_url)
        return _MONGO_INSTANCES[database_url]

    raise ValueError(f"Unsupported database provider: {resolved_settings.database_type}")
