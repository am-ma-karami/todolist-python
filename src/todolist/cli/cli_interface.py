"""
CLI interface for ToDoList application.

This module provides the command-line interface for interacting with
projects and tasks.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from ..services.project_service import ProjectService
from ..services.task_service import TaskService
from ..services.config_service import ConfigService


class CLIInterface:
    """
    Command-line interface for the ToDoList application.
    
    This class provides methods to interact with projects and tasks
    through a text-based interface.
    """
    
    def __init__(self, project_service: ProjectService, 
                 task_service: TaskService, config: ConfigService) -> None:
        """
        Initialize the CLI interface.
        
        Args:
            project_service: The project service to use
            task_service: The task service to use
            config: The configuration service to use
        """
        self._project_service = project_service
        self._task_service = task_service
        self._config = config
    
    def run(self) -> None:
        """Run the main CLI loop."""
        self._print_welcome()
        
        while True:
            try:
                self._print_main_menu()
                choice = input("Enter your choice: ").strip()
                
                if choice == '1':
                    self._handle_project_menu()
                elif choice == '2':
                    self._handle_task_menu()
                elif choice == '3':
                    self._handle_statistics()
                elif choice == '4':
                    self._handle_search()
                elif choice == '0':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def _print_welcome(self) -> None:
        """Print welcome message."""
        print("=" * 60)
        print(f"Welcome to {self._config.get_app_name()} v{self._config.get_app_version()}")
        print("=" * 60)
        print()
    
    def _print_main_menu(self) -> None:
        """Print the main menu."""
        print("\n" + "=" * 40)
        print("MAIN MENU")
        print("=" * 40)
        print("1. Manage Projects")
        print("2. Manage Tasks")
        print("3. View Statistics")
        print("4. Search")
        print("0. Exit")
        print("=" * 40)
    
    def _handle_project_menu(self) -> None:
        """Handle project management menu."""
        while True:
            print("\n" + "=" * 40)
            print("PROJECT MANAGEMENT")
            print("=" * 40)
            print("1. Create Project")
            print("2. List Projects")
            print("3. View Project Details")
            print("4. Edit Project")
            print("5. Delete Project")
            print("0. Back to Main Menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self._create_project()
            elif choice == '2':
                self._list_projects()
            elif choice == '3':
                self._view_project_details()
            elif choice == '4':
                self._edit_project()
            elif choice == '5':
                self._delete_project()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _handle_task_menu(self) -> None:
        """Handle task management menu."""
        while True:
            print("\n" + "=" * 40)
            print("TASK MANAGEMENT")
            print("=" * 40)
            print("1. Create Task")
            print("2. List Tasks")
            print("3. View Task Details")
            print("4. Edit Task")
            print("5. Change Task Status")
            print("6. Delete Task")
            print("0. Back to Main Menu")
            print("=" * 40)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self._create_task()
            elif choice == '2':
                self._list_tasks()
            elif choice == '3':
                self._view_task_details()
            elif choice == '4':
                self._edit_task()
            elif choice == '5':
                self._change_task_status()
            elif choice == '6':
                self._delete_task()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _create_project(self) -> None:
        """Create a new project."""
        try:
            print("\n--- Create New Project ---")
            name = input("Project name: ").strip()
            description = input("Project description: ").strip()
            
            project = self._project_service.create_project(name, description)
            print(f"\n✅ Project created successfully!")
            print(f"Project ID: {project.id}")
            print(f"Name: {project.name}")
            print(f"Description: {project.description}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def _list_projects(self) -> None:
        """List all projects."""
        projects = self._project_service.get_all_projects()
        
        if not projects:
            print("\n📝 No projects found.")
            return
        
        print(f"\n📋 Projects ({len(projects)}):")
        print("-" * 80)
        for i, project in enumerate(projects, 1):
            task_count = self._task_service.get_task_count_by_project(project.id)
            print(f"{i}. {project.name}")
            print(f"   ID: {project.id}")
            print(f"   Description: {project.description}")
            print(f"   Tasks: {task_count}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 80)
    
    def _view_project_details(self) -> None:
        """View detailed information about a project."""
        project_id = self._get_project_id_input()
        if not project_id:
            return
        
        project = self._project_service.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        print(f"\n📋 Project Details:")
        print(f"Name: {project.name}")
        print(f"Description: {project.description}")
        print(f"ID: {project.id}")
        print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        # Show project statistics
        stats = self._project_service.get_project_statistics(project_id)
        print(f"\n📊 Statistics:")
        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"Todo: {stats['todo_tasks']}")
        print(f"Doing: {stats['doing_tasks']}")
        print(f"Done: {stats['done_tasks']}")
        print(f"Overdue: {stats['overdue_tasks']}")
        
        # Show tasks
        tasks = self._task_service.get_tasks_by_project(project_id)
        if tasks:
            print(f"\n📝 Tasks ({len(tasks)}):")
            for i, task in enumerate(tasks, 1):
                status_emoji = {"todo": "⏳", "doing": "🔄", "done": "✅"}.get(task.status, "❓")
                overdue = " (OVERDUE)" if task.is_overdue() else ""
                print(f"{i}. {status_emoji} {task.title}{overdue}")
                print(f"   Status: {task.status}")
                if task.deadline:
                    print(f"   Deadline: {task.deadline}")
                print(f"   Description: {task.description[:100]}{'...' if len(task.description) > 100 else ''}")
                print("-" * 40)
        else:
            print("\n📝 No tasks in this project.")
    
    def _edit_project(self) -> None:
        """Edit a project."""
        project_id = self._get_project_id_input()
        if not project_id:
            return
        
        project = self._project_service.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        print(f"\n--- Edit Project: {project.name} ---")
        
        new_name = input(f"New name (current: {project.name}): ").strip()
        new_description = input(f"New description (current: {project.description}): ").strip()
        
        try:
            self._project_service.update_project(
                project_id,
                new_name if new_name else None,
                new_description if new_description else None
            )
            print("✅ Project updated successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def _delete_project(self) -> None:
        """Delete a project."""
        project_id = self._get_project_id_input()
        if not project_id:
            return
        
        project = self._project_service.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        print(f"\n⚠️  Are you sure you want to delete project '{project.name}'?")
        print("This will also delete ALL tasks in this project!")
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        
        if confirm == 'yes':
            if self._project_service.delete_project(project_id):
                print("✅ Project deleted successfully!")
            else:
                print("❌ Failed to delete project.")
        else:
            print("❌ Deletion cancelled.")
    
    def _create_task(self) -> None:
        """Create a new task."""
        project_id = self._get_project_id_input()
        if not project_id:
            return
        
        project = self._project_service.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        try:
            print(f"\n--- Create New Task in '{project.name}' ---")
            title = input("Task title: ").strip()
            description = input("Task description: ").strip()
            
            print("Status options: todo, doing, done")
            status = input("Status (default: todo): ").strip() or 'todo'
            
            deadline_str = input("Deadline (YYYY-MM-DD, optional): ").strip()
            deadline = None
            if deadline_str:
                try:
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                except ValueError:
                    print("❌ Invalid date format. Task created without deadline.")
            
            task = self._task_service.create_task(project_id, title, description, status, deadline)
            print(f"\n✅ Task created successfully!")
            print(f"Task ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Status: {task.status}")
            if task.deadline:
                print(f"Deadline: {task.deadline}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def _list_tasks(self) -> None:
        """List tasks."""
        print("\n--- List Tasks ---")
        print("1. All tasks")
        print("2. Tasks in a project")
        print("3. Tasks by status")
        print("4. Overdue tasks")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            self._list_all_tasks()
        elif choice == '2':
            self._list_tasks_by_project()
        elif choice == '3':
            self._list_tasks_by_status()
        elif choice == '4':
            self._list_overdue_tasks()
        else:
            print("Invalid choice.")
    
    def _list_all_tasks(self) -> None:
        """List all tasks."""
        tasks = self._task_service.get_all_tasks()
        
        if not tasks:
            print("\n📝 No tasks found.")
            return
        
        print(f"\n📝 All Tasks ({len(tasks)}):")
        self._print_tasks_list(tasks)
    
    def _list_tasks_by_project(self) -> None:
        """List tasks in a project."""
        project_id = self._get_project_id_input()
        if not project_id:
            return
        
        tasks = self._task_service.get_tasks_by_project(project_id)
        
        if not tasks:
            print("\n📝 No tasks found in this project.")
            return
        
        print(f"\n📝 Tasks in Project ({len(tasks)}):")
        self._print_tasks_list(tasks)
    
    def _list_tasks_by_status(self) -> None:
        """List tasks by status."""
        print("Status options: todo, doing, done")
        status = input("Enter status: ").strip()
        
        if status not in ['todo', 'doing', 'done']:
            print("❌ Invalid status.")
            return
        
        tasks = self._task_service.get_tasks_by_status(status)
        
        if not tasks:
            print(f"\n📝 No {status} tasks found.")
            return
        
        print(f"\n📝 {status.title()} Tasks ({len(tasks)}):")
        self._print_tasks_list(tasks)
    
    def _list_overdue_tasks(self) -> None:
        """List overdue tasks."""
        tasks = self._task_service.get_overdue_tasks()
        
        if not tasks:
            print("\n📝 No overdue tasks found.")
            return
        
        print(f"\n📝 Overdue Tasks ({len(tasks)}):")
        self._print_tasks_list(tasks)
    
    def _print_tasks_list(self, tasks) -> None:
        """Print a list of tasks."""
        print("-" * 80)
        for i, task in enumerate(tasks, 1):
            status_emoji = {"todo": "⏳", "doing": "🔄", "done": "✅"}.get(task.status, "❓")
            overdue = " (OVERDUE)" if task.is_overdue() else ""
            print(f"{i}. {status_emoji} {task.title}{overdue}")
            print(f"   ID: {task.id}")
            print(f"   Status: {task.status}")
            if task.deadline:
                print(f"   Deadline: {task.deadline}")
            print(f"   Description: {task.description[:100]}{'...' if len(task.description) > 100 else ''}")
            print("-" * 80)
    
    def _view_task_details(self) -> None:
        """View detailed information about a task."""
        task_id = self._get_task_id_input()
        if not task_id:
            return
        
        task = self._task_service.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return
        
        print(f"\n📝 Task Details:")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Status: {task.status}")
        print(f"ID: {task.id}")
        if task.deadline:
            print(f"Deadline: {task.deadline}")
            if task.is_overdue():
                print("⚠️  This task is OVERDUE!")
        print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")
    
    def _edit_task(self) -> None:
        """Edit a task."""
        task_id = self._get_task_id_input()
        if not task_id:
            return
        
        task = self._task_service.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return
        
        print(f"\n--- Edit Task: {task.title} ---")
        
        new_title = input(f"New title (current: {task.title}): ").strip()
        new_description = input(f"New description (current: {task.description}): ").strip()
        
        deadline_str = input(f"New deadline (current: {task.deadline or 'None'}, YYYY-MM-DD): ").strip()
        new_deadline = None
        if deadline_str and deadline_str.lower() != 'none':
            try:
                new_deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            except ValueError:
                print("❌ Invalid date format. Keeping current deadline.")
                new_deadline = task.deadline
        
        try:
            self._task_service.update_task(
                task_id,
                new_title if new_title else None,
                new_description if new_description else None,
                None,  # status handled separately
                new_deadline
            )
            print("✅ Task updated successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def _change_task_status(self) -> None:
        """Change task status."""
        task_id = self._get_task_id_input()
        if not task_id:
            return
        
        task = self._task_service.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return
        
        print(f"\n--- Change Status for: {task.title} ---")
        print(f"Current status: {task.status}")
        print("Available statuses: todo, doing, done")
        
        new_status = input("New status: ").strip()
        
        try:
            self._task_service.update_task(task_id, status=new_status)
            print("✅ Task status updated successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def _delete_task(self) -> None:
        """Delete a task."""
        task_id = self._get_task_id_input()
        if not task_id:
            return
        
        task = self._task_service.get_task(task_id)
        if not task:
            print("❌ Task not found.")
            return
        
        print(f"\n⚠️  Are you sure you want to delete task '{task.title}'?")
        confirm = input("Type 'yes' to confirm: ").strip().lower()
        
        if confirm == 'yes':
            if self._task_service.delete_task(task_id):
                print("✅ Task deleted successfully!")
            else:
                print("❌ Failed to delete task.")
        else:
            print("❌ Deletion cancelled.")
    
    def _handle_statistics(self) -> None:
        """Handle statistics menu."""
        print("\n--- Statistics ---")
        print("1. Overall statistics")
        print("2. Project statistics")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            self._show_overall_statistics()
        elif choice == '2':
            self._show_project_statistics()
        else:
            print("Invalid choice.")
    
    def _show_overall_statistics(self) -> None:
        """Show overall statistics."""
        stats = self._task_service.get_task_statistics()
        
        print(f"\n📊 Overall Statistics:")
        print(f"Total Projects: {self._project_service.get_project_count()}")
        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"Todo Tasks: {stats['todo_tasks']}")
        print(f"Doing Tasks: {stats['doing_tasks']}")
        print(f"Done Tasks: {stats['done_tasks']}")
        print(f"Overdue Tasks: {stats['overdue_tasks']}")
        print(f"Completed Tasks: {stats['completed_tasks']}")
    
    def _show_project_statistics(self) -> None:
        """Show project statistics."""
        project_id = self._get_project_id_input()
        if not project_id:
            return
        
        project = self._project_service.get_project(project_id)
        if not project:
            print("❌ Project not found.")
            return
        
        stats = self._project_service.get_project_statistics(project_id)
        
        print(f"\n📊 Statistics for '{project.name}':")
        print(f"Total Tasks: {stats['total_tasks']}")
        print(f"Todo Tasks: {stats['todo_tasks']}")
        print(f"Doing Tasks: {stats['doing_tasks']}")
        print(f"Done Tasks: {stats['done_tasks']}")
        print(f"Overdue Tasks: {stats['overdue_tasks']}")
    
    def _handle_search(self) -> None:
        """Handle search functionality."""
        print("\n--- Search ---")
        print("1. Search projects")
        print("2. Search tasks")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            self._search_projects()
        elif choice == '2':
            self._search_tasks()
        else:
            print("Invalid choice.")
    
    def _search_projects(self) -> None:
        """Search projects."""
        query = input("Enter search query: ").strip()
        
        if not query:
            print("❌ Search query cannot be empty.")
            return
        
        projects = self._project_service.search_projects(query)
        
        if not projects:
            print(f"\n📝 No projects found matching '{query}'.")
            return
        
        print(f"\n📝 Found {len(projects)} project(s) matching '{query}':")
        for i, project in enumerate(projects, 1):
            task_count = self._task_service.get_task_count_by_project(project.id)
            print(f"{i}. {project.name}")
            print(f"   Description: {project.description}")
            print(f"   Tasks: {task_count}")
            print("-" * 40)
    
    def _search_tasks(self) -> None:
        """Search tasks."""
        query = input("Enter search query: ").strip()
        
        if not query:
            print("❌ Search query cannot be empty.")
            return
        
        tasks = self._task_service.search_tasks(query)
        
        if not tasks:
            print(f"\n📝 No tasks found matching '{query}'.")
            return
        
        print(f"\n📝 Found {len(tasks)} task(s) matching '{query}':")
        self._print_tasks_list(tasks)
    
    def _get_project_id_input(self) -> Optional[UUID]:
        """Get project ID from user input."""
        try:
            project_id_str = input("Enter project ID: ").strip()
            if not project_id_str:
                return None
            return UUID(project_id_str)
        except ValueError:
            print("❌ Invalid project ID format.")
            return None
    
    def _get_task_id_input(self) -> Optional[UUID]:
        """Get task ID from user input."""
        try:
            task_id_str = input("Enter task ID: ").strip()
            if not task_id_str:
                return None
            return UUID(task_id_str)
        except ValueError:
            print("❌ Invalid task ID format.")
            return None
