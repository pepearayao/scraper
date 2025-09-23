from typing import List, Optional
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from scraper.models import Results, Run

router = Router()


class ResultSchema(Schema):
    id: UUID
    run_id: UUID = None
    payload: dict = None
    artifacts: dict = None
    created_at: str


class ResultCreateSchema(Schema):
    run_id: UUID
    payload: dict = None
    artifacts: dict = None


class ResultUpdateSchema(Schema):
    payload: dict = None
    artifacts: dict = None


@router.get("/", response=List[ResultSchema])
def list_results(request, run_id: UUID = None):
    results = Results.objects.all()
    if run_id:
        results = results.filter(run_id=run_id)

    return [
        {
            "id": result.id,
            "run_id": result.run_id,
            "payload": result.payload,
            "artifacts": result.artifacts,
            "created_at": result.created_at.isoformat(),
        }
        for result in results
    ]


@router.post("/", response=ResultSchema)
def create_result(request, data: ResultCreateSchema):
    run = get_object_or_404(Run, id=data.run_id)

    result = Results.objects.create(
        run=run, payload=data.payload, artifacts=data.artifacts
    )

    return {
        "id": result.id,
        "run_id": result.run_id,
        "payload": result.payload,
        "artifacts": result.artifacts,
        "created_at": result.created_at.isoformat(),
    }


@router.get("/{result_id}", response=ResultSchema)
def get_result(request, result_id: UUID):
    result = get_object_or_404(Results, id=result_id)
    return {
        "id": result.id,
        "run_id": result.run_id,
        "payload": result.payload,
        "artifacts": result.artifacts,
        "created_at": result.created_at.isoformat(),
    }


@router.put("/{result_id}", response=ResultSchema)
def update_result(request, result_id: UUID, data: ResultUpdateSchema):
    result = get_object_or_404(Results, id=result_id)

    if data.payload is not None:
        result.payload = data.payload
    if data.artifacts is not None:
        result.artifacts = data.artifacts

    result.save()

    return {
        "id": result.id,
        "run_id": result.run_id,
        "payload": result.payload,
        "artifacts": result.artifacts,
        "created_at": result.created_at.isoformat(),
    }


@router.delete("/{result_id}")
def delete_result(request, result_id: UUID):
    result = get_object_or_404(Results, id=result_id)
    result.delete()
    return {"success": True}


@router.get("/{result_id}/download")
def download_result(request, result_id: UUID):
    result = get_object_or_404(Results, id=result_id)
    return {
        "id": result.id,
        "payload": result.payload,
        "artifacts": result.artifacts,
        "download_url": f"/api/results/{result_id}/download",
    }
