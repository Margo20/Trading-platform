from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, TradeViewSet

app_name = "offer"


router = DefaultRouter()
router.register("offer", OfferViewSet, basename="offer")
router.register("trade", TradeViewSet, basename="trade")
urlpatterns = router.urls
