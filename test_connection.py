"""Quick test script to verify database connection and repositories."""

from todolist.db.session import get_session
from todolist.repositories.project_repository import SQLAlchemyProjectRepository
from todolist.repositories.task_repository import SQLAlchemyTaskRepository

if __name__ == "__main__":
    with get_session() as session:
        project_repo = SQLAlchemyProjectRepository(session)
        task_repo = SQLAlchemyTaskRepository(session)
        print("✅ Repositories created successfully")
        print(f"Projects count: {project_repo.count()}")
        print(f"Tasks count: {task_repo.count()}")

