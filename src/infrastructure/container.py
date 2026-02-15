"""Application container for managing dependencies.

This module provides centralized dependency injection and management
for the application, following Clean Architecture principles.
"""

from src.application.use_cases.get_system_prompt import GetSystemPromptUseCase
from src.application.use_cases.load_history import LoadHistoryUseCase
from src.application.use_cases.send_message import SendMessageUseCase
from src.config.app import AppConfig
from src.config.prompts import PromptConfig
from src.domain.interfaces.frontend_adapter import IMessageAdapter, ISessionAdapter
from src.domain.interfaces.provider import Provider
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.adapters.chainlit.message_adapter import ChainlitMessageAdapter
from src.infrastructure.adapters.chainlit.session_adapter import ChainlitSessionAdapter
from src.infrastructure.adapters.providers.factory import build_provider
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.repositories.sqlite_message_repository import (
    SQLiteMessageRepository,
)
from src.infrastructure.repositories.sqlite_user_repository import (
    SQLiteUserRepository,
)


class Container:  # pylint: disable=too-many-instance-attributes
    """Manages application dependencies and lifecycle.

    This container provides clean dependency injection without frameworks,
    keeping the architecture simple while maintaining testability.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        config: AppConfig,
        database_connection: DatabaseConnection | None = None,
        message_repository: IMessageRepository | None = None,
        user_repository: IUserRepository | None = None,
        provider: Provider | None = None,
        session_adapter: ISessionAdapter | None = None,
        message_adapter: IMessageAdapter | None = None,
    ) -> None:
        """Initialize the container with optional overrides.

        Args:
            config: Application configuration.
            database_connection: Optional database connection override.
            message_repository: Optional message repository override.
            user_repository: Optional user repository override.
            provider: Optional provider override.
            session_adapter: Optional session adapter override.
            message_adapter: Optional message adapter override.
        """
        self._config = config

        self._db_connection = database_connection
        self._message_repository = message_repository
        self._user_repository = user_repository
        self._provider = provider
        self._session_adapter = session_adapter
        self._message_adapter = message_adapter

        self._load_history_use_case: LoadHistoryUseCase | None = None
        self._get_system_prompt_use_case: GetSystemPromptUseCase | None = None
        self._send_message_use_case: SendMessageUseCase | None = None

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
            self._message_repository = SQLiteMessageRepository(
                self.get_database_connection().connection,
            )
        return self._message_repository

    def get_user_repository(self) -> IUserRepository:
        """Get user repository, creating if needed.

        Returns:
            User repository instance.
        """
        if self._user_repository is None:
            self._user_repository = SQLiteUserRepository(
                self.get_database_connection().connection,
            )
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

    def get_session_adapter(self) -> ISessionAdapter:
        """Get session adapter, creating if needed.

        Returns:
            Session adapter instance.
        """
        if self._session_adapter is None:
            self._session_adapter = ChainlitSessionAdapter(
                user_repository=self.get_user_repository(),
            )
        return self._session_adapter

    def get_message_adapter(self) -> IMessageAdapter:
        """Get message adapter, creating if needed.

        Returns:
            Message adapter instance.
        """
        if self._message_adapter is None:
            self._message_adapter = ChainlitMessageAdapter()
        return self._message_adapter

    def get_load_history_use_case(self) -> LoadHistoryUseCase:
        """Get load history use case, creating if needed.

        Returns:
            LoadHistoryUseCase instance.
        """
        if self._load_history_use_case is None:
            self._load_history_use_case = LoadHistoryUseCase(
                message_repository=self.get_message_repository(),
            )
        return self._load_history_use_case

    def get_system_prompt_use_case(self) -> GetSystemPromptUseCase:
        """Get system prompt use case, creating if needed.

        Returns:
            GetSystemPromptUseCase instance.
        """
        if self._get_system_prompt_use_case is None:
            self._get_system_prompt_use_case = GetSystemPromptUseCase(
                prompt_config=self.get_prompt_config(),
            )
        return self._get_system_prompt_use_case

    def get_send_message_use_case(self) -> SendMessageUseCase:
        """Get send message use case, creating if needed.

        Returns:
            SendMessageUseCase instance.
        """
        if self._send_message_use_case is None:
            self._send_message_use_case = SendMessageUseCase(
                message_repository=self.get_message_repository(),
                provider=self.get_provider(),
                load_history_use_case=self.get_load_history_use_case(),
                get_system_prompt_use_case=self.get_system_prompt_use_case(),
            )
        return self._send_message_use_case
