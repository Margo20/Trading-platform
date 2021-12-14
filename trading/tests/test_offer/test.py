from model_bakery import baker
import json
import pytest
from offer.models import Currency, Trade, Offer, Inventory, Item, StockBase, WatchList, Money, Price
from authentication.models import User
from django.urls import reverse

pytestmark = [pytest.mark.urls('config.urls'), pytest.mark.django_db, pytest.mark.unit]


def test_detail_show_currenc(client):
    currenc = Currency.objects.create(name='USD', course=15)
    client.login(username='admin', password='admin')

    my_request = reverse('offer:currency-detail', args=[currenc.id])
    response = client.get(my_request)

    assert response.status_code == 200
    assert 'USD' in response.content.decode()
    assert '15' in response.content.decode()


def test_detail_show_inventory(client):
    currenc = Currency.objects.create(name='USD', course=11)
    stockbase = StockBase.objects.create(name='Apple')
    item = Item.objects.create(name=stockbase, price=15, currenc=currenc)

    client.login(username='admin', password='admin')
    user = User.objects.get(username='admin')

    inventory = Inventory.objects.create(user=user, item=item, quantity=5)
    my_request = reverse('offer:inventory-detail', args=[inventory.id])
    response = client.get(my_request)

    assert response.status_code == 200
    assert '5' in response.content.decode()
    assert '1' in response.content.decode()


def test_detail_show_trade(client):
    currenc = Currency.objects.create(name='USD', course=1)
    user = User.objects.create()
    seller = User.objects.get(username='admin')
    stockbase = StockBase.objects.create(name='Apple')
    item = Item.objects.create(name=stockbase)
    client.login(username='admin', password='admin')

    trade = Trade.objects.create(item=item, quantity=3, unit_price=17.00,
                                 currenc=currenc, seller=seller, buyer=user)
    response = client.get(reverse('offer:trade-detail', args=[trade.id]))

    assert response.status_code == 200
    assert '17' in response.content.decode()


class TestCurrencyEndpoints:
    endpoint = '/currency/'

    def test_list(self, api_client):
        client = api_client()
        client.login(username='admin', password='admin')
        baker.make(Currency, _quantity=1)

        url = self.endpoint
        response = client.get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_create(self, api_client):
        client = api_client()
        client.login(username='admin', password='admin')

        currency = baker.prepare(Currency)
        expected_json = {
            'name': currency.name,
            'course': currency.course
        }

        response = client.post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json

    def test_retrieve(self, api_client):
        client = api_client()
        client.login(username='admin', password='admin')

        currency = baker.make(Currency)
        expected_json = {
            'name': currency.name,
            'course': currency.course,
        }
        url = f'{self.endpoint}{currency.id}/'

        response = client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, rf, api_client):
        client = api_client()
        client.login(username='admin', password='admin')

        old_currency = baker.make(Currency)
        new_currency = baker.prepare(Currency)
        currency_dict = {
            'course': new_currency.course,
            'name': new_currency.name,
        }

        url = f'{self.endpoint}{old_currency.id}/'

        response = client.put(
            url,
            currency_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) == currency_dict

    @pytest.mark.parametrize('field', [
        'name',
        'course',
    ])
    def test_partial_update(self, rf, field, api_client):
        client = api_client()
        client.login(username='admin', password='admin')

        currency = baker.make(Currency)
        currency_dict = {
            'course': currency.course,
            'name': currency.name,
        }
        valid_field = currency_dict[field]
        url = f'{self.endpoint}{currency.id}/'

        response = client.patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field

    def test_delete(self, api_client):
        client = api_client()
        client.login(username='admin', password='admin')

        currency = baker.make(Currency)
        url = f'{self.endpoint}{currency.id}/'

        response = client.delete(url)

        assert response.status_code == 204
        assert Currency.objects.all().count() == 0


class TestTradeEndpoints:
    endpoint = '/trade/'

    def test_list(self, api_client):
        client = api_client()
        client.login(username='admin', password='admin')
        url = self.endpoint
        response = client.get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_create(self, api_client, filled_trade_bakery):
        client = api_client()
        client.login(username='admin', password='admin')

        t = filled_trade_bakery()
        valid_data_dict = {
            'currenc': str(t.currenc),
            'item': t.item.pk,
            'quantity': 3,
            'unit_price': 15,
            'seller': t.seller.pk,
            'buyer': t.buyer.pk
        }

        url = self.endpoint

        response = client.post(
            url,
            data=valid_data_dict,
            format='json'
        )
        assert response.status_code == 201
        response_json = json.loads(response.content)
        assert response_json['date'] is not None
        del response_json['date']
        expected_json = json.loads(
            '{"item": 1, "unit_price": "15.00", "quantity": 3, "buyer": 3, '
            '"buyer_offer": null, "seller": 2, "seller_offer": null}')
        assert response_json == expected_json

    def test_retrieve(self, api_client, filled_trade_bakery):
        client = api_client()
        client.login(username='admin', password='admin')

        t = filled_trade_bakery()
        expected_json = {
            'item': t.item.pk,
            'quantity': t.quantity,
            'unit_price': str(t.unit_price),
            'seller': t.seller.pk,
            'buyer': t.buyer.pk,
            'buyer_offer': None,
            'seller_offer': None,
        }

        url = f'{self.endpoint}{t.id}/'

        response = client.get(url)

        assert response.status_code == 200 or response.status_code == 301

        response_json = json.loads(response.content)
        assert response_json['date'] is not None
        del response_json['date']
        assert response_json == expected_json

    def test_update(self, api_client, filled_trade_bakery):
        client = api_client()
        client.login(username='admin', password='admin')

        old_transaction = filled_trade_bakery()
        # noinspection PyUnusedLocal
        to_be_updated = filled_trade_bakery()
        expected_json = {
            'id': old_transaction.id,
            'item': old_transaction.item.pk,
            'quantity': 5,
            'unit_price': '15.00',
            'seller': old_transaction.seller.pk,
            'buyer': old_transaction.buyer.pk,
            'buyer_offer': None,
            'seller_offer': None
        }

        url = f'{self.endpoint}{old_transaction.id}/'

        response = client.put(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200 or response.status_code == 301
        response_json = json.loads(response.content)
        assert response_json['date'] is not None
        del response_json['date']
        del expected_json['id']
        assert response_json == expected_json

    def test_delete(self, api_client, filled_trade_bakery):
        client = api_client()
        client.login(username='admin', password='admin')
        transaction = filled_trade_bakery()
        url = f'{self.endpoint}{transaction.id}/'

        response = client.delete(
            url
        )

        assert response.status_code == 204 or response.status_code == 301


class TestModels:
    def test_trade_str(self):
        currenc = Currency.objects.create(name='USD', course=1)
        buyer = User.objects.create(username='myBuyer')
        seller = User.objects.get(username='admin')
        stockbase = StockBase.objects.create(name='Apple')
        item = Item.objects.create(name=stockbase, price=12.0)
        trade = Trade.objects.create(item=item, quantity=3, unit_price=17.00,
                                     currenc=currenc, seller=seller, buyer=buyer)
        as_str = str(trade)
        assert as_str == 'Apple-12.0-17.0-myBuyer'

    def test_currency_str(self):
        currenc = Currency.objects.create(name='USD', course=15)

        as_str = str(currenc)
        assert as_str == 'USD'

    def test_inventory_str(self):
        currenc = Currency.objects.create(name='USD', course=11)
        stockbase = StockBase.objects.create(name='Apple')
        item = Item.objects.create(name=stockbase, price=15, currenc=currenc)
        user = User.objects.create(username='vasia')

        inventory = Inventory.objects.create(user=user, item=item, quantity=5)

        as_str = str(inventory)
        assert as_str == 'vasia-Apple-15-5'

    def test_watchlist_str(self):
        stockbase = StockBase.objects.create(name='Apple')
        user = User.objects.create(username='vasia')

        watchlist = WatchList.objects.create(user=user, item=stockbase)

        as_str = str(watchlist)
        assert as_str == 'vasia:Apple'

    def test_offer_str(self):
        user = User.objects.create(username='vasia')
        stockbase = StockBase.objects.create(name='Apple')
        item = Item.objects.create(name=stockbase, price=15)
        offer = Offer.objects.create(item=item, order_type='sale', price=10,
                                     user=user, quantity=3, entry_quantity=3)
        as_str = str(offer)
        assert as_str == 'Apple-15-sale-10-vasia-3'

    def test_money_str(self):
        currenc = Currency.objects.create(name='USD', course=11)
        user = User.objects.create(username='myBuyer')
        money = Money.objects.create(user=user, sum=3, currenc=currenc)

        as_str = str(money)
        assert as_str == 'myBuyer-3-USD'

    def test_price_str(self):
        currenc = Currency.objects.create(name='USD', course=11)
        stockbase = StockBase.objects.create(name='Apple')
        item = Item.objects.create(name=stockbase, price=15)
        price = Price.objects.create(item=item, price=10.0, currenc=currenc)

        as_str = str(price)
        assert as_str == 'Apple-15-10.0'
