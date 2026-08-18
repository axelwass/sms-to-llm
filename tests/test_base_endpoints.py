from typing import Any


def test_version_endpoint_returns_about_version(client: Any) -> None:
    response: Any = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}


def test_health_endpoint_returns_ok_status(client: Any) -> None:
    response: Any = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
