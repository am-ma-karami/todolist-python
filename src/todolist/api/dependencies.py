"""
FastAPI dependency providers for services and repositories.

These functions wire FastAPI endpoints to the existing service and
repository layers using constructor injection.
"""

from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from ..db.session import get_session as db_get_session
from ..repositories.project_repository import ProjectRepository, SQLAlchemyProjectRepository
from ..repositories.task_repository import SQLAlchemyTaskRepository, TaskRepository
from ..services.config_service import ConfigService
from ..services.project_service import ProjectService
from ..services.task_service import TaskService


def get_session() -> Generator[Session, None, None]:
    """Provide a database session for FastAPI dependencies."""
    with db_get_session() as session:
        yield session


def get_config_service() -> ConfigService:
    """Provide configuration service."""
    return ConfigService()


def get_project_repository(session: Session = Depends(get_session)) -> ProjectRepository:
    """Provide SQLAlchemy-based project repository."""
    return SQLAlchemyProjectRepository(session)


def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    """Provide SQLAlchemy-based task repository."""
    return SQLAlchemyTaskRepository(session)


def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repository),
    config: ConfigService = Depends(get_config_service),
) -> ProjectService:
    """Provide project service wired with repository and config."""
    return ProjectService(project_repo, config)


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    project_repo: ProjectRepository = Depends(get_project_repository),
    config: ConfigService = Depends(get_config_service),
) -> TaskService:
    """Provide task service wired with repositories and config."""
    return TaskService(task_repo, project_repo, config)


