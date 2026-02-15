"""Provider message model for LLM communication."""

from dataclasses import dataclass

from src.domain.models.message_role import MessageRole


@dataclass(kw_only=True, frozen=True)
class ProviderMessage:
    """Message format for provider communication.

    This dataclass represents a message in the format expected by LLM providers,
    with a role and content. It serves as the bridge between domain messages
    and provider-specific message formats.

    Attributes:
        role: The role of the message sender (system, user, assistant)
        content: The text content of the message
    """

    role: MessageRole
    content: str

    def to_dict(self) -> dict[str, str]:
        """Convert message to dictionary format for API calls.

        Returns:
            Dictionary with 'role' and 'content' keys
        """
        return {"role": self.role.value, "content": self.content}
