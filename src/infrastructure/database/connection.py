"""Database connection management.

This module provides database connection handling and initialization for the application.
It manages SQLite connections with async context manager support.
"""

import asyncio
import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from typing import Any, cast

from src.config.app import AppConfig, get_config
from src.domain.errors.exceptions import StorageError
from src.infrastructure.database.migrator import DatabaseMigrator

logger = getLogger(__name__)

# Global configuration for simple Phase 0 usage
_GLOBAL_CONFIG: AppConfig | None = None
_GLOBAL_CONNECTION: sqlite3.Connection | None = None


def init_database(config: AppConfig | None = None) -> None:
    """Initialize the database schema (synchronous for Phase 0).

    Args:
        config: Optional application configuration override.

    Raises:
        StorageError: If database connection or migrations fail.
    """
    global _GLOBAL_CONFIG, _GLOBAL_CONNECTION  # pylint: disable=global-statement

    if _GLOBAL_CONFIG is None:
        _GLOBAL_CONFIG = config or get_config()
    if _GLOBAL_CONFIG is None:
        logger.error("Database configuration not initialized")
        raise StorageError("Database configuration not initialized")
    current_config = cast(AppConfig, _GLOBAL_CONFIG)

    if _GLOBAL_CONNECTION is None:
        _GLOBAL_CONNECTION = sqlite3.connect(current_config.database_path, check_same_thread=False)
        _GLOBAL_CONNECTION.row_factory = sqlite3.Row

    try:
        migrator = DatabaseMigrator(_GLOBAL_CONNECTION, Path("migrations"))
        migrator.migrate()
        logger.info("Database migrations completed")
    except sqlite3.ProgrammingError as exc:
        if "Cannot operate on a closed database" in str(exc):
            logger.warning("Database connection closed; reconnecting")
            _GLOBAL_CONNECTION = sqlite3.connect(current_config.database_path, check_same_thread=False)
            _GLOBAL_CONNECTION.row_factory = sqlite3.Row
            migrator = DatabaseMigrator(_GLOBAL_CONNECTION, Path("migrations"))
            migrator.migrate()
            logger.info("Database migrations completed after reconnect")
        else:
            logger.exception("Database initialization failed")
            raise StorageError(f"Database initialization failed: {exc}") from exc
    except sqlite3.Error as exc:
        logger.exception("Database initialization failed")
        raise StorageError(f"Database initialization failed: {exc}") from exc


def get_connection(config: AppConfig | None = None) -> sqlite3.Connection:
    """Get global database connection (synchronous for Phase 0).

    Args:
        config: Optional application configuration override.

    Returns:
        SQLite connection object.

    Raises:
        StorageError: If database not initialized.
    """
    if _GLOBAL_CONNECTION is None:
        init_database(config)

    if _GLOBAL_CONNECTION is None:
        logger.error("Database connection not initialized")
        raise StorageError("Database connection not initialized")

    return _GLOBAL_CONNECTION


class DatabaseConnection:
    """Manages SQLite database connections (async for future phases)."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize database connection manager.

        Args:
            config: Database configuration.
        """
        self.config = config
        self._connection: sqlite3.Connection | None = None
        self._lock: asyncio.Lock = asyncio.Lock()

    @property
    def connection(self) -> sqlite3.Connection:
        """Access the underlying SQLite connection directly.

        Synchronous method for Phase 0 that returns the connection
        without context manager overhead.

        Returns:
            SQLite connection object.

        Raises:
            StorageError: If connection fails.
        """
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(self.config.database_path, check_same_thread=False)
                self._connection.row_factory = sqlite3.Row
            except sqlite3.Error as exc:
                logger.exception("Failed to get database connection")
                raise StorageError(f"Failed to get database connection: {exc}") from exc

        return self._connection

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[sqlite3.Connection]:
        """Get a database connection (async context manager for future phases).

        Yields:
            SQLite connection object.

        Raises:
            StorageError: If connection fails.
        """
        try:
            yield self.connection
        except sqlite3.Error as exc:
            logger.exception("Failed to get database connection")
            raise StorageError(f"Failed to get database connection: {exc}") from exc

    async def close(self) -> None:
        """Close the database connection."""
        async with self._lock:
            if self._connection is not None:
                self._connection.close()
                self._connection = None

    async def execute(self, query: str, params: tuple[Any, ...] = (), commit: bool = False) -> sqlite3.Cursor:
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
            async with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                if commit:
                    conn.commit()

                return cursor
        except sqlite3.Error as exc:
            logger.exception("Query execution failed")
            raise StorageError(f"Query execution failed: {exc}") from exc

    async def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        """Fetch all rows from a query.

        Args:
            query: SQL query string.
            params: Query parameters.

        Returns:
            List of row dictionaries.
        """
        cursor = await self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    async def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        """Fetch one row from a query.

        Args:
            query: SQL query string.
            params: Query parameters.

        Returns:
            Row dictionary or None if not found.
        """
        rows = await self.fetch_all(query, params)
        return rows[0] if rows else None
