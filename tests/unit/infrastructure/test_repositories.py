"""Unit tests for infrastructure layer using mocks."""

# pylint: disable=protected-access

import sqlite3
from unittest.mock import MagicMock

import pytest

from src.domain.errors.exceptions import StorageError
from src.domain.models.chat_message import ChatMessage
from src.domain.models.message_role import MessageRole
from src.domain.models.user import User
from src.infrastructure.repositories.sqlite_message_repository import (
    SQLiteMessageRepository,
)
from src.infrastructure.repositories.sqlite_user_repository import (
    SQLiteUserRepository,
)


class TestSQLiteUserRepositoryUnit:
    """Unit tests for SQLiteUserRepository with mocked database."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_save_user(self, mock_database_connection: MagicMock) -> None:
        """Test saving a user.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)
        user = User.create_new("testuser")

        # Mock cursor - aiosqlite returns cursor from execute()
        mock_cursor = mock_database_connection._cursor
        mock_cursor.lastrowid = 42

        saved_user = await repo.save(user)

        assert saved_user.id == 42
        mock_database_connection.execute.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_id_existing(self, mock_database_connection: MagicMock) -> None:
        """Test finding existing user by ID.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)

        # Mock cursor.fetchone to return user data
        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = (
            1,
            "testuser",
            "2024-01-01 12:00:00",
            "2024-01-01 12:00:00",
        )

        user = await repo.find_by_id(1)

        assert user is not None
        assert user.id == 1
        assert user.username == "testuser"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, mock_database_connection: MagicMock) -> None:
        """Test finding non-existent user by ID.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = None

        user = await repo.find_by_id(999)

        assert user is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_username(self, mock_database_connection: MagicMock) -> None:
        """Test finding user by username.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = (
            1,
            "testuser",
            "2024-01-01 12:00:00",
            "2024-01-01 12:00:00",
        )

        user = await repo.find_by_username("testuser")

        assert user is not None
        assert user.username == "testuser"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exists_true(self, mock_database_connection: MagicMock) -> None:
        """Test exists method when user exists.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = (1,)

        exists = await repo.exists("testuser")

        assert exists is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exists_false(self, mock_database_connection: MagicMock) -> None:
        """Test exists method when user does not exist.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = None

        exists = await repo.exists("nonexistent")

        assert exists is False


class TestSQLiteMessageRepositoryUnit:
    """Unit tests for SQLiteMessageRepository with mocked database."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_save_message(self, mock_database_connection: MagicMock) -> None:
        """Test saving a message.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteMessageRepository(mock_database_connection)
        message = ChatMessage.create(
            user_id=1,
            content="Test message",
            provider="ollama",
            role=MessageRole.USER,
        )

        mock_cursor = mock_database_connection._cursor
        mock_cursor.lastrowid = 100

        saved_message = await repo.save(message)

        assert saved_message.id == 100
        mock_database_connection.execute.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_id_existing(self, mock_database_connection: MagicMock) -> None:
        """Test finding existing message by ID.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteMessageRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = (
            1,
            42,
            "ollama",
            "user",
            "Hello",
            "2024-01-01 12:00:00",
        )

        message = await repo.find_by_id(1)

        assert message is not None
        assert message.id == 1
        assert message.content == "Hello"
        assert message.role == MessageRole.USER

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_user_id(self, mock_database_connection: MagicMock) -> None:
        """Test finding messages by user ID.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteMessageRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchall.return_value = [
            (1, 42, "ollama", "user", "Hello", "2024-01-01 12:00:00"),
            (2, 42, "ollama", "assistant", "Hi there!", "2024-01-01 12:01:00"),
        ]

        messages = await repo.find_by_user_id(42, limit=10)

        assert len(messages) == 2
        assert messages[0].role == MessageRole.USER
        assert messages[1].role == MessageRole.ASSISTANT

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_delete_by_user_id(self, mock_database_connection: MagicMock) -> None:
        """Test deleting messages by user ID.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteMessageRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.rowcount = 5

        deleted = await repo.delete_by_user_id(42)

        assert deleted == 5

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_count_by_user_id(self, mock_database_connection: MagicMock) -> None:
        """Test counting messages by user ID.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteMessageRepository(mock_database_connection)

        mock_cursor = mock_database_connection._cursor
        mock_cursor.fetchone.return_value = (10,)

        count = await repo.count_by_user_id(42)

        assert count == 10


class TestRepositoryErrorHandling:
    """Test error handling in repositories."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_user_repo_handles_database_error(self, mock_database_connection: MagicMock) -> None:
        """Test that user repository handles database errors.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteUserRepository(mock_database_connection)

        # Simulate database error
        mock_database_connection.execute.side_effect = sqlite3.Error("Database error")

        with pytest.raises(StorageError):
            await repo.save(User.create_new("testuser"))

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_message_repo_handles_database_error(self, mock_database_connection: MagicMock) -> None:
        """Test that message repository handles database errors.

        Args:
            mock_database_connection: Mocked database connection.
        """
        repo = SQLiteMessageRepository(mock_database_connection)

        mock_database_connection.execute.side_effect = sqlite3.Error("Database error")

        with pytest.raises(StorageError):
            await repo.save(
                ChatMessage.create(
                    user_id=1,
                    content="Test",
                    provider="ollama",
                    role=MessageRole.USER,
                )
            )
