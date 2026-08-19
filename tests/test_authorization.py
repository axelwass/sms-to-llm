import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from sms_to_llm.auth.authorization import AuthorizationService


def _credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_authorization_service_authorizes_known_users() -> None:
    service = AuthorizationService()

    assert service.is_authorized("admin") is True
    assert service.is_authorized("user") is True
    assert service.is_authorized("someone") is False


def test_authorization_service_recognizes_admins() -> None:
    service = AuthorizationService()

    assert service.is_admin("admin") is True
    assert service.is_admin("user") is False


def test_ensure_user_rejects_unknown_token() -> None:
    service = AuthorizationService()

    with pytest.raises(HTTPException) as exc_info:
        service.ensure_user(_credentials("unknown"))

    assert exc_info.value.status_code == 401


def test_ensure_admin_rejects_non_admin_user() -> None:
    service = AuthorizationService()

    with pytest.raises(HTTPException) as exc_info:
        service.ensure_admin(_credentials("user"))

    assert exc_info.value.status_code == 403


def test_ensure_admin_accepts_admin() -> None:
    service = AuthorizationService()

    service.ensure_admin(_credentials("admin"))
