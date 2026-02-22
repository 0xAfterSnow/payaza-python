"""
Example: Create a Dynamic Virtual Account

Run with:
    python examples/create_dynamic_virtual_account.py
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

account_reference = f"VA-{uuid.uuid4().hex[:12]}"

def create_va():
    try:
        response = client.virtual_accounts.create_dynamic_virtual_account(
            account_name="John Doe",
            account_type="Dynamic",
            bank_code="1067",  # 78 FINANCE
            account_reference=account_reference,
            customer_first_name="John",
            customer_last_name="Doe",
            customer_email="john.doe@example.com",
            customer_phone_number="08012345678",
            transaction_amount=5000.00,
            bvn="12345678901",  # optional
            has_amount_validation=True,  # optional, only for 1067 or 140
            transaction_description="Payment for invoice #12345",  # optional
            expires_in_minutes=45,  # optional, only for 1067
        )
        print("\n=== DYNAMIC VIRTUAL ACCOUNT CREATED ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== CREATION FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    create_va()