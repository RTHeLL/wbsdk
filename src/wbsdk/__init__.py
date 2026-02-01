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
from wbsdk.schemas import (
    OrdersNewResponse,
    SupplyCreateResponse,
    SubjectsResponse,
    TagsResponse,
)

__version__ = "0.2.0"
__all__ = [
    "WBClient",
    "WBAPIError",
    "WBAuthError",
    "WBConflictError",
    "WBNotFoundError",
    "WBRateLimitError",
    "WBValidationError",
    "OrdersNewResponse",
    "SupplyCreateResponse",
    "SubjectsResponse",
    "TagsResponse",
]
