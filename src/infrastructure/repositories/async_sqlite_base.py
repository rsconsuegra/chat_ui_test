"""Async base class for repositories using thread pool executor."""

# pylint: disable=duplicate-code
# TECH-DEBT-001: Duplicate error handling code with sqlite_base_repository.py

import asyncio
import sqlite3
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from src.domain.errors.exceptions import RepositoryError, StorageError


class AsyncSQLiteRepositoryBase:
    """Base class for async SQLite repositories using thread pool."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Initialize the repository.

        Args:
            connection: SQLite connection to use.
        """
        self._connection = connection
        self._executor = ThreadPoolExecutor(max_workers=1)

    async def _execute_sync(
        self,
        operation: Callable[..., Any],
        *args: Any,
    ) -> Any:
        """Execute a synchronous operation in thread pool.

        Args:
            operation: Synchronous function to execute.
            *args: Arguments to pass to the operation.

        Returns:
            Result of the operation.

        Raises:
            StorageError: If database operation fails.
        """
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(self._executor, lambda: operation(*args))
        except sqlite3.Error as e:
            raise StorageError(f"Database operation failed: {e}") from e

    async def _execute_query(
        self,
        sql: str,
        params: tuple[Any, ...] = (),
        *,
        commit: bool = False,
    ) -> sqlite3.Cursor:
        """Execute a SQL query asynchronously.

        Args:
            sql: SQL query string.
            params: Query parameters.
            commit: Whether to commit after execution.

        Returns:
            Cursor object.
        """

        def _exec() -> sqlite3.Cursor:
            cursor = self._connection.execute(sql, params)
            if commit:
                self._connection.commit()
            return cursor

        return await self._execute_sync(_exec)

    async def _fetchone(self, sql: str, params: tuple[Any, ...] = ()) -> Any | None:
        """Fetch one row asynchronously.

        Args:
            sql: SQL query string.
            params: Query parameters.

        Returns:
            Row tuple or None.
        """

        def _fetch() -> Any | None:
            cursor = self._connection.execute(sql, params)
            return cursor.fetchone()

        return await self._execute_sync(_fetch)

    async def _fetchall(self, sql: str, params: tuple[Any, ...] = ()) -> list[Any]:
        """Fetch all rows asynchronously.

        Args:
            sql: SQL query string.
            params: Query parameters.

        Returns:
            List of row tuples.
        """

        def _fetch() -> list[Any]:
            cursor = self._connection.execute(sql, params)
            return cursor.fetchall()

        return await self._execute_sync(_fetch)

    async def _insert_returning_id(
        self,
        sql: str,
        params: tuple[Any, ...],
        *,
        integrity_error_message: str | None = None,
    ) -> int:
        """Insert and return the new ID asynchronously.

        Args:
            sql: INSERT SQL statement.
            params: Parameters for the insert.
            integrity_error_message: Custom message for integrity errors.

        Returns:
            The ID of the newly inserted row.
        """

        def _insert() -> int:
            try:
                cursor = self._connection.execute(sql, params)
                self._connection.commit()

                new_id = cursor.lastrowid
                if new_id is None:
                    raise StorageError("Failed to get lastrowid after insert")
                return int(new_id)
            except sqlite3.IntegrityError as e:
                if integrity_error_message:
                    raise RepositoryError(integrity_error_message) from e
                raise StorageError(f"SQLite integrity error: {e}") from e
            except sqlite3.Error as e:
                raise StorageError(f"SQLite insert failed: {e}") from e

        return await self._execute_sync(_insert)
