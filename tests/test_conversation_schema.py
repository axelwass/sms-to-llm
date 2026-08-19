import pytest
from pydantic import ValidationError

from sms_to_llm.schema.conversation import ConversationMessage


def test_conversation_message_schema_accepts_record_shape() -> None:
    message = ConversationMessage(
        id="conv_123",
        phoneNumber="+36123456789",
        incomingMessage="How do I reset my password?",
        llmResponse=(
            "You can reset your password by clicking 'Forgot password' on the login page."
        ),
        providerMessageId="SM123456789",
        status="completed",
        createdAt="2026-07-27T12:00:00Z",
        feedback="positive",
    )

    assert message.model_dump() == {
        "id": "conv_123",
        "phoneNumber": "+36123456789",
        "incomingMessage": "How do I reset my password?",
        "llmResponse": (
            "You can reset your password by clicking 'Forgot password' on the login page."
        ),
        "providerMessageId": "SM123456789",
        "status": "completed",
        "createdAt": "2026-07-27T12:00:00Z",
        "feedback": "positive",
    }

    with pytest.raises(ValidationError):
        ConversationMessage.model_validate(
            {
                "id": "conv_124",
                "phoneNumber": "+36123456789",
                "incomingMessage": "Can I change my plan?",
                "llmResponse": "Yes, you can change it from Settings.",
                "providerMessageId": "SM123456790",
                "status": "completed",
                "createdAt": "2026-07-27T12:05:00Z",
                "feedback": "none",
            }
        )
