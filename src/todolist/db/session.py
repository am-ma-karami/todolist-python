"""
Database session management.

This module handles database connection, session creation, and
initialization of the database schema.
"""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .base import Base


def get_database_url() -> str:
    """
    Get database URL from environment variables.

    Returns:
        Database connection URL string

    Raises:
        ValueError: If DATABASE_URL is not set
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return database_url


def get_session_factory() -> sessionmaker[Session]:
    """
    Create and return a session factory.

    Returns:
        SQLAlchemy session factory
    """
    database_url = get_database_url()
    engine = create_engine(database_url, echo=False)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session (context manager).

    Yields:
        SQLAlchemy session instance

    Example:
        with get_session() as session:
            # Use session here
            pass
    """
    factory = get_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """
    Initialize database schema.

    Creates all tables defined in the models.
    This should be called after Alembic migrations are set up.
    """
    database_url = get_database_url()
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(bind=engine)

