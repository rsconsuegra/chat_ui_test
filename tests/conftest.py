"""Pytest configuration and shared fixtures."""

# pylint: disable=protected-access

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.domain.models.chat_message import ChatMessage
from src.domain.models.message_role import MessageRole
from src.domain.models.user import User
from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository


@pytest.fixture(name="_mock_env_vars")
def _fixture_mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
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


@pytest.fixture(name="sample_user")
def fixture_sample_user() -> User:
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


@pytest.fixture(name="sample_chat_message")
def fixture_sample_chat_message(sample_user: User) -> ChatMessage:
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


@pytest.fixture(name="mock_user_repository")
def fixture_mock_user_repository(mocker: MockerFixture) -> IUserRepository:
    """Create a mocked user repository.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        A mocked IUserRepository instance.
    """
    repo = mocker.AsyncMock(spec=IUserRepository)
    return repo


@pytest.fixture(name="mock_message_repository")
def fixture_mock_message_repository(mocker: MockerFixture) -> IMessageRepository:
    """Create a mocked message repository.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        A mocked IMessageRepository instance.
    """
    repo = mocker.AsyncMock(spec=IMessageRepository)
    return repo


@pytest.fixture(name="mock_datetime_now")
def fixture_mock_datetime_now() -> datetime:
    """Return a fixed datetime for testing.

    Returns:
        A fixed datetime instance.
    """
    return datetime(2024, 1, 15, 10, 30, 0)


@pytest.fixture(name="mock_database_connection")
def fixture_mock_database_connection(mocker: MockerFixture) -> MagicMock:
    """Create a mocked async database connection.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        A mocked aiosqlite.Connection-like instance with async methods.
    """
    conn = mocker.MagicMock()
    cursor = mocker.AsyncMock()

    # aiosqlite uses async methods
    # connection.execute() returns cursor directly (no .cursor() method)
    conn.execute = mocker.AsyncMock(return_value=cursor)
    conn.commit = mocker.AsyncMock()
    conn.close = mocker.AsyncMock()

    # Cursor async methods
    cursor.fetchone = mocker.AsyncMock()
    cursor.fetchall = mocker.AsyncMock()
    cursor.close = mocker.AsyncMock()
    cursor.lastrowid = 1
    cursor.rowcount = 0

    # Store cursor for test access
    conn._cursor = cursor

    return conn
