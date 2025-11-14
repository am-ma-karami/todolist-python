"""
Repository for Project entity data access.

This module provides the interface and SQLAlchemy implementation
for project data persistence operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..exceptions import StorageNotFoundError
from ..models.project import Project


class ProjectRepository(ABC):
    """
    Abstract repository interface for Project entity.

    Defines the contract for project data access operations.
    """

    @abstractmethod
    def create(self, project: Project) -> Project:
        """
        Create a new project.

        Args:
            project: The project entity to create

        Returns:
            The created project

        Raises:
            DuplicateResourceError: If project with same ID already exists
        """
        pass

    @abstractmethod
    def get_by_id(self, project_id: UUID | str) -> Optional[Project]:
        """
        Get a project by its ID.

        Args:
            project_id: The ID of the project

        Returns:
            The project if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Project]:
        """
        Get all projects.

        Returns:
            List of all projects, sorted by creation time
        """
        pass

    @abstractmethod
    def update(self, project: Project) -> Project:
        """
        Update an existing project.

        Args:
            project: The project entity to update

        Returns:
            The updated project

        Raises:
            StorageNotFoundError: If project doesn't exist
        """
        pass

    @abstractmethod
    def delete(self, project_id: UUID | str) -> bool:
        """
        Delete a project by its ID.

        Args:
            project_id: The ID of the project to delete

        Returns:
            True if the project was deleted, False if not found
        """
        pass

    @abstractmethod
    def exists(self, project_id: UUID | str) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: The ID of the project to check

        Returns:
            True if the project exists, False otherwise
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Get the total number of projects.

        Returns:
            The number of projects
        """
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Project]:
        """
        Get a project by its name.

        Args:
            name: The name of the project

        Returns:
            The project if found, None otherwise
        """
        pass


class SQLAlchemyProjectRepository(ProjectRepository):
    """
    SQLAlchemy implementation of ProjectRepository.

    Provides database persistence for Project entities using SQLAlchemy ORM.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session

    def create(self, project: Project) -> Project:
        """Create a new project in the database."""
        self._session.add(project)
        self._session.flush()
        return project

    def get_by_id(self, project_id: UUID | str) -> Optional[Project]:
        """Get a project by its ID."""
        project_id_str = str(project_id)
        stmt = select(Project).where(Project.id == project_id_str)
        return self._session.scalar(stmt)

    def get_all(self) -> list[Project]:
        """Get all projects, sorted by creation time."""
        stmt = select(Project).order_by(Project.created_at)
        return list(self._session.scalars(stmt).all())

    def update(self, project: Project) -> Project:
        """Update an existing project."""
        if not self.exists(project.id):
            raise StorageNotFoundError(f"Project with ID {project.id} not found")
        self._session.flush()
        return project

    def delete(self, project_id: UUID | str) -> bool:
        """Delete a project by its ID."""
        project = self.get_by_id(project_id)
        if not project:
            return False
        self._session.delete(project)
        return True

    def exists(self, project_id: UUID | str) -> bool:
        """Check if a project exists."""
        return self.get_by_id(project_id) is not None

    def count(self) -> int:
        """Get the total number of projects."""
        stmt = select(func.count(Project.id))
        result = self._session.scalar(stmt)
        return result if result is not None else 0

    def get_by_name(self, name: str) -> Optional[Project]:
        """Get a project by its name (case-insensitive)."""
        stmt = select(Project).where(Project.name.ilike(name))
        return self._session.scalar(stmt)

