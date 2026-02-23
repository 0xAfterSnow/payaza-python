"""
Example: Initiate a Payout (Bank Transfer or Mobile Money)

Run with:
    python examples/initiate_payout.py
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

# Example: NGN bank transfer (nuban)
def payout_ngn():
    try:
        response = client.payouts.initiate_payout(
            transaction_type="nuban",
            payout_amount=5000,
            transaction_pin=1111,  # Replace with your actual PIN
            account_reference="5012345678",  # From View Payaza Account Details
            currency="NGN",
            country="NGA",
            payout_beneficiaries=[
                {
                    "credit_amount": 5000,
                    "account_number": "9207067319",
                    "account_name": "John Doe",
                    "bank_code": "000013",
                    "narration": "Invoice payment",
                    "transaction_reference": f"BEN-{uuid.uuid4().hex[:12]}",
                }
            ],
            sender={
                "sender_name": "Sender Name",
                "sender_id": "SND001",  # optional
                "sender_phone_number": "08012345678",
                "sender_address": "Taraba, Nigeria",
                # dial_code not required for NGN
            },
        )
        print("\n=== NGN PAYOUT RESPONSE ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== NGN PAYOUT FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


# Example: XOF mobile money with required country
def payout_xof():
    try:
        response = client.payouts.initiate_payout(
            transaction_type="mobile_money",
            payout_amount=25000,
            transaction_pin=1234,
            account_reference="5012345678",  # XOF account reference
            currency="XOF",
            country="BEN",  # required for XOF
            payout_beneficiaries=[
                {
                    "credit_amount": 25000,
                    "account_number": "22901012345678",  # Benin format
                    "account_name": "Beneficiary Name",
                    "bank_code": "BENCODE",
                    "narration": "Paiement facture",
                    "transaction_reference": f"BEN-{uuid.uuid4().hex[:12]}",
                }
            ],
            sender={
                "sender_name": "Sender Name",
                "sender_phone_number": "22990000000",
                "sender_address": "Cotonou, Benin",
            },
        )
        print("\n=== XOF PAYOUT RESPONSE ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== XOF PAYOUT FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)


if __name__ == "__main__":
    payout_ngn()
    # payout_xof()  # uncomment if you have XOF access