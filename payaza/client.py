"""
Payaza Python SDK - Main Client
"""
from __future__ import annotations

import base64
import logging
from typing import Optional

import requests
from requests import Response, Session

from payaza.exceptions import PayazaAPIError, PayazaAuthError, PayazaNetworkError
from payaza.resources.collections import Collections
from payaza.resources.virtual_accounts import VirtualAccounts
from payaza.resources.payouts import Payouts
from payaza.resources.accounts import Accounts
from payaza.resources.transactions import Transactions

logger = logging.getLogger("payaza")

LIVE_BASE_URL = "https://api.payaza.africa"

DEFAULT_TIMEOUT = 30


class Payaza:
    """
    Payaza API client.

    Usage::

        client = Payaza(api_key="your-api-key")

        # Sandbox / test mode
        client = Payaza(api_key="your-test-key", sandbox=True)

    Args:
        api_key: Your Payaza API key (from the dashboard).
        sandbox: Send requests to the sandbox environment. Defaults to False.
        timeout: HTTP request timeout in seconds. Defaults to 30.
        session: Optional custom ``requests.Session``.
    """

    def __init__(
        self,
        api_key: str,
        *,
        sandbox: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
        session: Optional[Session] = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key must not be empty.")

        self.api_key = api_key
        self.sandbox = sandbox
        self.timeout = timeout
        self.base_url = LIVE_BASE_URL

        self._session = session or requests.Session()
        self._session.headers.update(self._default_headers())

        # Resources
        self.collections = Collections(self)
        self.virtual_accounts = VirtualAccounts(self)
        self.payouts = Payouts(self)
        self.accounts = Accounts(self)
        self.transactions = Transactions(self)

    def _default_headers(self) -> dict:
        token = base64.b64encode(self.api_key.encode()).decode()
        return {
            "Authorization": f"Payaza {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _handle_response(self, response: Response) -> dict:
        try:
            data = response.json()
        except ValueError:
            data = {"message": response.text}

        if response.status_code == 401:
            raise PayazaAuthError(
                message=data.get("message", "Unauthorised"),
                status_code=response.status_code,
                response=data,
            )
        if not response.ok:
            raise PayazaAPIError(
                message=data.get("message", f"HTTP {response.status_code}"),
                status_code=response.status_code,
                response=data,
            )
        return data

    def get(self, path: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        try:
            resp = self._session.get(self._url(path), params=params, timeout=self.timeout, headers=headers)
        except requests.exceptions.RequestException as exc:
            raise PayazaNetworkError(str(exc)) from exc
        return self._handle_response(resp)

    def post(self, path: str, payload: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        final_headers = self._default_headers()
        if headers:
            final_headers.update(headers)
        try:
            resp = self._session.post(self._url(path), json=payload or {}, timeout=self.timeout, headers=final_headers)
        except requests.exceptions.RequestException as exc:
            raise PayazaNetworkError(str(exc)) from exc
        return self._handle_response(resp)
    def put(self, path: str, payload: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        final_headers = self._default_headers()
        if headers:
            final_headers.update(headers)
        try:
            resp = self._session.put(self._url(path), json=payload or {}, timeout=self.timeout, headers=final_headers)
        except requests.exceptions.RequestException as exc:
            raise PayazaNetworkError(str(exc)) from exc
        return self._handle_response(resp)

    def delete(self, path: str, headers: Optional[dict] = None) -> dict:
        final_headers = self._default_headers()
        if headers:
            final_headers.update(headers)
        try:
            resp = self._session.delete(self._url(path), timeout=self.timeout, headers=final_headers)
        except requests.exceptions.RequestException as exc:
            raise PayazaNetworkError(str(exc)) from exc
        return self._handle_response(resp)