"""
FastAPI application entry point for ToDoList.

This module defines the FastAPI app and includes project and task routers.
"""

from __future__ import annotations

from fastapi import FastAPI

from .routers.projects import router as projects_router
from .routers.tasks import router as tasks_router


app = FastAPI(
    title="ToDoList API",
    version="0.1.0",
    description="FastAPI-based Web API for ToDoList application.",
)


app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


