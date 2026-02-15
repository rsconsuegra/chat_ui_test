"""Frontend adapter interfaces for UI-agnostic operations.

These interfaces abstract frontend-specific operations (session management,
message display, streaming) to decouple the application from any particular
frontend framework (Chainlit, Streamlit, etc.).
"""

# pylint: disable=unnecessary-ellipsis

from abc import ABC, abstractmethod
from typing import Any, Protocol

from src.domain.models.user import User


class FrontendError(Exception):
    """Base exception for frontend adapter errors."""


class UsernamePromptTimeoutError(FrontendError):
    """Raised when username prompt times out."""


class SessionDataNotFoundError(FrontendError):
    """Raised when required session data is not found."""


class IStreamingMessage(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for streaming message output.

    This protocol defines the interface for incremental message output,
    allowing tokens to be streamed to the UI as they are generated.
    """

    async def stream_token(self, token: str) -> None:
        """Append a token to the streaming message.

        Args:
            token: Text chunk to append.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    async def send(self) -> None:
        """Finalize and send the message."""
        ...  # pylint: disable=unnecessary-ellipsis


class ISessionAdapter(ABC):
    """Abstract session management for frontend-agnostic operations.

    This interface handles user session concerns including username
    prompting, session data storage, and user creation/retrieval.
    """

    @abstractmethod
    async def get_or_prompt_username(
        self,
        prompt: str,
        timeout: int = 300,
    ) -> str | None:
        """Get existing username or prompt user for input.

        Args:
            prompt: Message to display when prompting.
            timeout: Seconds to wait for response.

        Returns:
            Username string or None if timeout/cancelled.
        """
        ...

    @abstractmethod
    async def get_session_data(self, key: str) -> Any:
        """Retrieve data from session.

        Args:
            key: Session key to retrieve.

        Returns:
            Session value or None if not found.
        """
        ...

    @abstractmethod
    async def set_session_data(self, key: str, value: Any) -> None:
        """Store data in session.

        Args:
            key: Session key to set.
            value: Value to store.
        """
        ...

    @abstractmethod
    async def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one.

        Args:
            username: Username to look up or create.

        Returns:
            User domain object.

        Raises:
            RepositoryError: If database operation fails.
        """
        ...


class IMessageAdapter(ABC):
    """Abstract message handling for frontend-agnostic operations.

    This interface handles message display concerns including
    complete messages and streaming output.
    """

    @abstractmethod
    async def send_message(self, content: str) -> None:
        """Send a complete message to the user.

        Args:
            content: Message content to display.
        """
        ...

    @abstractmethod
    def create_streaming_message(self) -> IStreamingMessage:
        """Create a new streaming message for incremental output.

        Returns:
            Streaming message object.
        """
        ...
