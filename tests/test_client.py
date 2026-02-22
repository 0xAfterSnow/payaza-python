"""
Tests for the core Payaza client — init, auth headers, error handling.
"""
import pytest
import responses as rsps

from payaza import Payaza, PayazaAPIError, PayazaAuthError, PayazaNetworkError


def test_requires_api_key():
    with pytest.raises(ValueError):
        Payaza(api_key="")


def test_live_base_url():
    c = Payaza(api_key="key")
    assert c.base_url == "https://api.payaza.africa"

def test_resources_are_attached(client):
    assert hasattr(client, "collections")