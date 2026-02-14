"""User repository interface definition.

This module defines the abstract interface for user data access operations
following the Repository pattern.
"""

from abc import ABC, abstractmethod

from src.domain.models.user import User


class IUserRepository(ABC):
    """Interface for user data access operations."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user to the repository.

        Args:
            user: The user entity to save.

        Returns:
            The saved user with assigned ID.
        """

    @abstractmethod
    async def find_by_id(self, user_id: int) -> User | None:
        """Find a user by ID.

        Args:
            user_id: The user ID to search for.

        Returns:
            The user if found, None otherwise.
        """

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        """Find a user by username (case-insensitive).

        Args:
            username: The username to search for.

        Returns:
            The user if found, None otherwise.
        """

    @abstractmethod
    async def get_or_create(self, username: str) -> User:
        """Get an existing user or create a new one.

        Args:
            username: The username to get or create.

        Returns:
            The existing or newly created user.
        """

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID.

        Args:
            user_id: The user ID to delete.

        Returns:
            True if deleted, False if not found.
        """
