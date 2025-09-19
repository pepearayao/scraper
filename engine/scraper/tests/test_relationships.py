import pytest
from django.db import IntegrityError
from scraper.models import Job, Project, Results, Run
from scraper.tests.factories import (
    CompletedRunFactory,
    JobFactory,
    ProjectFactory,
    ResultsFactory,
    RunFactory,
)
from users.tests.factories import UserFactory


@pytest.mark.unit
@pytest.mark.models
class TestModelRelationships:
    """Test cases for relationships between models."""

    @pytest.mark.django_db
    def test_project_to_user_relationship(self):
        """Test the relationship from Project to User."""
        user = UserFactory()
        project = ProjectFactory(owner=user)

        assert project.owner == user
        # Test reverse relationship access
        user_projects = user.project_set.all()
        assert project in user_projects

    @pytest.mark.django_db
    def test_job_to_project_relationship(self):
        """Test the relationship from Job to Project."""
        project = ProjectFactory()
        job = JobFactory(project=project)

        assert job.project == project
        # Test reverse relationship access
        project_jobs = project.job_set.all()
        assert job in project_jobs

    @pytest.mark.django_db
    def test_run_to_job_relationship(self):
        """Test the relationship from Run to Job."""
        job = JobFactory()
        run = RunFactory(job=job)

        assert run.job == job
        # Test reverse relationship access
        job_runs = job.run_set.all()
        assert run in job_runs

    @pytest.mark.django_db
    def test_results_to_run_relationship(self):
        """Test the relationship from Results to Run."""
        run = CompletedRunFactory()
        results = ResultsFactory(run=run)

        assert results.run == run
        # Test reverse relationship access
        run_results = run.results_set.all()
        assert results in run_results

    @pytest.mark.django_db
    def test_cascade_protection_user_project(self):
        """Test that user deletion is protected when projects exist."""
        user = UserFactory()
        ProjectFactory(owner=user)

        # Attempting to delete user should be protected
        # Note: This depends on the on_delete=models.PROTECT setting
        with pytest.raises(IntegrityError):
            user.delete()

    @pytest.mark.django_db
    def test_cascade_protection_project_job(self):
        """Test that project deletion is protected when jobs exist."""
        project = ProjectFactory()
        JobFactory(project=project)

        # Attempting to delete project should be protected
        with pytest.raises(IntegrityError):
            project.delete()

    @pytest.mark.django_db
    def test_cascade_protection_job_run(self):
        """Test that job deletion is protected when runs exist."""
        job = JobFactory()
        RunFactory(job=job)

        # Attempting to delete job should be protected
        with pytest.raises(IntegrityError):
            job.delete()

    @pytest.mark.django_db
    def test_cascade_protection_run_results(self):
        """Test that run deletion is protected when results exist."""
        run = CompletedRunFactory()
        ResultsFactory(run=run)

        # Attempting to delete run should be protected
        with pytest.raises(IntegrityError):
            run.delete()

    @pytest.mark.django_db
    def test_multiple_jobs_per_project(self):
        """Test that a project can have multiple jobs."""
        project = ProjectFactory()
        job1 = JobFactory(project=project, name="Job 1")
        job2 = JobFactory(project=project, name="Job 2")
        job3 = JobFactory(project=project, name="Job 3")

        project_jobs = project.job_set.all()
        assert len(project_jobs) == 3
        assert job1 in project_jobs
        assert job2 in project_jobs
        assert job3 in project_jobs

    @pytest.mark.django_db
    def test_multiple_runs_per_job(self):
        """Test that a job can have multiple runs."""
        job = JobFactory()
        run1 = RunFactory(job=job, status="success")
        run2 = RunFactory(job=job, status="failure")
        run3 = RunFactory(job=job, status="queued")

        job_runs = job.run_set.all()
        assert len(job_runs) == 3
        assert run1 in job_runs
        assert run2 in job_runs
        assert run3 in job_runs

    @pytest.mark.django_db
    def test_multiple_results_per_run(self):
        """Test that a run can have multiple results (if needed)."""
        run = CompletedRunFactory()
        result1 = ResultsFactory(run=run, payload={"batch": 1})
        result2 = ResultsFactory(run=run, payload={"batch": 2})

        run_results = run.results_set.all()
        assert len(run_results) == 2
        assert result1 in run_results
        assert result2 in run_results

    @pytest.mark.django_db
    def test_complex_relationship_chain(self):
        """Test navigating through the complete relationship chain."""
        user = UserFactory(email="owner@example.com")
        project = ProjectFactory(owner=user, name="Test Project")
        job = JobFactory(project=project, name="Test Job")
        run = CompletedRunFactory(job=job, status="success")
        results = ResultsFactory(run=run)

        # Test navigating from results back to user
        assert results.run.job.project.owner == user
        assert results.run.job.project.name == "Test Project"
        assert results.run.job.name == "Test Job"

        # Test navigating from user forward to results
        user_results = Results.objects.filter(run__job__project__owner=user)
        assert results in user_results

    @pytest.mark.django_db
    def test_null_relationships(self):
        """Test that null relationships work as expected."""
        # Project without owner
        project = ProjectFactory(owner=None)
        assert project.owner is None

        # Job without project
        job = JobFactory(project=None)
        assert job.project is None

        # Run without job
        run = RunFactory(job=None)
        assert run.job is None

        # Results without run
        results = ResultsFactory(run=None)
        assert results.run is None
