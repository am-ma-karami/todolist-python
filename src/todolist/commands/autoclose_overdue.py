"""
Command to automatically close overdue tasks.

This module provides functionality to automatically mark overdue tasks
as done and set their closed_at timestamp.
"""

from __future__ import annotations

from datetime import date, datetime

from ..db.session import get_session
from ..repositories.task_repository import SQLAlchemyTaskRepository


def autoclose_overdue_tasks() -> int:
    """
    Automatically close overdue tasks.

    Finds all tasks that have a deadline in the past and are not yet done,
    marks them as done, and sets their closed_at timestamp.

    Returns:
        Number of tasks that were closed
    """
    with get_session() as session:
        task_repo = SQLAlchemyTaskRepository(session)
        today = date.today()

        # Get all tasks that are not done
        all_tasks = task_repo.get_all()
        overdue_tasks = [
            task
            for task in all_tasks
            if task.deadline
            and task.deadline < today
            and task.status != "done"
        ]

        # Close each overdue task
        closed_count = 0
        for task in overdue_tasks:
            task.status = "done"
            task.closed_at = datetime.now()
            task_repo.update(task)
            closed_count += 1

        return closed_count


if __name__ == "__main__":
    """Run the command when executed directly."""
    count = autoclose_overdue_tasks()
    print(f"Closed {count} overdue task(s)")

