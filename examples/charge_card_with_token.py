"""
Example: Charge a Card Using a Token Reference

Run with:
    python examples/charge_card_with_token.py
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

transaction_reference = f"TXN-{uuid.uuid4().hex[:12]}"
TOKEN_REFERENCE = "TOK-a488f5867507"  # Replace with actual token from tokenization 

def charge_with_token():
    try:
        response = client.collections.charge_card_with_token(
            transaction_reference=transaction_reference,
            amount=2500.00,
            currency="NGN",
            payaza_token_reference=TOKEN_REFERENCE,
            description="Payment for invoice #12345",
            callback_url="https://example.com/callback",
        )

        print("\n=== CHARGE WITH TOKEN RESPONSE ===")
        print(response)

        # Check payment completion
        if response.get("paymentCompleted"):
            print(f"Payment successful! Amount paid: {response.get('amountPaid')}")
            print(f"RRN: {response.get('rrn')}")
        elif response.get("do3dsAuth"):
            print("3DS authentication required. Display the HTML in an iframe.")
            # In a real integration, you would render response['threeDsHtml']
        else:
            print("Payment pending or failed.")

    except PayazaAPIError as e:
        print("\n=== CHARGE FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    charge_with_token()