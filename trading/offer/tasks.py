from trading.celery import app
from django.db import transaction
from offer.models import Offer, Trade
from offer.services import change_quantity, change_sum, change_price


@app.task
def req():
    buyers = Offer.objects.filter(order_type="buying", quantity__gt=0).select_related('item', 'item__currenc')
    sellers = Offer.objects.filter(order_type="sale", quantity__gt=0).order_by("price").select_related('item')

    trades = []
    for buyer in buyers:
        sel = []
        for seller in sellers:
            if buyer.item == seller.item and buyer.price >= seller.price:
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
        Offer.objects.bulk_update(buyers, ['quantity'])
        Offer.objects.bulk_update(sellers, ['quantity'])
        change_quantity(trades)
        change_sum(trades)
        change_price(trades)
