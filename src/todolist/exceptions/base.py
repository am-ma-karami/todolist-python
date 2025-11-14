"""
Base exception classes for ToDoList application.
"""


class ToDoListError(Exception):
    """Base exception class for ToDoList application."""

    pass


class ValidationError(ToDoListError):
    """Raised when validation fails."""

    pass

