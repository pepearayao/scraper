from typing import List
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from scraper.models import Project

router = Router()


class ProjectSchema(Schema):
    id: UUID
    name: str
    owner_id: int = None
    created_at: str


class ProjectCreateSchema(Schema):
    name: str


class ProjectUpdateSchema(Schema):
    name: str


@router.get("/", response=List[ProjectSchema])
def list_projects(request):
    projects = Project.objects.all()
    return [
        {
            "id": project.id,
            "name": project.name,
            "owner_id": project.owner_id,
            "created_at": project.created_at.isoformat(),
        }
        for project in projects
    ]


@router.post("/", response=ProjectSchema)
def create_project(request, data: ProjectCreateSchema):
    project = Project.objects.create(
        name=data.name, owner=request.auth if hasattr(request, "auth") else None
    )
    return {
        "id": project.id,
        "name": project.name,
        "owner_id": project.owner_id,
        "created_at": project.created_at.isoformat(),
    }


@router.get("/{project_id}", response=ProjectSchema)
def get_project(request, project_id: UUID):
    project = get_object_or_404(Project, id=project_id)
    return {
        "id": project.id,
        "name": project.name,
        "owner_id": project.owner_id,
        "created_at": project.created_at.isoformat(),
    }


@router.put("/{project_id}", response=ProjectSchema)
def update_project(request, project_id: UUID, data: ProjectUpdateSchema):
    project = get_object_or_404(Project, id=project_id)
    project.name = data.name
    project.save()
    return {
        "id": project.id,
        "name": project.name,
        "owner_id": project.owner_id,
        "created_at": project.created_at.isoformat(),
    }


@router.delete("/{project_id}")
def delete_project(request, project_id: UUID):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True}
