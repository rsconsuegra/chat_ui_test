"""SQLite implementation of user repository.

This module provides a concrete implementation of the user repository
interface using SQLite as the storage backend.
"""

from datetime import datetime

from src.domain.models.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.repositories.sqlite_base_repository import SQLiteRepositoryBase


class SQLiteUserRepository(SQLiteRepositoryBase, IUserRepository):
    """SQLite implementation of IUserRepository."""

    async def save(self, user: User) -> User:
        """Save a user to the database.

        Args:
            user: The user to save.

        Returns:
            The saved user with generated ID.
        """
        user_id = self._insert_returning_id(
            """
            INSERT INTO users (username, created_at, updated_at)
            VALUES (?, ?, ?)
            """,
            (user.username.lower(), user.created_at, user.updated_at),
            integrity_error_message=f"User already exists: {user.username}",
        )

        return User(
            id=user_id,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def find_by_id(self, user_id: int) -> User | None:
        """Find a user by ID.

        Args:
            user_id: The user ID to search for.

        Returns:
            The user if found, None otherwise.
        """
        row = self._fetchone(
            "SELECT id, username, created_at, updated_at FROM users WHERE id = ?",
            (user_id,),
        )
        return None if row is None else self._row_to_user(row)

    async def find_by_username(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to search for (case-insensitive).

        Returns:
            The user if found, None otherwise.
        """
        row = self._fetchone(
            "SELECT id, username, created_at, updated_at FROM users WHERE username = ?",
            (username.lower(),),
        )
        return None if row is None else self._row_to_user(row)

    async def exists(self, username: str) -> bool:
        """Check if a user exists.

        Args:
            username: The username to check.

        Returns:
            True if user exists, False otherwise.
        """
        row = self._fetchone(
            "SELECT COUNT(*) FROM users WHERE username = ?",
            (username.lower(),),
        )
        return bool(row and row[0] > 0)

    async def get_or_create(self, username: str) -> User:
        """Get existing user or create new one.

        Args:
            username: The username to get or create.

        Returns:
            The existing or newly created user.
        """
        existing = await self.find_by_username(username)
        if existing:
            return existing
        return await self.save(User.create_new(username=username))

    async def delete(self, user_id: int) -> bool:
        """Delete a user.

        Args:
            user_id: The user ID to delete.

        Returns:
            True if user was deleted, False if not found.
        """
        cur = self._execute("DELETE FROM users WHERE id = ?", (user_id,), commit=True)
        return cur.rowcount > 0

    @staticmethod
    def _row_to_user(row: tuple) -> User:
        """Convert a database row tuple to a User domain object.

        Args:
            row: Database row tuple with columns (id, username, created_at,
                updated_at).

        Returns:
            User domain object.
        """
        return User(
            id=row[0],
            username=row[1],
            created_at=datetime.fromisoformat(row[2]),
            updated_at=datetime.fromisoformat(row[3]),
        )
