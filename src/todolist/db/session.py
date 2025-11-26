"""
Database session management.

This module handles database connection, session creation, and
initialization of the database schema.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .base import Base

# Load environment variables
load_dotenv()


def get_database_url() -> str:
    """
    Get database URL from environment variables.

    Supports both DATABASE_URL format and separate DB_* variables.

    Returns:
        Database connection URL string

    Raises:
        ValueError: If DATABASE_URL or required DB_* variables are not set
    """
    # Try DATABASE_URL first
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Fallback to separate variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    if not all([db_user, db_password, db_name]):
        raise ValueError(
            "Either DATABASE_URL or DB_USER, DB_PASSWORD, and DB_NAME "
            "must be set in environment variables"
        )

    return (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )


def get_session_factory() -> sessionmaker[Session]:
    """
    Create and return a session factory.

    Returns:
        SQLAlchemy session factory
    """
    database_url = get_database_url()
    engine = create_engine(database_url, echo=False)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
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

