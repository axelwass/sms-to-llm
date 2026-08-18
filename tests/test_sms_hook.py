from typing import Any
from unittest.mock import Mock

from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.schema.conversation import ConversationMessage
from sms_to_llm.schema.sms import SmsIncomingMessage
from sms_to_llm.service.sms_hook import SmsHookService
from sms_to_llm.sms.base import BaseSmsProvider

llm = Mock(spec=BaseLLM)
llm.generate_response.return_value = "Hello, I'm your LLM assistant."

database = Mock(spec=BaseDatabase)
database.get_conversation.return_value = [
    ConversationMessage(
        id="conv_1",
        phoneNumber="+36123456789",
        incomingMessage="First question",
        llmResponse="First answer",
        providerMessageId="SM1",
        status="completed",
        createdAt="2026-07-27T12:00:00Z",
    )
]

sms_provider = Mock(spec=BaseSmsProvider)
sms_provider.send_message.return_value = "sms_123"


def test_sms_hook_endpoint_accepts_message_payload(client: Any) -> None:
    payload: dict[str, Any] = {
        "from": "+36123456789",
        "body": "Hi",
        "messageId": "SM123456789",
        "timestamp": "2026-07-27T12:00:00Z",
    }

    response: Any = client.post("/sms/hook", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "accepted": True,
        "from": "+36123456789",
        "messageId": "SM123456789",
        "body": "Hello, I'm your LLM assistant.",
        "timestamp": "2026-07-27T12:00:00Z",
    }


def test_sms_hook_endpoint_accepts_twilio_form_payload(client: Any) -> None:
    payload = {
        "From": "+36123456789",
        "Body": "Hello from Twilio",
        "MessageSid": "SM123456789",
        "MessageStatus": "received",
        "To": "+15005550006",
    }

    response: Any = client.post(
        "/sms/hook",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert response.json()["from"] == "+36123456789"
    assert response.json()["body"] == "Hello, I'm your LLM assistant."
    assert response.json()["messageId"] == "SM123456789"


def test_sms_hook_service_builds_history_and_sends_response() -> None:
    service = SmsHookService(llm=llm, database=database, sms_provider=sms_provider, history_limit=2)

    payload = SmsIncomingMessage.model_validate(
        {
            "from": "+36123456789",
            "body": "Second question",
            "messageId": "SM2",
            "timestamp": "2026-07-27T12:00:00Z",
        }
    )

    response = service.accept_message(payload)

    assert response.body == "Hello, I'm your LLM assistant."
    llm.generate_response.assert_called_once()
    prompt = llm.generate_response.call_args[0][0]
    assert prompt.startswith("User: First question")
    assert "User: Second question" in prompt
    sms_provider.send_message.assert_called_once_with(
        "+36123456789",
        "Hello, I'm your LLM assistant.",
    )
    database.store_message.assert_called_once()
    stored_message = database.store_message.call_args[0][0]
    assert stored_message.incomingMessage == "Second question"
    assert stored_message.llmResponse == "Hello, I'm your LLM assistant."
