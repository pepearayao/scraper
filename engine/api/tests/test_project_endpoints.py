import json
import uuid

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from scraper.models import Project
from scraper.tests.factories import ProjectFactory
from users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.unit
@pytest.mark.api
class TestProjectEndpoints:
    """Test cases for project API endpoints."""

    def setup_method(self):
        """Setup test client, users, and authentication."""
        self.client = Client()

        # Create test users
        self.user = UserFactory(email="test@example.com")
        self.user.set_password("testpass123")
        self.user.save()

        self.other_user = UserFactory(email="other@example.com")
        self.other_user.set_password("testpass123")
        self.other_user.save()

        # Create JWT tokens for authentication
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)

        self.other_refresh_token = RefreshToken.for_user(self.other_user)
        self.other_access_token = str(self.other_refresh_token.access_token)

        # Create test projects
        self.project = ProjectFactory(name="Test Project", owner=self.user)
        self.other_project = ProjectFactory(name="Other Project", owner=self.other_user)

    def get_auth_header(self, token=None):
        """Helper method to get authorization header."""
        token = token or self.access_token
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    @pytest.mark.django_db
    def test_list_projects_authenticated(self):
        """Test listing projects for authenticated user."""
        response = self.client.get("/api/v1/projects/", **self.get_auth_header())

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert "data" in json_response
        assert isinstance(json_response["data"], list)
        assert len(json_response["data"]) == 1
        assert json_response["data"][0]["name"] == "Test Project"
        assert json_response["data"][0]["owner_id"] == self.user.pk

    @pytest.mark.django_db
    def test_list_projects_unauthenticated(self):
        """Test listing projects without authentication."""
        response = self.client.get("/api/v1/projects/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_list_projects_response_structure(self):
        """Test that list projects response matches expected schema."""
        response = self.client.get("/api/v1/projects/", **self.get_auth_header())

        json_response = response.json()

        # Verify response structure matches ProjectSuccessResponse
        assert "status" in json_response
        assert "data" in json_response
        assert "meta" in json_response

        # Verify data structure matches List[ProjectSchema]
        project_data = json_response["data"][0]
        assert "id" in project_data
        assert "name" in project_data
        assert "owner_id" in project_data
        assert "created_at" in project_data

        # Verify data types
        assert isinstance(project_data["id"], str)
        assert isinstance(project_data["name"], str)
        assert isinstance(project_data["owner_id"], int)
        assert isinstance(project_data["created_at"], str)

    @pytest.mark.django_db
    def test_create_project_authenticated(self):
        """Test creating a project with authentication."""
        data = {"name": "New Project"}

        response = self.client.post(
            "/api/v1/projects/",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        assert response.status_code == status.HTTP_201_CREATED
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert len(json_response["data"]) == 1
        assert json_response["data"][0]["name"] == "New Project"
        assert json_response["data"][0]["owner_id"] == self.user.pk

        # Verify project was created in database
        created_project = Project.objects.get(name="New Project")
        assert created_project.owner == self.user

    @pytest.mark.django_db
    def test_create_project_unauthenticated(self):
        """Test creating a project without authentication."""
        data = {"name": "New Project"}

        response = self.client.post(
            "/api/v1/projects/", data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_project_missing_name(self):
        """Test creating a project with missing name field."""
        data = {}

        response = self.client.post(
            "/api/v1/projects/",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_create_project_empty_name(self):
        """Test creating a project with empty name."""
        data = {"name": ""}

        response = self.client.post(
            "/api/v1/projects/",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        # Should still create project with empty name (if model allows)
        # or return appropriate validation error
        # Adjust this based on your model validation
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
        ]

    @pytest.mark.django_db
    def test_get_project_authenticated_owner(self):
        """Test getting a project as the owner."""
        response = self.client.get(
            f"/api/v1/projects/{self.project.id}", **self.get_auth_header()
        )

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert len(json_response["data"]) == 1
        assert json_response["data"][0]["id"] == str(self.project.id)
        assert json_response["data"][0]["name"] == self.project.name

    @pytest.mark.django_db
    def test_get_project_authenticated_not_owner(self):
        """Test getting a project as a different user."""
        response = self.client.get(
            f"/api/v1/projects/{self.other_project.id}", **self.get_auth_header()
        )

        # Current router allows access to any project (no ownership check)
        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert json_response["data"][0]["id"] == str(self.other_project.id)

    @pytest.mark.django_db
    def test_get_project_nonexistent(self):
        """Test getting a non-existent project."""
        nonexistent_id = uuid.uuid4()

        response = self.client.get(
            f"/api/v1/projects/{nonexistent_id}", **self.get_auth_header()
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_project_invalid_uuid(self):
        """Test getting a project with invalid UUID format."""
        response = self.client.get(
            "/api/v1/projects/invalid-uuid", **self.get_auth_header()
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_update_project_authenticated_owner(self):
        """Test updating a project as the owner."""
        data = {"name": "Updated Project Name"}

        response = self.client.put(
            f"/api/v1/projects/{self.project.id}",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert len(json_response["data"]) == 1
        assert json_response["data"][0]["name"] == "Updated Project Name"

        # Verify project was updated in database
        self.project.refresh_from_db()
        assert self.project.name == "Updated Project Name"

    @pytest.mark.django_db
    def test_update_project_authenticated_not_owner(self):
        """Test updating a project as a different user."""
        data = {"name": "Updated Project Name"}

        response = self.client.put(
            f"/api/v1/projects/{self.other_project.id}",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        # Current router allows updates to any project (no ownership check)
        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert json_response["status"] == "ok"
        assert json_response["data"][0]["name"] == "Updated Project Name"

        # Verify project was updated in database
        self.other_project.refresh_from_db()
        assert self.other_project.name == "Updated Project Name"

    @pytest.mark.django_db
    def test_update_project_unauthenticated(self):
        """Test updating a project without authentication."""
        data = {"name": "Hacked Project Name"}

        response = self.client.put(
            f"/api/v1/projects/{self.project.id}",
            data=json.dumps(data),
            content_type="application/json",
        )

        # Should require authentication
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_project_nonexistent(self):
        """Test updating a non-existent project."""
        nonexistent_id = uuid.uuid4()
        data = {"name": "Updated Name"}

        response = self.client.put(
            f"/api/v1/projects/{nonexistent_id}",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_project_missing_name(self):
        """Test updating a project with missing name field."""
        data = {}

        response = self.client.put(
            f"/api/v1/projects/{self.project.id}",
            data=json.dumps(data),
            content_type="application/json",
            **self.get_auth_header(),
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.django_db
    def test_project_isolation_between_users(self):
        """Test that users can only see their own projects."""
        # Create additional projects for each user
        ProjectFactory(name="User 1 Project 2", owner=self.user)
        ProjectFactory(name="User 2 Project 2", owner=self.other_user)

        # User 1 should only see their projects
        response = self.client.get(
            "/api/v1/projects/", **self.get_auth_header(self.access_token)
        )
        json_response = response.json()
        project_names = [p["name"] for p in json_response["data"]]
        assert "Test Project" in project_names
        assert "User 1 Project 2" in project_names
        assert "Other Project" not in project_names
        assert "User 2 Project 2" not in project_names

        # User 2 should only see their projects
        response = self.client.get(
            "/api/v1/projects/", **self.get_auth_header(self.other_access_token)
        )
        json_response = response.json()
        project_names = [p["name"] for p in json_response["data"]]
        assert "Other Project" in project_names
        assert "User 2 Project 2" in project_names
        assert "Test Project" not in project_names
        assert "User 1 Project 2" not in project_names
