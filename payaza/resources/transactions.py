"""
Payaza Transactions API resource.
"""
from __future__ import annotations

from typing import List, Optional

from payaza.resources.base import Resource

class Transactions(Resource):
    """Interact with the Payaza Transactions API."""
    
    # ------------------------------------------------------------------
    # Transaction Status
    # ------------------------------------------------------------------

    def get_transaction_status(self, transaction_reference: str) -> dict:
        """
        Retrieve the status of a specific transaction using its unique reference.

        Possible statuses returned:
            - TRANSACTION_INITIATED: Received and queued for processing.
            - NIP_SUCCESS: Transaction successful.
            - NIP_PENDING: Transaction still in progress.
            - NIP_FAILURE: Transaction failed.
            - ESCROW_SUCCESS: Amount deducted but processing by bank; may be reversed.

        Args:
            transaction_reference: The unique identifier of the transaction.

        Returns:
            dict: API response containing the transaction status and details.
        """
        headers = self._client._default_headers()
        headers["X-TenantID"] = "test" if self._client.sandbox else "live"
        path = f"/live/payaza-account/api/v1/mainaccounts/merchant/transaction/{transaction_reference}"
        return self._client.get(path, headers=headers)