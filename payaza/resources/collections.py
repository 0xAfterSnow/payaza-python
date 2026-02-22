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
    # Mobile Payments (Apple Pay / Google Pay)
    # ------------------------------------------------------------------

    def initiate_mobile_payment(
        self,
        *,
        amount: float,
        first_name: str,
        last_name: str,
        payment_option: str,
        description: str,
        transaction_reference: str,
        country_code: str,
        currency_code: str,
        redirect_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        error_url: Optional[str] = None,
        tenant_id: Optional[str] = "test",  # if provided, overrides the default api_key
    ) -> dict:
        """
        Initiate an Apple Pay or Google Pay collection.

        Args:
            amount: The amount to be paid.
            first_name: Customer's first name.
            last_name: Customer's last name.
            payment_option: Either ``"APPLEPAY"`` or ``"GOOGLEPAY"``.
            description: The description of this transaction.
            transaction_reference: The unique identifier of the transaction.
            country_code: The country code (ISO 3166-1 alpha-3), e.g. ``"USA"``.
            currency_code: Currency code, e.g. ``"GBP"``, ``"EUR"``, ``"USD"``.
            redirect_url: URL to redirect on successful payment (optional).
            cancel_url: URL to redirect when user cancels (optional).
            error_url: URL to redirect on failed payment (optional).

        Returns:
            dict: API response containing the payment initiation result.
        """

        headers = self._client._default_headers()
        if tenant_id:
            headers["X-TenantID"] = tenant_id
        payload = {
            "amount": amount,
            "first_name": first_name,
            "last_name": last_name,
            "payment_option": payment_option,
            "description": description,
            "transaction_reference": transaction_reference,
            "country_code": country_code,
            "currency_code": currency_code,
        }
        if redirect_url is not None:
            payload["redirect_url"] = redirect_url
        if cancel_url is not None:
            payload["cancel_url"] = cancel_url
        if error_url is not None:
            payload["error_url"] = error_url

        return self._client.post("/live/merchant-collection/mobile_payment/initiate", payload)
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