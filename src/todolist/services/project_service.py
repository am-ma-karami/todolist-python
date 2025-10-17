"""
Project service for ToDoList application.

This module contains the business logic for managing projects,
including validation, limits, and business rules.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from ..exceptions import (
    DuplicateProjectError,
    ProjectLimitExceededError,
    ProjectNotFoundError,
)
from ..models.project import Project
from ..storage.in_memory_storage import InMemoryStorage
from .config_service import ConfigService


class ProjectService:
    """
    Service for managing projects with business logic.

    This class provides methods to create, read, update, and delete projects
    with proper validation and business rule enforcement.
    """

    def __init__(self, storage: InMemoryStorage, config: ConfigService) -> None:
        """
        Initialize the project service.

        Args:
            storage: The storage layer to use
            config: The configuration service to use
        """
        self._storage = storage
        self._config = config

    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project.

        Args:
            name: The name of the project
            description: The description of the project

        Returns:
            The created project

        Raises:
            ValueError: If validation fails or limits are exceeded
        """
        # Check project limit
        if self._storage.get_project_count() >= self._config.get_project_max_count():
            raise ProjectLimitExceededError(
                f"Maximum number of projects ({self._config.get_project_max_count()}) exceeded"
            )

        # Check for duplicate project names
        existing_projects = self._storage.get_all_projects()
        for project in existing_projects:
            if project.name.lower() == name.lower():
                raise DuplicateProjectError(f"Project with name '{name}' already exists")

        # Create and store the project
        project = Project(name, description)
        return self._storage.create_project(project)

    def get_project(self, project_id: UUID) -> Optional[Project]:
        """
        Get a project by its ID.

        Args:
            project_id: The ID of the project to retrieve

        Returns:
            The project if found, None otherwise
        """
        return self._storage.get_project(project_id)

    def get_all_projects(self) -> list[Project]:
        """
        Get all projects.

        Returns:
            List of all projects
        """
        return self._storage.get_all_projects()

    def update_project(
        self,
        project_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        """
        Update a project.

        Args:
            project_id: The ID of the project to update
            name: The new name (optional)
            description: The new description (optional)

        Returns:
            The updated project

        Raises:
            ValueError: If project not found or validation fails
        """
        project = self._storage.get_project(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        # Check for duplicate names if name is being updated
        if name is not None:
            existing_projects = self._storage.get_all_projects()
            for existing_project in existing_projects:
                if (
                    existing_project.id != project_id
                    and existing_project.name.lower() == name.lower()
                ):
                    raise DuplicateProjectError(f"Project with name '{name}' already exists")
            project.update_name(name)

        if description is not None:
            project.update_description(description)

        return self._storage.update_project(project)

    def delete_project(self, project_id: UUID) -> bool:
        """
        Delete a project and all its tasks (cascade delete).

        Args:
            project_id: The ID of the project to delete

        Returns:
            True if the project was deleted, False if not found
        """
        return self._storage.delete_project(project_id)

    def project_exists(self, project_id: UUID) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: The ID of the project to check

        Returns:
            True if the project exists, False otherwise
        """
        return self._storage.project_exists(project_id)

    def get_project_count(self) -> int:
        """
        Get the total number of projects.

        Returns:
            The number of projects
        """
        return self._storage.get_project_count()

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """
        Get a project by its name.

        Args:
            name: The name of the project to find

        Returns:
            The project if found, None otherwise
        """
        projects = self._storage.get_all_projects()
        for project in projects:
            if project.name.lower() == name.lower():
                return project
        return None

    def search_projects(self, query: str) -> list[Project]:
        """
        Search projects by name or description.

        Args:
            query: The search query

        Returns:
            List of projects matching the query
        """
        if not query or not query.strip():
            return []

        query_lower = query.lower().strip()
        projects = self._storage.get_all_projects()

        matching_projects = []
        for project in projects:
            if (
                query_lower in project.name.lower()
                or query_lower in project.description.lower()
            ):
                matching_projects.append(project)

        return matching_projects

    def get_project_statistics(self, project_id: UUID) -> dict:
        """
        Get statistics for a project.

        Args:
            project_id: The ID of the project

        Returns:
            Dictionary with project statistics

        Raises:
            ValueError: If project not found
        """
        project = self._storage.get_project(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        tasks = self._storage.get_tasks_by_project(project_id)

        stats = {
            "total_tasks": len(tasks),
            "todo_tasks": len([t for t in tasks if t.status == "todo"]),
            "doing_tasks": len([t for t in tasks if t.status == "doing"]),
            "done_tasks": len([t for t in tasks if t.status == "done"]),
            "overdue_tasks": len([t for t in tasks if t.is_overdue()]),
        }

        return stats
