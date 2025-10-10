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

```bash
poetry run python -m todolist.cli.main
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
