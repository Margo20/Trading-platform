from offer.models import Inventory, Item, Price, Money


def change_quantity(trades):
    stocks = Inventory.objects.select_related('item', 'user').filter(
        user__in=[i.buyer for i in trades] + [i.seller for i in trades])

    for stock in stocks:
        for trade in trades:
            if trade.item == stock.item:
                stock.quantity += trade.quantity if stock.user == trade.buyer else -trade.quantity
    Inventory.objects.bulk_update(stocks, ['quantity'])


def change_sum(trades):
    wallets = Money.objects.select_related('user').filter(
        user__in=[i.buyer for i in trades] + [i.seller for i in trades])
    for trade in trades:
        for wallet in wallets:
            wallet.sum += trade.unit_price * trade.quantity if wallet.user == trade.seller else -trade.unit_price * trade.quantity
    Money.objects.bulk_update(wallets, ['sum'])


def change_price(trades):
    prices = Price.objects.select_related('item', 'item__currenc').all()
    items = Item.objects.select_related('currenc').all()

    for trade in trades:
        for price in prices:
            if price.item == trade.item:
                price.price = trade.unit_price
                for item in items:
                    item.price = price.price

    Item.objects.bulk_update(items, ['price'])
    Price.objects.bulk_update(prices, ['price'])
