import factory
from offer.models import Currency, Trade, Offer, Item, StockBase, Inventory
from tests.test_authentication.factories import UserFactory

class CurrencyFactory(factory.Factory):
    class Meta:
        model = Currency
CurrencyFactory()

class StockBaseFactory(factory.Factory):
    class Meta:
        model= StockBase

class ItemFactory(factory.Factory):
    class Meta:
        model= Item
    currenc = factory.SubFactory(CurrencyFactory)
    name = factory.SubFactory(StockBaseFactory)
ItemFactory()

class InventoryFactory(factory.Factory):
    class Meta:
        model= Inventory
    user = factory.SubFactory(UserFactory)
    item = factory.SubFactory(ItemFactory)
ItemFactory.create_batch(3)

class OfferFactory(factory.Factory):
    class Meta:
        model = Offer
    user = factory.SubFactory(UserFactory)
    item = factory.SubFactory(ItemFactory)

OfferFactory.create_batch(2)# --> Batch of 2 instances

class TradeFactory(factory.Factory):
    class Meta:
        model = Trade
    currenc = factory.SubFactory(CurrencyFactory)
    seller = factory.SubFactory(UserFactory)
    buyer = factory.SubFactory(UserFactory)
    item = factory.SubFactory(ItemFactory)

TradeFactory()
