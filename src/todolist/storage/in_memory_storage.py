"""
In-memory storage implementation for ToDoList application.

This module provides an in-memory storage layer that stores projects and tasks
in memory during the application's runtime.
"""

from typing import List, Optional, Dict
from uuid import UUID

from ..models.project import Project
from ..models.task import Task


class InMemoryStorage:
    """
    In-memory storage implementation for projects and tasks.
    
    This class provides methods to store, retrieve, update, and delete
    projects and tasks in memory. Data is lost when the application stops.
    """
    
    def __init__(self) -> None:
        """Initialize the in-memory storage."""
        self._projects: Dict[UUID, Project] = {}
        self._tasks: Dict[UUID, Task] = {}
        self._project_tasks: Dict[UUID, List[UUID]] = {}  # project_id -> list of task_ids
    
    # Project methods
    def create_project(self, project: Project) -> Project:
        """
        Create a new project in storage.
        
        Args:
            project: The project to create
            
        Returns:
            The created project
            
        Raises:
            ValueError: If project with same ID already exists
        """
        if project.id in self._projects:
            raise ValueError(f"Project with ID {project.id} already exists")
        
        self._projects[project.id] = project
        self._project_tasks[project.id] = []
        return project
    
    def get_project(self, project_id: UUID) -> Optional[Project]:
        """
        Get a project by its ID.
        
        Args:
            project_id: The ID of the project to retrieve
            
        Returns:
            The project if found, None otherwise
        """
        return self._projects.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """
        Get all projects.
        
        Returns:
            List of all projects, sorted by creation time
        """
        projects = list(self._projects.values())
        return sorted(projects, key=lambda p: p.created_at)
    
    def update_project(self, project: Project) -> Project:
        """
        Update an existing project.
        
        Args:
            project: The project to update
            
        Returns:
            The updated project
            
        Raises:
            ValueError: If project doesn't exist
        """
        if project.id not in self._projects:
            raise ValueError(f"Project with ID {project.id} not found")
        
        self._projects[project.id] = project
        return project
    
    def delete_project(self, project_id: UUID) -> bool:
        """
        Delete a project and all its tasks (cascade delete).
        
        Args:
            project_id: The ID of the project to delete
            
        Returns:
            True if the project was deleted, False if not found
        """
        if project_id not in self._projects:
            return False
        
        # Delete all tasks belonging to this project
        if project_id in self._project_tasks:
            for task_id in self._project_tasks[project_id]:
                self._tasks.pop(task_id, None)
            del self._project_tasks[project_id]
        
        # Delete the project
        del self._projects[project_id]
        return True
    
    def project_exists(self, project_id: UUID) -> bool:
        """
        Check if a project exists.
        
        Args:
            project_id: The ID of the project to check
            
        Returns:
            True if the project exists, False otherwise
        """
        return project_id in self._projects
    
    def get_project_count(self) -> int:
        """
        Get the total number of projects.
        
        Returns:
            The number of projects
        """
        return len(self._projects)
    
    # Task methods
    def create_task(self, task: Task, project_id: UUID) -> Task:
        """
        Create a new task in storage and associate it with a project.
        
        Args:
            task: The task to create
            project_id: The ID of the project this task belongs to
            
        Returns:
            The created task
            
        Raises:
            ValueError: If task with same ID already exists or project doesn't exist
        """
        if task.id in self._tasks:
            raise ValueError(f"Task with ID {task.id} already exists")
        
        if project_id not in self._projects:
            raise ValueError(f"Project with ID {project_id} not found")
        
        self._tasks[task.id] = task
        self._project_tasks[project_id].append(task.id)
        return task
    
    def get_task(self, task_id: UUID) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def get_tasks_by_project(self, project_id: UUID) -> List[Task]:
        """
        Get all tasks belonging to a project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            List of tasks belonging to the project, sorted by creation time
        """
        if project_id not in self._project_tasks:
            return []
        
        task_ids = self._project_tasks[project_id]
        tasks = [self._tasks[task_id] for task_id in task_ids if task_id in self._tasks]
        return sorted(tasks, key=lambda t: t.created_at)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks, sorted by creation time
        """
        tasks = list(self._tasks.values())
        return sorted(tasks, key=lambda t: t.created_at)
    
    def update_task(self, task: Task) -> Task:
        """
        Update an existing task.
        
        Args:
            task: The task to update
            
        Returns:
            The updated task
            
        Raises:
            ValueError: If task doesn't exist
        """
        if task.id not in self._tasks:
            raise ValueError(f"Task with ID {task.id} not found")
        
        self._tasks[task.id] = task
        return task
    
    def delete_task(self, task_id: UUID) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False if not found
        """
        if task_id not in self._tasks:
            return False
        
        # Remove task from project's task list
        for project_id, task_ids in self._project_tasks.items():
            if task_id in task_ids:
                task_ids.remove(task_id)
                break
        
        # Delete the task
        del self._tasks[task_id]
        return True
    
    def task_exists(self, task_id: UUID) -> bool:
        """
        Check if a task exists.
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            True if the task exists, False otherwise
        """
        return task_id in self._tasks
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            The number of tasks
        """
        return len(self._tasks)
    
    def get_task_count_by_project(self, project_id: UUID) -> int:
        """
        Get the number of tasks in a specific project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            The number of tasks in the project
        """
        if project_id not in self._project_tasks:
            return 0
        return len(self._project_tasks[project_id])
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Get all tasks with a specific status.
        
        Args:
            status: The status to filter by
            
        Returns:
            List of tasks with the specified status
        """
        return [task for task in self._tasks.values() if task.status == status]
    
    def get_tasks_by_project_and_status(self, project_id: UUID, status: str) -> List[Task]:
        """
        Get tasks in a project with a specific status.
        
        Args:
            project_id: The ID of the project
            status: The status to filter by
            
        Returns:
            List of tasks in the project with the specified status
        """
        project_tasks = self.get_tasks_by_project(project_id)
        return [task for task in project_tasks if task.status == status]
    
    def clear_all_data(self) -> None:
        """Clear all projects and tasks from storage."""
        self._projects.clear()
        self._tasks.clear()
        self._project_tasks.clear()
