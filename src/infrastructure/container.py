"""Application container for managing dependencies.

This module provides centralized dependency injection and management
for the application, following Clean Architecture principles.
"""

from src.config import AppConfig
from src.config.prompts import PromptConfig
from src.domain.interfaces.provider import Provider
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.adapters.providers.factory import build_provider
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.repositories.sqlite_message_repository import (
    SQLiteMessageRepository,
)
from src.infrastructure.repositories.sqlite_user_repository import (
    SQLiteUserRepository,
)


class Container:
    """Manages application dependencies and lifecycle.

    This container provides clean dependency injection without frameworks,
    keeping the architecture simple for Phase 0 while maintaining testability.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        config: AppConfig,
        database_connection: DatabaseConnection | None = None,
        message_repository: IMessageRepository | None = None,
        user_repository: IUserRepository | None = None,
        provider: Provider | None = None,
    ) -> None:
        """Initialize the container with optional overrides.

        Args:
            config: Application configuration.
            database_connection: Optional database connection override.
            message_repository: Optional message repository override.
            user_repository: Optional user repository override.
            provider: Optional provider override.
        """
        self._config = config

        # Database connection (lazy initialization)
        self._db_connection = database_connection

        # Repositories (lazy initialization)
        self._message_repository = message_repository
        self._user_repository = user_repository

        # Provider (lazy initialization)
        self._provider = provider

    def get_database_connection(self) -> DatabaseConnection:
        """Get database connection, creating if needed.

        Returns:
            Database connection instance.
        """
        if self._db_connection is None:
            self._db_connection = DatabaseConnection(self._config)
        return self._db_connection

    def get_message_repository(self) -> IMessageRepository:
        """Get message repository, creating if needed.

        Returns:
            Message repository instance.
        """
        if self._message_repository is None:
            self._message_repository = SQLiteMessageRepository(self.get_database_connection().connection)
        return self._message_repository

    def get_user_repository(self) -> IUserRepository:
        """Get user repository, creating if needed.

        Returns:
            User repository instance.
        """
        if self._user_repository is None:
            self._user_repository = SQLiteUserRepository(self.get_database_connection().connection)
        return self._user_repository

    def get_provider(self, name: str | None = None) -> Provider:
        """Get LLM provider, creating if needed.

        Args:
            name: Optional provider name identifier.

        Returns:
            Provider instance.
        """
        if self._provider is None:
            self._provider = build_provider(
                config=self._config.provider_config,
                name=name,
            )
        return self._provider

    def get_prompt_config(self) -> PromptConfig:
        """Get prompt configuration.

        Returns:
            Prompt configuration instance.
        """
        return PromptConfig.default()


__all__ = ["Container"]
