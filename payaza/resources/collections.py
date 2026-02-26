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

    # ------------------------------------------------------------------
    # Card Tokenization
    # ------------------------------------------------------------------

    # Create Card Token
    def tokenize_card(
        self,
        *,
        card_number: str,
        expiry_month: str,
        expiry_year: str,
        cvv: str,
        merchant_reference: str,
        currency: str,
        first_name: str,
        last_name: str,
        email_address: str,
        callback_url: Optional[str] = None,
    ) -> dict:
        """
        Tokenize a card and perform a verification charge (automatically refunded within 1‑3 days).

        Tokenization and verification charge are separate operations:
        - If tokenization succeeds (``success: true``), you receive a token (the ``merchant_reference``)
          even if the verification charge fails.
        - If the verification charge fails, the token is still valid for future charges.
        - Always check the ``verification_charge_status`` field in the response.

        Args:
            card_number: The card number.
            expiry_month: Card expiry month in MM format (e.g., ``"12"``).
            expiry_year: Card expiry year in YYYY format (e.g., ``"2025"``).
            cvv: Card CVV.
            merchant_reference: Your unique reference for this tokenization.
                This value becomes the token and must be used as ``payaza_token_reference``
                when charging the card later.
            currency: Currency code for the verification charge (e.g., ``"NGN"``, ``"USD"``).
            first_name: Cardholder's first name.
            last_name: Cardholder's last name.
            email_address: Cardholder's email address.
            callback_url: URL to redirect after 3DS authentication (optional).

        Returns:
            dict: API response containing:
                - ``success`` (bool): Whether tokenization succeeded.
                - ``token`` (str or None): The token (same as merchant_reference) if created.
                - ``verification_charge_status`` (str): ``"success"``, ``"failed"``, ``"pending"``, or ``"not_attempted"``.
                - ``message`` (str): Human‑readable description.
                - Possible error codes in case of failure.
        """
        payload = {
            "card_number": card_number,
            "expiry_month": expiry_month,
            "expiry_year": expiry_year,
            "cvv": cvv,
            "merchant_reference": merchant_reference,
            "currency": currency,
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
        }
        if callback_url is not None:
            payload["callback_url"] = callback_url

        return self._client.post("/live/card/merchant/tokenization/token", payload)

    # Charge with Token
    def charge_card_with_token(
        self,
        *,
        transaction_reference: str,
        amount: float,
        currency: str,
        payaza_token_reference: str,
        description: Optional[str] = None,
        callback_url: Optional[str] = None,
    ) -> dict:
        """
        Charge a card using a previously generated token reference.

        When using a token, the system automatically retrieves the stored card details.
        If 3DS is required (``do3dsAuth: true``), display the ``threeDsHtml`` in an iframe or popup
        and handle the callback. Tokens can be reused multiple times.

        Args:
            transaction_reference: Your unique identifier for this transaction (max 15 chars).
            amount: The amount to charge.
            currency: Currency code (e.g., ``"NGN"``, ``"USD"``).
            payaza_token_reference: The token reference obtained from tokenization.
            description: Optional description of the transaction.
            callback_url: Optional URL for 3DS callback (must accept POST).

        Returns:
            dict: API response containing:
                - ``paymentCompleted`` (bool): True if payment successful.
                - ``amountPaid`` (float): Total amount charged.
                - ``valueAmount`` (float): Net amount after fees.
                - ``rrn`` (str): Retrieval Reference Number for successful transactions.
                - ``do3dsAuth`` (bool): Whether 3DS authentication is required.
                - ``threeDsHtml`` (str): HTML for 3DS iframe/popup (if do3dsAuth is true).
        """
        service_payload = {
            "transaction_reference": transaction_reference,
            "amount": amount,
            "currency": currency,
            "payaza_token_reference": payaza_token_reference,
        }
        if description is not None:
            service_payload["description"] = description
        if callback_url is not None:
            service_payload["callback_url"] = callback_url

        return self._client.post(
            "/live/card/card_charge/",
            {"service_payload": service_payload}
        )

    # List Tokens
    def list_tokens(
        self,
        *,
        start_at: int = 1,
        limit: int = 50,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        """
        Retrieve all tokens created by your merchant account with pagination and optional date filtering.

        Args:
            start_at: The page number to retrieve (default: 1).
            limit: Number of records per page (default: 50).
            start_date: Optional start date for filtering (format: YYYY-MM-DD).
            end_date: Optional end date for filtering (format: YYYY-MM-DD).

        Returns:
            dict: API response containing a list of tokens and pagination metadata.
        """
        params = {
            "start_at": start_at,
            "limit": limit,
        }
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date

        return self._client.get("/live/card/merchant/tokenization/tokens", params=params)

    # Delete Token
    def delete_token(self, token_id: str) -> dict:
        """
        Delete a token using its token ID (the value returned from tokenization, not the merchant_reference).

        Args:
            token_id: The token ID assigned to the card (from the create token response).

        Returns:
            dict: API response confirming deletion.
        """
        path = f"/live/card/merchant/tokenization/token/{token_id}"
        return self._client.delete(path)