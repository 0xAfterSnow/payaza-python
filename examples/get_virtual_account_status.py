"""
Example: Retrieve Static Virtual Account Status

Run with:
    python examples/get_virtual_account_status.py
"""

import os
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)  # or sandbox=False for live

VIRTUAL_ACCOUNT_NUMBER = "3010066808"  # Replace with actual account number

def get_status():
    try:
        response = client.virtual_accounts.get_virtual_account_status(
            virtual_account_number=VIRTUAL_ACCOUNT_NUMBER
        )
        print("\n=== VIRTUAL ACCOUNT STATUS ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== STATUS CHECK FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    get_status()