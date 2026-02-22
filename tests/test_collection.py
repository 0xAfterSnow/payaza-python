"""Tests for the updated Collections resource (Card endpoints only)."""

import responses as rsps
import pytest
from payaza import PayazaAPIError


# --------------------------------------------------
# Check 3DS Availability
# --------------------------------------------------

@rsps.activate
def test_check_3ds_availability(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/check_3ds_availability",
        json={"status": "success", "is_3ds": True},
        status=200,
    )

    resp = client.collections.check_3ds_availability(
        card_number="5531886652142950",
        currency="NGN",
    )

    assert resp["status"] == "success"
    assert resp["is_3ds"] is True


# --------------------------------------------------
# Charge Card
# --------------------------------------------------

@rsps.activate
def test_charge_card(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/",
        json={"status": "pending", "flw_ref": "FLW-001"},
        status=200,
    )

    resp = client.collections.charge_card(
        amount=2000,
        currency="NGN",
        first_name="Test",
        last_name="User",
        email_address="test@example.com",
        phone_number="08012345678",
        transaction_reference="TXN-003",
        description="Test charge",
        card_number="5531886652142950",
        expiry_month="09",
        expiry_year="32",
        security_code="564",
        callback_url="https://example.com/webhook",
    )

    assert resp["status"] == "pending"
    assert resp["flw_ref"] == "FLW-001"


# --------------------------------------------------
# Check Transaction Status
# --------------------------------------------------

@rsps.activate
def test_check_transaction_status(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/transaction_status",
        json={"status": "successful", "amount": 2000},
        status=200,
    )

    resp = client.collections.check_transaction_status("TXN-003")

    assert resp["status"] == "successful"
    assert resp["amount"] == 2000


# --------------------------------------------------
# Check Refund Status
# --------------------------------------------------

@rsps.activate
def test_check_refund_status(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/refund_status",
        json={"status": "completed"},
        status=200,
    )

    resp = client.collections.check_refund_status("REF-001")

    assert resp["status"] == "completed"


# --------------------------------------------------
# Error Handling Test
# --------------------------------------------------

@rsps.activate
def test_charge_card_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/",
        json={"message": "Invalid card"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.collections.charge_card(
            amount=2000,
            currency="NGN",
            first_name="Test",
            last_name="User",
            email_address="test@example.com",
            phone_number="08012345678",
            transaction_reference="TXN-004",
            description="Test charge",
            card_number="0000000000000000",
            expiry_month="09",
            expiry_year="32",
            security_code="000",
        )