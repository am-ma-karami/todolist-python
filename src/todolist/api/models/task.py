"""
Pydantic models for Task API.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from ...models.task import VALID_STATUSES


class TaskBase(BaseModel):
    """Base properties shared by Task models."""

    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=15, max_length=1000)
    status: str = Field(
        default="todo",
        description="Task status",
    )
    deadline: Optional[date] = None


class TaskCreate(TaskBase):
    """Payload for creating a new task."""

    project_id: str = Field(..., description="ID of the project this task belongs to")


class TaskUpdate(BaseModel):
    """Payload for updating an existing task."""

    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=15, max_length=1000)
    status: Optional[str] = Field(
        None,
        description=f"Task status, one of: {', '.join(sorted(VALID_STATUSES))}",
    )
    deadline: Optional[date] = None


class TaskRead(TaskBase):
    """Task data returned from API."""

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""

        from_attributes = True


