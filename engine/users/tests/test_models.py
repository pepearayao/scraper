import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from users.tests.factories import StaffUserFactory, SuperUserFactory, UserFactory

User = get_user_model()


@pytest.mark.unit
@pytest.mark.models
class TestUserModel:
    """Test cases for the User model."""

    @pytest.mark.django_db
    def test_create_user_with_email(self):
        """Test creating a user with email."""
        user = UserFactory()
        assert user.email
        assert user.is_active is True
        assert user.is_staff is False
        assert user.date_joined
        assert str(user) == user.email

    @pytest.mark.django_db
    def test_create_staff_user(self):
        """Test creating a staff user."""
        user = StaffUserFactory()
        assert user.is_staff is True
        assert user.is_active is True

    @pytest.mark.django_db
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = SuperUserFactory()
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True

    @pytest.mark.django_db
    def test_email_uniqueness(self):
        """Test that email addresses must be unique."""
        email = "test@example.com"
        UserFactory(email=email)

        with pytest.raises(IntegrityError):
            UserFactory(email=email)

    @pytest.mark.django_db
    def test_user_str_representation(self):
        """Test the string representation of a user."""
        email = "test@example.com"
        user = UserFactory(email=email)
        assert str(user) == email


@pytest.mark.unit
@pytest.mark.models
class TestUserManager:
    """Test cases for the UserManager."""

    @pytest.mark.django_db
    def test_create_user_with_email_and_password(self):
        """Test creating a user with email and password."""
        email = "test@example.com"
        password = "testpass123"

        user = User.objects.create_user(email=email, password=password)

        assert user.email == email
        assert user.check_password(password)
        assert user.is_active is True
        assert user.is_staff is False

    @pytest.mark.django_db
    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", password="testpass123")

    @pytest.mark.django_db
    def test_create_user_normalizes_email(self):
        """Test that email is normalized when creating a user."""
        email = "Test@EXAMPLE.COM"
        user = User.objects.create_user(email=email, password="testpass123")

        assert user.email == "Test@example.com"  # Domain should be lowercase

    @pytest.mark.django_db
    def test_create_superuser(self):
        """Test creating a superuser."""
        email = "admin@example.com"
        password = "adminpass123"

        user = User.objects.create_superuser(email=email, password=password)

        assert user.email == email
        assert user.check_password(password)
        assert user.is_active is True
        assert user.is_staff is True
        assert user.is_superuser is True

    @pytest.mark.django_db
    def test_create_superuser_with_extra_fields(self):
        """Test creating a superuser with additional fields."""
        email = "admin@example.com"
        password = "adminpass123"

        user = User.objects.create_superuser(
            email=email, password=password, is_active=False  # This should be overridden
        )

        assert user.is_staff is True
        assert user.is_superuser is True

    @pytest.mark.django_db
    def test_create_superuser_without_staff_raises_error(self):
        """Test that creating superuser with is_staff=False raises ValueError."""
        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email="admin@example.com", password="adminpass123", is_staff=False
            )

    @pytest.mark.django_db
    def test_create_superuser_without_superuser_raises_error(self):
        """Test that creating superuser with is_superuser=False raises ValueError."""
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True"):
            User.objects.create_superuser(
                email="admin@example.com", password="adminpass123", is_superuser=False
            )
