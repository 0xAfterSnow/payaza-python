"""
Payaza Virtual Accounts API resource.

Virtual accounts (static and dynamic) let you generate unique account
numbers to receive payments without a checkout page.
"""
from __future__ import annotations

from typing import Optional

from payaza.resources.base import Resource


class VirtualAccounts(Resource):
    """Interact with the Payaza Virtual Accounts API."""

    # ------------------------------------------------------------------
    # Virtual Account Management
    # ------------------------------------------------------------------

    # Create Dynamic Virtual Account
    def create_dynamic_virtual_account(
        self,
        *,
        account_name: str,
        account_type: str = "Dynamic",
        bank_code: str,
        account_reference: str,
        customer_first_name: str,
        customer_last_name: str,
        customer_email: str,
        customer_phone_number: str,
        transaction_amount: float,
        bvn: Optional[str] = None,
        has_amount_validation: Optional[bool] = None,
        transaction_description: Optional[str] = None,
        expires_in_minutes: Optional[int] = None,
    ) -> dict:
        """
        Create a dynamic virtual account (valid for 30 minutes by default).

        Args:
            account_name: The name assigned to the account being created.
            account_type: Type of virtual account. Defaults to ``"Dynamic"``.
            bank_code: The code of the bank providing the virtual account.
                Supported banks:
                - ``"1067"`` for 78 FINANCE COMPANY LIMITED
                - ``"117"`` for FIDELITY BANK LIMITED
                - ``"140"`` for GLOBUS BANK LIMITED.
            account_reference: Unique identifier for the transaction.
            customer_first_name: First name of the customer.
            customer_last_name: Last name of the customer.
            customer_email: Email address of the customer.
            customer_phone_number: Phone number of the customer.
            transaction_amount: The amount to be paid in the transaction.
            bvn: Bank Verification Number (BVN) of the customer (optional).
            has_amount_validation: Enable control over amount validation
                (underpayment/overpayment). Only available for GLOBUS BANK LIMITED
                and 78 FINANCE COMPANY LIMITED (optional).
            transaction_description: Description or narration of the transaction (optional).
            expires_in_minutes: Number of minutes for which the virtual account will be valid.
                Minimum: 15, Maximum: 480. Only available for 78 FINANCE COMPANY LIMITED.
                Defaults to 30 if not provided.

        Returns:
            dict: API response containing the virtual account details.
        """
        payload = {
            "account_name": account_name,
            "account_type": account_type,
            "bank_code": bank_code,
            "account_reference": account_reference,
            "customer_first_name": customer_first_name,
            "customer_last_name": customer_last_name,
            "customer_email": customer_email,
            "customer_phone_number": customer_phone_number,
            "transaction_amount": transaction_amount,
        }
        if bvn is not None:
            payload["bvn"] = bvn
        if has_amount_validation is not None:
            payload["has_amount_validation"] = has_amount_validation
        if transaction_description is not None:
            payload["transaction_description"] = transaction_description
        if expires_in_minutes is not None:
            payload["expires_in_minutes"] = expires_in_minutes

        return self._client.post(
            "/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
            payload,
        )

    # Create static virtual account 
    def create_static_virtual_account(
        self,
        *,
        account_name: str,
        account_type: str = "Static",
        bank_code: str,
        bvn: str,
        bvn_validated: bool,
        account_reference: str,
        customer_first_name: str,
        customer_last_name: str,
        customer_email: str,
        customer_phone_number: str,
    ) -> dict:
        """
        Create a static (reserved) virtual account.

        Static virtual accounts are permanently assigned to a customer and
        can receive multiple payments. BVN validation is required.

        Args:
            account_name: The name assigned to the account being created.
            account_type: Type of virtual account. Defaults to ``"Static"``.
            bank_code: The code of the bank providing the virtual account.
                Supported banks:
                - ``"1067"`` for 78 FINANCE COMPANY LIMITED
                - ``"117"`` for FIDELITY BANK LIMITED
                - ``"140"`` for GLOBUS BANK LIMITED.
            bvn: Bank Verification Number (BVN) of the customer (required).
            bvn_validated: Indicates whether the BVN has been validated by the merchant.
            account_reference: Unique identifier for the account.
            customer_first_name: First name of the customer.
            customer_last_name: Last name of the customer.
            customer_email: Email address of the customer.
            customer_phone_number: Phone number of the customer.

        Returns:
            dict: API response containing the static virtual account details.
        """
        payload = {
            "account_name": account_name,
            "account_type": account_type,
            "bank_code": bank_code,
            "bvn": bvn,
            "bvn_validated": bvn_validated,
            "account_reference": account_reference,
            "customer_first_name": customer_first_name,
            "customer_last_name": customer_last_name,
            "customer_email": customer_email,
            "customer_phone_number": customer_phone_number,
        }

        return self._client.post(
            "/live/merchant-collection/merchant/virtual_account/generate_virtual_account/",
            payload,
        )

    # Get virtual account status
    def get_virtual_account_status(self, virtual_account_number: str) -> dict:
        """
        Retrieve the status of a static virtual account using its account number.

        This endpoint works only for static (reserved) virtual accounts.

        Args:
            virtual_account_number: The virtual account number to query.

        Returns:
            dict: API response containing the account status and details.
        """
        path = f"/live/merchant-collection/merchant/virtual_account/detail/virtual_account/{virtual_account_number}"
        return self._client.get(path)