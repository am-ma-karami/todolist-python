# ToDoList Python OOP

A Python Object-Oriented Programming ToDoList application with PostgreSQL database.

## Features

- Project management (create, edit, delete, list)
- Task management (create, edit, delete, change status)
- PostgreSQL database with SQLAlchemy ORM (Phase 2)
- Repository Pattern for data access
- Database migrations with Alembic
- CLI interface
- Scheduled task for auto-closing overdue tasks
- Comprehensive error handling and validation

## Prerequisites

- Python 3.11+
- Poetry
- Docker (for PostgreSQL database)

## Installation

```bash
poetry install
```

## Database Setup

### Start PostgreSQL with Docker

```bash
docker run --name todolist-db \
  -e POSTGRES_USER=todolist_user \
  -e POSTGRES_PASSWORD=todolist_password \
  -e POSTGRES_DB=todolist_db \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### Stop PostgreSQL Container

```bash
docker stop todolist-db
docker rm todolist-db
```

### Environment Configuration

Create a `.env` file in the project root:

```bash
# Application Configuration
APP_NAME=ToDoList
APP_VERSION=0.1.0

# Project Limits
PROJECT_OF_NUMBER_MAX=10
TASK_OF_NUMBER_MAX=50

# Database Configuration
DATABASE_URL=postgresql+psycopg2://todolist_user:todolist_password@localhost:5432/todolist_db
```

Or use separate variables:

```bash
DB_USER=todolist_user
DB_PASSWORD=todolist_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todolist_db
```

### Database Migrations

After setting up the database, run migrations:

**Important:** Always ensure the database is up to date before creating new migrations.

```bash
# Apply existing migrations (run this first!)
PYTHONPATH=src poetry run alembic upgrade head

# Check current migration status
PYTHONPATH=src poetry run alembic current

# Create a new migration (only if you changed models)
PYTHONPATH=src poetry run alembic revision --autogenerate -m "description of changes"

# Apply the new migration
PYTHONPATH=src poetry run alembic upgrade head

# Rollback last migration (if needed)
PYTHONPATH=src poetry run alembic downgrade -1

# View migration history
PYTHONPATH=src poetry run alembic history
```

**Note:** The initial migration (`cd1443faf836`) already exists. You only need to create new migrations when you modify the database models (Project or Task).

## Usage

### Run Web API (FastAPI) — Phase 3

```bash
PYTHONPATH=src uvicorn todolist.api.main:app --reload
```

The API will be available at:

```bash
http://127.0.0.1:8000
```

Interactive API documentation (Swagger UI) is available at:

```bash
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation is available at:

```bash
http://127.0.0.1:8000/redoc
```

### Example API Endpoints

- `GET /health` → simple health check
- `GET /api/projects` → list all projects
- `POST /api/projects` → create project
- `GET /api/projects/{project_id}` → get single project
- `PATCH /api/projects/{project_id}` → update project
- `DELETE /api/projects/{project_id}` → delete project
- `GET /api/projects/search?query=...` → search projects
- `GET /api/projects/{project_id}/statistics` → project statistics

- `GET /api/tasks` → list tasks (supports `status` and `project_id` filters)
- `POST /api/tasks` → create task
- `GET /api/tasks/{task_id}` → get single task
- `PATCH /api/tasks/{task_id}` → update task
- `DELETE /api/tasks/{task_id}` → delete task
- `GET /api/tasks/overdue/list` → list overdue tasks
- `GET /api/tasks/project/{project_id}` → list tasks in a project
- `GET /api/tasks/search?query=...` → search tasks
- `GET /api/tasks/statistics/summary` → global or per-project task statistics

All request and response schemas are documented automatically in `/docs`
using Pydantic models and FastAPI's OpenAPI integration.

### CLI Application (Deprecated in Phase 3)

The CLI is kept only for backward compatibility and will be removed
in a future phase. The recommended way to use the application is
through the HTTP API described above.

To run the deprecated CLI:

```bash
PYTHONPATH=src poetry run python -m todolist.cli.main
```

Or with explicit env:

```bash
poetry run env PYTHONPATH=src python -m todolist.cli.main
```

When the CLI starts, it prints a deprecation warning and suggests
using the FastAPI HTTP API instead.

### Run Autoclose Overdue Tasks Command

```bash
PYTHONPATH=src poetry run python -m todolist.cli.commands autoclose
```

This command automatically closes tasks that have passed their deadline.

### Schedule Autoclose Command (Cron Job)

Add to crontab to run every 15 minutes:

```bash
*/15 * * * * cd /path/to/todolist-python && PYTHONPATH=src poetry run python -m todolist.cli.commands autoclose
```

## Development

```bash
# Run tests
poetry run pytest

# Format code
poetry run black .

# Lint code
poetry run flake8

# Type checking
poetry run mypy .
```

## Project Structure

```
src/todolist/
├── api/              # FastAPI app, routers, Pydantic models, dependencies
├── commands/         # Scheduled tasks and commands
├── db/               # Database configuration and session management
├── exceptions/       # Custom exception classes
├── models/           # SQLAlchemy ORM models
├── repositories/     # Repository Pattern implementations
├── services/         # Business logic layer
└── cli/              # Command-line interface (deprecated)
```

## Architecture

- **Models**: SQLAlchemy ORM models (Project, Task)
- **Repositories**: Data access layer with Repository Pattern
- **Services**: Business logic and validation
- **API**: FastAPI HTTP API (primary user-facing interface in Phase 3)
- **CLI**: Command-line interface (deprecated in Phase 3)
- **Commands**: Scheduled tasks and automation
