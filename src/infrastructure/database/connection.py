"""Database connection management using aiosqlite.

This module provides async database connection handling and initialization
for the application.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from typing import Any

import aiosqlite

from src.config.app import AppConfig, get_config
from src.domain.errors.exceptions import StorageError
from src.infrastructure.database.migrator import AsyncDatabaseMigrator

logger = getLogger(__name__)

_GLOBAL_CONFIG: AppConfig | None = None
_GLOBAL_CONNECTION: aiosqlite.Connection | None = None
_CONNECTION_LOCK = asyncio.Lock()


async def init_database(config: AppConfig | None = None) -> aiosqlite.Connection:
    """Initialize the database schema (async).

    Args:
        config: Optional application configuration override.

    Returns:
        The initialized database connection.

    Raises:
        StorageError: If database connection or migrations fail.
    """
    global _GLOBAL_CONFIG, _GLOBAL_CONNECTION  # pylint: disable=global-statement

    async with _CONNECTION_LOCK:
        if _GLOBAL_CONFIG is None:
            _GLOBAL_CONFIG = config or get_config()
        if _GLOBAL_CONFIG is None:
            logger.error("Database configuration not initialized")
            raise StorageError("Database configuration not initialized")

        if _GLOBAL_CONNECTION is None:
            try:
                _GLOBAL_CONNECTION = await aiosqlite.connect(
                    _GLOBAL_CONFIG.database_path,
                )
                _GLOBAL_CONNECTION.row_factory = aiosqlite.Row

                migrator = AsyncDatabaseMigrator(_GLOBAL_CONNECTION, Path("migrations"))
                await migrator.migrate()
                logger.info("Database migrations completed")
            except aiosqlite.Error as exc:
                logger.exception("Database initialization failed")
                raise StorageError(f"Database initialization failed: {exc}") from exc

    if _GLOBAL_CONNECTION is None:
        raise StorageError("Database connection not initialized after init")
    return _GLOBAL_CONNECTION


async def get_connection(config: AppConfig | None = None) -> aiosqlite.Connection:
    """Get global database connection (async).

    Args:
        config: Optional application configuration override.

    Returns:
        aiosqlite connection object.
    """
    if _GLOBAL_CONNECTION is None:
        return await init_database(config)
    return _GLOBAL_CONNECTION


async def close_connection() -> None:
    """Close the global database connection."""
    global _GLOBAL_CONNECTION  # pylint: disable=global-statement
    async with _CONNECTION_LOCK:
        if _GLOBAL_CONNECTION is not None:
            await _GLOBAL_CONNECTION.close()
            _GLOBAL_CONNECTION = None


class DatabaseConnection:
    """Manages SQLite database connections using aiosqlite."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize database connection manager.

        Args:
            config: Database configuration.
        """
        self.config = config
        self._connection: aiosqlite.Connection | None = None
        self._lock = asyncio.Lock()

    @property
    def connection(self) -> aiosqlite.Connection:
        """Access the underlying aiosqlite connection.

        Returns:
            aiosqlite connection object.

        Raises:
            StorageError: If connection is not initialized.
        """
        if self._connection is None:
            raise StorageError("Database connection not initialized. Call init() first.")
        return self._connection

    async def init(self) -> None:
        """Initialize the database connection and run migrations.

        Raises:
            StorageError: If database initialization fails.
        """
        async with self._lock:
            if self._connection is None:
                try:
                    self._connection = await aiosqlite.connect(
                        self.config.database_path,
                    )
                    self._connection.row_factory = aiosqlite.Row

                    migrator = AsyncDatabaseMigrator(
                        self._connection,
                        Path("migrations"),
                    )
                    await migrator.migrate()
                    logger.info("Database connection initialized and migrated")
                except aiosqlite.Error as exc:
                    logger.exception("Failed to initialize database connection")
                    raise StorageError(f"Failed to initialize database connection: {exc}") from exc

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        """Get a database connection (async context manager).

        Yields:
            aiosqlite connection object.

        Raises:
            StorageError: If connection fails.
        """
        if self._connection is None:
            await self.init()
        if self._connection is None:
            raise StorageError("Database connection not initialized after init")
        try:
            yield self._connection
        except aiosqlite.Error as exc:
            logger.exception("Database connection error")
            raise StorageError(f"Database connection error: {exc}") from exc

    async def close(self) -> None:
        """Close the database connection."""
        async with self._lock:
            if self._connection is not None:
                await self._connection.close()
                self._connection = None

    async def execute(
        self,
        query: str,
        params: tuple[Any, ...] = (),
        commit: bool = False,
    ) -> aiosqlite.Cursor:
        """Execute a SQL query.

        Args:
            query: SQL query string.
            params: Query parameters.
            commit: Whether to commit after execution.

        Returns:
            Cursor object.

        Raises:
            StorageError: If query execution fails.
        """
        try:
            cursor = await self.connection.execute(query, params)
            if commit:
                await self.connection.commit()
            return cursor
        except aiosqlite.Error as exc:
            logger.exception("Query execution failed")
            raise StorageError(f"Query execution failed: {exc}") from exc

    async def fetch_all(
        self,
        query: str,
        params: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        """Fetch all rows from a query.

        Args:
            query: SQL query string.
            params: Query parameters.

        Returns:
            List of row dictionaries.
        """
        cursor = await self.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def fetch_one(
        self,
        query: str,
        params: tuple[Any, ...] = (),
    ) -> dict[str, Any] | None:
        """Fetch one row from a query.

        Args:
            query: SQL query string.
            params: Query parameters.

        Returns:
            Row dictionary or None if not found.
        """
        cursor = await self.execute(query, params)
        row = await cursor.fetchone()
        return dict(row) if row else None
