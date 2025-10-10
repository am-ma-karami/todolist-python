"""
Task service for ToDoList application.

This module contains the business logic for managing tasks,
including validation, limits, and business rules.
"""

from datetime import date
from typing import List, Optional
from uuid import UUID

from ..models.task import Task
from ..storage.in_memory_storage import InMemoryStorage
from .config_service import ConfigService


class TaskService:
    """
    Service for managing tasks with business logic.
    
    This class provides methods to create, read, update, and delete tasks
    with proper validation and business rule enforcement.
    """
    
    def __init__(self, storage: InMemoryStorage, config: ConfigService) -> None:
        """
        Initialize the task service.
        
        Args:
            storage: The storage layer to use
            config: The configuration service to use
        """
        self._storage = storage
        self._config = config
    
    def create_task(self, project_id: UUID, title: str, description: str,
                   status: str = 'todo', deadline: Optional[date] = None) -> Task:
        """
        Create a new task in a project.
        
        Args:
            project_id: The ID of the project this task belongs to
            title: The title of the task
            description: The description of the task
            status: The status of the task (default: 'todo')
            deadline: Optional deadline for the task
            
        Returns:
            The created task
            
        Raises:
            ValueError: If validation fails or limits are exceeded
        """
        # Check if project exists
        if not self._storage.project_exists(project_id):
            raise ValueError(f"Project with ID {project_id} not found")
        
        # Check task limit for the project
        current_task_count = self._storage.get_task_count_by_project(project_id)
        if current_task_count >= self._config.get_task_max_count():
            raise ValueError(
                f"Maximum number of tasks ({self._config.get_task_max_count()}) "
                f"exceeded for this project"
            )
        
        # Create and store the task
        task = Task(title, description, status, deadline)
        return self._storage.create_task(task, project_id)
    
    def get_task(self, task_id: UUID) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        return self._storage.get_task(task_id)
    
    def get_tasks_by_project(self, project_id: UUID) -> List[Task]:
        """
        Get all tasks in a project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            List of tasks in the project
        """
        return self._storage.get_tasks_by_project(project_id)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self._storage.get_all_tasks()
    
    def update_task(self, task_id: UUID, title: Optional[str] = None,
                   description: Optional[str] = None, status: Optional[str] = None,
                   deadline: Optional[date] = None) -> Task:
        """
        Update a task.
        
        Args:
            task_id: The ID of the task to update
            title: The new title (optional)
            description: The new description (optional)
            status: The new status (optional)
            deadline: The new deadline (optional)
            
        Returns:
            The updated task
            
        Raises:
            ValueError: If task not found or validation fails
        """
        task = self._storage.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        if title is not None:
            task.update_title(title)
        
        if description is not None:
            task.update_description(description)
        
        if status is not None:
            task.update_status(status)
        
        if deadline is not None:
            task.update_deadline(deadline)
        
        return self._storage.update_task(task)
    
    def delete_task(self, task_id: UUID) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False if not found
        """
        return self._storage.delete_task(task_id)
    
    def task_exists(self, task_id: UUID) -> bool:
        """
        Check if a task exists.
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            True if the task exists, False otherwise
        """
        return self._storage.task_exists(task_id)
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Get all tasks with a specific status.
        
        Args:
            status: The status to filter by
            
        Returns:
            List of tasks with the specified status
        """
        return self._storage.get_tasks_by_status(status)
    
    def get_tasks_by_project_and_status(self, project_id: UUID, status: str) -> List[Task]:
        """
        Get tasks in a project with a specific status.
        
        Args:
            project_id: The ID of the project
            status: The status to filter by
            
        Returns:
            List of tasks in the project with the specified status
        """
        return self._storage.get_tasks_by_project_and_status(project_id, status)
    
    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks.
        
        Returns:
            List of overdue tasks
        """
        all_tasks = self._storage.get_all_tasks()
        return [task for task in all_tasks if task.is_overdue()]
    
    def get_overdue_tasks_by_project(self, project_id: UUID) -> List[Task]:
        """
        Get overdue tasks in a specific project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            List of overdue tasks in the project
        """
        project_tasks = self._storage.get_tasks_by_project(project_id)
        return [task for task in project_tasks if task.is_overdue()]
    
    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.
        
        Returns:
            List of completed tasks
        """
        return self._storage.get_tasks_by_status('done')
    
    def get_completed_tasks_by_project(self, project_id: UUID) -> List[Task]:
        """
        Get completed tasks in a specific project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            List of completed tasks in the project
        """
        return self._storage.get_tasks_by_project_and_status(project_id, 'done')
    
    def search_tasks(self, query: str, project_id: Optional[UUID] = None) -> List[Task]:
        """
        Search tasks by title or description.
        
        Args:
            query: The search query
            project_id: Optional project ID to limit search to
            
        Returns:
            List of tasks matching the query
        """
        if not query or not query.strip():
            return []
        
        query_lower = query.lower().strip()
        
        if project_id:
            tasks = self._storage.get_tasks_by_project(project_id)
        else:
            tasks = self._storage.get_all_tasks()
        
        matching_tasks = []
        for task in tasks:
            if (query_lower in task.title.lower() or 
                query_lower in task.description.lower()):
                matching_tasks.append(task)
        
        return matching_tasks
    
    def get_task_statistics(self, project_id: Optional[UUID] = None) -> dict:
        """
        Get task statistics.
        
        Args:
            project_id: Optional project ID to limit statistics to
            
        Returns:
            Dictionary with task statistics
        """
        if project_id:
            tasks = self._storage.get_tasks_by_project(project_id)
        else:
            tasks = self._storage.get_all_tasks()
        
        stats = {
            'total_tasks': len(tasks),
            'todo_tasks': len([t for t in tasks if t.status == 'todo']),
            'doing_tasks': len([t for t in tasks if t.status == 'doing']),
            'done_tasks': len([t for t in tasks if t.status == 'done']),
            'overdue_tasks': len([t for t in tasks if t.is_overdue()]),
            'completed_tasks': len([t for t in tasks if t.is_completed()])
        }
        
        return stats
    
    def get_task_count_by_project(self, project_id: UUID) -> int:
        """
        Get the number of tasks in a project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            The number of tasks in the project
        """
        return self._storage.get_task_count_by_project(project_id)
