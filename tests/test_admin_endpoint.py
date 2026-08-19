from typing import Any
from uuid import uuid4

from sms_to_llm.database.factory import create_database
from sms_to_llm.schema.conversation import ConversationMessage


def test_admin_conversations_requires_admin_access(client: Any) -> None:
    response: Any = client.get(
        "/admin/conversations/me",
        headers={"Authorization": "Bearer user"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


def test_admin_conversations_returns_history_for_phone_number(client: Any) -> None:
    phone_number = f"me-{uuid4()}"
    database = create_database()
    database.store_message(
        ConversationMessage(
            id=f"conv_{uuid4()}",
            phoneNumber=phone_number,
            incomingMessage="hello",
            llmResponse="hi there",
            providerMessageId=f"SM{uuid4()}",
            status="completed",
            createdAt="2026-07-27T12:00:00Z",
        )
    )

    response: Any = client.get(
        f"/admin/conversations/{phone_number}",
        headers={"Authorization": "Bearer admin"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["phoneNumber"] == phone_number
    assert payload[0]["incomingMessage"] == "hello"
