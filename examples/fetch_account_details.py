"""
Example: Fetch Account Details (Account Name Enquiry)

Run with:
    python examples/fetch_account_details.py
"""

import os
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)

def fetch_details():
    try:
        response = client.accounts.fetch_account_details(
            currency="NGN",
            bank_code="000014",  # Example: ACCESS BANK
            account_number="0239573384",
        )
        print("\n=== ACCOUNT DETAILS ===")
        print(response)
        if response.get("status") == "success":
            account_name = response.get("data", {}).get("account_name")
            print(f"Verified Account Name: {account_name}")
    except PayazaAPIError as e:
        print("\n=== ENQUIRY FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    fetch_details()