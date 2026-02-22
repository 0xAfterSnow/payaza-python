"""
Shared pytest fixtures for all test modules.
"""
import pytest
from payaza import Payaza

SANDBOX_URL = "https://api.payaza.africa"
TEST_API_KEY = "test_key_abc123"


@pytest.fixture
def client() -> Payaza:
    """Return a Payaza client pointed at the sandbox."""
    return Payaza(api_key=TEST_API_KEY, sandbox=True)


@pytest.fixture
def base_url() -> str:
    return SANDBOX_URL