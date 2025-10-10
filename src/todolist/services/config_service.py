"""
Configuration service for ToDoList application.

This module handles loading and managing application configuration
from environment variables and .env files.
"""

import os
from typing import Optional
from dotenv import load_dotenv


class ConfigService:
    """
    Service for managing application configuration.

    This class handles loading configuration from environment variables
    and .env files, providing default values and validation.
    """

    def __init__(self, env_file: str = ".env") -> None:
        """
        Initialize the configuration service.

        Args:
            env_file: Path to the .env file to load
        """
        self._env_file = env_file
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from .env file."""
        if os.path.exists(self._env_file):
            load_dotenv(self._env_file)

    def get_project_max_count(self) -> int:
        """
        Get the maximum number of projects allowed.

        Returns:
            The maximum number of projects
        """
        return self._get_int_config("PROJECT_OF_NUMBER_MAX", 10)

    def get_task_max_count(self) -> int:
        """
        Get the maximum number of tasks allowed per project.

        Returns:
            The maximum number of tasks per project
        """
        return self._get_int_config("TASK_OF_NUMBER_MAX", 50)

    def get_app_name(self) -> str:
        """
        Get the application name.

        Returns:
            The application name
        """
        return self._get_str_config("APP_NAME", "ToDoList")

    def get_app_version(self) -> str:
        """
        Get the application version.

        Returns:
            The application version
        """
        return self._get_str_config("APP_VERSION", "0.1.0")

    def _get_int_config(self, key: str, default: int) -> int:
        """
        Get an integer configuration value.

        Args:
            key: The configuration key
            default: The default value if not found

        Returns:
            The configuration value as integer
        """
        value = os.getenv(key)
        if value is None:
            return default

        try:
            return int(value)
        except ValueError:
            return default

    def _get_str_config(self, key: str, default: str) -> str:
        """
        Get a string configuration value.

        Args:
            key: The configuration key
            default: The default value if not found

        Returns:
            The configuration value as string
        """
        return os.getenv(key, default)

    def _get_bool_config(self, key: str, default: bool) -> bool:
        """
        Get a boolean configuration value.

        Args:
            key: The configuration key
            default: The default value if not found

        Returns:
            The configuration value as boolean
        """
        value = os.getenv(key)
        if value is None:
            return default

        return value.lower() in ("true", "1", "yes", "on")
