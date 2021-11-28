from django.contrib import admin

from .models import Item, Price, Currency, Offer, Trade, WatchList, Inventory, Money


admin.site.register(Price)
admin.site.register(Item)
admin.site.register(Currency)
admin.site.register(Offer)
admin.site.register(Trade)
admin.site.register(Inventory)
admin.site.register(WatchList)
admin.site.register(Money)
