from rest_framework.viewsets import ModelViewSet
from .models import Offer, Trade
from .serializers import OfferSerializer, TradeSerializer


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class TradeViewSet(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
