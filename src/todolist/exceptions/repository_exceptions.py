"""
Repository layer exception classes.

These exceptions are raised by repository layer when database
operations fail or data integrity issues occur.
"""

from .base import ToDoListError


class StorageError(ToDoListError):
    """Base exception for storage-related errors."""

    pass


class StorageNotFoundError(StorageError):
    """Raised when a resource is not found in storage."""

    pass


class DuplicateResourceError(StorageError):
    """Raised when trying to create a duplicate resource."""

    pass

