# from celery import shared_task
from trading.celery import app
from django.db import transaction
from .models import Offer, Trade


@app.task
# @transaction.atomic
def req():
    buyers = Offer.objects.filter(order_type="buying", quantity__gt=0)
    sellers = Offer.objects.filter(order_type="sale", quantity__gt=0).order_by("price")
    trades = []
    for i in buyers:
        sel = []
        for j in sellers:
            if i.item == j.item and i.price >= j.price:
                sel.append(j)
                if i.quantity <= j.quantity:
                    trades.append(Trade(item=i.item, quantity=i.quantity, unit_price=j.price, buyer_offer=i,
                                        seller_offer=j, seller=j.user, buyer=i.user))
                    j.quantity = j.quantity - i.quantity
                    i.quantity = 0
                    break
                else:
                    trades.append(Trade(item=i.item, quantity=j.quantity, unit_price=j.price, buyer_offer=i,
                                        seller_offer=j, seller=j.user, buyer=i.user))
                    i.quantity -= j.quantity
                    j.quantity = 0
    print(sellers[0].quantity)
    with transaction.atomic():
        Trade.objects.bulk_create(trades)
        Offer.objects.bulk_update(buyers, ['quantity'])
        Offer.objects.bulk_update(sellers, ['quantity'])














    # buyer_results = []
    # seller_results = []
    # offers = Offer.objects.all()
    # for offer in offers:
    #     b = Offer.objects.filter(order_type="buyer")
    #     s = Offer.objects.filter(order_type="seller")

        # if b:
        #     json = resp.json()
        #     buyer_results.append(json)
        #     return buyer_results
        # elif s:
        #     json = resp.json()
        #     seller_results.append(json)
        #     return seller_results

    # instance = Trade()
    # for i in buyer_results:
    #     for j in seller_results:
    #         if i.item == j.item and i.price <= j.price and i.entry_quantity <= j.entry_quantity:
    #             instance.unit_price = i.price  # как добавить сразу в trade?
    #             offers = Offer.objects.all()
    #             for offer in offers:
    #                 if i.quantity < j.quantity:
    #                     instance.quantity = i.quantity  # как добавить сразу в trade?
    #                     j.quantity = j.quantity - i.quantity
    #                     i.quantity = 0
    #                 else:
    #                     instance.quantity = j.quantity  # как добавить сразу в trade?
    #                     i.quantity = i.quantity - j.quantity
    #                     j.quantity = 0
    #             instance.save()
    #             return instance



# from celery import shared_task
# from celery.utils.log import get_task_logger
#
#
# logger = get_task_logger(__name__)
#
#
# @shared_task
# def sample_task():
#     logger.info("The sample task just ran.")