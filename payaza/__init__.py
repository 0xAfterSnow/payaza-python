"""
Payaza Python SDK
~~~~~~~~~~~~~~~~~

An unofficial Python client library for the Payaza Africa API.

Basic usage::

    from payaza import Payaza

    client = Payaza(api_key="your-api-key")

    # Initiate a collection
    response = client.collections.initiate(
        amount=5000,
        currency="NGN",
        email="customer@example.com",
        first_name="Jane",
        last_name="Doe",
        phone_number="08012345678",
        transaction_reference="TXN-001",
        description="Payment for order #001",
        callback_url="https://yourapp.com/webhook/payaza",
    )

    print(response["payment_url"])

Full documentation: https://docs.payaza.africa/developers/apis
"""

from payaza.client import Payaza
from payaza.exceptions import (
    PayazaAPIError,
    PayazaAuthError,
    PayazaError,
    PayazaNetworkError,
    PayazaValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "Payaza",
    "PayazaError",
    "PayazaAPIError",
    "PayazaAuthError",
    "PayazaNetworkError",
    "PayazaValidationError",
]