from django.db import models
from authentication.models import User


class Currency(models.Model):
    name = models.CharField(max_length=25)
    course = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюта"

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    """Particular stock"""
    name = models.OneToOneField('StockBase', related_name='item_name', max_length=30, blank=True, null=True,
                                on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currenc = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f"{self.name}-{self.price}"


class Price(models.Model):
    """Item prices"""
    currenc = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Стоимость акции"
        verbose_name_plural = "Стоимость акций"

    def __str__(self):
        return f"{self.item}-{self.price}"


class Money(models.Model):
    """users money"""
    user = models.ForeignKey(User, related_name='wallets', on_delete=models.CASCADE)
    sum = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currenc = models.ForeignKey("Currency", max_length=15, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Сумма на счету"
        verbose_name_plural = "Средства на счетах"

    def __str__(self):
        return f"{self.user}-{self.sum}-{self.currenc}"


class Offer(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    entry_quantity = models.IntegerField("Requested quantity")
    quantity = models.IntegerField("Current quantity")
    OrderType = [("sale", "sale"), ("buying", "buying")]
    order_type = models.CharField(max_length=25, choices=OrderType, default="buying", verbose_name="Тип сделки", )
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Купля-продажа"
        verbose_name_plural = "Купля-продажа"

    def __str__(self):
        return f"{self.item}-{self.order_type}-{self.price}-{self.user}-{self.quantity}"


class Trade(models.Model):
    """Information about a certain transaction"""
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    currenc = models.CharField(max_length=20, blank=True, null=True)
    buyer_offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL, related_name='buyer_trade',
                                    related_query_name='buyer_trade')
    seller_offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='seller_trade',
                                     related_query_name='seller_trade')

    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='seller_trade')
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='buyer_trade')
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    def __str__(self):
        return f"{self.item}-{self.unit_price}-{self.buyer}"


class Inventory(models.Model):
    """The number of stocks a particular user has"""
    user = models.ForeignKey(User, related_name='stocks', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField("Stocks quantity", default=0)

    class Meta:
        verbose_name = "Акция пользователя"
        verbose_name_plural = "Акции пользователей"

    def __str__(self):
        return f"{self.user}-{self.item}-{self.quantity}"


class StockBase(models.Model):
    """Base"""
    name = models.CharField("Name", max_length=128, unique=True)
    code = models.CharField("Code", max_length=8, unique=True)

    class Meta:
        verbose_name = "Имя и код акции"
        verbose_name_plural = "Имена и коды акций"

    def __str__(self):
        return f"{self.name}"


class WatchList(models.Model):
    """Current user, favorite list of stocks"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey('StockBase', related_name='watchlist', max_length=30, blank=True, null=True,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Список предпочтений"
        verbose_name_plural = "Списки предпочтений"

    def __str__(self):
        return f"{self.user}:{self.item}"
