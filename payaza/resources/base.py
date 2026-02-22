"""
Base class for all Payaza API resources.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from payaza.client import Payaza


class Resource:
    """Thin wrapper that holds a reference to the Payaza client."""

    def __init__(self, client: "Payaza") -> None:
        self._client = client