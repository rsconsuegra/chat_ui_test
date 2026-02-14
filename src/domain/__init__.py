"""Domain layer containing business entities and logic."""

from src.domain.errors import (
    AuthenticationError,
    ChatAppError,
    ConfigurationError,
    ProviderError,
    ProviderNotFoundError,
    RepositoryError,
    StorageError,
    ValidationError,
)
from src.domain.models import (
    ChatMessage,
    MessageRole,
    User,
)
from src.domain.repositories import (
    IMessageRepository,
    IUserRepository,
)

__all__ = [
    AuthenticationError.__name__,
    ChatAppError.__name__,
    ConfigurationError.__name__,
    ProviderError.__name__,
    ProviderNotFoundError.__name__,
    RepositoryError.__name__,
    StorageError.__name__,
    ValidationError.__name__,
    "ChatMessage",
    "MessageRole",
    "User",
    "IMessageRepository",
    "IUserRepository",
]
