from model_bakery import baker
import json
import pytest
from offer.models import Currency, Trade, Offer, Inventory, Item, StockBase
from authentication.models import User
from django.urls import reverse


pytestmark = [pytest.mark.urls('config.urls'), pytest.mark.django_db, pytest.mark.unit]

def test_detail_show_currenc(client):
    currenc = Currency.objects.create(name = 'USD', course=15)
    client.login(username='admin', password='admin')

    myRequest = reverse('offer:currency-detail', args=[currenc.id])
    response = client.get(myRequest)

    assert  response.status_code==200
    assert 'USD' in response.content.decode()
    assert '15' in response.content.decode()

def test_detail_show_invenory(client):
    currenc = Currency.objects.create(name='USD', course=11)
    stockbase = StockBase.objects.create(name='Apple')
    item = Item.objects.create(name = stockbase, price=15, currenc=currenc)

    client.login(username='admin', password='admin')
    user = User.objects.get(username='admin')

    inventory = Inventory.objects.create(user=user, item = item, quantity=5)
    myRequest = reverse('offer:inventory-detail', args=[inventory.id])
    response = client.get(myRequest)

    assert  response.status_code==200
    assert '5' in response.content.decode()
    assert '1' in response.content.decode()


def test_detail_show_trade(client):
    currenc = Currency.objects.create(name = 'USD', course=1)
    user = User.objects.create()
    seller = User.objects.get(username='admin')
    stockbase = StockBase.objects.create(name='Apple')
    item = Item.objects.create(name=stockbase)
    client.login(username='admin', password='admin')

    trade = Trade.objects.create(item = item, quantity = 3, unit_price=17.00,
                                  currenc=currenc, seller=seller, buyer=user)
    response = client.get(reverse('offer:trade-detail', args=[trade.id]))

    assert  response.status_code==200
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

    @pytest.mark.parametrize('field',[
        ('name'),
        ('course'),
    ])
    def test_partial_update(self, mocker, rf, field, api_client):
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

    def test_delete(self, mocker, api_client):
        client = api_client()
        client.login(username='admin', password='admin')

        currency = baker.make(Currency)
        url = f'{self.endpoint}{currency.id}/'

        response = client.delete(url)

        assert response.status_code == 204
        assert Currency.objects.all().count() == 0



class TestTradeEndpoints:

    endpoint = '/trade/'

    def test_list(self, api_client, utbb):
        client = api_client()
        client.login(username='admin', password='admin')
        # utbb(3)
        url = self.endpoint
        response = client.get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_create(self, api_client, utbb2):
        client = api_client()
        client.login(username='admin', password='admin')

        t = utbb2(1)[0]
        valid_data_dict = {
            'currenc': str(t.currenc),
            'item': t.item.pk,
            'quantity':3,
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
        responseJson = json.loads(response.content)
        assert responseJson['date'] is not None
        del responseJson['date']
        expectedJson = json.loads(
            '{"item": 1, "unit_price": "15.00", "quantity": 3, "buyer": 3, "buyer_offer": null, "seller": 2, "seller_offer": null}')
        assert responseJson == expectedJson


    def test_retrieve(self, api_client, ftb):
        client = api_client()
        client.login(username='admin', password='admin')

        t = ftb()
        expected_json = {} # t.__dict__
        expected_json['item'] = t.item.pk
        expected_json['quantity'] = t.quantity
        expected_json['unit_price'] = str(t.unit_price)
        expected_json['seller'] = t.seller.pk
        expected_json['buyer'] = t.buyer.pk
        expected_json['buyer_offer'] = None
        expected_json['seller_offer'] = None


        url = f'{self.endpoint}{t.id}/'

        response = client.get(url)

        assert response.status_code == 200 or response.status_code == 301

        responseJson = json.loads(response.content)
        assert responseJson['date'] is not None
        del responseJson['date']
        assert responseJson == expected_json


    def test_update(self, api_client, utbb):
        client = api_client()
        client.login(username='admin', password='admin')

        old_transaction = utbb(1)[0]
        t = utbb(1)[0]
        expected_json = {}
        expected_json['id'] = old_transaction.id
        expected_json['item'] = old_transaction.item.pk
        # expected_json['currenc'] = 11
        expected_json['quantity'] = 5
        expected_json['unit_price'] = '15.00'
        expected_json['seller'] = old_transaction.seller.pk
        expected_json['buyer'] = old_transaction.buyer.pk
        expected_json['buyer_offer'] = None
        expected_json['seller_offer'] = None

        url = f'{self.endpoint}{old_transaction.id}/'

        response = client.put(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200 or response.status_code == 301
        responseJson = json.loads(response.content)
        assert responseJson['date'] is not None
        del responseJson['date']
        del expected_json['id']
        assert responseJson == expected_json

    def test_delete(self, api_client, utbb):
        client = api_client()
        client.login(username='admin', password='admin')
        transaction = utbb(1)[0]
        url = f'{self.endpoint}{transaction.id}/'

        response = client.delete(
            url
        )

        assert response.status_code == 204 or response.status_code == 301
