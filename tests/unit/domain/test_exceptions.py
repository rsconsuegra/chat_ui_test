"""Unit tests for domain exceptions."""

import pytest

from src.domain.errors.exceptions import (
    ChatAppError,
    ConfigurationError,
    ProviderError,
    RepositoryError,
    StorageError,
    ValidationError,
)


class TestChatAppError:
    """Test suite for base ChatAppError."""

    @pytest.mark.unit
    def test_chat_app_error_creation(self) -> None:
        """Test basic chat app error creation."""
        error = ChatAppError("Test error message")

        assert str(error) == "Test error message"

    @pytest.mark.unit
    def test_chat_app_error_inheritance(self) -> None:
        """Test that ChatAppError inherits from Exception."""
        error = ChatAppError("Test")

        assert isinstance(error, Exception)


class TestValidationError:
    """Test suite for ValidationError."""

    @pytest.mark.unit
    def test_validation_error_creation(self) -> None:
        """Test validation error creation."""
        error = ValidationError("Invalid input")

        assert str(error) == "Invalid input"
        assert isinstance(error, ChatAppError)

    @pytest.mark.unit
    def test_validation_error_raises_correctly(self) -> None:
        """Test that ValidationError can be raised and caught."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Field is required")

        assert str(exc_info.value) == "Field is required"


class TestStorageError:
    """Test suite for StorageError."""

    @pytest.mark.unit
    def test_storage_error_creation(self) -> None:
        """Test storage error creation."""
        error = StorageError("Database connection failed")

        assert str(error) == "Database connection failed"
        assert isinstance(error, ChatAppError)


class TestConfigurationError:
    """Test suite for ConfigurationError."""

    @pytest.mark.unit
    def test_configuration_error_creation(self) -> None:
        """Test configuration error creation."""
        error = ConfigurationError("Missing API key")

        assert str(error) == "Missing API key"
        assert isinstance(error, ChatAppError)


class TestRepositoryError:
    """Test suite for RepositoryError."""

    @pytest.mark.unit
    def test_repository_error_creation(self) -> None:
        """Test repository error creation."""
        error = RepositoryError("User not found")

        assert str(error) == "User not found"
        assert isinstance(error, ChatAppError)

    @pytest.mark.unit
    def test_repository_error_raises_correctly(self) -> None:
        """Test that RepositoryError can be raised and caught."""
        with pytest.raises(RepositoryError) as exc_info:
            raise RepositoryError("Entity not found")

        assert str(exc_info.value) == "Entity not found"


class TestProviderError:
    """Test suite for ProviderError."""

    @pytest.mark.unit
    def test_provider_error_creation(self) -> None:
        """Test provider error creation."""
        error = ProviderError("API rate limit exceeded")

        assert str(error) == "API rate limit exceeded"
        assert isinstance(error, ChatAppError)


class TestExceptionHierarchy:
    """Test suite for exception hierarchy."""

    @pytest.mark.unit
    def test_all_inherit_from_chat_app_error(self) -> None:
        """Test that all domain exceptions inherit from ChatAppError."""
        exceptions = [
            ValidationError("test"),
            StorageError("test"),
            ConfigurationError("test"),
            RepositoryError("test"),
            ProviderError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, ChatAppError)

    @pytest.mark.unit
    def test_all_can_be_caught_as_chat_app_error(self) -> None:
        """Test that all exceptions can be caught as ChatAppError."""
        exceptions_to_test = [
            ValidationError,
            StorageError,
            ConfigurationError,
            RepositoryError,
            ProviderError,
        ]

        for exc_class in exceptions_to_test:
            with pytest.raises(ChatAppError):
                raise exc_class("Test")

    @pytest.mark.unit
    def test_all_can_be_caught_as_exception(self) -> None:
        """Test that all exceptions can be caught as generic Exception."""
        exceptions_to_test = [
            ChatAppError,
            ValidationError,
            StorageError,
            ConfigurationError,
            RepositoryError,
            ProviderError,
        ]

        for exc_class in exceptions_to_test:
            with pytest.raises(exc_class, match="Test"):
                raise exc_class("Test")
