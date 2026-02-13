"""API-модули WB SDK."""

from wbsdk.api.analytics import AnalyticsAPI
from wbsdk.api.base import BaseAPI
from wbsdk.api.click_collect import ClickCollectAPI
from wbsdk.api.communications import CommunicationsAPI
from wbsdk.api.content import ContentAPI
from wbsdk.api.finances import DocumentsAPI, FinancesAPI
from wbsdk.api.general import GeneralAPI
from wbsdk.api.marketplace import MarketplaceAPI
from wbsdk.api.orders_dbs import OrdersDBSAPI
from wbsdk.api.orders_dbw import OrdersDBWAPI
from wbsdk.api.orders_fbw import OrdersFBWAPI
from wbsdk.api.prices import PricesAPI
from wbsdk.api.promotion import PromotionAPI, PromotionCalendarAPI
from wbsdk.api.reports import ReportsAPI
from wbsdk.api.tariffs import TariffsAPI
from wbsdk.api.user_management import UserManagementAPI
from wbsdk.api.warehouses import WarehousesAPI
from wbsdk.api.wbd import WBDAPI

__all__ = [
    "AnalyticsAPI",
    "BaseAPI",
    "ClickCollectAPI",
    "CommunicationsAPI",
    "ContentAPI",
    "DocumentsAPI",
    "FinancesAPI",
    "GeneralAPI",
    "MarketplaceAPI",
    "OrdersDBWAPI",
    "OrdersDBSAPI",
    "OrdersFBWAPI",
    "PricesAPI",
    "PromotionAPI",
    "PromotionCalendarAPI",
    "ReportsAPI",
    "TariffsAPI",
    "UserManagementAPI",
    "WarehousesAPI",
    "WBDAPI",
]
