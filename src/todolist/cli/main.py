"""
Main CLI application for ToDoList.

This module provides the main command-line interface for the ToDoList application.
"""

from __future__ import annotations

import sys

from ..db.session import get_session
from ..repositories.project_repository import SQLAlchemyProjectRepository
from ..repositories.task_repository import SQLAlchemyTaskRepository
from ..services.config_service import ConfigService
from ..services.project_service import ProjectService
from ..services.task_service import TaskService
from .cli_interface import CLIInterface


def main() -> None:
    """
    Main entry point for the ToDoList CLI application.

    Deprecated:
        In Phase 3, the primary interface is the FastAPI HTTP API.
        This CLI entry point is kept only for backward compatibility
        and will be removed in a future version.
    """
    try:
        # Initialize configuration
        config = ConfigService()

        # Get database session (context manager)
        with get_session() as session:
            # Initialize repositories
            project_repo = SQLAlchemyProjectRepository(session)
            task_repo = SQLAlchemyTaskRepository(session)

            # Initialize services
            project_service = ProjectService(project_repo, config)
            task_service = TaskService(task_repo, project_repo, config)

        # Create and run CLI interface
        cli = CLIInterface(project_service, task_service, config)
        cli.run()

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
