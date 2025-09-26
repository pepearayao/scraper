import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status
from users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.unit
@pytest.mark.api
class TestAuthEndpoints:
    """Test cases for authentication API endpoints."""

    def setup_method(self):
        """Setup test client and base data."""
        self.client = Client()
        self.user = UserFactory(email="test@example.com")
        self.user.set_password("testpass123")
        self.user.save()

    @pytest.mark.django_db
    def test_obtain_token_success(self):
        """Test successful token generation."""
        data = {"email": "test@example.com", "password": "testpass123"}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert "data" in json_response
        assert "access" in json_response["data"]
        assert "refresh" in json_response["data"]
        assert json_response["meta"] is None

    @pytest.mark.django_db
    def test_obtain_token_invalid_credentials(self):
        """Test token generation with invalid credentials."""
        data = {"email": "test@example.com", "password": "wrongpassword"}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        json_response = response.json()
        assert json_response["status"] == "error"
        assert json_response["code"] == "INVALID_CREDENTIALS"

    @pytest.mark.django_db
    def test_obtain_token_nonexistent_user(self):
        """Test token generation with non-existent user."""
        data = {"email": "nonexistent@example.com", "password": "testpass123"}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        json_response = response.json()
        assert json_response["status"] == "error"
        assert json_response["code"] == "INVALID_CREDENTIALS"

    @pytest.mark.django_db
    def test_obtain_token_missing_email(self):
        """Test token generation with missing email."""
        data = {"password": "testpass123"}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_obtain_token_missing_password(self):
        """Test token generation with missing password."""
        data = {"email": "test@example.com"}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_obtain_token_empty_data(self):
        """Test token generation with empty data."""
        data = {}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_refresh_token_success(self):
        """Test successful token refresh."""
        # First, obtain tokens
        login_data = {"email": "test@example.com", "password": "testpass123"}
        login_response = self.client.post(
            "/api/v1/auth/token",
            data=login_data,
            content_type="application/json",
        )
        refresh_token = login_response.json()["data"]["refresh"]

        # Now refresh the token
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(
            "/api/v1/auth/refresh",
            data=refresh_data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert "data" in json_response
        assert "access" in json_response["data"]
        assert json_response["meta"] is None

    @pytest.mark.django_db
    def test_refresh_token_invalid_token(self):
        """Test token refresh with invalid refresh token."""
        data = {"refresh": "invalid.token.here"}

        response = self.client.post(
            "/api/v1/auth/refresh",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        json_response = response.json()
        assert json_response["status"] == "error"
        assert json_response["code"] == "INVALID_REFRESH_TOKEN"

    @pytest.mark.django_db
    def test_refresh_token_missing_token(self):
        """Test token refresh with missing refresh token."""
        data = {}

        response = self.client.post(
            "/api/v1/auth/refresh",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_token_response_structure(self):
        """Test that token response matches expected schema."""
        data = {"email": "test@example.com", "password": "testpass123"}

        response = self.client.post(
            "/api/v1/auth/token",
            data=data,
            content_type="application/json",
        )

        json_response = response.json()

        # Verify response structure matches TokenSuccessResponse schema
        assert "status" in json_response
        assert "data" in json_response
        assert "meta" in json_response

        # Verify data structure matches TokenResponse schema
        data_section = json_response["data"]
        assert "access" in data_section
        assert "refresh" in data_section
        assert isinstance(data_section["access"], str)
        assert isinstance(data_section["refresh"], str)

    @pytest.mark.django_db
    def test_refresh_response_structure(self):
        """Test that refresh response matches expected schema."""
        # First, obtain tokens
        login_data = {"email": "test@example.com", "password": "testpass123"}
        login_response = self.client.post(
            "/api/v1/auth/token",
            data=login_data,
            content_type="application/json",
        )
        refresh_token = login_response.json()["data"]["refresh"]

        # Now refresh the token
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(
            "/api/v1/auth/refresh",
            data=refresh_data,
            content_type="application/json",
        )

        json_response = response.json()

        # Verify response structure matches RefreshSuccessResponse schema
        assert "status" in json_response
        assert "data" in json_response
        assert "meta" in json_response

        # Verify data structure matches RefreshResponse schema
        data_section = json_response["data"]
        assert "access" in data_section
        assert isinstance(data_section["access"], str)
        # Refresh response should not contain refresh token
        assert "refresh" not in data_section
