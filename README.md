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

```bash
# Create initial migration
PYTHONPATH=src poetry run alembic revision --autogenerate -m "initial migration"

# Apply migrations
PYTHONPATH=src poetry run alembic upgrade head

# Rollback last migration
PYTHONPATH=src poetry run alembic downgrade -1
```

## Usage

### Run CLI Application

```bash
PYTHONPATH=src poetry run python -m todolist.cli.main
```

Or with explicit env:

```bash
poetry run env PYTHONPATH=src python -m todolist.cli.main
```

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
├── commands/          # Scheduled tasks and commands
├── db/               # Database configuration and session management
├── exceptions/       # Custom exception classes
├── models/           # SQLAlchemy ORM models
├── repositories/     # Repository Pattern implementations
├── services/         # Business logic layer
└── cli/              # Command-line interface
```

## Architecture

- **Models**: SQLAlchemy ORM models (Project, Task)
- **Repositories**: Data access layer with Repository Pattern
- **Services**: Business logic and validation
- **CLI**: User interface layer
- **Commands**: Scheduled tasks and automation
