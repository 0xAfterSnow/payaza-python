"""
Payaza Python SDK
~~~~~~~~~~~~~~~~~

An unofficial Python client library for the Payaza Africa API.

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