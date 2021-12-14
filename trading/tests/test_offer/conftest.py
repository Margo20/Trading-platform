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
        username='admin',
    )
    user.set_password('admin')
    user.save()
    return user


@pytest.fixture
def filled_trade_bakery():
    def creator():
        trade = baker.make(
            'offer.Trade',
            item=baker.make('offer.Item'),
            currenc=baker.make('offer.Currency'),
            seller=baker.make('authentication.User'),
            buyer=baker.make('authentication.User'),
        )
        return trade

    return creator
