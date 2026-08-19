from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.database.mongo import MongoDatabase
from sms_to_llm.schema.conversation import ConversationMessage


def test_mongo_database_implements_base_contract() -> None:
    database: BaseDatabase = MongoDatabase("mongodb://localhost:27017/sms_to_llm")

    first_message = ConversationMessage(
        id="conv_123",
        phoneNumber="+36123456789",
        incomingMessage="How do I reset my password?",
        llmResponse="You can reset your password by clicking 'Forgot password' on the login page.",
        providerMessageId="SM123456789",
        status="completed",
        createdAt="2026-07-27T12:00:00Z",
    )
    second_message = ConversationMessage(
        id="conv_124",
        phoneNumber="+36123456789",
        incomingMessage="What about my billing?",
        llmResponse="You can review charges in the billing section.",
        providerMessageId="SM123456790",
        status="completed",
        createdAt="2026-07-27T12:05:00Z",
    )

    database.store_message(first_message)
    database.store_message(second_message)

    updated = database.update_message_feedback("conv_124", "positive")

    conversation = database.get_conversation("+36123456789")
    messages = database.list_messages("+36123456789")

    assert updated is not None
    assert updated.feedback == "positive"
    assert updated.providerMessageId == "SM123456790"
    assert conversation[-1].feedback == "positive"
    assert conversation[0].feedback is None
    assert messages == conversation
