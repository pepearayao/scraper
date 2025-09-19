import pytest
from django.contrib.auth import get_user_model
from users.models import UserManager

User = get_user_model()


@pytest.mark.unit
@pytest.mark.models
class TestUserManagerMethods:
    """Test cases for UserManager specific methods."""

    @pytest.mark.django_db
    def test_user_manager_instance(self):
        """Test that User.objects is an instance of UserManager."""
        assert isinstance(User.objects, UserManager)

    @pytest.mark.django_db
    def test_manager_create_user_defaults(self):
        """Test default values when creating user through manager."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

        assert user.is_active is True
        assert user.is_staff is False
        assert not hasattr(user, "is_superuser") or user.is_superuser is False

    @pytest.mark.django_db
    def test_manager_create_user_with_custom_fields(self):
        """Test creating user with custom field values."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", is_active=False
        )

        assert user.is_active is False
        assert user.is_staff is False

    @pytest.mark.django_db
    def test_manager_create_user_password_is_hashed(self):
        """Test that password is properly hashed when creating user."""
        password = "testpass123"
        user = User.objects.create_user(email="test@example.com", password=password)

        # Password should be hashed, not stored in plain text
        assert user.password != password
        assert user.check_password(password) is True

    @pytest.mark.django_db
    def test_manager_create_user_without_password(self):
        """Test creating user without password."""
        user = User.objects.create_user(email="test@example.com")

        assert user.email == "test@example.com"
        # User should have unusable password
        assert not user.has_usable_password()

    @pytest.mark.django_db
    def test_manager_create_superuser_sets_required_permissions(self):
        """Test that create_superuser properly sets all required permissions."""
        user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True

    @pytest.mark.django_db
    def test_manager_email_normalization(self):
        """Test that manager properly normalizes email addresses."""
        test_cases = [
            ("test@EXAMPLE.com", "test@example.com"),
            ("Test@Example.COM", "Test@example.com"),
            ("user@DOMAIN.ORG", "user@domain.org"),
        ]

        for input_email, expected_email in test_cases:
            user = User.objects.create_user(email=input_email, password="testpass123")
            assert user.email == expected_email
            user.delete()  # Clean up for next iteration
