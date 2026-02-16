"""Application bootstrap utilities."""

import asyncio
from logging import getLogger

import aiosqlite

from src.config.app import AppConfig, get_config
from src.infrastructure.container import Container
from src.infrastructure.database.migrator import AsyncDatabaseMigrator
from src.infrastructure.logging import configure_logging

logger = getLogger(__name__)

_container: Container | None = None  # pylint: disable=invalid-name


async def _init_database_connection(config: AppConfig) -> aiosqlite.Connection:
    """Initialize database connection with migrations.

    Args:
        config: Application configuration.

    Returns:
        Initialized aiosqlite connection.
    """
    connection = await aiosqlite.connect(config.database_path)
    connection.row_factory = aiosqlite.Row

    migrator = AsyncDatabaseMigrator(connection)
    await migrator.migrate()

    logger.info("Database connection initialized and migrated")
    return connection


async def build_container(*, config: AppConfig | None = None) -> Container:
    """Build a new application container.

    Args:
        config: Optional configuration override.

    Returns:
        Configured container instance.
    """
    configure_logging()
    resolved_config = config or get_config()

    connection = await _init_database_connection(resolved_config)

    container = Container(config=resolved_config)
    container.set_database_connection(connection)

    logger.info("Container initialized")
    return container


def get_container(*, config: AppConfig | None = None) -> Container:  # pylint: disable=global-statement
    """Get a shared container instance (sync wrapper).

    Args:
        config: Optional configuration override.

    Returns:
        Shared container instance.
    """
    global _container  # pylint: disable=global-statement
    if _container is None:
        _container = asyncio.run(build_container(config=config))
    return _container


async def get_container_async(*, config: AppConfig | None = None) -> Container:
    """Get a shared container instance (async).

    Args:
        config: Optional configuration override.

    Returns:
        Shared container instance.
    """
    global _container  # pylint: disable=global-statement
    if _container is None:
        _container = await build_container(config=config)
    return _container


def reset_container() -> None:
    """Reset the shared container instance."""
    global _container  # pylint: disable=global-statement
    _container = None
