import factory

from authentication.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

UserFactory()
