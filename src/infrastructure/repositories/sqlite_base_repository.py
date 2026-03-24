"""Shared helpers for SQLite repositories using aiosqlite."""

from collections.abc import Sequence
from typing import Any

import aiosqlite

from src.domain.errors.exceptions import RepositoryError, StorageError


class SQLiteRepositoryBase:
    """Base class to centralize async sqlite execution + error mapping."""

    def __init__(self, connection: aiosqlite.Connection) -> None:
        """Initialize SQLite repository base.

        Args:
            connection: aiosqlite database connection.
        """
        self._connection = connection

    async def _execute(
        self,
        sql: str,
        params: Sequence[Any] = (),
        *,
        commit: bool = False,
    ) -> aiosqlite.Cursor:
        """Execute a SQL statement.

        Args:
            sql: SQL statement to execute.
            params: Parameters for the SQL statement.
            commit: Whether to commit the transaction after execution.

        Returns:
            SQLite cursor after execution.

        Raises:
            StorageError: If the SQLite operation fails.
        """
        try:
            cursor = await self._connection.execute(sql, params)
            if commit:
                await self._connection.commit()
            return cursor
        except aiosqlite.Error as e:
            raise StorageError(f"SQLite operation failed: {e}") from e

    async def _fetchone(self, sql: str, params: Sequence[Any] = ()) -> Any | None:
        """Execute a SQL query and fetch a single row.

        Args:
            sql: SQL query to execute.
            params: Parameters for the SQL query.

        Returns:
            A single row tuple if found, None otherwise.
        """
        cursor = await self._execute(sql, params, commit=False)
        return await cursor.fetchone()

    async def _fetchall(self, sql: str, params: Sequence[Any] = ()) -> list[Any]:
        """Execute a SQL query and fetch all rows.

        Args:
            sql: SQL query to execute.
            params: Parameters for the SQL query.

        Returns:
            List of row tuples.
        """
        cursor = await self._execute(sql, params, commit=False)
        return list(await cursor.fetchall())

    async def _insert_returning_id(
        self,
        sql: str,
        params: Sequence[Any],
        *,
        integrity_error_message: str | None = None,
    ) -> int:
        """Execute an INSERT statement and return the generated ID.

        Args:
            sql: INSERT SQL statement to execute.
            params: Parameters for the SQL statement.
            integrity_error_message: Custom message for integrity errors.

        Returns:
            The generated row ID.

        Raises:
            RepositoryError: If an integrity constraint is violated and
                integrity_error_message is provided.
            StorageError: If the insert operation fails or no ID is returned.
        """
        try:
            cursor = await self._connection.execute(sql, params)
            await self._connection.commit()

            lastrowid = cursor.lastrowid
            if lastrowid is None:
                raise StorageError("Failed to get lastrowid after insert")
            return int(lastrowid)

        except aiosqlite.IntegrityError as e:
            if integrity_error_message:
                raise RepositoryError(integrity_error_message) from e
            raise StorageError(f"SQLite integrity error: {e}") from e

        except aiosqlite.Error as e:
            raise StorageError(f"SQLite insert failed: {e}") from e
