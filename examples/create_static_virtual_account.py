"""
Example: Create a Static Virtual Account

Run with:
    python examples/create_static_virtual_account.py
"""

import os
import uuid
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)  # or sandbox=False for live

account_reference = f"STATIC-{uuid.uuid4().hex[:12]}"

def create_static_va():
    try:
        response = client.virtual_accounts.create_static_virtual_account(
            account_name="John Doe Static",
            bank_code="1067",  # 78 FINANCE
            bvn="12345678901",
            bvn_validated=True,
            account_reference=account_reference,
            customer_first_name="John",
            customer_last_name="Doe",
            customer_email="john.doe@example.com",
            customer_phone_number="08012345678",
        )
        print("\n=== STATIC VIRTUAL ACCOUNT CREATED ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== CREATION FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    create_static_va()