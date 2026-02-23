"""
Payaza Payouts API resource.

Payouts (disbursements) let you send money to bank accounts,
mobile wallets, and other destinations.
"""
from __future__ import annotations

from typing import List, Optional

from payaza.resources.base import Resource


class Payouts(Resource):
    """Interact with the Payaza Payouts / Disbursements API."""

    # ------------------------------------------------------------------
    # Payouts
    # ------------------------------------------------------------------

    # Bank Transfers & Mobile Money
    def initiate_payout(
        self,
        *,
        transaction_type: str,
        payout_amount: float,
        transaction_pin: int,
        account_reference: str,
        currency: str,
        payout_beneficiaries: list[dict],
        sender: dict,
        country: Optional[str] = None,
    ) -> dict:
        """
        Initiate a transfer from your Payaza account to a bank account or mobile money account.

        The request structure varies by currency – see the official documentation for details.
        For XOF payouts, the `country` parameter is required.

        Args:
            transaction_type: The type of account being transferred to.
                For NGN: "nuban"
                For GHS: "mobile_money" or "ghipps"
                For UGX: "mobile_money"
                For TZS: "mobile_money" or "tiss"
                For KES: "mobile_money" or "kepss"
                For XOF: "mobile_money" or "wave"
                For XAF: "mobile_money"
                For ZAR: "RTC"
            payout_amount: The amount of the transaction.
            transaction_pin: Your unique transaction PIN.
            account_reference: The reference of your Payaza account for the given currency
                (obtained from the "View Payaza Account Details" API).
            currency: Transfer currency code (e.g., NGN, GHS, TZS, UGX, KES, XOF, XAF, ZAR).
            payout_beneficiaries: A list of beneficiary dictionaries, each containing:
                - credit_amount (float): Amount for this beneficiary.
                - account_number (str): Beneficiary account number (format depends on country).
                - account_name (str): Beneficiary account name.
                - bank_code (str): Beneficiary bank code.
                - narration (str): Narration (max 25 chars, no special characters).
                - transaction_reference (str): Unique reference for this beneficiary transaction.
            sender: A dictionary containing sender details:
                - sender_name (str): Name of the sender.
                - sender_id (str, optional): Unique identifier of the sender.
                - sender_phone_number (str): Phone number of the sender.
                - sender_address (str): Address of the sender.
                - dial_code (str, optional): Country dial code (required for XAF payouts).
            country: ISO 3166-1 alpha-3 country code (required for XOF payouts).

        Returns:
            dict: API response containing the payout result.
        """
        headers = self._client._default_headers()
        headers["X-TenantID"] = "test" if self._client.sandbox else "live"        
        service_payload = {
            "payout_amount": payout_amount,
            "transaction_pin": transaction_pin,
            "account_reference": account_reference,
            "currency": currency,
            "payout_beneficiaries": payout_beneficiaries,
            "sender": sender,
        }
        if country is not None:
            service_payload["country"] = country

        payload = {
            "transaction_type": transaction_type,
            "service_payload": service_payload,
        }

        return self._client.post("/live/payout-receptor/payout", payload, headers=headers)