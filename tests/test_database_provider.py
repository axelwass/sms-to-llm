from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.mongo import MongoDatabase
from sms_to_llm.schema.conversation import ConversationMessage


def test_mongo_database_implements_base_contract() -> None:
    database: BaseDatabase = MongoDatabase("mongodb://localhost:27017/sms_to_llm")

    message = ConversationMessage(
        id="conv_123",
        phoneNumber="+36123456789",
        incomingMessage="How do I reset my password?",
        llmResponse="You can reset your password by clicking 'Forgot password' on the login page.",
        providerMessageId="SM123456789",
        status="completed",
        createdAt="2026-07-27T12:00:00Z",
    )

    saved = database.store_message(message)

    conversation = database.get_conversation("+36123456789")
    messages = database.list_messages("+36123456789")

    assert saved.model_dump() == message.model_dump()
    assert conversation == [message]
    assert messages == conversation
