"""Tests for the Payouts resource."""

import responses as rsps
import pytest
from payaza import PayazaAPIError


# --------------------------------------------------
# Initiate Payout
# --------------------------------------------------

@rsps.activate
def test_initiate_payout_ngn(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/payout-receptor/payout",
        json={
            "status": "success",
            "message": "Payout initiated successfully",
            "data": {
                "transaction_reference": "PO-123456"
            }
        },
        status=200,
    )

    resp = client.payouts.initiate_payout(
        transaction_type="nuban",
        payout_amount=5000.00,
        transaction_pin=1234,
        account_reference="5012345678",
        currency="NGN",
        payout_beneficiaries=[
            {
                "credit_amount": 5000.00,
                "account_number": "0123456789",
                "account_name": "John Doe",
                "bank_code": "011",
                "narration": "Test payout",
                "transaction_reference": "BEN-001",
            }
        ],
        sender={
            "sender_name": "Sender",
            "sender_phone_number": "08012345678",
            "sender_address": "Lagos",
        },
    )

    # Verify request payload
    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["transaction_type"] == "nuban"
    sp = body["service_payload"]
    assert sp["payout_amount"] == 5000.00
    assert sp["currency"] == "NGN"
    assert len(sp["payout_beneficiaries"]) == 1
    assert sp["sender"]["sender_name"] == "Sender"

    assert resp["status"] == "success"


@rsps.activate
def test_initiate_payout_xof_with_country(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/payout-receptor/payout",
        json={"status": "success"},
        status=200,
    )

    resp = client.payouts.initiate_payout(
        transaction_type="mobile_money",
        payout_amount=25000,
        transaction_pin=1234,
        account_reference="5012345678",
        currency="XOF",
        country="BEN",
        payout_beneficiaries=[
            {
                "credit_amount": 25000,
                "account_number": "22901012345678",
                "account_name": "Beneficiary",
                "bank_code": "BENCODE",
                "narration": "Paiement",
                "transaction_reference": "BEN-002",
            }
        ],
        sender={
            "sender_name": "Sender",
            "sender_phone_number": "22990000000",
            "sender_address": "Cotonou",
        },
    )

    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["service_payload"]["country"] == "BEN"
    assert resp["status"] == "success"


@rsps.activate
def test_initiate_payout_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/payout-receptor/payout",
        json={"message": "Invalid transaction pin"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.payouts.initiate_payout(
            transaction_type="nuban",
            payout_amount=1000,
            transaction_pin=0000,
            account_reference="5012345678",
            currency="NGN",
            payout_beneficiaries=[],
            sender={},
        )