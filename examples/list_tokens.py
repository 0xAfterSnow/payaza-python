"""
Example: List All Tokens with Pagination and Date Filtering

Run with:
    python examples/list_tokens.py
"""

import os
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)

def list_tokens():
    try:
        # Basic listing (page 1, 50 records)
        response = client.collections.list_tokens()
        print("\n=== TOKENS (PAGE 1) ===")
        print(response)

        # With date filters
        response = client.collections.list_tokens(
            start_at=2,
            limit=20,
            start_date="2025-01-01",
            end_date="2025-01-31"
        )
        print("\n=== TOKENS (PAGE 2, FILTERED JAN 2025) ===")
        print(response)

    except PayazaAPIError as e:
        print("\n=== LIST TOKENS FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    list_tokens()