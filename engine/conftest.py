import pytest
from django.test import override_settings
from users.models import User


@pytest.fixture
def user_manager():
    """Fixture providing User model manager."""
    return User.objects


@pytest.fixture
def create_user(db):
    """Fixture for creating test users."""

    def _create_user(email="test@example.com", password="testpass123", **kwargs):
        return User.objects.create_user(email=email, password=password, **kwargs)

    return _create_user


@pytest.fixture
def create_superuser(db):
    """Fixture for creating test superusers."""

    def _create_superuser(email="admin@example.com", password="adminpass123", **kwargs):
        return User.objects.create_superuser(email=email, password=password, **kwargs)

    return _create_superuser


@pytest.fixture
def user(create_user):
    """Fixture providing a standard test user."""
    return create_user()


@pytest.fixture
def superuser(create_superuser):
    """Fixture providing a test superuser."""
    return create_superuser()


@pytest.fixture
def multiple_users(create_user):
    """Fixture providing multiple test users."""
    return [
        create_user(email="user1@example.com"),
        create_user(email="user2@example.com"),
        create_user(email="user3@example.com"),
    ]


@pytest.fixture
def test_settings():
    """Fixture for test-specific Django settings overrides."""
    return override_settings(
        PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
