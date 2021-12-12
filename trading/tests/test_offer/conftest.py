import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from authentication.models import User


@pytest.fixture
def api_client():
    return APIClient

@pytest.fixture(autouse=True)
def test_user():
    user = User.objects.create(
        email='ad@mail.ru',
        username ='admin',
    )
    user.set_password('admin')
    user.save()
    return user

@pytest.fixture
def utbb():
    def unfilled_transaction_bakery_batch(n):
        utbb = baker.make(
            'offer.Trade',
            _fill_optional=[
                'item',
                'quantity',
                'unit_price',
                'currenc',
                'seller',
                'buyer',
            ],
            _quantity=n
        )
        return utbb
    return unfilled_transaction_bakery_batch

@pytest.fixture
def utbb2():
    def unfilled_transaction_bakery_batch(n):
        utbb = baker.make(
            'offer.Trade',
            item=baker.make('offer.Item'),
            currenc=baker.make('offer.Currency'),
            seller=baker.make('authentication.User'),
            buyer=baker.make('authentication.User'),
            _fill_optional=[
                'quantity',
                'unit_price',
            ],
            _quantity=n
        )
        return utbb
    return unfilled_transaction_bakery_batch

@pytest.fixture
def ftbb():
    def filled_transaction_bakery_batch(n):
        utbb = baker.make(
            'offer.Trade',
            _quantity=n
        )
        return utbb
    return filled_transaction_bakery_batch

@pytest.fixture
def ftb():
    def filled_transaction_bakery():
        utbb = baker.make(
            'offer.Trade',
            item = baker.make('offer.Item'),
            currenc = baker.make('offer.Currency'),
            seller = baker.make('authentication.User'),
            buyer = baker.make('authentication.User'),
        )
        return utbb
    return filled_transaction_bakery
