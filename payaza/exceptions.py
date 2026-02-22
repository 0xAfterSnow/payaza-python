"""
Payaza SDK custom exceptions.
"""
from __future__ import annotations

from typing import Any, Optional


class PayazaError(Exception):
    """Base exception for all Payaza SDK errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code!r})"
        )


class PayazaAuthError(PayazaError):
    """Raised when authentication fails (HTTP 401 / 403)."""


class PayazaAPIError(PayazaError):
    """Raised when the Payaza API returns a non-2xx response."""


class PayazaNetworkError(PayazaError):
    """Raised when a network-level error occurs (timeouts, DNS failures, etc.)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class PayazaValidationError(PayazaError):
    """Raised when required parameters are missing or invalid before making a request."""