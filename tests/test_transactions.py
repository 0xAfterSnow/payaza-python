"""Tests for transaction endpoints."""

import responses as rsps
import pytest
from payaza import PayazaAPIError


# --------------------------------------------------
# Get Transaction Status
# --------------------------------------------------

@rsps.activate
def test_get_transaction_status_success(client, base_url):
    txn_ref = "TXN-1234567890"
    rsps.add(
        rsps.GET,
        f"{base_url}/live/payaza-account/api/v1/mainaccounts/merchant/transaction/{txn_ref}",
        json={
            "status": "success",
            "data": {
                "transaction_reference": txn_ref,
                "status": "NIP_SUCCESS",
                "amount": 5000.00,
                "currency": "NGN",
                "timestamp": "2025-02-26T10:30:00Z"
            }
        },
        status=200,
    )

    resp = client.transactions.get_transaction_status(txn_ref)

    assert resp["status"] == "success"
    assert resp["data"]["status"] == "NIP_SUCCESS"
    assert resp["data"]["transaction_reference"] == txn_ref


@rsps.activate
def test_get_transaction_status_pending(client, base_url):
    txn_ref = "TXN-PENDING-001"
    rsps.add(
        rsps.GET,
        f"{base_url}/live/payaza-account/api/v1/mainaccounts/merchant/transaction/{txn_ref}",
        json={
            "status": "success",
            "data": {
                "transaction_reference": txn_ref,
                "status": "NIP_PENDING",
                "amount": 2500.00,
                "currency": "NGN"
            }
        },
        status=200,
    )

    resp = client.transactions.get_transaction_status(txn_ref)

    assert resp["status"] == "success"
    assert resp["data"]["status"] == "NIP_PENDING"


@rsps.activate
def test_get_transaction_status_not_found(client, base_url):
    txn_ref = "TXN-INVALID-999"
    rsps.add(
        rsps.GET,
        f"{base_url}/live/payaza-account/api/v1/mainaccounts/merchant/transaction/{txn_ref}",
        json={"message": "Transaction not found"},
        status=404,
    )

    with pytest.raises(PayazaAPIError) as excinfo:
        client.transactions.get_transaction_status(txn_ref)

    assert excinfo.value.status_code == 404
    assert excinfo.value.response["message"] == "Transaction not found"