"""
Project model for ToDoList application.

This module contains the Project class which represents a project
that can contain multiple tasks.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID


class Project:
    """
    Represents a project that can contain multiple tasks.

    A project has a unique identifier, name, description, and creation timestamp.
    It can contain multiple tasks and provides methods to manage them.
    """

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize a new Project.

        Args:
            name: The name of the project (minimum 3 characters)
            description: The description of the project (minimum 15 characters)

        Raises:
            ValueError: If name or description don't meet minimum length requirements
        """
        self._validate_name(name)
        self._validate_description(description)

        self._id: UUID = uuid4()
        self._name: str = name.strip()
        self._description: str = description.strip()
        self._created_at: datetime = datetime.now()
        self._tasks: list["Task"] = []

    @property
    def id(self) -> UUID:
        """Get the unique identifier of the project."""
        return self._id

    @property
    def name(self) -> str:
        """Get the name of the project."""
        return self._name

    @property
    def description(self) -> str:
        """Get the description of the project."""
        return self._description

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp of the project."""
        return self._created_at

    @property
    def tasks(self) -> list["Task"]:
        """Get a copy of the tasks list."""
        return self._tasks.copy()

    def update_name(self, new_name: str) -> None:
        """
        Update the project name.

        Args:
            new_name: The new name for the project

        Raises:
            ValueError: If the new name doesn't meet minimum length requirements
        """
        self._validate_name(new_name)
        self._name = new_name.strip()

    def update_description(self, new_description: str) -> None:
        """
        Update the project description.

        Args:
            new_description: The new description for the project

        Raises:
            ValueError: If the new description doesn't meet minimum length requirements
        """
        self._validate_description(new_description)
        self._description = new_description.strip()

    def add_task(self, task: "Task") -> None:
        """
        Add a task to the project.

        Args:
            task: The task to add to the project
        """
        if task not in self._tasks:
            self._tasks.append(task)

    def remove_task(self, task: "Task") -> bool:
        """
        Remove a task from the project.

        Args:
            task: The task to remove from the project

        Returns:
            True if the task was removed, False if it wasn't found
        """
        try:
            self._tasks.remove(task)
            return True
        except ValueError:
            return False

    def get_task_by_id(self, task_id: UUID) -> Optional["Task"]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to find

        Returns:
            The task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: str) -> list["Task"]:
        """
        Get all tasks with a specific status.

        Args:
            status: The status to filter by ('todo', 'doing', 'done')

        Returns:
            List of tasks with the specified status
        """
        return [task for task in self._tasks if task.status == status]

    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the project.

        Returns:
            The number of tasks in the project
        """
        return len(self._tasks)

    def _validate_name(self, name: str) -> None:
        """
        Validate the project name.

        Args:
            name: The name to validate

        Raises:
            ValueError: If the name doesn't meet requirements
        """
        if not isinstance(name, str):
            raise ValueError("Project name must be a string")

        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")

        if len(name.strip()) < 3:
            raise ValueError("Project name must be at least 3 characters long")

    def _validate_description(self, description: str) -> None:
        """
        Validate the project description.

        Args:
            description: The description to validate

        Raises:
            ValueError: If the description doesn't meet requirements
        """
        if not isinstance(description, str):
            raise ValueError("Project description must be a string")

        if not description or not description.strip():
            raise ValueError("Project description cannot be empty")

        if len(description.strip()) < 15:
            raise ValueError("Project description must be at least 15 characters long")

    def __str__(self) -> str:
        """Return a string representation of the project."""
        return f"Project(id={self._id}, name='{self._name}', tasks={len(self._tasks)})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the project."""
        return (
            f"Project(id={self._id}, name='{self._name}', "
            f"description='{self._description[:50]}...', "
            f"created_at={self._created_at}, tasks={len(self._tasks)})"
        )

    def __eq__(self, other) -> bool:
        """Check if two projects are equal based on their ID."""
        if not isinstance(other, Project):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Return the hash of the project based on its ID."""
        return hash(self._id)
