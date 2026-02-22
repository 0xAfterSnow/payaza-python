"""Tests for the Virtual Accounts resource."""

import responses as rsps
import pytest
from payaza import PayazaAPIError


# --------------------------------------------------
# Create Dynamic Virtual Account
# --------------------------------------------------

@rsps.activate
def test_create_dynamic_virtual_account(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
        json={
            "status": "success",
            "account_number": "1234567890",
            "bank_name": "78 FINANCE COMPANY LIMITED",
            "account_name": "John Doe",
            "account_reference": "VA-123abc",
        },
        status=200,
    )

    resp = client.virtual_accounts.create_dynamic_virtual_account(
        account_name="John Doe",
        account_type="Dynamic",
        bank_code="1067",
        account_reference="VA-123abc",
        customer_first_name="John",
        customer_last_name="Doe",
        customer_email="john@example.com",
        customer_phone_number="08012345678",
        transaction_amount=5000.00,
        bvn="12345678901",
        has_amount_validation=True,
        transaction_description="Test payment",
        expires_in_minutes=45,
    )

    # Verify the request payload (optional)
    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["account_name"] == "John Doe"
    assert body["bank_code"] == "1067"
    assert body["bvn"] == "12345678901"
    assert body["has_amount_validation"] is True
    assert body["expires_in_minutes"] == 45

    assert resp["status"] == "success"
    assert resp["account_number"] == "1234567890"


@rsps.activate
def test_create_dynamic_virtual_account_minimal(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
        json={
            "status": "success",
            "account_number": "0987654321",
            "bank_name": "FIDELITY BANK LIMITED",
            "account_name": "Jane Doe",
            "account_reference": "VA-456def",
        },
        status=200,
    )

    resp = client.virtual_accounts.create_dynamic_virtual_account(
        account_name="Jane Doe",
        bank_code="117",
        account_reference="VA-456def",
        customer_first_name="Jane",
        customer_last_name="Doe",
        customer_email="jane@example.com",
        customer_phone_number="08087654321",
        transaction_amount=2500.00,
    )

    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["account_type"] == "Dynamic"  # default
    assert "bvn" not in body
    assert "has_amount_validation" not in body
    assert "expires_in_minutes" not in body

    assert resp["status"] == "success"
    assert resp["account_number"] == "0987654321"


@rsps.activate
def test_create_dynamic_virtual_account_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
        json={"message": "Invalid bank code"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.virtual_accounts.create_dynamic_virtual_account(
            account_name="Error Test",
            bank_code="999",
            account_reference="VA-999",
            customer_first_name="Error",
            customer_last_name="Test",
            customer_email="error@example.com",
            customer_phone_number="08000000000",
            transaction_amount=100.00,
        )


# --------------------------------------------------
# Create Static Virtual Account
# --------------------------------------------------

@rsps.activate
def test_create_static_virtual_account(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
        json={
            "status": "success",
            "account_number": "1122334455",
            "bank_name": "78 FINANCE COMPANY LIMITED",
            "account_name": "John Doe Static",
            "account_reference": "STATIC-123abc",
        },
        status=200,
    )

    resp = client.virtual_accounts.create_static_virtual_account(
        account_name="John Doe Static",
        bank_code="1067",
        bvn="12345678901",
        bvn_validated=True,
        account_reference="STATIC-123abc",
        customer_first_name="John",
        customer_last_name="Doe",
        customer_email="john@example.com",
        customer_phone_number="08012345678",
    )

    # Verify the request payload
    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["account_type"] == "Static"  # default
    assert body["bvn"] == "12345678901"
    assert body["bvn_validated"] is True
    assert body["account_reference"] == "STATIC-123abc"
    assert "transaction_amount" not in body  # static accounts don't have amount

    assert resp["status"] == "success"
    assert resp["account_number"] == "1122334455"


@rsps.activate
def test_create_static_virtual_account_minimal(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
        json={
            "status": "success",
            "account_number": "9988776655",
            "bank_name": "FIDELITY BANK LIMITED",
            "account_name": "Jane Doe Static",
            "account_reference": "STATIC-456def",
        },
        status=200,
    )

    resp = client.virtual_accounts.create_static_virtual_account(
        account_name="Jane Doe Static",
        bank_code="117",
        bvn="98765432109",
        bvn_validated=False,
        account_reference="STATIC-456def",
        customer_first_name="Jane",
        customer_last_name="Doe",
        customer_email="jane@example.com",
        customer_phone_number="08087654321",
    )

    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["bvn_validated"] is False

    assert resp["status"] == "success"
    assert resp["account_number"] == "9988776655"


@rsps.activate
def test_create_static_virtual_account_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
        json={"message": "BVN already in use"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.virtual_accounts.create_static_virtual_account(
            account_name="Error Test",
            bank_code="1067",
            bvn="00000000000",
            bvn_validated=True,
            account_reference="STATIC-999",
            customer_first_name="Error",
            customer_last_name="Test",
            customer_email="error@example.com",
            customer_phone_number="08000000000",
        )

# --------------------------------------------------
# Get Virtual Account Status
# --------------------------------------------------

@rsps.activate
def test_get_virtual_account_status(client, base_url):
    account_number = "7000009201"
    rsps.add(
        rsps.GET,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/detail/virtual_account/{account_number}",
        json={
            "status": "success",
            "account_number": account_number,
            "account_name": "John Doe Static",
            "bank_name": "78 FINANCE COMPANY LIMITED",
            "balance": 5000.00,
            "is_active": True,
            "created_at": "2025-01-15T10:30:00Z",
        },
        status=200,
    )

    resp = client.virtual_accounts.get_virtual_account_status(account_number)

    assert resp["status"] == "success"
    assert resp["account_number"] == account_number
    assert resp["is_active"] is True


@rsps.activate
def test_get_virtual_account_status_not_found(client, base_url):
    account_number = "9999999999"
    rsps.add(
        rsps.GET,
        f"{base_url}/live/merchant-collection/merchant/virtual_account/detail/virtual_account/{account_number}",
        json={"message": "Virtual account not found"},
        status=404,
    )

    with pytest.raises(PayazaAPIError) as excinfo:
        client.virtual_accounts.get_virtual_account_status(account_number)

    assert excinfo.value.status_code == 404
    assert excinfo.value.response["message"] == "Virtual account not found"