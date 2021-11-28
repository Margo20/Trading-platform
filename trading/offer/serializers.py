from rest_framework import serializers

from .models import Offer, Trade


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['item', 'user', 'entry_quantity', 'quantity', 'order_type', 'price']

    def validate_entry_quantity(self, value):
        print(value)
        if value <= 0:
            raise serializers.ValidationError('Stock amount should be greater than 0')
        return value

    def validate_quantity(self, value):
        print(value)
        if value <= 0:
            raise serializers.ValidationError('Stock amount should be greater than 0')
        return value


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['item', 'unit_price', 'quantity', 'buyer', 'buyer_offer', 'seller', 'seller_offer']
