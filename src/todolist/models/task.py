"""
Task model for ToDoList application.

This module contains the Task class which represents a task
that belongs to a project.
"""

from __future__ import annotations

from datetime import datetime, date
from typing import Optional
from uuid import uuid4, UUID


class Task:
    """
    Represents a task that belongs to a project.

    A task has a unique identifier, title, description, status, optional deadline,
    and creation timestamp. The status can be 'todo', 'doing', or 'done'.
    """

    VALID_STATUSES = {"todo", "doing", "done"}

    def __init__(
        self,
        title: str,
        description: str,
        status: str = "todo",
        deadline: Optional[date] = None,
    ) -> None:
        """
        Initialize a new Task.

        Args:
            title: The title of the task (minimum 3 characters)
            description: The description of the task (minimum 15 characters)
            status: The status of the task ('todo', 'doing', or 'done')
            deadline: Optional deadline date for the task

        Raises:
            ValueError: If title, description, or status don't meet requirements
        """
        self._validate_title(title)
        self._validate_description(description)
        self._validate_status(status)
        if deadline is not None:
            self._validate_deadline(deadline)

        self._id: UUID = uuid4()
        self._title: str = title.strip()
        self._description: str = description.strip()
        self._status: str = status
        self._deadline: Optional[date] = deadline
        self._created_at: datetime = datetime.now()
        self._updated_at: datetime = datetime.now()

    @property
    def id(self) -> UUID:
        """Get the unique identifier of the task."""
        return self._id

    @property
    def title(self) -> str:
        """Get the title of the task."""
        return self._title

    @property
    def description(self) -> str:
        """Get the description of the task."""
        return self._description

    @property
    def status(self) -> str:
        """Get the status of the task."""
        return self._status

    @property
    def deadline(self) -> Optional[date]:
        """Get the deadline of the task."""
        return self._deadline

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp of the task."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp of the task."""
        return self._updated_at

    def update_title(self, new_title: str) -> None:
        """
        Update the task title.

        Args:
            new_title: The new title for the task

        Raises:
            ValueError: If the new title doesn't meet minimum length requirements
        """
        self._validate_title(new_title)
        self._title = new_title.strip()
        self._updated_at = datetime.now()

    def update_description(self, new_description: str) -> None:
        """
        Update the task description.

        Args:
            new_description: The new description for the task

        Raises:
            ValueError: If the new description doesn't meet minimum length requirements
        """
        self._validate_description(new_description)
        self._description = new_description.strip()
        self._updated_at = datetime.now()

    def update_status(self, new_status: str) -> None:
        """
        Update the task status.

        Args:
            new_status: The new status for the task ('todo', 'doing', or 'done')

        Raises:
            ValueError: If the new status is not valid
        """
        self._validate_status(new_status)
        self._status = new_status
        self._updated_at = datetime.now()

    def update_deadline(self, new_deadline: Optional[date]) -> None:
        """
        Update the task deadline.

        Args:
            new_deadline: The new deadline for the task (can be None)

        Raises:
            ValueError: If the new deadline is not valid
        """
        if new_deadline is not None:
            self._validate_deadline(new_deadline)
        self._deadline = new_deadline
        self._updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """
        Check if the task is overdue.

        Returns:
            True if the task has a deadline and it's past due, False otherwise
        """
        if self._deadline is None:
            return False
        return self._deadline < date.today()

    def is_completed(self) -> bool:
        """
        Check if the task is completed.

        Returns:
            True if the task status is 'done', False otherwise
        """
        return self._status == "done"

    def _validate_title(self, title: str) -> None:
        """
        Validate the task title.

        Args:
            title: The title to validate

        Raises:
            ValueError: If the title doesn't meet requirements
        """
        if not isinstance(title, str):
            raise ValueError("Task title must be a string")

        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        if len(title.strip()) < 3:
            raise ValueError("Task title must be at least 3 characters long")

    def _validate_description(self, description: str) -> None:
        """
        Validate the task description.

        Args:
            description: The description to validate

        Raises:
            ValueError: If the description doesn't meet requirements
        """
        if not isinstance(description, str):
            raise ValueError("Task description must be a string")

        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        if len(description.strip()) < 15:
            raise ValueError("Task description must be at least 15 characters long")

    def _validate_status(self, status: str) -> None:
        """
        Validate the task status.

        Args:
            status: The status to validate

        Raises:
            ValueError: If the status is not valid
        """
        if not isinstance(status, str):
            raise ValueError("Task status must be a string")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Task status must be one of {self.VALID_STATUSES}")

    def _validate_deadline(self, deadline: date) -> None:
        """
        Validate the task deadline.

        Args:
            deadline: The deadline to validate

        Raises:
            ValueError: If the deadline is not valid
        """
        if not isinstance(deadline, date):
            raise ValueError("Task deadline must be a date object")

        # Allow past dates for flexibility (tasks might be created after deadline)
        # This can be changed based on business requirements

    def __str__(self) -> str:
        """Return a string representation of the task."""
        deadline_str = f", deadline={self._deadline}" if self._deadline else ""
        return f"Task(id={self._id}, title='{self._title}', status='{self._status}'{deadline_str})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the task."""
        deadline_str = f", deadline={self._deadline}" if self._deadline else ""
        return (
            f"Task(id={self._id}, title='{self._title}', "
            f"description='{self._description[:50]}...', "
            f"status='{self._status}'{deadline_str}, "
            f"created_at={self._created_at})"
        )

    def __eq__(self, other) -> bool:
        """Check if two tasks are equal based on their ID."""
        if not isinstance(other, Task):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Return the hash of the task based on its ID."""
        return hash(self._id)
