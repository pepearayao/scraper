import factory
from django.contrib.auth.hashers import make_password
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    is_active = True
    is_staff = False

    @factory.lazy_attribute
    def password(self):
        return make_password("testpass123")


class StaffUserFactory(UserFactory):
    """Factory for creating staff User instances."""

    is_staff = True


class SuperUserFactory(UserFactory):
    """Factory for creating superuser instances."""

    is_staff = True
    is_superuser = True
