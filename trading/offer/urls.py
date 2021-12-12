from rest_framework.routers import DefaultRouter

from offer.views import CurrencyViewSet, OfferViewSet, ItemViewSet, TradeViewSet, MoneyViewSet, PriceViewSet, WatchListViewSet, InventoryViewSet

app_name = "offer"


router = DefaultRouter()
router.register("offer", OfferViewSet, basename="offer")
router.register("trade", TradeViewSet, basename="trade")
router.register("money", MoneyViewSet, basename="money")
router.register("currency", CurrencyViewSet, basename="currency")
router.register("watchList", WatchListViewSet, basename="watchList")
router.register("inventory", InventoryViewSet, basename="inventory")
router.register("price", PriceViewSet, basename="price")
router.register("item", ItemViewSet, basename="item")

urlpatterns = router.urls
