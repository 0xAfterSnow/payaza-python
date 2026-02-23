"""Tests for account enquiry endpoints."""

import responses as rsps
import pytest
from payaza import PayazaAPIError


# --------------------------------------------------
# Fetch Account Details
# --------------------------------------------------

@rsps.activate
def test_fetch_account_details_success(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/payaza-account/api/v1/mainaccounts/merchant/provider/enquiry",
        json={
            "status": "success",
            "data": {
                "account_name": "JOHN DOE",
                "account_number": "0123456789",
                "bank_code": "011"
            }
        },
        status=200,
    )

    resp = client.accounts.fetch_account_details(
        currency="NGN",
        bank_code="011",
        account_number="0123456789"
    )

    # Verify request payload
    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert "service_payload" in body
    sp = body["service_payload"]
    assert sp["currency"] == "NGN"
    assert sp["bank_code"] == "011"
    assert sp["account_number"] == "0123456789"

    assert resp["status"] == "success"
    assert resp["data"]["account_name"] == "JOHN DOE"


@rsps.activate
def test_fetch_account_details_not_found(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/payaza-account/api/v1/mainaccounts/merchant/provider/enquiry",
        json={
            "status": "error",
            "message": "Account not found"
        },
        status=404,
    )

    with pytest.raises(PayazaAPIError) as excinfo:
        client.accounts.fetch_account_details(
            currency="NGN",
            bank_code="011",
            account_number="0000000000"
        )

    assert excinfo.value.status_code == 404
    assert "Account not found" in str(excinfo.value)


@rsps.activate
def test_fetch_account_details_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/payaza-account/api/v1/mainaccounts/merchant/provider/enquiry",
        json={"message": "Invalid bank code"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.accounts.fetch_account_details(
            currency="NGN",
            bank_code="999",
            account_number="0123456789"
        )