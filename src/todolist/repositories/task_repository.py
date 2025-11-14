"""
Repository for Task entity data access.

This module provides the interface and SQLAlchemy implementation
for task data persistence operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..exceptions import StorageNotFoundError
from ..models.task import Task


class TaskRepository(ABC):
    """
    Abstract repository interface for Task entity.

    Defines the contract for task data access operations.
    """

    @abstractmethod
    def create(self, task: Task) -> Task:
        """
        Create a new task.

        Args:
            task: The task entity to create

        Returns:
            The created task

        Raises:
            DuplicateResourceError: If task with same ID already exists
        """
        pass

    @abstractmethod
    def get_by_id(self, task_id: UUID | str) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task

        Returns:
            The task if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks, sorted by creation time
        """
        pass

    @abstractmethod
    def get_by_project_id(self, project_id: UUID | str) -> list[Task]:
        """
        Get all tasks belonging to a project.

        Args:
            project_id: The ID of the project

        Returns:
            List of tasks belonging to the project, sorted by creation time
        """
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        """
        Update an existing task.

        Args:
            task: The task entity to update

        Returns:
            The updated task

        Raises:
            StorageNotFoundError: If task doesn't exist
        """
        pass

    @abstractmethod
    def delete(self, task_id: UUID | str) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        pass

    @abstractmethod
    def exists(self, task_id: UUID | str) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: The ID of the task to check

        Returns:
            True if the task exists, False otherwise
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            The number of tasks
        """
        pass

    @abstractmethod
    def count_by_project_id(self, project_id: UUID | str) -> int:
        """
        Get the number of tasks in a specific project.

        Args:
            project_id: The ID of the project

        Returns:
            The number of tasks in the project
        """
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> list[Task]:
        """
        Get all tasks with a specific status.

        Args:
            status: The status to filter by

        Returns:
            List of tasks with the specified status
        """
        pass

    @abstractmethod
    def get_by_project_and_status(
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
        pass


class SQLAlchemyTaskRepository(TaskRepository):
    """
    SQLAlchemy implementation of TaskRepository.

    Provides database persistence for Task entities using SQLAlchemy ORM.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session

    def create(self, task: Task) -> Task:
        """Create a new task in the database."""
        self._session.add(task)
        self._session.flush()
        return task

    def get_by_id(self, task_id: UUID | str) -> Optional[Task]:
        """Get a task by its ID."""
        task_id_str = str(task_id)
        stmt = select(Task).where(Task.id == task_id_str)
        return self._session.scalar(stmt)

    def get_all(self) -> list[Task]:
        """Get all tasks, sorted by creation time."""
        stmt = select(Task).order_by(Task.created_at)
        return list(self._session.scalars(stmt).all())

    def get_by_project_id(self, project_id: UUID | str) -> list[Task]:
        """Get all tasks belonging to a project."""
        project_id_str = str(project_id)
        stmt = (
            select(Task)
            .where(Task.project_id == project_id_str)
            .order_by(Task.created_at)
        )
        return list(self._session.scalars(stmt).all())

    def update(self, task: Task) -> Task:
        """Update an existing task."""
        if not self.exists(task.id):
            raise StorageNotFoundError(f"Task with ID {task.id} not found")
        self._session.flush()
        return task

    def delete(self, task_id: UUID | str) -> bool:
        """Delete a task by its ID."""
        task = self.get_by_id(task_id)
        if not task:
            return False
        self._session.delete(task)
        return True

    def exists(self, task_id: UUID | str) -> bool:
        """Check if a task exists."""
        return self.get_by_id(task_id) is not None

    def count(self) -> int:
        """Get the total number of tasks."""
        stmt = select(func.count(Task.id))
        result = self._session.scalar(stmt)
        return result if result is not None else 0

    def count_by_project_id(self, project_id: UUID | str) -> int:
        """Get the number of tasks in a specific project."""
        project_id_str = str(project_id)
        stmt = select(func.count(Task.id)).where(Task.project_id == project_id_str)
        result = self._session.scalar(stmt)
        return result if result is not None else 0

    def get_by_status(self, status: str) -> list[Task]:
        """Get all tasks with a specific status."""
        stmt = select(Task).where(Task.status == status).order_by(Task.created_at)
        return list(self._session.scalars(stmt).all())

    def get_by_project_and_status(
        self, project_id: UUID | str, status: str
    ) -> list[Task]:
        """Get tasks in a project with a specific status."""
        project_id_str = str(project_id)
        stmt = (
            select(Task)
            .where(Task.project_id == project_id_str, Task.status == status)
            .order_by(Task.created_at)
        )
        return list(self._session.scalars(stmt).all())

