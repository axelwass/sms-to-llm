from typing import Any, cast

from fastapi.testclient import TestClient

from sms_to_llm.main import app


def _get_json(path: str) -> dict[str, str]:
    client: Any = TestClient(app)
    response: Any = client.get(path)

    assert response.status_code == 200
    return cast(dict[str, str], response.json())


def test_version_endpoint_returns_about_version() -> None:
    assert _get_json("/version") == {"version": "0.1.0"}


def test_health_endpoint_returns_ok_status() -> None:
    assert _get_json("/health") == {"status": "ok"}
