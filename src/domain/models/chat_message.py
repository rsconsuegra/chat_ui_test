"""Domain model for ChatMessage entity."""

from dataclasses import dataclass
from datetime import datetime

from src.domain.models.message_role import MessageRole


@dataclass(kw_only=True)
class ChatMessage:
    """Chat message entity representing messages in conversations."""

    id: int
    user_id: int
    provider: str
    role: MessageRole
    content: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        user_id: int,
        provider: str,
        role: MessageRole,
        content: str,
    ) -> "ChatMessage":
        """Create a new chat message with current timestamp.

        Args:
            user_id: The ID of the user who sent the message.
            provider: The LLM provider used.
            role: The role of the message (user, assistant, or system).
            content: The message content.

        Returns:
            ChatMessage entity with timestamp set to now.
        """
        return cls(
            id=0,
            user_id=user_id,
            provider=provider,
            role=role,
            content=content,
            timestamp=datetime.now(),
        )

    def to_dict(self) -> dict[str, str | int]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation of the message.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "provider": self.provider,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }
