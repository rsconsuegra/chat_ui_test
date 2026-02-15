"""Chainlit session adapter implementation."""

from typing import Any

import chainlit as cl

from src.domain.errors.exceptions import RepositoryError
from src.domain.interfaces.frontend_adapter import (
    ISessionAdapter,
)
from src.domain.models.user import User
from src.domain.repositories.user_repository import IUserRepository


class ChainlitSessionAdapter(ISessionAdapter):
    """Chainlit-specific session management implementation.

    This adapter wraps Chainlit's session and user management APIs
    to provide a frontend-agnostic interface.
    """

    def __init__(self, *, user_repository: IUserRepository) -> None:
        """Initialize the adapter.

        Args:
            user_repository: Repository for user operations.
        """
        self._user_repository = user_repository

    async def get_or_prompt_username(
        self,
        prompt: str,
        timeout: int = 300,
    ) -> str | None:
        """Prompt user for username using Chainlit's AskUserMessage.

        Args:
            prompt: Message to display when prompting.
            timeout: Seconds to wait for response.

        Returns:
            Username string or None if timeout/cancelled.
        """
        response = await cl.AskUserMessage(
            content=prompt,
            timeout=timeout,
        ).send()

        if not response:
            return None

        username = response.get("content", "").strip()
        return username if username else None

    async def get_session_data(self, key: str) -> Any:
        """Retrieve data from Chainlit user session.

        Args:
            key: Session key to retrieve.

        Returns:
            Session value or None if not found.
        """
        return cl.user_session.get(key)

    async def set_session_data(self, key: str, value: Any) -> None:
        """Store data in Chainlit user session.

        Args:
            key: Session key to set.
            value: Value to store.
        """
        cl.user_session.set(key, value)

    async def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one.

        Args:
            username: Username to look up or create.

        Returns:
            User domain object.

        Raises:
            RepositoryError: If database operation fails.
        """
        try:
            user = await self._user_repository.get_or_create(username)
            return user
        except Exception as exc:
            raise RepositoryError(f"Failed to get or create user: {exc}") from exc
