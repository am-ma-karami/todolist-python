"""
Custom exceptions for ToDoList application.

This package defines custom exception classes for better error handling
and more specific error messages.
"""

from .base import ToDoListError, ValidationError
from .repository_exceptions import (
    DuplicateResourceError,
    StorageError,
    StorageNotFoundError,
)
from .service_exceptions import (
    DuplicateProjectError,
    InvalidStatusError,
    ProjectError,
    ProjectLimitExceededError,
    ProjectNotFoundError,
    TaskError,
    TaskLimitExceededError,
    TaskNotFoundError,
)

__all__ = [
    "ToDoListError",
    "ValidationError",
    "StorageError",
    "StorageNotFoundError",
    "DuplicateResourceError",
    "ProjectError",
    "ProjectNotFoundError",
    "ProjectLimitExceededError",
    "DuplicateProjectError",
    "TaskError",
    "TaskNotFoundError",
    "TaskLimitExceededError",
    "InvalidStatusError",
]

