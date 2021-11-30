from rest_framework.viewsets import ModelViewSet
from .models import Offer, Trade, Inventory, Money, WatchList
from .serializers import OfferSerializer, TradeSerializer, InventorySerializer, WatchListSerializer, MoneySerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class TradeViewSet(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class InventoryViewSet(ModelViewSet):
    queryset = Inventory
    serializer_class = InventorySerializer


class WatchListViewSet(ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class MoneyViewSet(ModelViewSet):
    queryset = Money.objects.all()
    serializer_class = MoneySerializer


