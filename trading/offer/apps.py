from django.apps import AppConfig
from trading.settings import INSTALLED_APPS
# print(INSTALLED_APPS)
class OfferConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'offer'
