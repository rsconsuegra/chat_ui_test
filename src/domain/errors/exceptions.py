"""Domain exceptions for chat application."""


class ChatAppError(Exception):
    """Base exception for all chat application errors."""


class ProviderError(ChatAppError):
    """Exception raised when LLM provider operations fail."""


class ProviderNotFoundError(ProviderError):
    """Exception raised when a requested provider is not found."""


class ConfigurationError(ChatAppError):
    """Exception raised when configuration is invalid or missing."""


class AuthenticationError(ChatAppError):
    """Exception raised when authentication fails."""


class StorageError(ChatAppError):
    """Exception raised when storage operations fail."""


class ValidationError(ChatAppError):
    """Exception raised when data validation fails."""


class RepositoryError(ChatAppError):
    """Exception raised when repository operations fail."""
