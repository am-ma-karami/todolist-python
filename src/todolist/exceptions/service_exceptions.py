"""
Service layer exception classes.

These exceptions are raised by service layer when business logic
validation fails or business rules are violated.
"""

from .base import ToDoListError


class ProjectError(ToDoListError):
    """Base exception for project-related errors."""

    pass


class ProjectNotFoundError(ProjectError):
    """Raised when a project is not found."""

    pass


class ProjectLimitExceededError(ProjectError):
    """Raised when project limit is exceeded."""

    pass


class DuplicateProjectError(ProjectError):
    """Raised when trying to create a project with duplicate name."""

    pass


class TaskError(ToDoListError):
    """Base exception for task-related errors."""

    pass


class TaskNotFoundError(TaskError):
    """Raised when a task is not found."""

    pass


class TaskLimitExceededError(TaskError):
    """Raised when task limit is exceeded."""

    pass


class InvalidStatusError(TaskError):
    """Raised when an invalid task status is provided."""

    pass

