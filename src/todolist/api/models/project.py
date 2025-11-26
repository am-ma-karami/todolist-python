"""
Pydantic models for Project API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base properties shared by Project models."""

    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=15, max_length=1000)


class ProjectCreate(ProjectBase):
    """Payload for creating a new project."""

    pass


class ProjectUpdate(BaseModel):
    """Payload for updating an existing project."""

    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=15, max_length=1000)


class ProjectRead(ProjectBase):
    """Project data returned from API."""

    id: str
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


