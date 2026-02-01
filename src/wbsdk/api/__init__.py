"""API-модули WB SDK."""

from wbsdk.api.base import BaseAPI
from wbsdk.api.analytics import AnalyticsAPI
from wbsdk.api.content import ContentAPI
from wbsdk.api.marketplace import MarketplaceAPI
from wbsdk.api.prices import PricesAPI
from wbsdk.api.warehouses import WarehousesAPI

__all__ = [
    "AnalyticsAPI",
    "BaseAPI",
    "ContentAPI",
    "MarketplaceAPI",
    "PricesAPI",
    "WarehousesAPI",
]
