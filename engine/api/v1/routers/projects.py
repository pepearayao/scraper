from typing import List
from uuid import UUID

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router
from scraper.models import Project

from ...responses import fail, success
from ..schemas import (
    ErrorResponse,
    ProjectCreateSchema,
    ProjectSchema,
    ProjectSuccessResponse,
    ProjectUpdateSchema,
)

router = Router()


@router.get(
    "/", response={200: ProjectSuccessResponse, 400: ErrorResponse, 404: ErrorResponse}
)
def list_projects(request):
    projects = (
        Project.objects.filter(owner=request.auth)
        if hasattr(request, "auth")
        else Project.objects.none()
    )
    data = [
        {
            "id": str(project.id),
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
        }
        for project in projects
    ]
    return success(data)


@router.post(
    "/", response={201: ProjectSuccessResponse, 400: ErrorResponse, 404: ErrorResponse}
)
def create_project(request, data: ProjectCreateSchema):
    project = Project.objects.create(
        name=data.name, owner=request.auth if hasattr(request, "auth") else None
    )
    data = [
        {
            "id": str(project.id),
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
        }
    ]

    return success(data)


@router.get(
    "/{project_id}",
    response={200: ProjectSuccessResponse, 400: ErrorResponse, 404: ErrorResponse},
)
def get_project(request, project_id: UUID):
    project = get_object_or_404(Project, id=project_id)
    data = [
        {
            "id": str(project.id),
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
        }
    ]

    return success(data)


@router.put(
    "/{project_id}",
    response={200: ProjectSuccessResponse, 400: ErrorResponse, 404: ErrorResponse},
)
def update_project(request, project_id: UUID, data: ProjectUpdateSchema):
    project = get_object_or_404(Project, id=project_id)
    project.name = data.name
    project.save()
    data = [
        {
            "id": str(project.id),
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
        }
    ]
    return success(data)
