"""
Payaza Collections API resource.

Collections allow you to accept payments from customers via card,
bank transfer, USSD, and other channels.
"""
from __future__ import annotations

from typing import Optional

from payaza.resources.base import Resource


class Collections(Resource):
    """Interact with the Payaza Collections API."""


    # ------------------------------------------------------------------
    # Card Collections
    # ------------------------------------------------------------------
    
    # Check 3DS Availability
    def check_3ds_availability(self, card_number: str, currency: str) -> dict:
        """
        Check if a card possesses 3D Secure (3DS) capabilities or not.

        Args:
            card_number: The number on the card.
            currency: Currency Code.

        Returns:
            dict: API response containing 3DS availability information.
        """
        payload = {
            "card_number": card_number,
            "currency": currency,
        }
        return self._client.post("/live/card/card_charge/check_3ds_availability", payload)

    # Charge (direct)
    def charge_card(
        self,
        *,
        amount: float,
        currency: str,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        transaction_reference: str,
        description: str,
        card_number: str,
        expiry_month: str,
        expiry_year: str,
        security_code: str,
        callback_url: Optional[str] = None,
    ) -> dict:
        """
        Charge a card directly.

        Args:
            amount: The amount to be charged.
            currency: Currency code for the transaction. The base currency is NGN (3-letter ISO 4217 currency code).
            first_name: The first name of the customer.
            last_name: The last name of the customer.
            email_address: The email address of the customer.
            phone_number: The phone number of the customer.
            transaction_reference: Your unique reference.
            description: Description of the transaction.
            card_number: The number on the card.
            expiry_month: 2-digit expiry month, e.g. ``"10"``.
            expiry_year: 2-digit expiry year, e.g. ``"26"``.
            security_code: Card security code (CVV).
            callback_url: The callback URL provided by the merchant (Kindly ensure this accepts POST request)

        Returns:
            dict: API response.
        """
        service_payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "phone_number": phone_number,
            "amount": amount,
            "transaction_reference": transaction_reference,
            "currency": currency,
            "description": description,
            "card": {
                "expiryMonth": expiry_month,
                "expiryYear": expiry_year,
                "securityCode": security_code,
                "cardNumber": card_number,
            },
        }
        if callback_url:
            service_payload["callback_url"] = callback_url

        return self._client.post("/live/card/card_charge/", {"service_payload": service_payload})

    # Check Transaction Status
    def check_transaction_status(self, transaction_reference: str) -> dict:
        """
        Gets the transaction status corresponding to the provided transaction reference.

        Args:
            transaction_reference: The transaction reference used for the card transaction.

        Returns:
            dict: Transaction status and details.
        """
        service_payload = {
            "transaction_reference": transaction_reference,
        }
        return self._client.post("/live/card/card_charge/transaction_status", {"service_payload": service_payload})

    # Check Refund Status
    def check_refund_status(self, refund_transaction_reference: str) -> dict:
        """
        Verify the status of a refund transaction.

        Args:
            refund_transaction_reference: The unique identifier given to a particular transaction you refunded. This can be found in the response body of the “Card Charge Refund API”


        Returns:
            dict: Refund status and details.
        """
        service_payload = {
            "refund_transaction_reference": refund_transaction_reference,
        }
        return self._client.post("/live/card/card_charge/refund_status", {"service_payload": service_payload})