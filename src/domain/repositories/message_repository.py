"""Message repository interface definition.

This module defines the abstract interface for message data access operations
following the Repository pattern.
"""

from abc import ABC, abstractmethod

from src.domain.models.chat_message import ChatMessage


class IMessageRepository(ABC):
    """Interface for message data access operations."""

    @abstractmethod
    async def save(self, message: ChatMessage) -> ChatMessage:
        """Save a message to the repository.

        Args:
            message: The message entity to save.

        Returns:
            The saved message with assigned ID.
        """

    @abstractmethod
    async def find_by_id(self, message_id: int) -> ChatMessage | None:
        """Find a message by ID.

        Args:
            message_id: The message ID to search for.

        Returns:
            The message if found, None otherwise.
        """

    @abstractmethod
    async def find_by_user_id(self, user_id: int, limit: int = 100, offset: int = 0) -> list[ChatMessage]:
        """Find all messages for a user.

        Args:
            user_id: The user ID to search for.
            limit: Maximum number of messages to return.
            offset: Number of messages to skip.

        Returns:
            List of messages for the user, ordered by timestamp descending.
        """

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> int:
        """Delete all messages for a user.

        Args:
            user_id: The user ID to delete messages for.

        Returns:
            Number of messages deleted.
        """
