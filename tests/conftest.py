from typing import Any

import pytest
from fastapi.testclient import TestClient

from sms_to_llm.main import app


@pytest.fixture
def client() -> Any:
    return TestClient(app)
