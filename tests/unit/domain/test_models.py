"""Unit tests for domain models."""

from datetime import datetime

import pytest

from src.domain.models.chat_message import ChatMessage
from src.domain.models.message_role import MessageRole
from src.domain.models.user import User


class TestUser:
    """Test suite for User model."""

    @pytest.mark.unit
    def test_user_creation(self) -> None:
        """Test basic user creation."""
        created_at = datetime(2024, 1, 1, 12, 0, 0)
        updated_at = datetime(2024, 1, 1, 13, 0, 0)

        user = User(
            id=1,
            username="testuser",
            created_at=created_at,
            updated_at=updated_at,
        )

        assert user.id == 1
        assert user.username == "testuser"
        assert user.normalized_username == "testuser"
        assert user.created_at == created_at
        assert user.updated_at == updated_at

    @pytest.mark.unit
    def test_user_create_new(self) -> None:
        """Test User.create_new factory method."""
        user = User.create_new("newuser")

        assert user.id == 0
        assert user.username == "newuser"
        assert user.normalized_username == "newuser"
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    @pytest.mark.unit
    def test_user_normalization(self) -> None:
        """Test username normalization."""
        user = User.create_new("TestUser123")
        assert user.normalized_username == "testuser123"

        user2 = User.create_new("USER_NAME")
        assert user2.normalized_username == "user_name"

    @pytest.mark.unit
    def test_user_equality(self) -> None:
        """Test user equality comparison with same timestamps."""
        now = datetime(2024, 1, 1, 12, 0, 0)
        user1 = User(id=1, username="user1", created_at=now, updated_at=now)
        user2 = User(id=1, username="user1", created_at=now, updated_at=now)
        user3 = User(id=2, username="user2", created_at=now, updated_at=now)

        assert user1 == user2
        assert user1 != user3

    @pytest.mark.unit
    def test_user_repr(self) -> None:
        """Test user string representation."""
        user = User.create_new("testuser")
        repr_str = repr(user)

        assert "User" in repr_str
        assert "testuser" in repr_str


class TestChatMessage:
    """Test suite for ChatMessage model."""

    @pytest.mark.unit
    def test_message_creation(self, mock_datetime_now: datetime) -> None:
        """Test basic message creation.

        Args:
            mock_datetime_now: Fixture providing fixed datetime.
        """
        message = ChatMessage(
            id=1,
            user_id=42,
            provider="ollama",
            role=MessageRole.USER,
            content="Hello, world!",
            timestamp=mock_datetime_now,
        )

        assert message.id == 1
        assert message.user_id == 42
        assert message.provider == "ollama"
        assert message.role == MessageRole.USER
        assert message.content == "Hello, world!"

    @pytest.mark.unit
    def test_message_create_factory(self) -> None:
        """Test ChatMessage.create factory method."""
        message = ChatMessage.create(
            user_id=1,
            provider="openrouter",
            role=MessageRole.USER,
            content="User message",
        )

        assert message.user_id == 1
        assert message.role == MessageRole.USER
        assert message.content == "User message"
        assert message.provider == "openrouter"
        assert message.id == 0

    @pytest.mark.unit
    def test_message_role_properties(self) -> None:
        """Test message role comparison."""
        user_msg = ChatMessage.create(
            user_id=1,
            provider="ollama",
            role=MessageRole.USER,
            content="Hello",
        )
        assistant_msg = ChatMessage.create(
            user_id=1,
            provider="ollama",
            role=MessageRole.ASSISTANT,
            content="Hi",
        )

        assert user_msg.role == MessageRole.USER
        assert assistant_msg.role == MessageRole.ASSISTANT
        assert user_msg.role != assistant_msg.role

    @pytest.mark.unit
    def test_message_to_dict(self) -> None:
        """Test to_dict serialization method."""
        message = ChatMessage(
            id=1,
            user_id=42,
            provider="ollama",
            role=MessageRole.USER,
            content="Test",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
        )

        data = message.to_dict()

        assert data["id"] == 1
        assert data["user_id"] == 42
        assert data["provider"] == "ollama"
        assert data["role"] == "user"
        assert data["content"] == "Test"
        assert "timestamp" in data


class TestMessageRole:
    """Test suite for MessageRole enum."""

    @pytest.mark.unit
    def test_role_values(self) -> None:
        """Test enum values."""
        assert MessageRole.USER.value == "user"
        assert MessageRole.ASSISTANT.value == "assistant"

    @pytest.mark.unit
    def test_role_comparison(self) -> None:
        """Test role comparison."""
        assert MessageRole.USER == MessageRole.USER
        assert MessageRole.USER != MessageRole.ASSISTANT
