"""
Storage package for ToDoList application.

Contains the storage layer implementations for data persistence.
"""

from .in_memory_storage import InMemoryStorage

__all__ = ["InMemoryStorage"]
