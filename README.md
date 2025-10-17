# ToDoList Python OOP

A Python Object-Oriented Programming ToDoList application with in-memory storage.

## Features

- Project management (create, edit, delete, list)
- Task management (create, edit, delete, change status)
- In-memory storage (Phase 1)
- CLI interface
- Comprehensive error handling and validation

## Installation

```bash
poetry install
```

## Usage

### With Poetry (recommended)

```bash
poetry install
PYTHONPATH=src poetry run python -m todolist.cli.main
```

If your shell doesn't export inline env vars as expected, use:

```bash
poetry run env PYTHONPATH=src python -m todolist.cli.main
```

### Without Poetry (venv)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r <(printf "python-dotenv\n")
PYTHONPATH=src python -m todolist.cli.main
```

### Optional .env configuration

Create a `.env` file in the project root to override defaults:

```bash
APP_NAME=ToDoList
APP_VERSION=0.1.0
PROJECT_OF_NUMBER_MAX=10
TASK_OF_NUMBER_MAX=50
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
