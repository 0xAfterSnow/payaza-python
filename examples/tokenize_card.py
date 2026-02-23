"""
Example: Tokenize a Card and Perform Verification Charge

Run with:
    python examples/tokenize_card.py
"""

import os
import uuid
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)

merchant_reference = f"TOK-{uuid.uuid4().hex[:12]}"

def tokenize():
    try:
        response = client.collections.tokenize_card(
            card_number="4508750015741019",
            expiry_month="01",
            expiry_year="39",
            cvv="100",
            merchant_reference=merchant_reference,
            currency="NGN",
            first_name="Shagbaor",
            last_name="Agber",
            email_address="dxtlive@gmail.com",
            callback_url="https://example.com/callback",
        )

        print("\n=== TOKENIZATION RESPONSE ===")
        print(response)

        # Interpret response
        if response.get("success"):
            token = response.get("token")
            print(f"\nToken created: {token}")
            status = response.get("verification_charge_status")
            if status == "success":
                print("Verification charge succeeded. Token is ready to use.")
            elif status == "failed":
                print("Verification charge failed, but token is still valid. Test with a small charge.")
            elif status == "pending":
                print("Verification charge is pending (3DS flow).")
        else:
            print("Tokenization failed. Do not retry with same merchant_reference.")
            print("Error code:", response.get("error_code"))

    except PayazaAPIError as e:
        print("\n=== TOKENIZATION FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    tokenize()