from trading.celery import app
from django.db import transaction
from offer.models import Offer, Trade, Money, Inventory, Item, Price


@app.task
def req():
    buyers = Offer.objects.filter(order_type="buying", quantity__gt=0).select_related('item','item__currenc')
    sellers = Offer.objects.filter(order_type="sale", quantity__gt=0).order_by("price").select_related('item','item__currenc')
    trades = []
    for buyer in buyers:
        sel = []
        for seller in sellers:
            if buyer.item == seller.item and buyer.price >= seller.price and buyer.item.currenc == seller.item.currenc:
                sel.append(seller)
                if buyer.quantity <= seller.quantity:
                    trades.append(Trade(item=buyer.item, quantity=buyer.quantity, unit_price=seller.price, currenc=buyer.item.currenc, buyer_offer=buyer,
                                        seller_offer=seller, seller=seller.user, buyer=buyer.user))
                    seller.quantity = seller.quantity - buyer.quantity
                    # seller.user.money_set.sum
                    buyer.quantity = 0
                    break
                else:
                    trades.append(Trade(item=buyer.item, quantity=seller.quantity, unit_price=seller.price, currenc=buyer.item.currenc, buyer_offer=buyer,
                                        seller_offer=seller, seller=seller.user, buyer=buyer.user))
                    buyer.quantity -= seller.quantity
                    seller.quantity = 0

    with transaction.atomic():
        Trade.objects.bulk_create(trades)
        stocks = Inventory.objects.select_related('item', 'user').all()
        wallets = Money.objects.select_related('user').all()
        prices = Price.objects.select_related('item', 'item__currenc').all()
        items = Item.objects.select_related('currenc').all()
        for trade in trades:
            for stock in stocks:
                if trade.item == stock.item and stock.user == trade.buyer:
                  stock.quantity += trade.quantity
                elif trade.item == stock.item and stock.user == trade.seller:
                    stock.quantity -= trade.quantity
            for wallet in wallets:
                if wallet.user == trade.buyer:
                    wallet.sum -= trade.unit_price*trade.quantity
                elif wallet.user == trade.seller:
                    wallet.sum += trade.unit_price*trade.quantity
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
