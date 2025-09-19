import pytest
from django.utils import timezone
from scraper.models import Job, Project, Results, Run
from scraper.tests.factories import (
    CompletedRunFactory,
    JobFactory,
    ProjectFactory,
    ResultsFactory,
    RunFactory,
)
from users.tests.factories import UserFactory


@pytest.mark.integration
@pytest.mark.slow
class TestScrapingWorkflow:
    """Integration tests for the complete scraping workflow."""

    @pytest.mark.django_db
    def test_complete_scraping_workflow(self):
        """Test a complete scraping workflow from user to results."""
        # Create user and project
        user = UserFactory(email="scraper@example.com")
        project = ProjectFactory(owner=user, name="E-commerce Product Scraper")

        # Create a scraping job
        job = JobFactory(
            project=project,
            name="Product Listings Scraper",
            raw_yaml="""
name: Product Listings Scraper
url: https://example-store.com/products
selectors:
  - name: .product-title
  - price: .price
  - availability: .stock-status
            """,
            parsed_yaml={
                "name": "Product Listings Scraper",
                "url": "https://example-store.com/products",
                "selectors": {
                    "name": ".product-title",
                    "price": ".price",
                    "availability": ".stock-status",
                },
            },
        )

        # Create a run for the job
        run = CompletedRunFactory(job=job, status="success", prefect_state="Completed")

        # Create results for the run
        results = ResultsFactory(
            run=run,
            payload={
                "scraped_items": [
                    {
                        "name": "Wireless Headphones",
                        "price": "$99.99",
                        "availability": "In Stock",
                    },
                    {
                        "name": "Bluetooth Speaker",
                        "price": "$49.99",
                        "availability": "Limited Stock",
                    },
                ],
                "metadata": {
                    "scraped_at": timezone.now().isoformat(),
                    "total_items": 2,
                    "success_rate": "100%",
                },
            },
            artifacts={
                "screenshots": ["products_page.png"],
                "logs": [
                    "Started scraping at 2024-01-01 10:00:00",
                    "Found 2 products",
                    "Scraping completed successfully",
                ],
            },
        )

        # Verify the complete workflow
        assert project.owner == user
        assert job.project == project
        assert run.job == job
        assert results.run == run

        # Verify data integrity
        assert len(results.payload["scraped_items"]) == 2
        assert results.payload["metadata"]["total_items"] == 2
        assert len(results.artifacts["logs"]) == 3

        # Test reverse relationships
        user_projects = user.project_set.all()
        assert project in user_projects

        project_jobs = project.job_set.all()
        assert job in project_jobs

        job_runs = job.run_set.all()
        assert run in job_runs

        run_results = run.results_set.all()
        assert results in run_results

    @pytest.mark.django_db
    def test_multiple_job_workflow(self):
        """Test workflow with multiple jobs in a project."""
        user = UserFactory()
        project = ProjectFactory(owner=user, name="Multi-Job Project")

        # Create multiple jobs
        job1 = JobFactory(project=project, name="News Articles")
        job2 = JobFactory(project=project, name="Product Reviews")
        job3 = JobFactory(project=project, name="Social Media Posts")

        # Create runs for each job
        run1 = CompletedRunFactory(job=job1, status="success")
        run2 = CompletedRunFactory(job=job2, status="success")
        run3 = CompletedRunFactory(job=job3, status="failure")

        # Create results for successful runs
        results1 = ResultsFactory(run=run1, payload={"articles": 50})
        results2 = ResultsFactory(run=run2, payload={"reviews": 25})

        # Verify all jobs belong to the same project
        project_jobs = project.job_set.all()
        assert len(project_jobs) == 3
        assert {job1, job2, job3} == set(project_jobs)

        # Verify successful results
        successful_runs = Run.objects.filter(job__project=project, status="success")
        assert len(successful_runs) == 2

        # Verify results exist for successful runs only
        project_results = Results.objects.filter(run__job__project=project)
        assert len(project_results) == 2

    @pytest.mark.django_db
    def test_failed_run_workflow(self):
        """Test workflow when a run fails."""
        user = UserFactory()
        project = ProjectFactory(owner=user)
        job = JobFactory(project=project, name="Failing Job")

        # Create a failed run
        failed_run = RunFactory(
            job=job,
            status="failure",
            prefect_state="Failed",
            logs="Error: Connection timeout after 30 seconds",
            started_at=timezone.now(),
            finished_at=timezone.now(),
        )

        # Verify failed run has no results
        run_results = failed_run.results_set.all()
        assert len(run_results) == 0

        # Verify error information is captured
        assert "Error:" in failed_run.logs
        assert failed_run.status == "failure"
        assert failed_run.prefect_state == "Failed"

    @pytest.mark.django_db
    def test_job_run_history(self):
        """Test multiple runs of the same job over time."""
        job = JobFactory(name="Daily News Scraper")

        # Create multiple runs over time
        run1 = CompletedRunFactory(
            job=job,
            status="success",
            started_at=timezone.now() - timezone.timedelta(days=3),
        )
        run2 = CompletedRunFactory(
            job=job,
            status="success",
            started_at=timezone.now() - timezone.timedelta(days=2),
        )
        run3 = RunFactory(
            job=job,
            status="failure",
            started_at=timezone.now() - timezone.timedelta(days=1),
        )
        run4 = CompletedRunFactory(job=job, status="success", started_at=timezone.now())

        # Create results for successful runs
        ResultsFactory(run=run1, payload={"articles": 45})
        ResultsFactory(run=run2, payload={"articles": 52})
        ResultsFactory(run=run4, payload={"articles": 48})

        # Verify run history
        job_runs = job.run_set.all().order_by("started_at")
        assert len(job_runs) == 4

        # Verify success rate
        successful_runs = job.run_set.filter(status="success")
        assert len(successful_runs) == 3

        # Verify results for successful runs only
        job_results = Results.objects.filter(run__job=job)
        assert len(job_results) == 3

    @pytest.mark.django_db
    def test_user_data_aggregation(self):
        """Test aggregating data across all user's projects."""
        user = UserFactory(email="power_user@example.com")

        # Create multiple projects
        project1 = ProjectFactory(owner=user, name="E-commerce")
        project2 = ProjectFactory(owner=user, name="News Monitoring")

        # Create jobs in each project
        job1 = JobFactory(project=project1, name="Product Scraper")
        job2 = JobFactory(project=project2, name="Article Scraper")

        # Create successful runs
        run1 = CompletedRunFactory(job=job1, status="success")
        run2 = CompletedRunFactory(job=job2, status="success")

        # Create results
        ResultsFactory(run=run1, payload={"products": 100})
        ResultsFactory(run=run2, payload={"articles": 75})

        # Aggregate user's data
        user_projects = user.project_set.all()
        total_projects = len(user_projects)

        user_jobs = Job.objects.filter(project__owner=user)
        total_jobs = len(user_jobs)

        user_runs = Run.objects.filter(job__project__owner=user)
        total_runs = len(user_runs)

        user_results = Results.objects.filter(run__job__project__owner=user)
        total_results = len(user_results)

        # Verify aggregation
        assert total_projects == 2
        assert total_jobs == 2
        assert total_runs == 2
        assert total_results == 2

        # Verify user owns all the data
        for project in user_projects:
            assert project.owner == user

        for result in user_results:
            assert result.run.job.project.owner == user
