from typing import Any
from unittest.mock import Mock

from pytest import MonkeyPatch

from sms_to_llm.config import SettingsWithoutEnv
from sms_to_llm.database.base import BaseDatabase
from sms_to_llm.llm.base import BaseLLM
from sms_to_llm.schema.conversation import ConversationMessage
from sms_to_llm.schema.sms import SmsIncomingMessage
from sms_to_llm.service.feedback_loop import FeedbackLoopService
from sms_to_llm.service.sms_hook import SmsHookService

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


def test_sms_hook_endpoint_accepts_message_payload(
    client: Any,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    payload: dict[str, Any] = {
        "from": "+36123456789",
        "body": "Hi",
        "messageId": "SM123456789",
        "timestamp": "2026-07-27T12:00:00Z",
    }

    response: Any = client.post("/sms/hook", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert "<Message>Hello, I'm your LLM assistant.</Message>" in response.text


def test_sms_hook_endpoint_accepts_twilio_form_payload(
    client: Any,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "mock")

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
    assert response.headers["content-type"].startswith("application/xml")
    assert "<Message>Hello, I'm your LLM assistant.</Message>" in response.text


def test_sms_hook_endpoint_rejects_empty_body_with_400(client: Any) -> None:
    response: Any = client.post("/sms/hook", data="")

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing SMS payload"


def test_test_sms_hook_requires_bearer_token(client: Any) -> None:
    response: Any = client.post(
        "/test/sms/hook",
        json={
            "from": "+36123456789",
            "body": "Hi",
            "messageId": "SM123456789",
            "timestamp": "2026-07-27T12:00:00Z",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_test_sms_hook_accepts_valid_bearer_token(
    client: Any,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    response: Any = client.post(
        "/test/sms/hook",
        json={
            "from": "+36123456789",
            "body": "Hi",
            "messageId": "SM123456789",
            "timestamp": "2026-07-27T12:00:00Z",
        },
        headers={"Authorization": "Bearer user"},
    )

    assert response.status_code == 200
    assert response.json()["body"] == "Hello, I'm your LLM assistant."


def test_sms_hook_service_builds_history_and_sends_response() -> None:
    service = SmsHookService(
        llm=llm,
        database=database,
        settings=SettingsWithoutEnv(),
        feedback_loop=FeedbackLoopService(database=database),
        history_limit=2,
    )

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
    assert "System:" in prompt
    assert "User: First question" in prompt
    assert "User: Second question" in prompt
    database.store_message.assert_called_once()
    stored_message = database.store_message.call_args[0][0]
    assert stored_message.incomingMessage == "Second question"
    assert stored_message.llmResponse == "Hello, I'm your LLM assistant."


def test_sms_hook_service_short_circuits_on_feedback_input() -> None:
    llm.reset_mock()
    database.reset_mock()
    database.get_last_message.return_value = ConversationMessage(
        id="conv_1",
        phoneNumber="+36123456789",
        incomingMessage="First question",
        llmResponse="First answer",
        providerMessageId="SM1",
        status="completed",
        createdAt="2026-07-27T12:00:00Z",
    )
    database.update_message_feedback.return_value = (
        database.get_last_message.return_value.model_copy(update={"feedback": "positive"})
    )

    service = SmsHookService(
        llm=llm,
        database=database,
        settings=SettingsWithoutEnv(),
        feedback_loop=FeedbackLoopService(database=database),
        history_limit=2,
    )

    payload = SmsIncomingMessage.model_validate(
        {
            "from": "+36123456789",
            "body": "1",
            "messageId": "SM3",
            "timestamp": "2026-07-27T12:00:00Z",
        }
    )

    response = service.accept_message(payload)

    assert response.body == "Thanks for the feedback."
    llm.generate_response.assert_not_called()
    database.update_message_feedback.assert_called_once_with("conv_1", "positive")
