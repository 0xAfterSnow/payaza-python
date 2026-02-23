"""Tests for the updated Collections resource (Card endpoints only)."""

import responses as rsps
import pytest
from payaza import PayazaAPIError, PayazaAuthError
from responses import matchers


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


# --------------------------------------------------
# Initiate Mobile Payment (Apple Pay / Google Pay)
# --------------------------------------------------

@rsps.activate
def test_initiate_mobile_payment_apple(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/mobile_payment/initiate",
        json={"status": "success", "payment_url": "https://payments.payaza.africa/applepay/123"},
        status=200,
    )

    resp = client.collections.initiate_mobile_payment(
        amount=49.99,
        first_name="John",
        last_name="Doe",
        payment_option="APPLEPAY",
        description="Digital goods",
        transaction_reference="MOB-001",
        country_code="USA",
        currency_code="USD",
        redirect_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        error_url="https://example.com/error",
    )

    assert resp["status"] == "success"
    assert "payment_url" in resp


@rsps.activate
def test_initiate_mobile_payment_google(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/mobile_payment/initiate",
        json={"status": "success", "payment_url": "https://payments.payaza.africa/googlepay/456"},
        status=200,
    )

    resp = client.collections.initiate_mobile_payment(
        amount=79.99,
        first_name="Jane",
        last_name="Smith",
        payment_option="GOOGLEPAY",
        description="Subscription",
        transaction_reference="MOB-002",
        country_code="GBR",
        currency_code="GBP",
    )

    assert resp["status"] == "success"
    assert "payment_url" in resp


@rsps.activate
def test_initiate_mobile_payment_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/merchant-collection/mobile_payment/initiate",
        json={"message": "Invalid payment option"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.collections.initiate_mobile_payment(
            amount=10.00,
            first_name="Error",
            last_name="User",
            payment_option="INVALID",
            description="Test error",
            transaction_reference="MOB-003",
            country_code="XXX",
            currency_code="USD",
        )

# --------------------------------------------------
# Card Tokenization
# --------------------------------------------------

@rsps.activate
def test_tokenize_card_success_verification_success(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/merchant/tokenization/token",
        json={
            "success": True,
            "token": "TOK-001",
            "verification_charge_status": "success",
            "message": "Token created successfully. Verification charge of 50.00 NGN completed."
        },
        status=200,
    )

    resp = client.collections.tokenize_card(
        card_number="4508750015741019",
        expiry_month="01",
        expiry_year="2039",
        cvv="100",
        merchant_reference="TOK-001",
        currency="NGN",
        first_name="Shagbaor",
        last_name="Agber",
        email_address="test@example.com",
        callback_url="https://example.com/callback",
    )

    # Verify payload
    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert body["merchant_reference"] == "TOK-001"
    assert body["callback_url"] == "https://example.com/callback"

    assert resp["success"] is True
    assert resp["token"] == "TOK-001"
    assert resp["verification_charge_status"] == "success"


@rsps.activate
def test_tokenize_card_success_verification_failed(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/merchant/tokenization/token",
        json={
            "success": True,
            "token": "TOK-002",
            "verification_charge_status": "failed",
            "verification_charge_message": "Insufficient funds",
            "message": "Token created successfully. However, the verification charge failed."
        },
        status=200,
    )

    resp = client.collections.tokenize_card(
        card_number="4508750015741019",
        expiry_month="01",
        expiry_year="2039",
        cvv="100",
        merchant_reference="TOK-002",
        currency="NGN",
        first_name="Shagbaor",
        last_name="Agber",
        email_address="test@example.com",
    )

    assert resp["success"] is True
    assert resp["token"] == "TOK-002"
    assert resp["verification_charge_status"] == "failed"
    assert "verification_charge_message" in resp


@rsps.activate
def test_tokenize_card_tokenization_failed(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/merchant/tokenization/token",
        json={
            "success": False,
            "token": None,
            "verification_charge_status": "not_attempted",
            "error_code": "TOKENIZATION_FAILED",
            "message": "Tokenization failed"
        },
        status=200,  # even though success false, HTTP 200
    )

    resp = client.collections.tokenize_card(
        card_number="4508750015741019",
        expiry_month="01",
        expiry_year="2039",
        cvv="100",
        merchant_reference="TOK-003",
        currency="NGN",
        first_name="Shagbaor",
        last_name="Agber",
        email_address="test@example.com",
    )

    assert resp["success"] is False
    assert resp["token"] is None
    assert resp["verification_charge_status"] == "not_attempted"
    assert resp["error_code"] == "TOKENIZATION_FAILED"


@rsps.activate
def test_tokenize_card_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/merchant/tokenization/token",
        json={"message": "Duplicate merchant reference"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.collections.tokenize_card(
            card_number="4508750015741019",
            expiry_month="01",
            expiry_year="2039",
            cvv="100",
            merchant_reference="DUPLICATE",
            currency="NGN",
            first_name="Shagbaor",
            last_name="Agber",
            email_address="test@example.com",
        )
# --------------------------------------------------
# Charge Card with Token
# --------------------------------------------------

@rsps.activate
def test_charge_card_with_token_success(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/",
        json={
            "paymentCompleted": True,
            "amountPaid": 2500.00,
            "valueAmount": 2450.00,
            "rrn": "123456789012",
            "do3dsAuth": False,
        },
        status=200,
    )

    resp = client.collections.charge_card_with_token(
        transaction_reference="TXN-001",
        amount=2500.00,
        currency="NGN",
        payaza_token_reference="TOK-001",
        description="Test charge",
        callback_url="https://example.com/callback",
    )

    # Verify request payload
    sent = rsps.calls[0].request
    import json
    body = json.loads(sent.body)
    assert "service_payload" in body
    sp = body["service_payload"]
    assert sp["transaction_reference"] == "TXN-001"
    assert sp["payaza_token_reference"] == "TOK-001"
    assert sp["description"] == "Test charge"
    assert sp["callback_url"] == "https://example.com/callback"

    assert resp["paymentCompleted"] is True
    assert resp["rrn"] == "123456789012"


@rsps.activate
def test_charge_card_with_token_3ds_required(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/",
        json={
            "paymentCompleted": False,
            "do3dsAuth": True,
            "threeDsHtml": "<html><body>3DS Form</body></html>",
            "amountPaid": 0,
        },
        status=200,
    )

    resp = client.collections.charge_card_with_token(
        transaction_reference="TXN-002",
        amount=1500.00,
        currency="NGN",
        payaza_token_reference="TOK-002",
    )

    assert resp["do3dsAuth"] is True
    assert "threeDsHtml" in resp
    assert resp["paymentCompleted"] is False


@rsps.activate
def test_charge_card_with_token_error_raises(client, base_url):
    rsps.add(
        rsps.POST,
        f"{base_url}/live/card/card_charge/",
        json={"message": "Invalid token"},
        status=400,
    )

    with pytest.raises(PayazaAPIError):
        client.collections.charge_card_with_token(
            transaction_reference="TXN-003",
            amount=100.00,
            currency="NGN",
            payaza_token_reference="INVALID-TOKEN",
        )

# --------------------------------------------------
# List Tokens
# --------------------------------------------------

@rsps.activate
def test_list_tokens_default(client, base_url):
    rsps.add(
        rsps.GET,
        f"{base_url}/live/card/merchant/tokenization/tokens?start_at=1&limit=50",
        json={
            "tokens": [
                {"merchant_reference": "TOK-001", "created_at": "2025-01-15"},
                {"merchant_reference": "TOK-002", "created_at": "2025-01-16"},
            ],
            "total": 2,
            "page": 1,
            "limit": 50,
        },
        status=200,
        match=[matchers.query_param_matcher({"start_at": "1", "limit": "50"})],
    )

    resp = client.collections.list_tokens()

    assert len(resp["tokens"]) == 2
    assert resp["page"] == 1


@rsps.activate
def test_list_tokens_with_dates(client, base_url):
    rsps.add(
        rsps.GET,
        f"{base_url}/live/card/merchant/tokenization/tokens?start_at=2&limit=20&start_date=2025-01-01&end_date=2025-01-31",
        json={
            "tokens": [
                {"merchant_reference": "TOK-003", "created_at": "2025-01-20"},
            ],
            "total": 1,
            "page": 2,
            "limit": 20,
        },
        status=200,
        match=[matchers.query_param_matcher({"start_at": "2", "limit": "20", "start_date": "2025-01-01", "end_date": "2025-01-31"})],
    )

    resp = client.collections.list_tokens(
        start_at=2,
        limit=20,
        start_date="2025-01-01",
        end_date="2025-01-31"
    )

    assert len(resp["tokens"]) == 1
    assert resp["page"] == 2


@rsps.activate
def test_list_tokens_error_raises(client, base_url):
    rsps.add(
        rsps.GET,
        f"{base_url}/live/card/merchant/tokenization/tokens?start_at=1&limit=50",
        json={"message": "Unauthorized"},
        status=401,
        match=[matchers.query_param_matcher({"start_at": "1", "limit": "50"})],
    )

    with pytest.raises(PayazaAuthError):
        client.collections.list_tokens()

# --------------------------------------------------
# Delete Token
# --------------------------------------------------

@rsps.activate
def test_delete_token_success(client, base_url):
    token_id = "TOK-001"
    rsps.add(
        rsps.DELETE,
        f"{base_url}/live/card/merchant/tokenization/token/{token_id}",
        json={"message": "Token deleted successfully"},
        status=200,
    )

    resp = client.collections.delete_token(token_id)

    assert resp["message"] == "Token deleted successfully"


@rsps.activate
def test_delete_token_not_found(client, base_url):
    token_id = "TOK-999"
    rsps.add(
        rsps.DELETE,
        f"{base_url}/live/card/merchant/tokenization/token/{token_id}",
        json={"message": "Token not found"},
        status=404,
    )

    with pytest.raises(PayazaAPIError) as excinfo:
        client.collections.delete_token(token_id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.response["message"] == "Token not found"