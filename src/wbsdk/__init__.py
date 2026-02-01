"""WB SDK — профессиональный Python SDK для Wildberries API."""

from wbsdk.client import WBClient
from wbsdk.exceptions import (
    WBAPIError,
    WBConflictError,
    WBAuthError,
    WBNotFoundError,
    WBRateLimitError,
    WBValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "WBClient",
    "WBAPIError",
    "WBAuthError",
    "WBConflictError",
    "WBNotFoundError",
    "WBRateLimitError",
    "WBValidationError",
]
