"""In-memory repository implementations for testing."""

from dataclasses import dataclass, field

from src.domain.errors.exceptions import RepositoryError
from src.domain.models.chat_message import ChatMessage
from src.domain.models.user import User
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository


@dataclass
class InMemoryUserRepository(IUserRepository):
    """In-memory implementation of user repository for testing."""

    _users: dict[int, User] = field(default_factory=dict)
    _next_id: int = field(default=1)

    async def save(self, user: User) -> User:
        """Save a user.

        Args:
            user: User entity to save.

        Returns:
            Saved user with assigned ID.

        Raises:
            RepositoryError: If username already exists.
        """
        normalized_username = user.username.lower()
        for existing_user in self._users.values():
            if existing_user.username.lower() == normalized_username:
                raise RepositoryError(f"User with username '{user.username}' already exists")

        user_with_id = user
        if user.id is None or user.id == 0:
            user_with_id = User(
                id=self._next_id,
                username=user.username,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self._next_id += 1

        self._users[user_with_id.id] = user_with_id
        return user_with_id

    async def create(self, user: User) -> User:
        """Create a new user.

        Args:
            user: User entity to create.

        Returns:
            Created user with assigned ID.
        """
        return await self.save(user)

    async def find_by_id(self, user_id: int) -> User | None:
        """Find a user by ID.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            User entity if found, None otherwise.
        """
        return self._users.get(user_id)

    async def find_by_username(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to search for.

        Returns:
            User entity if found, None otherwise.
        """
        normalized_username = username.lower()
        for user in self._users.values():
            if user.username.lower() == normalized_username:
                return user
        return None

    async def get_or_create(self, username: str) -> User:
        """Get existing user or create a new one.

        Args:
            username: The username to get or create.

        Returns:
            The existing or newly created user.
        """
        existing = await self.find_by_username(username)
        if existing is not None:
            return existing
        return await self.save(User.create_new(username=username))

    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID.

        Args:
            user_id: The user ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    async def exists(self, user_id: int) -> bool:
        """Check if a user exists.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            True if user exists, False otherwise.
        """
        return user_id in self._users

    def clear(self) -> None:
        """Clear all users (for testing)."""
        self._users.clear()
        self._next_id = 1


@dataclass
class InMemoryMessageRepository(IMessageRepository):
    """In-memory implementation of message repository for testing."""

    _messages: dict[int, ChatMessage] = field(default_factory=dict)
    _next_id: int = field(default=1)

    async def save(self, message: ChatMessage) -> ChatMessage:
        """Save a chat message.

        Args:
            message: Chat message entity to save.

        Returns:
            Saved message with assigned ID.
        """
        # Assign ID if not set
        message_with_id = message
        if message.id is None or message.id == 0:
            message_with_id = ChatMessage(
                id=self._next_id,
                user_id=message.user_id,
                provider=message.provider,
                role=message.role,
                content=message.content,
                timestamp=message.timestamp,
            )
            self._next_id += 1

        self._messages[message_with_id.id] = message_with_id
        return message_with_id

    async def find_by_id(self, message_id: int) -> ChatMessage | None:
        """Find a message by ID.

        Args:
            message_id: Unique identifier for the message.

        Returns:
            Chat message entity if found, None otherwise.
        """
        return self._messages.get(message_id)

    async def find_by_user_id(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list[ChatMessage]:
        """Find messages by user ID.

        Args:
            user_id: Unique identifier for the user.
            limit: Maximum number of messages to return.
            offset: Number of messages to skip.

        Returns:
            List of chat messages ordered by creation time (descending).
        """
        user_messages = [msg for msg in self._messages.values() if msg.user_id == user_id]

        # Sort by timestamp descending
        sorted_messages = sorted(
            user_messages,
            key=lambda m: m.timestamp,
            reverse=True,
        )

        # Apply pagination
        return sorted_messages[offset : offset + limit]

    async def find_by_user_and_provider(
        self,
        user_id: int,
        provider: str,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[ChatMessage]:
        """Find messages by user ID and provider.

        Args:
            user_id: Unique identifier for the user.
            provider: Provider identifier.
            limit: Maximum number of messages to return.
            offset: Number of messages to skip.

        Returns:
            List of chat messages ordered by creation time (descending).
        """
        filtered_messages = [msg for msg in self._messages.values() if msg.user_id == user_id and msg.provider == provider]

        # Sort by timestamp descending
        sorted_messages = sorted(
            filtered_messages,
            key=lambda m: m.timestamp,
            reverse=True,
        )

        # Apply pagination
        return sorted_messages[offset : offset + limit]

    async def delete_by_id(self, message_id: int) -> bool:
        """Delete a message by ID.

        Args:
            message_id: Unique identifier for the message.

        Returns:
            True if deleted, False if not found.
        """
        if message_id in self._messages:
            del self._messages[message_id]
            return True
        return False

    async def delete_by_user_id(self, user_id: int) -> int:
        """Delete all messages for a user.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            Number of messages deleted.
        """
        messages_to_delete = [msg_id for msg_id, msg in self._messages.items() if msg.user_id == user_id]

        for msg_id in messages_to_delete:
            del self._messages[msg_id]

        return len(messages_to_delete)

    def clear(self) -> None:
        """Clear all messages (for testing)."""
        self._messages.clear()
        self._next_id = 1
