"""Shared helpers for SQLite repositories (infrastructure layer)."""

import sqlite3
from collections.abc import Sequence
from typing import Any

from src.domain.errors.exceptions import RepositoryError, StorageError


class SQLiteRepositoryBase:  # pylint: disable=too-few-public-methods
    """Base class to centralize sqlite execution + error mapping."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Initialize SQLite repository base.

        Args:
            connection: SQLite database connection.
        """
        self._connection = connection

    def _execute(
        self,
        sql: str,
        params: Sequence[Any] = (),
        *,
        commit: bool = False,
    ) -> sqlite3.Cursor:
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
            cur = self._connection.execute(sql, params)
            if commit:
                self._connection.commit()
            return cur
        except sqlite3.Error as e:
            raise StorageError(f"SQLite operation failed: {e}") from e

    def _fetchone(self, sql: str, params: Sequence[Any] = ()) -> Any | None:
        """Execute a SQL query and fetch a single row.

        Args:
            sql: SQL query to execute.
            params: Parameters for the SQL query.

        Returns:
            A single row tuple if found, None otherwise.
        """
        cur = self._execute(sql, params, commit=False)
        return cur.fetchone()

    def _fetchall(self, sql: str, params: Sequence[Any] = ()) -> list[Any]:
        """Execute a SQL query and fetch all rows.

        Args:
            sql: SQL query to execute.
            params: Parameters for the SQL query.

        Returns:
            List of row tuples.
        """
        cur = self._execute(sql, params, commit=False)
        return cur.fetchall()

    def _insert_returning_id(
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
            cur = self._connection.execute(sql, params)
            self._connection.commit()

            new_id = cur.lastrowid
            if new_id is None:
                raise StorageError("Failed to get lastrowid after insert")
            return int(new_id)

        except sqlite3.IntegrityError as e:
            if integrity_error_message:
                raise RepositoryError(integrity_error_message) from e
            raise StorageError(f"SQLite integrity error: {e}") from e

        except sqlite3.Error as e:
            raise StorageError(f"SQLite insert failed: {e}") from e
