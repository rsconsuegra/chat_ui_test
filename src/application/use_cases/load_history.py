"""Use case for loading chat history for provider context."""

# pylint: disable=too-few-public-methods

from src.domain.interfaces.provider import ProviderMessage
from src.domain.repositories.message_repository import IMessageRepository


class LoadHistoryUseCase:
    """Load chat history and format for provider context."""

    def __init__(self, *, message_repository: IMessageRepository) -> None:
        """Initialize the use case.

        Args:
            message_repository: Repository for chat messages.
        """
        self._message_repository = message_repository

    async def execute(
        self,
        *,
        user_id: int,
        limit: int = 50,
    ) -> list[ProviderMessage]:
        """Load chat history for a user.

        Args:
            user_id: The ID of the user whose history to load.
            limit: Maximum number of messages to retrieve.

        Returns:
            List of ProviderMessages ready for provider context,
            ordered oldest to newest.
        """
        history = await self._message_repository.find_by_user_id(
            user_id,
            limit=limit,
            offset=0,
        )

        provider_messages = []
        for message in reversed(history):
            provider_messages.append(ProviderMessage(role=message.role, content=message.content))

        return provider_messages
