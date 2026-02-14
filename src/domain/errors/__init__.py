"""Custom exceptions for domain and application errors."""

from .exceptions import (
    AuthenticationError,
    ChatAppError,
    ConfigurationError,
    ProviderError,
    ProviderNotFoundError,
    RepositoryError,
    StorageError,
    ValidationError,
)

__all__ = [
    "AuthenticationError",
    "ChatAppError",
    "ConfigurationError",
    "ProviderError",
    "ProviderNotFoundError",
    "RepositoryError",
    "StorageError",
    "ValidationError",
]
