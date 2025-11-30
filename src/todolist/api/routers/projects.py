"""
Project endpoints for ToDoList API.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ...exceptions import DuplicateProjectError, ProjectNotFoundError, ValidationError
from ..dependencies import get_project_service, get_task_repository
from ..models.project import ProjectCreate, ProjectRead, ProjectUpdate
from ...repositories.task_repository import TaskRepository
from ...services.project_service import ProjectService


router = APIRouter()


@router.get(
    "/",
    response_model=list[ProjectRead],
    summary="List all projects",
)
def list_projects(
    project_service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    """Return all projects."""
    projects = project_service.get_all_projects()
    return [ProjectRead.model_validate(project) for project in projects]


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
def create_project(
    payload: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """Create a new project."""
    try:
        project = project_service.create_project(
            name=payload.name,
            description=payload.description,
        )
    except (ValidationError, DuplicateProjectError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ProjectRead.model_validate(project)


@router.get(
    "/search",
    response_model=list[ProjectRead],
    summary="Search projects",
)
def search_projects(
    query: str,
    project_service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    """Search projects by name or description."""
    projects = project_service.search_projects(query)
    return [ProjectRead.model_validate(project) for project in projects]


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Update a project",
)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """Update an existing project."""
    try:
        project = project_service.update_project(
            project_id=project_id,
            name=payload.name,
            description=payload.description,
        )
    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (ValidationError, DuplicateProjectError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ProjectRead.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service),
) -> Response:
    """Delete a project by ID."""
    deleted = project_service.delete_project(project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get project by ID",
)
def get_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """Get a single project by its ID."""
    project = project_service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )

    return ProjectRead.model_validate(project)


@router.get(
    "/{project_id}/statistics",
    summary="Get statistics for a project",
)
def project_statistics(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service),
    task_repo: TaskRepository = Depends(get_task_repository),
) -> dict[str, Any]:
    """Return aggregated statistics for a single project."""
    try:
        return project_service.get_project_statistics(project_id, task_repo)
    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


