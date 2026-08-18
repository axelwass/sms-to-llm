from typing import Any


def test_sms_hook_endpoint_accepts_message_payload(client: Any) -> None:
    payload: dict[str, Any] = {
        "from": "+36123456789",
        "body": "How do I reset my password?",
        "messageId": "SM123456789",
        "timestamp": "2026-07-27T12:00:00Z",
    }

    response: Any = client.post("/sms/hook", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "accepted": True,
        "from": "+36123456789",
        "messageId": "SM123456789",
        "body": "How do I reset my password?",
        "timestamp": "2026-07-27T12:00:00Z",
    }
