"""
Test script for Phase 2 functionality.

This script tests the main features of the ToDoList application
to ensure everything works correctly.
"""

from datetime import date, datetime, timedelta
from uuid import uuid4

from todolist.db.session import get_session
from todolist.models.project import Project
from todolist.models.task import Task
from todolist.repositories.project_repository import SQLAlchemyProjectRepository
from todolist.repositories.task_repository import SQLAlchemyTaskRepository
from todolist.services.config_service import ConfigService
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService


def test_database_connection():
    """Test database connection."""
    print("🔍 Testing database connection...")
    try:
        with get_session() as session:
            from sqlalchemy import text
            result = session.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection: OK")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_create_project():
    """Test creating a project."""
    print("\n🔍 Testing project creation...")
    try:
        config = ConfigService()
        with get_session() as session:
            project_repo = SQLAlchemyProjectRepository(session)
            project_service = ProjectService(project_repo, config)

            project = project_service.create_project(
                name="Test Project",
                description="This is a test project for Phase 2"
            )
            print(f"✅ Project created: {project.name} (ID: {project.id})")
            return project.id
    except Exception as e:
        print(f"❌ Project creation failed: {e}")
        return None


def test_create_task(project_id: str):
    """Test creating a task."""
    print("\n🔍 Testing task creation...")
    try:
        config = ConfigService()
        with get_session() as session:
            project_repo = SQLAlchemyProjectRepository(session)
            task_repo = SQLAlchemyTaskRepository(session)
            task_service = TaskService(task_repo, project_repo, config)

            # Create task with deadline in the past (for autoclose test)
            yesterday = date.today() - timedelta(days=1)
            task = task_service.create_task(
                project_id=project_id,
                title="Test Task",
                description="This is a test task with overdue deadline",
                status="todo",
                deadline=yesterday
            )
            print(f"✅ Task created: {task.title} (ID: {task.id})")
            print(f"   Status: {task.status}, Deadline: {task.deadline}")
            return task.id
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return None


def test_get_projects():
    """Test getting all projects."""
    print("\n🔍 Testing get all projects...")
    try:
        config = ConfigService()
        with get_session() as session:
            project_repo = SQLAlchemyProjectRepository(session)
            project_service = ProjectService(project_repo, config)

            projects = project_service.get_all_projects()
            print(f"✅ Found {len(projects)} project(s)")
            return len(projects) > 0
    except Exception as e:
        print(f"❌ Get projects failed: {e}")
        return False


def test_update_task(task_id: str):
    """Test updating a task."""
    print("\n🔍 Testing task update...")
    try:
        config = ConfigService()
        with get_session() as session:
            project_repo = SQLAlchemyProjectRepository(session)
            task_repo = SQLAlchemyTaskRepository(session)
            task_service = TaskService(task_repo, project_repo, config)

            task = task_service.update_task(
                task_id=task_id,
                status="doing"
            )
            print(f"✅ Task updated: Status changed to '{task.status}'")
            return task.status == "doing"
    except Exception as e:
        print(f"❌ Task update failed: {e}")
        return False


def test_autoclose_command():
    """Test autoclose overdue tasks command."""
    print("\n🔍 Testing autoclose overdue tasks...")
    try:
        from todolist.commands.autoclose_overdue import autoclose_overdue_tasks

        count = autoclose_overdue_tasks()
        print(f"✅ Autoclose command executed: {count} task(s) closed")
        return True
    except Exception as e:
        print(f"❌ Autoclose command failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_verify_autoclosed_task(task_id: str):
    """Verify that the task was autoclosed."""
    print("\n🔍 Verifying autoclosed task...")
    try:
        config = ConfigService()
        with get_session() as session:
            task_repo = SQLAlchemyTaskRepository(session)
            task = task_repo.get_by_id(task_id)

            if task and task.status == "done" and task.closed_at:
                print(f"✅ Task autoclosed successfully!")
                print(f"   Status: {task.status}")
                print(f"   Closed at: {task.closed_at}")
                return True
            else:
                print(f"❌ Task was not autoclosed properly")
                print(f"   Status: {task.status if task else 'None'}")
                print(f"   Closed at: {task.closed_at if task else 'None'}")
                return False
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("ToDoList Phase 2 - Test Suite")
    print("=" * 60)

    results = []

    # Test 1: Database connection
    results.append(("Database Connection", test_database_connection()))

    # Test 2: Create project
    project_id = test_create_project()
    results.append(("Create Project", project_id is not None))

    # Test 3: Create task
    task_id = None
    if project_id:
        task_id = test_create_task(project_id)
        results.append(("Create Task", task_id is not None))

    # Test 4: Get projects
    results.append(("Get Projects", test_get_projects()))

    # Test 5: Update task
    if task_id:
        results.append(("Update Task", test_update_task(task_id)))

    # Test 6: Autoclose command
    results.append(("Autoclose Command", test_autoclose_command()))

    # Test 7: Verify autoclosed task
    if task_id:
        results.append(("Verify Autoclosed Task", test_verify_autoclosed_task(task_id)))

    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All tests passed! Phase 2 is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

