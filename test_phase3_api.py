"""
End-to-end tests for Phase 3 FastAPI Web API.

This script assumes:
    - PostgreSQL is running and accessible
    - Alembic migrations have been applied (upgrade head)
    - FastAPI server is running on http://127.0.0.1:8000

Run with:
    PYTHONPATH=src python test_phase3_api.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4


BASE_URL = "http://127.0.0.1:8000"


@dataclass
class ApiResponse:
    """Simple container for API responses."""

    status: int
    body: Any


def call_api(
    method: str,
    path: str,
    body: Any | None = None,
    expected_status: int | None = None,
) -> ApiResponse:
    """Send an HTTP request to the running FastAPI server."""
    url = f"{BASE_URL}{path}"
    data: bytes | None = None
    headers = {"Accept": "application/json"}

    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method=method.upper())

    try:
        with urlopen(request) as response:
            status = response.getcode()
            raw_body = response.read().decode("utf-8")
    except HTTPError as exc:
        status = exc.code
        raw_body = exc.read().decode("utf-8")
    except URLError as exc:  # pragma: no cover - network error
        raise SystemExit(f"Cannot connect to API at {BASE_URL}: {exc}") from exc

    parsed_body: Any
    if raw_body:
        try:
            parsed_body = json.loads(raw_body)
        except json.JSONDecodeError:
            parsed_body = raw_body
    else:
        parsed_body = None

    if expected_status is not None:
        assert (
            status == expected_status
        ), f"Expected {expected_status}, got {status}, body={parsed_body!r}"

    return ApiResponse(status=status, body=parsed_body)


def test_phase3_api() -> None:
    """Run a sequence of API calls to verify Phase 3 behaviour."""
    print("=== Phase 3 API tests starting ===")

    # 1. Health check
    health = call_api("GET", "/health", expected_status=200)
    assert health.body == {"status": "ok"}, f"Unexpected health body: {health.body}"
    print("[OK] Health check")

    # 2. Create a project
    project_payload = {
        "name": f"Phase3 Test Project {uuid4().hex[:8]}",
        "description": "This is a sample project for testing the Phase 3 API.",
    }
    created_project = call_api(
        "POST",
        "/api/projects/",
        body=project_payload,
        expected_status=201,
    ).body
    project_id = created_project["id"]
    print(f"[OK] Created project: {project_id}")

    # 3. List projects
    projects = call_api("GET", "/api/projects/", expected_status=200).body
    assert any(p["id"] == project_id for p in projects), "Project not in list"
    print("[OK] List projects includes created project")

    # 4. Get project by ID
    project = call_api(
        "GET",
        f"/api/projects/{project_id}",
        expected_status=200,
    ).body
    assert project["name"] == project_payload["name"]
    print("[OK] Get project by ID")

    # 5. Update project (use a unique name to avoid duplicate-name constraint)
    updated_name = f"Phase3 Updated Project {project_id[:8]}"
    updated_project = call_api(
        "PATCH",
        f"/api/projects/{project_id}",
        body={"name": updated_name},
        expected_status=200,
    ).body
    assert updated_project["name"] == updated_name
    print("[OK] Update project")

    # 6. Search projects
    search_results = call_api(
        "GET",
        "/api/projects/search?query=Updated",
        expected_status=200,
    ).body
    assert any(p["id"] == project_id for p in search_results)
    print("[OK] Search projects")

    # 7. Project statistics (initially zero tasks)
    stats = call_api(
        "GET",
        f"/api/projects/{project_id}/statistics",
        expected_status=200,
    ).body
    assert stats["total_tasks"] == 0
    print("[OK] Project statistics with zero tasks")

    # 8. Create a normal task
    task_payload = {
        "project_id": project_id,
        "title": "First API Task",
        "description": "This is a task created via the FastAPI endpoint.",
        "status": "todo",
    }
    created_task = call_api(
        "POST",
        "/api/tasks/",
        body=task_payload,
        expected_status=201,
    ).body
    task_id = created_task["id"]
    print(f"[OK] Created task: {task_id}")

    # 9. List all tasks
    tasks_all = call_api("GET", "/api/tasks/", expected_status=200).body
    assert any(t["id"] == task_id for t in tasks_all)
    print("[OK] List all tasks includes created task")

    # 10. List tasks for project
    tasks_for_project = call_api(
        "GET",
        f"/api/tasks/project/{project_id}",
        expected_status=200,
    ).body
    assert any(t["id"] == task_id for t in tasks_for_project)
    print("[OK] List tasks by project")

    # 11. Get single task
    task = call_api(
        "GET",
        f"/api/tasks/{task_id}",
        expected_status=200,
    ).body
    assert task["title"] == task_payload["title"]
    print("[OK] Get task by ID")

    # 12. Update task status
    updated_task = call_api(
        "PATCH",
        f"/api/tasks/{task_id}",
        body={"status": "doing"},
        expected_status=200,
    ).body
    assert updated_task["status"] == "doing"
    print("[OK] Update task status")

    # 13. Filter tasks by status
    doing_tasks = call_api(
        "GET",
        "/api/tasks?status=doing",
        expected_status=200,
    ).body
    assert any(t["id"] == task_id for t in doing_tasks)
    print("[OK] Filter tasks by status")

    # 14. Search tasks
    search_tasks = call_api(
        "GET",
        "/api/tasks/search?query=First",
        expected_status=200,
    ).body
    assert any(t["id"] == task_id for t in search_tasks)
    print("[OK] Search tasks")

    # 15. Task statistics (at least one task now)
    task_stats = call_api(
        "GET",
        "/api/tasks/statistics/summary",
        expected_status=200,
    ).body
    assert task_stats["total_tasks"] >= 1
    print("[OK] Global task statistics")

    # 16. Create an overdue task (deadline in the past)
    overdue_payload = {
        "project_id": project_id,
        "title": "Overdue API Task",
        "description": "This task has a past deadline and should be overdue.",
        "status": "todo",
        "deadline": "2020-01-01",
    }
    overdue_task = call_api(
        "POST",
        "/api/tasks/",
        body=overdue_payload,
        expected_status=201,
    ).body
    overdue_task_id = overdue_task["id"]
    print(f"[OK] Created overdue task: {overdue_task_id}")

    # 17. List overdue tasks
    overdue_list = call_api(
        "GET",
        "/api/tasks/overdue/list",
        expected_status=200,
    ).body
    assert any(t["id"] == overdue_task_id for t in overdue_list)
    print("[OK] List overdue tasks")

    # 18. Delete tasks
    call_api("DELETE", f"/api/tasks/{task_id}", expected_status=204)
    call_api("DELETE", f"/api/tasks/{overdue_task_id}", expected_status=204)
    print("[OK] Deleted tasks")

    # 19. Confirm deleted task returns 404
    not_found = call_api("GET", f"/api/tasks/{task_id}")
    assert not_found.status == 404
    print("[OK] 404 for deleted task")

    # 20. Delete project
    call_api("DELETE", f"/api/projects/{project_id}", expected_status=204)
    not_found_project = call_api("GET", f"/api/projects/{project_id}")
    assert not_found_project.status == 404
    print("[OK] Deleted project and confirmed 404")

    print("=== Phase 3 API tests finished successfully ===")


if __name__ == "__main__":
    test_phase3_api()


