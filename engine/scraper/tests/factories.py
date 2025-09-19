import uuid

import factory
from django.utils import timezone
from scraper.models import Job, Project, Results, Run
from users.tests.factories import UserFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    """Factory for creating Project instances."""

    class Meta:
        model = Project

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Test Project {n}")
    owner = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)


class JobFactory(factory.django.DjangoModelFactory):
    """Factory for creating Job instances."""

    class Meta:
        model = Job

    id = factory.LazyFunction(uuid.uuid4)
    project = factory.SubFactory(ProjectFactory)
    name = factory.Sequence(lambda n: f"Test Job {n}")
    raw_yaml = factory.LazyAttribute(
        lambda obj: f"""
name: {obj.name}
url: https://example.com
selector: .content
"""
    )
    parsed_yaml = factory.LazyAttribute(
        lambda obj: {
            "name": obj.name,
            "url": "https://example.com",
            "selector": ".content",
        }
    )
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    is_active = True


class RunFactory(factory.django.DjangoModelFactory):
    """Factory for creating Run instances."""

    class Meta:
        model = Run

    id = factory.LazyFunction(uuid.uuid4)
    job = factory.SubFactory(JobFactory)
    status = "queued"
    prefect_state = "Pending"
    prefect_flow_run_id = factory.LazyFunction(lambda: str(uuid.uuid4()))


class RunningRunFactory(RunFactory):
    """Factory for creating running Run instances."""

    status = "running"
    prefect_state = "Running"
    started_at = factory.LazyFunction(timezone.now)


class CompletedRunFactory(RunFactory):
    """Factory for creating completed Run instances."""

    status = "success"
    prefect_state = "Completed"
    started_at = factory.LazyFunction(timezone.now)
    finished_at = factory.LazyFunction(timezone.now)


class FailedRunFactory(RunFactory):
    """Factory for creating failed Run instances."""

    status = "failure"
    prefect_state = "Failed"
    started_at = factory.LazyFunction(timezone.now)
    finished_at = factory.LazyFunction(timezone.now)
    logs = "Error: Something went wrong during scraping"


class ResultsFactory(factory.django.DjangoModelFactory):
    """Factory for creating Results instances."""

    class Meta:
        model = Results

    id = factory.LazyFunction(uuid.uuid4)
    run = factory.SubFactory(CompletedRunFactory)
    payload = factory.LazyAttribute(
        lambda obj: {
            "data": [
                {"title": "Sample Title 1", "content": "Sample content 1"},
                {"title": "Sample Title 2", "content": "Sample content 2"},
            ],
            "metadata": {"scraped_at": timezone.now().isoformat()},
        }
    )
    artifacts = factory.LazyAttribute(
        lambda obj: {
            "screenshots": ["screenshot_1.png"],
            "logs": ["Scraped 2 items successfully"],
        }
    )
    created_at = factory.LazyFunction(timezone.now)
