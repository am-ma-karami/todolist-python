"""
Task service for ToDoList application.

This module contains the business logic for managing tasks,
including validation, limits, and business rules.
"""

from __future__ import annotations

from datetime import date
from typing import Optional
from uuid import UUID

from ..exceptions import (
    InvalidStatusError,
    ProjectNotFoundError,
    TaskLimitExceededError,
    TaskNotFoundError,
    ValidationError,
)
from ..models.task import Task, VALID_STATUSES
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from .config_service import ConfigService


class TaskService:
    """
    Service for managing tasks with business logic.

    This class provides methods to create, read, update, and delete tasks
    with proper validation and business rule enforcement.
    """

    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        config: ConfigService,
    ) -> None:
        """
        Initialize the task service.

        Args:
            task_repository: The task repository to use
            project_repository: The project repository to use
            config: The configuration service to use
        """
        self._task_repo = task_repository
        self._project_repo = project_repository
        self._config = config

    def create_task(
        self,
        project_id: UUID | str,
        title: str,
        description: str,
        status: str = "todo",
        deadline: Optional[date] = None,
    ) -> Task:
        """
        Create a new task in a project.

        Args:
            project_id: The ID of the project this task belongs to
            title: The title of the task
            description: The description of the task
            status: The status of the task (default: 'todo')
            deadline: Optional deadline for the task

        Returns:
            The created task

        Raises:
            ValidationError: If validation fails
            ProjectNotFoundError: If project not found
            TaskLimitExceededError: If task limit is exceeded
        """
        # Validate inputs
        self._validate_title(title)
        self._validate_description(description)
        self._validate_status(status)
        if deadline is not None:
            self._validate_deadline(deadline)

        # Check if project exists
        if not self._project_repo.exists(project_id):
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        # Check task limit for the project
        current_task_count = self._task_repo.count_by_project_id(project_id)
        if current_task_count >= self._config.get_task_max_count():
            raise TaskLimitExceededError(
                f"Maximum number of tasks ({self._config.get_task_max_count()}) "
                f"exceeded for this project"
            )

        # Create and store the task
        project_id_str = str(project_id)
        task = Task(
            project_id=project_id_str,
            title=title.strip(),
            description=description.strip(),
            status=status,
            deadline=deadline,
        )
        return self._task_repo.create(task)

    def get_task(self, task_id: UUID | str) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self._task_repo.get_by_id(task_id)

    def get_tasks_by_project(self, project_id: UUID | str) -> list[Task]:
        """
        Get all tasks in a project.

        Args:
            project_id: The ID of the project

        Returns:
            List of tasks in the project
        """
        return self._task_repo.get_by_project_id(project_id)

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return self._task_repo.get_all()

    def update_task(
        self,
        task_id: UUID | str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[date] = None,
    ) -> Task:
        """
        Update a task.

        Args:
            task_id: The ID of the task to update
            title: The new title (optional)
            description: The new description (optional)
            status: The new status (optional)
            deadline: The new deadline (optional)

        Returns:
            The updated task

        Raises:
            TaskNotFoundError: If task not found
            ValidationError: If validation fails
        """
        task = self._task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        if title is not None:
            self._validate_title(title)
            task.title = title.strip()

        if description is not None:
            self._validate_description(description)
            task.description = description.strip()

        if status is not None:
            self._validate_status(status)
            task.status = status

        if deadline is not None:
            self._validate_deadline(deadline)
            task.deadline = deadline

        return self._task_repo.update(task)

    def delete_task(self, task_id: UUID | str) -> bool:
        """
        Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        return self._task_repo.delete(task_id)

    def task_exists(self, task_id: UUID | str) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: The ID of the task to check

        Returns:
            True if the task exists, False otherwise
        """
        return self._task_repo.exists(task_id)

    def get_tasks_by_status(self, status: str) -> list[Task]:
        """
        Get all tasks with a specific status.

        Args:
            status: The status to filter by

        Returns:
            List of tasks with the specified status
        """
        return self._task_repo.get_by_status(status)

    def get_tasks_by_project_and_status(
        self, project_id: UUID | str, status: str
    ) -> list[Task]:
        """
        Get tasks in a project with a specific status.

        Args:
            project_id: The ID of the project
            status: The status to filter by

        Returns:
            List of tasks in the project with the specified status
        """
        return self._task_repo.get_by_project_and_status(project_id, status)

    def get_overdue_tasks(self) -> list[Task]:
        """
        Get all overdue tasks.

        Returns:
            List of overdue tasks
        """
        all_tasks = self._task_repo.get_all()
        today = date.today()
        return [
            task
            for task in all_tasks
            if task.deadline
            and task.deadline < today
            and task.status != "done"
        ]

    def get_overdue_tasks_by_project(self, project_id: UUID | str) -> list[Task]:
        """
        Get overdue tasks in a specific project.

        Args:
            project_id: The ID of the project

        Returns:
            List of overdue tasks in the project
        """
        project_tasks = self._task_repo.get_by_project_id(project_id)
        today = date.today()
        return [
            task
            for task in project_tasks
            if task.deadline
            and task.deadline < today
            and task.status != "done"
        ]

    def get_completed_tasks(self) -> list[Task]:
        """
        Get all completed tasks.

        Returns:
            List of completed tasks
        """
        return self._task_repo.get_by_status("done")

    def get_completed_tasks_by_project(self, project_id: UUID | str) -> list[Task]:
        """
        Get completed tasks in a specific project.

        Args:
            project_id: The ID of the project

        Returns:
            List of completed tasks in the project
        """
        return self._task_repo.get_by_project_and_status(project_id, "done")

    def search_tasks(
        self, query: str, project_id: Optional[UUID | str] = None
    ) -> list[Task]:
        """
        Search tasks by title or description.

        Args:
            query: The search query
            project_id: Optional project ID to limit search to

        Returns:
            List of tasks matching the query
        """
        if not query or not query.strip():
            return []

        query_lower = query.lower().strip()

        if project_id:
            tasks = self._task_repo.get_by_project_id(project_id)
        else:
            tasks = self._task_repo.get_all()

        matching_tasks = []
        for task in tasks:
            if (
                query_lower in task.title.lower()
                or query_lower in task.description.lower()
            ):
                matching_tasks.append(task)

        return matching_tasks

    def get_task_statistics(
        self, project_id: Optional[UUID | str] = None
    ) -> dict:
        """
        Get task statistics.

        Args:
            project_id: Optional project ID to limit statistics to

        Returns:
            Dictionary with task statistics
        """
        if project_id:
            tasks = self._task_repo.get_by_project_id(project_id)
        else:
            tasks = self._task_repo.get_all()

        today = date.today()
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
                    and t.deadline < today
                    and t.status != "done"
                ]
            ),
            "completed_tasks": len([t for t in tasks if t.status == "done"]),
        }

        return stats

    def get_task_count_by_project(self, project_id: UUID | str) -> int:
        """
        Get the number of tasks in a project.

        Args:
            project_id: The ID of the project

        Returns:
            The number of tasks in the project
        """
        return self._task_repo.count_by_project_id(project_id)

    def _validate_title(self, title: str) -> None:
        """
        Validate the task title.

        Args:
            title: The title to validate

        Raises:
            ValidationError: If the title doesn't meet requirements
        """
        if not isinstance(title, str):
            raise ValidationError("Task title must be a string")

        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        if len(title.strip()) < 3:
            raise ValidationError("Task title must be at least 3 characters long")

    def _validate_description(self, description: str) -> None:
        """
        Validate the task description.

        Args:
            description: The description to validate

        Raises:
            ValidationError: If the description doesn't meet requirements
        """
        if not isinstance(description, str):
            raise ValidationError("Task description must be a string")

        if not description or not description.strip():
            raise ValidationError("Task description cannot be empty")

        if len(description.strip()) < 15:
            raise ValidationError(
                "Task description must be at least 15 characters long"
            )

    def _validate_status(self, status: str) -> None:
        """
        Validate the task status.

        Args:
            status: The status to validate

        Raises:
            ValidationError: If the status is not valid
        """
        if not isinstance(status, str):
            raise ValidationError("Task status must be a string")

        if status not in VALID_STATUSES:
            raise InvalidStatusError(
                f"Task status must be one of {VALID_STATUSES}"
            )

    def _validate_deadline(self, deadline: date) -> None:
        """
        Validate the task deadline.

        Args:
            deadline: The deadline to validate

        Raises:
            ValidationError: If the deadline is not valid
        """
        if not isinstance(deadline, date):
            raise ValidationError("Task deadline must be a date object")
