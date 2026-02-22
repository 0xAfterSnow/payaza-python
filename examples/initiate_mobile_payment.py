"""
Example: Initiate Apple Pay / Google Pay Collection

Run with:
    python examples/initiate_mobile_payment.py
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

transaction_reference = f"MOB-{uuid.uuid4().hex[:12]}"

# Example 1: Initiate Apple Pay
def initiate_apple_pay():
    try:
        response = client.collections.initiate_mobile_payment(
            amount=49.99,
            first_name="John",
            last_name="Doe",
            payment_option="APPLEPAY",
            description="Purchase of digital goods",
            transaction_reference=transaction_reference,
            country_code="NGN",
            currency_code="USD",
            redirect_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            error_url="https://example.com/error",
        )
        print("\n=== APPLE PAY INITIATION ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== APPLE PAY FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


# Example 2: Initiate Google Pay (using a different reference)
def initiate_google_pay():
    try:
        response = client.collections.initiate_mobile_payment(
            amount=79.99,
            first_name="Jane",
            last_name="Smith",
            payment_option="GOOGLEPAY",
            description="Subscription payment",
            transaction_reference=f"MOB-{uuid.uuid4().hex[:12]}",
            country_code="NGN",
            currency_code="USD",
            redirect_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            error_url="https://example.com/error",
        )
        print("\n=== GOOGLE PAY INITIATION ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== GOOGLE PAY FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


if __name__ == "__main__":
    initiate_apple_pay()
    initiate_google_pay()