import uuid

from django.db import models
from users.models import User


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, blank=True, null=True
    )
    name = models.CharField(max_length=255)
    raw_yaml = models.TextField(blank=True, null=True)
    parsed_yaml = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_run_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Run(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("success", "Success"),
        ("failure", "Failure"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="queued")
    prefect_state = models.CharField(max_length=100, blank=True, null=True)
    prefect_flow_run_id = models.CharField(max_length=100, blank=True, null=True)
    logs = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Run {self.job.name} - {self.started_at} - {self.status}"


class Results(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run = models.ForeignKey(Run, on_delete=models.PROTECT, blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    artifacts = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
