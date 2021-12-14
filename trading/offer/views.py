from rest_framework.viewsets import ModelViewSet
from offer.models import Offer, Trade, Inventory, Money, WatchList, Currency, Price, Item
from offer.serializers import OfferSerializer, PriceSerializer, TradeSerializer, InventorySerializer, \
    WatchListSerializer, MoneySerializer, CurrencySerializer, ItemSerializer
from offer.filters import FilterByUser


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class TradeViewSet(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class InventoryViewSet(ModelViewSet):
    filter_backends = [FilterByUser]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class WatchListViewSet(ModelViewSet):
    filter_backends = [FilterByUser]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class MoneyViewSet(ModelViewSet):
    filter_backends = [FilterByUser]
    queryset = Money.objects.all()
    serializer_class = MoneySerializer


class PriceViewSet(ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
