"""
Custom exceptions for ToDoList application.

This module defines custom exception classes for better error handling
and more specific error messages.
"""


class ToDoListError(Exception):
    """Base exception class for ToDoList application."""

    pass


class ValidationError(ToDoListError):
    """Raised when validation fails."""

    pass


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


class StorageError(ToDoListError):
    """Base exception for storage-related errors."""

    pass


class StorageNotFoundError(StorageError):
    """Raised when a resource is not found in storage."""

    pass


class DuplicateResourceError(StorageError):
    """Raised when trying to create a duplicate resource."""

    pass
