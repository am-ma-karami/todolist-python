"""
Project ORM model for ToDoList application.

This module contains the Project SQLAlchemy model which represents
a project that can contain multiple tasks in the database.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base

if TYPE_CHECKING:
    from .task import Task


class Project(Base):
    """
    SQLAlchemy ORM model for Project entity.

    Represents a project that can contain multiple tasks.
    Each project has a unique name, description, and creation timestamp.
    """

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, nullable=False
    )

    # Relationship: One-to-Many with Task
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="select",
    )

    __table_args__ = (UniqueConstraint("name", name="uq_project_name"),)

    def __repr__(self) -> str:
        """Return string representation of the project."""
        return (
            f"<Project(id={self.id!r}, name={self.name!r}, "
            f"tasks_count={len(self.tasks)})>"
        )
