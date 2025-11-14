"""
Base declarative class for SQLAlchemy models.

This module provides the base class that all ORM models should inherit from.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass

