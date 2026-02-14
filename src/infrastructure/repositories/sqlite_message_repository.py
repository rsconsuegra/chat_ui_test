"""SQLite implementation of message repository.

This module provides a concrete implementation of the message repository
interface using SQLite as the storage backend.
"""

from datetime import datetime

from src.domain.models.chat_message import ChatMessage
from src.domain.models.message_role import MessageRole
from src.domain.repositories.message_repository import IMessageRepository
from src.infrastructure.repositories.sqlite_base_repository import SQLiteRepositoryBase


class SQLiteMessageRepository(SQLiteRepositoryBase, IMessageRepository):
    """SQLite implementation of IMessageRepository."""

    async def save(self, message: ChatMessage) -> ChatMessage:
        """Save a chat message to the database.

        Args:
            message: The chat message to save.

        Returns:
            The saved message with generated ID.
        """
        message_id = self._insert_returning_id(
            """
            INSERT INTO chat_messages (user_id, provider, role, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                message.user_id,
                message.provider,
                message.role.value,
                message.content,
                str(message.timestamp),
            ),
        )

        return ChatMessage(
            id=message_id,
            user_id=message.user_id,
            provider=message.provider,
            role=message.role,
            content=message.content,
            timestamp=message.timestamp,
        )

    async def find_by_id(self, message_id: int) -> ChatMessage | None:
        """Find a chat message by its ID.

        Args:
            message_id: The message ID to search for.

        Returns:
            The message if found, None otherwise.
        """
        row = self._fetchone(
            """
            SELECT id, user_id, provider, role, content, timestamp
            FROM chat_messages WHERE id = ?
            """,
            (message_id,),
        )
        return None if row is None else self._row_to_message(row)

    async def find_by_user_id(
        self,
        user_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ChatMessage]:
        """Find all messages for a user.

        Args:
            user_id: The user ID to search for.
            limit: Maximum number of messages to return.
            offset: Number of messages to skip.

        Returns:
            List of messages for the user, ordered by timestamp descending.
        """
        rows = self._fetchall(
            """
            SELECT id, user_id, provider, role, content, timestamp
            FROM chat_messages
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset),
        )
        return [self._row_to_message(r) for r in rows]

    async def delete_by_user_id(self, user_id: int) -> int:
        """Delete all messages for a user.

        Args:
            user_id: The user ID to delete messages for.

        Returns:
            Number of messages deleted.
        """
        cur = self._execute(
            "DELETE FROM chat_messages WHERE user_id = ?",
            (user_id,),
            commit=True,
        )
        return cur.rowcount

    async def count_by_user_id(self, user_id: int) -> int:
        """Count messages for a user.

        Args:
            user_id: The user ID to count messages for.

        Returns:
            Number of messages for the user.
        """
        row = self._fetchone(
            "SELECT COUNT(*) FROM chat_messages WHERE user_id = ?",
            (user_id,),
        )
        return int(row[0]) if row else 0

    @staticmethod
    def _row_to_message(row: tuple) -> ChatMessage:
        """Convert a database row tuple to a ChatMessage domain object.

        Args:
            row: Database row tuple with columns (id, user_id, provider,
                role, content, timestamp).

        Returns:
            ChatMessage domain object.
        """
        return ChatMessage(
            id=row[0],
            user_id=row[1],
            provider=row[2],
            role=MessageRole(row[3]),
            content=row[4],
            timestamp=datetime.fromisoformat(row[5]),
        )
