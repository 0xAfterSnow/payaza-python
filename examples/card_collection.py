"""
Example: Full Card Collection Flow

Run with:
    python examples/card_collection.py
"""

import os
import uuid
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

# Toggle sandbox as needed
client = Payaza(api_key=api_key, sandbox=True)

transaction_reference = f"TXN-{uuid.uuid4().hex[:12]}"
refund_reference = f"REF-{uuid.uuid4().hex[:12]}"

CARD_NUMBER = "4508750015741019"
CURRENCY = "NGN"

# Check 3DS Availability
def check_3ds():
    try:
        response = client.collections.check_3ds_availability(
            card_number=CARD_NUMBER,
            currency=CURRENCY,
        )
        print("\n=== 3DS AVAILABILITY ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== 3DS CHECK FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


# Charge Card
def charge_card():
    try:
        response = client.collections.charge_card(
            amount=1000,
            currency=CURRENCY,
            first_name="Shagbaor",
            last_name="Agber",
            email_address="dxtlive@gmail.com",
            phone_number="08012345678",
            transaction_reference=transaction_reference,
            description="Payment for goods",
            card_number=CARD_NUMBER,
            expiry_month="01",
            expiry_year="39",
            security_code="100",
            callback_url="https://example.com/callback",
        )

        print("\n=== CARD CHARGE RESPONSE ===")
        print(response)

    except PayazaAPIError as e:
        print("\n=== CARD CHARGE FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


# Check Transaction Status
def check_transaction_status():
    try:
        response = client.collections.check_transaction_status(
            transaction_reference=transaction_reference,
        )

        print("\n=== TRANSACTION STATUS ===")
        print(response)

    except PayazaAPIError as e:
        print("\n=== STATUS CHECK FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


# Check Refund Status
def check_refund_status():
    try:
        response = client.collections.check_refund_status(
            refund_transaction_reference=refund_reference,
        )

        print("\n=== REFUND STATUS ===")
        print(response)

    except PayazaAPIError as e:
        print("\n=== REFUND STATUS FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


# Execute Flow
if __name__ == "__main__":
    check_3ds()
    charge_card()
    check_transaction_status()
    check_refund_status()