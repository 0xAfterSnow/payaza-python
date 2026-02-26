"""
Example: Check Transaction Status

Run with:
    python examples/get_transaction_status.py
"""

import os
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)

TRANSACTION_REFERENCE = "TXN-1234567890"  # Replace with an actual transaction reference

def check_status():
    try:
        response = client.transactions.get_transaction_status(TRANSACTION_REFERENCE)
        print("\n=== TRANSACTION STATUS ===")
        print(response)

        # Interpret common statuses
        status = response.get("data", {}).get("status")
        if status:
            print(f"\nStatus: {status}")
            if status == "NIP_SUCCESS":
                print("✅ Transaction completed successfully.")
            elif status == "NIP_PENDING":
                print("⏳ Transaction is still processing.")
            elif status in ["NIP_FAILURE", "TRANSACTION_INITIATED"]:
                print("❌ Transaction failed or needs review.")
            elif status == "ESCROW_SUCCESS":
                print("⚠️  Amount in escrow – confirm with bank.")

    except PayazaAPIError as e:
        print("\n=== STATUS CHECK FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    check_status()