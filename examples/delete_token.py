"""
Example: Delete a Token

Run with:
    python examples/delete_token.py
"""

import os
from dotenv import load_dotenv
from payaza import Payaza, PayazaAPIError

load_dotenv()

api_key = os.getenv("PAYAZA_API_KEY")
if not api_key:
    raise RuntimeError("PAYAZA_API_KEY not set")

client = Payaza(api_key=api_key, sandbox=True)

TOKEN_ID = "TOK-001"  # Replace with actual token ID from tokenization

def delete_token():
    try:
        response = client.collections.delete_token(TOKEN_ID)
        print("\n=== DELETE TOKEN RESPONSE ===")
        print(response)
    except PayazaAPIError as e:
        print("\n=== DELETE FAILED ===")
        print("Status Code:", e.status_code)
        print("Response:", e.response)

if __name__ == "__main__":
    delete_token()