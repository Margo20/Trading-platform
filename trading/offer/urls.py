from rest_framework.routers import DefaultRouter

from offer.views import OfferViewSet, TradeViewSet, MoneyViewSet, WatchListViewSet, InventoryViewSet

app_name = "offer"


router = DefaultRouter()
router.register("offer", OfferViewSet, basename="offer")
router.register("trade", TradeViewSet, basename="trade")
router.register("money", MoneyViewSet, basename="money")
router.register("watchList", WatchListViewSet, basename="watchList")
router.register("inventory", InventoryViewSet, basename="inventory")

urlpatterns = router.urls

