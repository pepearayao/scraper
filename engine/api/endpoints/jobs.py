from typing import List, Optional
from uuid import UUID

import yaml
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from scraper.models import Job, Project

router = Router()


class JobSchema(Schema):
    id: UUID
    project_id: UUID = None
    name: str
    raw_yaml: str = None
    parsed_yaml: dict = None
    created_at: str
    updated_at: str
    last_run_at: str = None
    is_active: bool


class JobCreateSchema(Schema):
    project_id: UUID = None
    name: str
    raw_yaml: str = None


class JobUpdateSchema(Schema):
    name: str = None
    raw_yaml: str = None
    is_active: bool = None


@router.get("/", response=List[JobSchema])
def list_jobs(request, project_id: UUID = None):
    jobs = Job.objects.all()
    if project_id:
        jobs = jobs.filter(project_id=project_id)

    return [
        {
            "id": job.id,
            "project_id": job.project_id,
            "name": job.name,
            "raw_yaml": job.raw_yaml,
            "parsed_yaml": job.parsed_yaml,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
            "last_run_at": job.last_run_at.isoformat() if job.last_run_at else None,
            "is_active": job.is_active,
        }
        for job in jobs
    ]


@router.post("/", response=JobSchema)
def create_job(request, data: JobCreateSchema):
    parsed_yaml = None
    if data.raw_yaml:
        try:
            parsed_yaml = yaml.safe_load(data.raw_yaml)
        except yaml.YAMLError:
            return 400, {"error": "Invalid YAML format"}

    project = None
    if data.project_id:
        project = get_object_or_404(Project, id=data.project_id)

    job = Job.objects.create(
        project=project, name=data.name, raw_yaml=data.raw_yaml, parsed_yaml=parsed_yaml
    )

    return {
        "id": job.id,
        "project_id": job.project_id,
        "name": job.name,
        "raw_yaml": job.raw_yaml,
        "parsed_yaml": job.parsed_yaml,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
        "last_run_at": job.last_run_at.isoformat() if job.last_run_at else None,
        "is_active": job.is_active,
    }


@router.get("/{job_id}", response=JobSchema)
def get_job(request, job_id: UUID):
    job = get_object_or_404(Job, id=job_id)
    return {
        "id": job.id,
        "project_id": job.project_id,
        "name": job.name,
        "raw_yaml": job.raw_yaml,
        "parsed_yaml": job.parsed_yaml,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
        "last_run_at": job.last_run_at.isoformat() if job.last_run_at else None,
        "is_active": job.is_active,
    }


@router.put("/{job_id}", response=JobSchema)
def update_job(request, job_id: UUID, data: JobUpdateSchema):
    job = get_object_or_404(Job, id=job_id)

    if data.name is not None:
        job.name = data.name
    if data.is_active is not None:
        job.is_active = data.is_active
    if data.raw_yaml is not None:
        job.raw_yaml = data.raw_yaml
        try:
            job.parsed_yaml = yaml.safe_load(data.raw_yaml) if data.raw_yaml else None
        except yaml.YAMLError:
            return 400, {"error": "Invalid YAML format"}

    job.save()

    return {
        "id": job.id,
        "project_id": job.project_id,
        "name": job.name,
        "raw_yaml": job.raw_yaml,
        "parsed_yaml": job.parsed_yaml,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
        "last_run_at": job.last_run_at.isoformat() if job.last_run_at else None,
        "is_active": job.is_active,
    }


@router.delete("/{job_id}")
def delete_job(request, job_id: UUID):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return {"success": True}
