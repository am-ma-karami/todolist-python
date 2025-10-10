"""
Main CLI application for ToDoList.

This module provides the main command-line interface for the ToDoList application.
"""

import sys
from typing import Optional

from ..storage.in_memory_storage import InMemoryStorage
from ..services.config_service import ConfigService
from ..services.project_service import ProjectService
from ..services.task_service import TaskService
from .cli_interface import CLIInterface


def main() -> None:
    """
    Main entry point for the ToDoList CLI application.
    """
    try:
        # Initialize services
        config = ConfigService()
        storage = InMemoryStorage()
        project_service = ProjectService(storage, config)
        task_service = TaskService(storage, config)

        # Create and run CLI interface
        cli = CLIInterface(project_service, task_service, config)
        cli.run()

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
