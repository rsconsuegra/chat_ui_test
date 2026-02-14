"""Pytest configuration and shared fixtures."""

import sqlite3
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.domain.models.chat_message import ChatMessage
from src.domain.models.message_role import MessageRole
from src.domain.models.user import User
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository


@pytest.fixture
def _mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock all required environment variables.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("DATABASE_PATH", ":memory:")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_openrouter_key")
    monkeypatch.setenv("ZAI_API_KEY", "test_zai_key")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("AGENTA_API_KEY", "test_agenta_key")
    monkeypatch.setenv("AGENTA_BASE_URL", "http://localhost:8000")
    monkeypatch.setenv("MEM0_BASE_URL", "http://localhost:8080")


@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing.

    Returns:
        A User instance with test data.
    """
    return User(
        id=1,
        username="testuser",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 1, 12, 0, 0),
    )


@pytest.fixture
def sample_chat_message(sample_user: User) -> ChatMessage:  # pylint: disable=redefined-outer-name
    """Create a sample chat message for testing.

    Args:
        sample_user: Fixture providing a sample user.

    Returns:
        A ChatMessage instance with test data.
    """
    return ChatMessage(
        id=1,
        user_id=sample_user.id,
        provider="ollama",
        role=MessageRole.USER,
        content="Hello, this is a test message",
        timestamp=datetime(2024, 1, 1, 12, 0, 0),
    )


@pytest.fixture
def mock_user_repository(mocker: MockerFixture) -> IUserRepository:
    """Create a mocked user repository.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        A mocked IUserRepository instance.
    """
    repo = mocker.AsyncMock(spec=IUserRepository)
    return repo


@pytest.fixture
def mock_message_repository(mocker: MockerFixture) -> IMessageRepository:
    """Create a mocked message repository.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        A mocked IMessageRepository instance.
    """
    repo = mocker.AsyncMock(spec=IMessageRepository)
    return repo


@pytest.fixture
def mock_datetime_now() -> datetime:
    """Return a fixed datetime for testing.

    Returns:
        A fixed datetime instance.
    """
    return datetime(2024, 1, 15, 10, 30, 0)


@pytest.fixture
def mock_database_connection(mocker: MockerFixture) -> MagicMock:
    """Create a mocked database connection.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        A mocked sqlite3.Connection instance.
    """
    conn = mocker.MagicMock(spec=sqlite3.Connection)
    cursor = mocker.MagicMock()
    conn.cursor.return_value = cursor
    conn.execute.return_value = cursor
    return conn
