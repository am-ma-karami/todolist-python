"""
Task ORM model for ToDoList application.

This module contains the Task SQLAlchemy model which represents
a task that belongs to a project in the database.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import CheckConstraint, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base

VALID_STATUSES = {"todo", "doing", "done"}


class Task(Base):
    """
    SQLAlchemy ORM model for Task entity.

    Represents a task that belongs to a project.
    Each task has a title, description, status, optional deadline,
    and timestamps for creation and updates.
    """

    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
        index=True,
    )
    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="todo",
    )
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(
        default=None, nullable=True
    )

    # Relationship: Many-to-One with Project
    project: Mapped["Project"] = relationship(
        "Project", back_populates="tasks", lazy="select"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'doing', 'done')",
            name="ck_task_status",
        ),
    )

    def __repr__(self) -> str:
        """Return string representation of the task."""
        return (
            f"<Task(id={self.id!r}, title={self.title!r}, "
            f"status={self.status!r}, project_id={self.project_id!r})>"
        )
