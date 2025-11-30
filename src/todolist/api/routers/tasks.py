"""
Task endpoints for ToDoList API.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from ...exceptions import (
    InvalidStatusError,
    ProjectNotFoundError,
    TaskNotFoundError,
    ValidationError,
)
from ...services.task_service import TaskService
from ..dependencies import get_task_service
from ..models.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter()


@router.get(
    "/",
    response_model=list[TaskRead],
    summary="List tasks",
)
def list_tasks(
    status_filter: Optional[str] = Query(
        default=None, alias="status", description="Filter by task status"
    ),
    project_id: Optional[str] = Query(
        default=None, description="Filter by project ID",
    ),
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskRead]:
    """Return tasks with optional filtering by status and project."""
    if status_filter is not None and project_id is not None:
        tasks = task_service.get_tasks_by_project_and_status(project_id, status_filter)
    elif status_filter is not None:
        tasks = task_service.get_tasks_by_status(status_filter)
    elif project_id is not None:
        tasks = task_service.get_tasks_by_project(project_id)
    else:
        tasks = task_service.get_all_tasks()

    return [TaskRead.model_validate(task) for task in tasks]


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    payload: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
) -> TaskRead:
    """Create a new task."""
    try:
        task = task_service.create_task(
            project_id=payload.project_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
        )
    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (ValidationError, InvalidStatusError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return TaskRead.model_validate(task)


@router.get(
    "/search",
    response_model=list[TaskRead],
    summary="Search tasks",
)
def search_tasks(
    query: str,
    project_id: Optional[str] = Query(
        default=None, description="Limit search to a specific project",
    ),
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskRead]:
    """Search tasks by title or description."""
    tasks = task_service.search_tasks(query=query, project_id=project_id)
    return [TaskRead.model_validate(task) for task in tasks]


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update a task",
)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> TaskRead:
    """Update an existing task."""
    try:
        task = task_service.update_task(
            task_id=task_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
        )
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (ValidationError, InvalidStatusError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return TaskRead.model_validate(task)


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get task by ID",
)
def get_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> TaskRead:
    """Return a single task by ID."""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return TaskRead.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> Response:
    """Delete a task by ID."""
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/overdue/list",
    response_model=list[TaskRead],
    summary="List overdue tasks",
)
def list_overdue_tasks(
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskRead]:
    """Return all overdue tasks."""
    tasks = task_service.get_overdue_tasks()
    return [TaskRead.model_validate(task) for task in tasks]


@router.get(
    "/project/{project_id}",
    response_model=list[TaskRead],
    summary="List tasks for a project",
)
def list_project_tasks(
    project_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskRead]:
    """Return tasks belonging to a specific project."""
    tasks = task_service.get_tasks_by_project(project_id)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get(
    "/statistics/summary",
    summary="Get global task statistics",
)
def task_statistics(
    project_id: Optional[str] = Query(
        default=None, description="Limit statistics to a specific project",
    ),
    task_service: TaskService = Depends(get_task_service),
) -> dict[str, Any]:
    """Return aggregated statistics for tasks."""
    return task_service.get_task_statistics(project_id=project_id)


