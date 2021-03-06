from rest_framework import serializers

from offer.models import Offer, Trade, Inventory, Money, WatchList, Currency, Price, Item


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['item', 'user', 'entry_quantity', 'quantity', 'order_type', 'price']

    def validate_entry_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Stock amount should be greater than 0')
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Stock amount should be greater than 0')
        return value


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['item', 'unit_price', 'quantity', 'buyer', 'buyer_offer', 'seller', 'seller_offer', 'date']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'price', 'currenc']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['user', 'item', 'quantity']


class MoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Money
        fields = ['user', 'sum']


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ['user', 'item']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'course']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['item', 'currenc', "price"]
