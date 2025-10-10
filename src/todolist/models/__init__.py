"""
Models package for ToDoList application.

Contains the core domain models: Project and Task.
"""

from .project import Project
from .task import Task

__all__ = ["Project", "Task"]
