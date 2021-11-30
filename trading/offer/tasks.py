from trading.celery import app
from django.db import transaction
from .models import Offer, Trade, Money, Inventory, Item, Price


@app.task
def req():
    buyers = Offer.objects.filter(order_type="buying", quantity__gt=0)
    sellers = Offer.objects.filter(order_type="sale", quantity__gt=0).order_by("price")
    trades = []
    for buyer in buyers:
        sel = []
        for seller in sellers:
            if buyer.item == seller.item and buyer.price >= seller.price:
                sel.append(seller)
                if buyer.quantity <= seller.quantity:
                    trades.append(Trade(item=buyer.item, quantity=buyer.quantity, unit_price=seller.price, buyer_offer=buyer,
                                        seller_offer=seller, seller=seller.user, buyer=buyer.user))
                    seller.quantity = seller.quantity - buyer.quantity
                    buyer.quantity = 0
                    break
                else:
                    trades.append(Trade(item=buyer.item, quantity=seller.quantity, unit_price=seller.price, buyer_offer=buyer,
                                        seller_offer=seller, seller=seller.user, buyer=buyer.user))
                    buyer.quantity -= seller.quantity
                    seller.quantity = 0

    with transaction.atomic():
        Trade.objects.bulk_create(trades)
        stocks = Inventory.objects.all()
        wallets = Money.objects.all()
        prices = Price.objects.all()
        items = Item.objects.all()
        for trade in trades:
            for s in stocks:
                if trade.item == s.item and s.user == trade.buyer:
                  s.quantity += trade.quantity
                elif trade.item == s.item and s.user == trade.seller:
                    s.quantity -= trade.quantity
            for w in wallets:
                if w.user == trade.buyer:
                    w.sum -= trade.unit_price*trade.quantity
                elif w.user == trade.seller:
                    w.sum += trade.unit_price*trade.quantity
            for price in prices:
                if price.item == trade.item:
                    price.price = trade.unit_price
                    for item in items:
                        item.price = price.price
            Inventory.objects.bulk_update(stocks, ['quantity'])
            Money.objects.bulk_update(wallets, ['sum'])
            Item.objects.bulk_update(items, ['price'])
            Price.objects.bulk_update(prices, ['price'])
        Offer.objects.bulk_update(buyers, ['quantity'])
        Offer.objects.bulk_update(sellers, ['quantity'])
