"""
Repository layer for data access.

This package provides repository interfaces and implementations
for accessing project and task data.
"""

from .project_repository import ProjectRepository
from .task_repository import TaskRepository

__all__ = ["ProjectRepository", "TaskRepository"]

