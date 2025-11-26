"""
CLI commands entry point.

This module provides command-line entry points for various commands.
"""

from __future__ import annotations

import sys

from ..commands.autoclose_overdue import autoclose_overdue_tasks


def autoclose_command() -> None:
    """
    CLI entry point for autoclose overdue tasks command.

    Usage:
        python -m todolist.cli.commands autoclose
    """
    try:
        count = autoclose_overdue_tasks()
        print(f"✅ Closed {count} overdue task(s)")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "autoclose":
        autoclose_command()
    else:
        print("Usage: python -m todolist.cli.commands autoclose")

