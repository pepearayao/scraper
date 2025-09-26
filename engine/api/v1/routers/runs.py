from typing import List, Optional
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from scraper.models import Job, Run

router = Router()


class RunSchema(Schema):
    id: UUID
    job_id: UUID = None
    status: str
    prefect_state: str = None
    prefect_flow_run_id: str = None
    logs: str = None
    started_at: str = None
    finished_at: str = None


class RunCreateSchema(Schema):
    job_id: UUID


class RunUpdateSchema(Schema):
    status: str = None
    prefect_state: str = None
    prefect_flow_run_id: str = None
    logs: str = None


@router.get("/", response=List[RunSchema])
def list_runs(request, job_id: UUID = None, status: str = None):
    runs = Run.objects.all()
    if job_id:
        runs = runs.filter(job_id=job_id)
    if status:
        runs = runs.filter(status=status)

    return [
        {
            "id": run.id,
            "job_id": run.job_id,
            "status": run.status,
            "prefect_state": run.prefect_state,
            "prefect_flow_run_id": run.prefect_flow_run_id,
            "logs": run.logs,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "finished_at": run.finished_at.isoformat() if run.finished_at else None,
        }
        for run in runs
    ]


@router.post("/", response=RunSchema)
def create_run(request, data: RunCreateSchema):
    job = get_object_or_404(Job, id=data.job_id)

    run = Run.objects.create(job=job, status="queued")

    return {
        "id": run.id,
        "job_id": run.job_id,
        "status": run.status,
        "prefect_state": run.prefect_state,
        "prefect_flow_run_id": run.prefect_flow_run_id,
        "logs": run.logs,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "finished_at": run.finished_at.isoformat() if run.finished_at else None,
    }


@router.get("/{run_id}", response=RunSchema)
def get_run(request, run_id: UUID):
    run = get_object_or_404(Run, id=run_id)
    return {
        "id": run.id,
        "job_id": run.job_id,
        "status": run.status,
        "prefect_state": run.prefect_state,
        "prefect_flow_run_id": run.prefect_flow_run_id,
        "logs": run.logs,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "finished_at": run.finished_at.isoformat() if run.finished_at else None,
    }


@router.put("/{run_id}", response=RunSchema)
def update_run(request, run_id: UUID, data: RunUpdateSchema):
    run = get_object_or_404(Run, id=run_id)

    if data.status is not None:
        run.status = data.status
    if data.prefect_state is not None:
        run.prefect_state = data.prefect_state
    if data.prefect_flow_run_id is not None:
        run.prefect_flow_run_id = data.prefect_flow_run_id
    if data.logs is not None:
        run.logs = data.logs

    run.save()

    return {
        "id": run.id,
        "job_id": run.job_id,
        "status": run.status,
        "prefect_state": run.prefect_state,
        "prefect_flow_run_id": run.prefect_flow_run_id,
        "logs": run.logs,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "finished_at": run.finished_at.isoformat() if run.finished_at else None,
    }


@router.delete("/{run_id}")
def delete_run(request, run_id: UUID):
    run = get_object_or_404(Run, id=run_id)
    run.delete()
    return {"success": True}


@router.post("/{run_id}/trigger")
def trigger_run(request, run_id: UUID):
    run = get_object_or_404(Run, id=run_id)

    if run.status not in ["queued", "failure"]:
        return 400, {"error": "Run cannot be triggered in current status"}

    run.status = "running"
    run.save()

    return {"message": "Run triggered successfully", "run_id": run.id}
