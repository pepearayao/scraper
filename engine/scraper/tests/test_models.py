import uuid

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from scraper.models import Job, Project, Results, Run
from scraper.tests.factories import (
    CompletedRunFactory,
    FailedRunFactory,
    JobFactory,
    ProjectFactory,
    ResultsFactory,
    RunFactory,
    RunningRunFactory,
)
from users.tests.factories import UserFactory


@pytest.mark.unit
@pytest.mark.models
class TestProjectModel:
    """Test cases for the Project model."""

    @pytest.mark.django_db
    def test_create_project(self):
        """Test creating a project."""
        project = ProjectFactory()
        assert isinstance(project.id, uuid.UUID)
        assert project.name
        assert project.owner
        assert project.created_at
        assert str(project) == project.name

    @pytest.mark.django_db
    def test_project_without_owner(self):
        """Test creating a project without an owner."""
        project = ProjectFactory(owner=None)
        assert project.owner is None
        assert project.name
        assert project.created_at

    @pytest.mark.django_db
    def test_project_str_representation(self):
        """Test the string representation of a project."""
        name = "Test Scraping Project"
        project = ProjectFactory(name=name)
        assert str(project) == name

    @pytest.mark.django_db
    def test_project_owner_relationship(self):
        """Test the relationship between project and owner."""
        user = UserFactory()
        project = ProjectFactory(owner=user)
        assert project.owner == user


@pytest.mark.unit
@pytest.mark.models
class TestJobModel:
    """Test cases for the Job model."""

    @pytest.mark.django_db
    def test_create_job(self):
        """Test creating a job."""
        job = JobFactory()
        assert isinstance(job.id, uuid.UUID)
        assert job.project
        assert job.name
        assert job.raw_yaml
        assert job.parsed_yaml
        assert job.is_active is True
        assert job.created_at
        assert job.updated_at
        assert str(job) == job.name

    @pytest.mark.django_db
    def test_job_without_project(self):
        """Test creating a job without a project."""
        job = JobFactory(project=None)
        assert job.project is None
        assert job.name

    @pytest.mark.django_db
    def test_job_yaml_fields(self):
        """Test job YAML fields."""
        raw_yaml = "name: test\nurl: https://example.com"
        parsed_yaml = {"name": "test", "url": "https://example.com"}

        job = JobFactory(raw_yaml=raw_yaml, parsed_yaml=parsed_yaml)
        assert job.raw_yaml == raw_yaml
        assert job.parsed_yaml == parsed_yaml

    @pytest.mark.django_db
    def test_job_default_values(self):
        """Test job default values."""
        job = JobFactory()
        assert job.is_active is True
        assert job.last_run_at is None

    @pytest.mark.django_db
    def test_job_inactive(self):
        """Test creating an inactive job."""
        job = JobFactory(is_active=False)
        assert job.is_active is False


@pytest.mark.unit
@pytest.mark.models
class TestRunModel:
    """Test cases for the Run model."""

    @pytest.mark.django_db
    def test_create_run(self):
        """Test creating a run."""
        run = RunFactory()
        assert isinstance(run.id, uuid.UUID)
        assert run.job
        assert run.status == "queued"
        assert run.prefect_state
        assert run.prefect_flow_run_id

    @pytest.mark.django_db
    def test_run_status_choices(self):
        """Test run status choices."""
        # Test each status choice
        statuses = ["queued", "running", "success", "failure"]
        for status in statuses:
            run = RunFactory(status=status)
            assert run.status == status

    @pytest.mark.django_db
    def test_running_run(self):
        """Test creating a running run."""
        run = RunningRunFactory()
        assert run.status == "running"
        assert run.started_at
        assert run.finished_at is None

    @pytest.mark.django_db
    def test_completed_run(self):
        """Test creating a completed run."""
        run = CompletedRunFactory()
        assert run.status == "success"
        assert run.started_at
        assert run.finished_at
        assert run.finished_at >= run.started_at

    @pytest.mark.django_db
    def test_failed_run(self):
        """Test creating a failed run."""
        run = FailedRunFactory()
        assert run.status == "failure"
        assert run.started_at
        assert run.finished_at
        assert run.logs
        assert "Error" in run.logs

    @pytest.mark.django_db
    def test_run_str_representation(self):
        """Test the string representation of a run."""
        run = RunningRunFactory()
        expected = f"Run {run.job.name} - {run.started_at} - {run.status}"
        assert str(run) == expected

    @pytest.mark.django_db
    def test_run_without_job(self):
        """Test creating a run without a job."""
        run = RunFactory(job=None)
        assert run.job is None

    @pytest.mark.django_db
    def test_run_prefect_integration_fields(self):
        """Test Prefect integration fields."""
        prefect_state = "Running"
        prefect_flow_run_id = str(uuid.uuid4())

        run = RunFactory(
            prefect_state=prefect_state, prefect_flow_run_id=prefect_flow_run_id
        )
        assert run.prefect_state == prefect_state
        assert run.prefect_flow_run_id == prefect_flow_run_id


@pytest.mark.unit
@pytest.mark.models
class TestResultsModel:
    """Test cases for the Results model."""

    @pytest.mark.django_db
    def test_create_results(self):
        """Test creating results."""
        results = ResultsFactory()
        assert isinstance(results.id, uuid.UUID)
        assert results.run
        assert results.payload
        assert results.artifacts
        assert results.created_at

    @pytest.mark.django_db
    def test_results_payload_structure(self):
        """Test results payload structure."""
        results = ResultsFactory()
        assert "data" in results.payload
        assert "metadata" in results.payload
        assert isinstance(results.payload["data"], list)

    @pytest.mark.django_db
    def test_results_artifacts_structure(self):
        """Test results artifacts structure."""
        results = ResultsFactory()
        assert "screenshots" in results.artifacts
        assert "logs" in results.artifacts
        assert isinstance(results.artifacts["screenshots"], list)
        assert isinstance(results.artifacts["logs"], list)

    @pytest.mark.django_db
    def test_results_without_run(self):
        """Test creating results without a run."""
        results = ResultsFactory(run=None)
        assert results.run is None

    @pytest.mark.django_db
    def test_results_empty_payload(self):
        """Test creating results with empty payload."""
        results = ResultsFactory(payload=None, artifacts=None)
        assert results.payload is None
        assert results.artifacts is None

    @pytest.mark.django_db
    def test_results_custom_payload(self):
        """Test creating results with custom payload."""
        custom_payload = {"scraped_items": 42, "errors": [], "success": True}
        custom_artifacts = {
            "files": ["data.json", "report.html"],
            "duration": "00:05:23",
        }

        results = ResultsFactory(payload=custom_payload, artifacts=custom_artifacts)
        assert results.payload == custom_payload
        assert results.artifacts == custom_artifacts
