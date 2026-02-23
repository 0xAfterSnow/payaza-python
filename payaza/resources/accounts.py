"""
Payaza Accounts API resource.

Accounts let you view your Payaza account details.
"""
from __future__ import annotations

from payaza.resources.base import Resource


class Accounts(Resource):
    """Interact with the Payaza Accounts API."""

    # ------------------------------------------------------------------
    # Account Enquiry / Fetch Details
    # ------------------------------------------------------------------

    def fetch_account_details(
        self,
        *,
        currency: str,
        bank_code: str,
        account_number: str,
    ) -> dict:
        """
        Fetch account details (e.g., account name) from a provider using the account number and bank code.

        This is typically used to verify the account name before initiating a payout.

        Args:
            currency: The currency code (e.g., "NGN").
            bank_code: The bank code of the account provider.
            account_number: The account number to query.

        Returns:
            dict: API response containing the account details, such as the account name.
        """
        headers = self._client._default_headers()
        headers["X-TenantID"] = "test" if self._client.sandbox else "live"  
        service_payload = {
            "currency": currency,
            "bank_code": bank_code,
            "account_number": account_number,
        }
        payload = {
            "service_payload": service_payload
        }

        return self._client.post(
            "/live/payaza-account/api/v1/mainaccounts/merchant/provider/enquiry",
            payload,
            headers=headers
        )