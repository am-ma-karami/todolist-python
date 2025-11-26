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
    ValidationError,
)
from ..models.project import Project
from ..repositories.project_repository import ProjectRepository
from .config_service import ConfigService


class ProjectService:
    """
    Service for managing projects with business logic.

    This class provides methods to create, read, update, and delete projects
    with proper validation and business rule enforcement.
    """

    def __init__(
        self, project_repository: ProjectRepository, config: ConfigService
    ) -> None:
        """
        Initialize the project service.

        Args:
            project_repository: The project repository to use
            config: The configuration service to use
        """
        self._repository = project_repository
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
            ValidationError: If validation fails
            ProjectLimitExceededError: If project limit is exceeded
            DuplicateProjectError: If project with same name exists
        """
        # Validate inputs
        self._validate_name(name)
        self._validate_description(description)

        # Check project limit
        if self._repository.count() >= self._config.get_project_max_count():
            raise ProjectLimitExceededError(
                f"Maximum number of projects ({self._config.get_project_max_count()}) exceeded"
            )

        # Check for duplicate project names
        existing_project = self._repository.get_by_name(name)
        if existing_project:
            raise DuplicateProjectError(f"Project with name '{name}' already exists")

        # Create and store the project
        project = Project(name=name.strip(), description=description.strip())
        return self._repository.create(project)

    def get_project(self, project_id: UUID | str) -> Optional[Project]:
        """
        Get a project by its ID.

        Args:
            project_id: The ID of the project to retrieve

        Returns:
            The project if found, None otherwise
        """
        return self._repository.get_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
        """
        Get all projects.

        Returns:
            List of all projects
        """
        return self._repository.get_all()

    def update_project(
        self,
        project_id: UUID | str,
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
            ProjectNotFoundError: If project not found
            ValidationError: If validation fails
            DuplicateProjectError: If duplicate name exists
        """
        project = self._repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        # Check for duplicate names if name is being updated
        if name is not None:
            self._validate_name(name)
            existing_project = self._repository.get_by_name(name)
            if existing_project and existing_project.id != str(project_id):
                raise DuplicateProjectError(
                    f"Project with name '{name}' already exists"
                )
            project.name = name.strip()

        if description is not None:
            self._validate_description(description)
            project.description = description.strip()

        return self._repository.update(project)

    def delete_project(self, project_id: UUID | str) -> bool:
        """
        Delete a project and all its tasks (cascade delete).

        Args:
            project_id: The ID of the project to delete

        Returns:
            True if the project was deleted, False if not found
        """
        return self._repository.delete(project_id)

    def project_exists(self, project_id: UUID | str) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: The ID of the project to check

        Returns:
            True if the project exists, False otherwise
        """
        return self._repository.exists(project_id)

    def get_project_count(self) -> int:
        """
        Get the total number of projects.

        Returns:
            The number of projects
        """
        return self._repository.count()

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """
        Get a project by its name.

        Args:
            name: The name of the project to find

        Returns:
            The project if found, None otherwise
        """
        return self._repository.get_by_name(name)

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
        projects = self._repository.get_all()

        matching_projects = []
        for project in projects:
            if (
                query_lower in project.name.lower()
                or query_lower in project.description.lower()
            ):
                matching_projects.append(project)

        return matching_projects

    def get_project_statistics(
        self, project_id: UUID | str, task_repository
    ) -> dict:
        """
        Get statistics for a project.

        Args:
            project_id: The ID of the project
            task_repository: Task repository to get task statistics

        Returns:
            Dictionary with project statistics

        Raises:
            ProjectNotFoundError: If project not found
        """
        project = self._repository.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        tasks = task_repository.get_by_project_id(project_id)

        stats = {
            "total_tasks": len(tasks),
            "todo_tasks": len([t for t in tasks if t.status == "todo"]),
            "doing_tasks": len([t for t in tasks if t.status == "doing"]),
            "done_tasks": len([t for t in tasks if t.status == "done"]),
            "overdue_tasks": len(
                [
                    t
                    for t in tasks
                    if t.deadline
                    and t.deadline < __import__("datetime").date.today()
                    and t.status != "done"
                ]
            ),
        }

        return stats

    def _validate_name(self, name: str) -> None:
        """
        Validate the project name.

        Args:
            name: The name to validate

        Raises:
            ValidationError: If the name doesn't meet requirements
        """
        if not isinstance(name, str):
            raise ValidationError("Project name must be a string")

        if not name or not name.strip():
            raise ValidationError("Project name cannot be empty")

        if len(name.strip()) < 3:
            raise ValidationError("Project name must be at least 3 characters long")

    def _validate_description(self, description: str) -> None:
        """
        Validate the project description.

        Args:
            description: The description to validate

        Raises:
            ValidationError: If the description doesn't meet requirements
        """
        if not isinstance(description, str):
            raise ValidationError("Project description must be a string")

        if not description or not description.strip():
            raise ValidationError("Project description cannot be empty")

        if len(description.strip()) < 15:
            raise ValidationError(
                "Project description must be at least 15 characters long"
            )
