# Phase 0 Completion Plan

## Overview

This plan outlines the detailed steps to complete Phase 0: Foundation of the Clean/Hexagonal Architecture LLM Chat Application.

**Current State:**
- Basic project structure exists with src/app.py (Chainlit echo handler)
- pyproject.toml has chainlit>=2.9.6 and langchain>=1.2.8
- Repository initialized with git
- AGENTS.md guidelines defined
- Makefile with dev commands

**Phase 0 Goals:**
1. Create folder structure for Clean/Hexagonal architecture
2. Set up environment configuration (.env.example)
3. Create basic domain models (User, ChatMessage)
4. Initialize SQLite database

**Success Criteria:**
- Folder structure matches architecture plan
- .env.example has all required variables
- Database initialization script created
- Basic application can run

---

## Task Breakdown

### Task 1: Update Dependencies (pyproject.toml)

**Status:** Pending

**Description:** Add missing dependencies required for Phase 0 and future phases.

**Changes Required:**
```toml
[project]
dependencies = [
    "chainlit>=2.9.6",
    "langchain>=1.2.8",
    "httpx>=0.27.0",              # Async HTTP client for providers
    "pydantic>=2.0.0",            # Data validation (for future use)
    "python-dotenv>=1.0.0",       # Environment variable loading
    "langchain-community>=0.2.0", # Community integrations (Ollama)
]

[project.optional-dependencies]
dev = [
    "ruff>=0.6.0",
    "black>=24.0.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",     # Async testing support
]
```

**Commands to Run:**
```bash
uv sync
```

**Acceptance Criteria:**
- All dependencies install successfully with `uv sync`
- No version conflicts

---

### Task 2: Create Clean/Hexagonal Folder Structure

**Status:** Pending

**Description:** Create the complete folder structure as defined in architecture document.

**Directory Structure to Create:**
```
src/
├── __init__.py
├── domain/                          # Core domain layer
│   ├── __init__.py
│   ├── models/                      # Entities and value objects
│   │   ├── __init__.py
│   │   ├── chat_message.py          # Phase 0
│   │   ├── user.py                  # Phase 0
│   │   ├── message_role.py          # Phase 0
│   │   ├── timestamp.py             # Phase 0
│   │   ├── prompt.py                # Phase 3
│   │   └── memory.py                # Phase 5
│   ├── repositories/                # Repository interfaces (ports)
│   │   ├── __init__.py
│   │   ├── message_repository.py   # Phase 0 (interface)
│   │   ├── user_repository.py      # Phase 0 (interface)
│   │   ├── prompt_repository.py     # Phase 3
│   │   └── memory_repository.py     # Phase 5
│   ├── interfaces/                  # Domain interfaces
│   │   ├── __init__.py
│   │   └── provider.py              # Phase 1
│   └── errors/                      # Domain exceptions
│       ├── __init__.py
│       └── exceptions.py            # Phase 0 (base errors)
├── application/                     # Application layer
│   ├── __init__.py
│   ├── use_cases/                   # Business logic
│   │   ├── __init__.py
│   │   ├── send_message_use_case.py      # Phase 1
│   │   ├── load_history_use_case.py      # Phase 1
│   │   ├── switch_provider_use_case.py   # Phase 2
│   │   ├── manage_prompts_use_case.py    # Phase 3
│   │   ├── get_system_prompt_use_case.py # Phase 3
│   │   └── configure_memory_use_case.py  # Phase 5
│   └── services/                    # Application services
│       └── __init__.py
├── infrastructure/                  # Infrastructure layer (adapters)
│   ├── __init__.py
│   ├── repositories/                # Repository implementations
│   │   ├── __init__.py
│   │   ├── sqlite_message_repository.py # Phase 0
│   │   └── sqlite_user_repository.py     # Phase 0
│   ├── adapters/                    # External service adapters
│   │   ├── __init__.py
│   │   ├── providers/               # LLM provider adapters
│   │   │   ├── __init__.py
│   │   │   ├── base_provider.py    # Phase 1
│   │   │   ├── ollama_provider.py  # Phase 1
│   │   │   ├── openrouter_provider.py # Phase 2
│   │   │   └── zai_provider.py     # Phase 2
│   │   ├── agentaai/                # AgentaAI adapter
│   │   │   ├── __init__.py
│   │   │   └── agentaai_prompt_adapter.py # Phase 3
│   │   └── mem0/                    # Mem0 adapter
│   │       ├── __init__.py
│   │       └── mem0_memory_adapter.py   # Phase 5
│   └── database/                    # Database utilities
│       ├── __init__.py
│       └── connection.py            # Phase 0
└── config/                          # Configuration
    ├── __init__.py
    ├── providers.py                 # Provider configuration
    ├── prompts.py                   # Prompt configuration
    └── database.py                  # Database configuration
```

**Commands to Run:**
```bash
mkdir -p src/domain/{models,repositories,interfaces,errors}
mkdir -p src/application/{use_cases,services}
mkdir -p src/infrastructure/{repositories,adapters/{providers,agentaai,mem0},database}
mkdir -p src/config
```

**Files to Create:**
- `src/__init__.py`
- `src/domain/__init__.py`
- `src/domain/models/__init__.py`
- `src/domain/repositories/__init__.py`
- `src/domain/interfaces/__init__.py`
- `src/domain/errors/__init__.py`
- `src/application/__init__.py`
- `src/application/use_cases/__init__.py`
- `src/application/services/__init__.py`
- `src/infrastructure/__init__.py`
- `src/infrastructure/repositories/__init__.py`
- `src/infrastructure/adapters/__init__.py`
- `src/infrastructure/adapters/providers/__init__.py`
- `src/infrastructure/adapters/agentaai/__init__.py`
- `src/infrastructure/adapters/mem0/__init__.py`
- `src/infrastructure/database/__init__.py`
- `src/config/__init__.py`

**Acceptance Criteria:**
- All directories created
- All `__init__.py` files created
- Directory structure matches architecture plan

---

### Task 3: Create Environment Configuration

**Status:** Pending

**Description:** Create `.env.example` with all required environment variables.

**File to Create:** `.env.example`

**Content:**
```bash
# ==========================================
# LLM Provider Configuration
# ==========================================

# OpenRouter Provider (https://openrouter.ai/)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# z.AI Provider (https://z.ai/)
ZAI_API_KEY=your-zai-api-key-here
ZAI_BASE_URL=https://api.z.ai/v1

# Ollama Provider (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# ==========================================
# Prompt Management (AgentaAI)
# ==========================================

# AgentaAI Configuration
AGENTA_API_KEY=agenta-api-key-here
AGENTA_BASE_URL=https://api.agenta.ai

# ==========================================
# Memory Configuration (Optional - Phase 5)
# ==========================================

# Mem0 Configuration
MEM0_ENABLED=false
MEM0_BASE_URL=http://localhost:8080
MEM0_API_KEY=mem0-api-key-here

# ==========================================
# Storage Configuration
# ==========================================

# SQLite Database
DATABASE_PATH=./chat_history.db

# ==========================================
# Application Configuration
# ==========================================

# Default Provider (ollama, openrouter, zai)
DEFAULT_PROVIDER=ollama

# Default System Prompt
DEFAULT_SYSTEM_PROMPT=You are a helpful AI assistant.

# Chat History Limit
CHAT_HISTORY_LIMIT=100

# ==========================================
# Debug/Development
# ==========================================

# Log Level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Enable Debug Mode
DEBUG=false
```

**File to Update:** `.gitignore`

**Additions:**
```gitignore
# Environment variables
.env

# Database
*.db
*.db-shm
*.db-wal

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

**Acceptance Criteria:**
- `.env.example` created with all required variables
- `.gitignore` updated to exclude sensitive files
- Clear documentation for each variable

---

### Task 4: Create Domain Models

**Status:** Pending

**Description:** Create basic domain models following Python 3.12 standards with full typing.

#### 4.1 Create MessageRole Enum

**File:** `src/domain/models/message_role.py`

**Content:**
```python
from enum import Enum

class MessageRole(Enum):
    """Enumeration for message roles in chat conversations."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
```

#### 4.2 Create Timestamp Data Class

**File:** `src/domain/models/timestamp.py`

**Content:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True, frozen=True)
class Timestamp:
    """Value object representing a point in time."""

    value: datetime

    @classmethod
    def now(cls) -> "Timestamp":
        """Create a timestamp for the current time."""
        return cls(value=datetime.now())

    def __str__(self) -> str:
        """Return ISO format string representation."""
        return self.value.isoformat()
```

#### 4.3 Create User Entity

**File:** `src/domain/models/user.py`

**Content:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True)
class User:
    """User entity representing application users."""

    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    @property
    def normalized_username(self) -> str:
        """Return username in lowercase for case-insensitive comparison."""
        return self.username.lower()

    @classmethod
    def create_new(cls, username: str) -> "User":
        """Create a new user with current timestamps."""
        now = datetime.now()
        return cls(
            id=0,  # Will be set by repository
            username=username,
            created_at=now,
            updated_at=now
        )

    def update_timestamp(self) -> "User":
        """Return a new User instance with updated timestamp."""
        return User(
            id=self.id,
            username=self.username,
            created_at=self.created_at,
            updated_at=datetime.now()
        )
```

#### 4.4 Create ChatMessage Entity

**File:** `src/domain/models/chat_message.py`

**Content:**
```python
from dataclasses import dataclass
from datetime import datetime

from .message_role import MessageRole
from .timestamp import Timestamp

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
        content: str
    ) -> "ChatMessage":
        """Create a new chat message with current timestamp."""
        return cls(
            id=0,  # Will be set by repository
            user_id=user_id,
            provider=provider,
            role=role,
            content=content,
            timestamp=datetime.now()
        )

    def to_dict(self) -> dict[str, str | int]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "provider": self.provider,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }
```

#### 4.5 Update __init__.py Files

**File:** `src/domain/models/__init__.py`

**Content:**
```python
from .chat_message import ChatMessage
from .message_role import MessageRole
from .timestamp import Timestamp
from .user import User

__all__ = [
    "ChatMessage",
    "MessageRole",
    "Timestamp",
    "User",
]
```

**Acceptance Criteria:**
- All domain models created with full typing
- All public methods have Google docstrings
- All code follows Python 3.12 syntax
- `uv run ruff check` passes with no errors
- `uv run black` formatting consistent

---

### Task 5: Create Repository Interfaces (Ports)

**Status:** Pending

**Description:** Create repository interfaces following dependency inversion principle.

#### 5.1 Create UserRepository Interface

**File:** `src/domain/repositories/user_repository.py`

**Content:**
```python
from abc import ABC, abstractmethod
from typing import Optional

from ..models.user import User

class IUserRepository(ABC):
    """Interface for user data access operations."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user to the repository.

        Args:
            user: The user entity to save.

        Returns:
            The saved user with assigned ID.
        """
        pass

    @abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by ID.

        Args:
            user_id: The user ID to search for.

        Returns:
            The user if found, None otherwise.
        """
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username (case-insensitive).

        Args:
            username: The username to search for.

        Returns:
            The user if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_or_create(self, username: str) -> User:
        """Get an existing user or create a new one.

        Args:
            username: The username to get or create.

        Returns:
            The existing or newly created user.
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID.

        Args:
            user_id: The user ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        pass
```

#### 5.2 Create MessageRepository Interface

**File:** `src/domain/repositories/message_repository.py`

**Content:**
```python
from abc import ABC, abstractmethod
from typing import List

from ..models.chat_message import ChatMessage

class IMessageRepository(ABC):
    """Interface for message data access operations."""

    @abstractmethod
    async def save(self, message: ChatMessage) -> ChatMessage:
        """Save a message to the repository.

        Args:
            message: The message entity to save.

        Returns:
            The saved message with assigned ID.
        """
        pass

    @abstractmethod
    async def find_by_id(self, message_id: int) -> ChatMessage | None:
        """Find a message by ID.

        Args:
            message_id: The message ID to search for.

        Returns:
            The message if found, None otherwise.
        """
        pass

    @abstractmethod
    async def find_by_user(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Find all messages for a user.

        Args:
            user_id: The user ID to search for.
            limit: Maximum number of messages to return.

        Returns:
            List of messages for the user, ordered by timestamp descending.
        """
        pass

    @abstractmethod
    async def delete_by_user(self, user_id: int) -> int:
        """Delete all messages for a user.

        Args:
            user_id: The user ID to delete messages for.

        Returns:
            Number of messages deleted.
        """
        pass
```

#### 5.3 Update __init__.py File

**File:** `src/domain/repositories/__init__.py`

**Content:**
```python
from .message_repository import IMessageRepository
from .user_repository import IUserRepository

__all__ = [
    "IMessageRepository",
    "IUserRepository",
]
```

**Acceptance Criteria:**
- All repository interfaces created with proper abstract methods
- All methods have Google docstrings
- Full typing coverage
- Follows Python 3.12 syntax

---

### Task 6: Create Domain Exceptions

**Status:** Pending

**Description:** Create base exception hierarchy for domain errors.

**File:** `src/domain/errors/exceptions.py`

**Content:**
```python
class ChatAppError(Exception):
    """Base exception for all chat application errors."""

    pass


class ProviderError(ChatAppError):
    """Exception raised when LLM provider operations fail."""

    pass


class ProviderNotFoundError(ProviderError):
    """Exception raised when a requested provider is not found."""

    pass


class ConfigurationError(ChatAppError):
    """Exception raised when configuration is invalid or missing."""

    pass


class AuthenticationError(ChatAppError):
    """Exception raised when authentication fails."""

    pass


class StorageError(ChatAppError):
    """Exception raised when storage operations fail."""

    pass


class ValidationError(ChatAppError):
    """Exception raised when data validation fails."""

    pass
```

**File:** `src/domain/errors/__init__.py`

**Content:**
```python
from .exceptions import (
    AuthenticationError,
    ChatAppError,
    ConfigurationError,
    ProviderError,
    ProviderNotFoundError,
    StorageError,
    ValidationError,
)

__all__ = [
    "AuthenticationError",
    "ChatAppError",
    "ConfigurationError",
    "ProviderError",
    "ProviderNotFoundError",
    "StorageError",
    "ValidationError",
]
```

**Acceptance Criteria:**
- Exception hierarchy created
- Clear inheritance structure
- All exceptions documented

---

### Task 7: Create Database Configuration

**Status:** Pending

**Description:** Create database configuration and connection utilities.

#### 7.1 Create Database Configuration

**File:** `src/config/database.py`

**Content:**
```python
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(kw_only=True)
class DatabaseConfig:
    """Configuration for SQLite database connection."""

    database_path: str

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Load database configuration from environment variables.

        Returns:
            DatabaseConfig instance with values from environment.
        """
        return cls(
            database_path=os.getenv(
                "DATABASE_PATH",
                "./chat_history.db"
            )
        )


def get_database_config() -> DatabaseConfig:
    """Get the database configuration.

    Returns:
        DatabaseConfig instance.
    """
    return DatabaseConfig.from_env()
```

#### 7.2 Create Database Connection Utility

**File:** `src/infrastructure/database/connection.py`

**Content:**
```python
import sqlite3
from pathlib import Path
from contextlib import contextmanager

from config.database import get_database_config

_config = get_database_config()


@contextmanager
def get_connection():
    """Context manager for database connections.

    Yields:
        sqlite3.Connection: Database connection with row factory set.

    Raises:
        sqlite3.Error: If connection fails.
    """
    # Ensure database directory exists
    db_path = Path(_config.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(_config.database_path)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database() -> None:
    """Initialize the database with schema.

    Creates tables and indexes if they don't exist.

    Raises:
        sqlite3.Error: If initialization fails.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create chat_messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                provider TEXT NOT NULL CHECK(provider IN ('ollama', 'openrouter', 'zai')),
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id "
            "ON chat_messages(user_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp "
            "ON chat_messages(timestamp)"
        )

        conn.commit()
```

**Acceptance Criteria:**
- Configuration loads from environment variables
- Connection utility works correctly
- Database initialization creates proper schema
- All code has full typing and docstrings

---

### Task 8: Create SQLite Repository Implementations

**Status:** Pending

**Description:** Implement repository interfaces with SQLite.

#### 8.1 Create SQLiteUserRepository

**File:** `src/infrastructure/repositories/sqlite_user_repository.py`

**Content:**
```python
import sqlite3
from typing import Optional

from domain.models.user import User
from domain.repositories.user_repository import IUserRepository
from infrastructure.database.connection import get_connection


class SQLiteUserRepository(IUserRepository):
    """SQLite implementation of IUserRepository."""

    async def save(self, user: User) -> User:
        """Save a user to the database.

        Args:
            user: The user entity to save.

        Returns:
            The saved user with assigned ID.

        Raises:
            sqlite3.IntegrityError: If username already exists.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (username, created_at, updated_at)
                VALUES (?, ?, ?)
            """, (
                user.username,
                user.created_at,
                user.updated_at
            ))

            user.id = cursor.lastrowid
            conn.commit()

            return user

    async def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by ID.

        Args:
            user_id: The user ID to search for.

        Returns:
            The user if found, None otherwise.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, username, created_at, updated_at
                FROM users
                WHERE id = ?
            """, (user_id,))

            row = cursor.fetchone()

            if not row:
                return None

            return User(
                id=row["id"],
                username=row["username"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username (case-insensitive).

        Args:
            username: The username to search for.

        Returns:
            The user if found, None otherwise.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, username, created_at, updated_at
                FROM users
                WHERE LOWER(username) = LOWER(?)
            """, (username,))

            row = cursor.fetchone()

            if not row:
                return None

            return User(
                id=row["id"],
                username=row["username"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

    async def get_or_create(self, username: str) -> User:
        """Get an existing user or create a new one.

        Args:
            username: The username to get or create.

        Returns:
            The existing or newly created user.
        """
        existing = await self.find_by_username(username)

        if existing:
            return existing

        new_user = User.create_new(username)
        return await self.save(new_user)

    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID.

        Args:
            user_id: The user ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM users
                WHERE id = ?
            """, (user_id,))

            conn.commit()

            return cursor.rowcount > 0
```

#### 8.2 Create SQLiteMessageRepository

**File:** `src/infrastructure/repositories/sqlite_message_repository.py`

**Content:**
```python
from typing import List

from domain.models.chat_message import ChatMessage
from domain.models.message_role import MessageRole
from domain.repositories.message_repository import IMessageRepository
from infrastructure.database.connection import get_connection


class SQLiteMessageRepository(IMessageRepository):
    """SQLite implementation of IMessageRepository."""

    async def save(self, message: ChatMessage) -> ChatMessage:
        """Save a message to the database.

        Args:
            message: The message entity to save.

        Returns:
            The saved message with assigned ID.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO chat_messages
                (user_id, provider, role, content, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                message.user_id,
                message.provider,
                message.role.value,
                message.content,
                message.timestamp
            ))

            message.id = cursor.lastrowid
            conn.commit()

            return message

    async def find_by_id(self, message_id: int) -> ChatMessage | None:
        """Find a message by ID.

        Args:
            message_id: The message ID to search for.

        Returns:
            The message if found, None otherwise.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, user_id, provider, role, content, timestamp
                FROM chat_messages
                WHERE id = ?
            """, (message_id,))

            row = cursor.fetchone()

            if not row:
                return None

            return ChatMessage(
                id=row["id"],
                user_id=row["user_id"],
                provider=row["provider"],
                role=MessageRole(row["role"]),
                content=row["content"],
                timestamp=row["timestamp"]
            )

    async def find_by_user(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Find all messages for a user.

        Args:
            user_id: The user ID to search for.
            limit: Maximum number of messages to return.

        Returns:
            List of messages for the user, ordered by timestamp descending.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, user_id, provider, role, content, timestamp
                FROM chat_messages
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))

            rows = cursor.fetchall()

            return [
                ChatMessage(
                    id=row["id"],
                    user_id=row["user_id"],
                    provider=row["provider"],
                    role=MessageRole(row["role"]),
                    content=row["content"],
                    timestamp=row["timestamp"]
                )
                for row in rows
            ]

    async def delete_by_user(self, user_id: int) -> int:
        """Delete all messages for a user.

        Args:
            user_id: The user ID to delete messages for.

        Returns:
            Number of messages deleted.
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM chat_messages
                WHERE user_id = ?
            """, (user_id,))

            conn.commit()

            return cursor.rowcount
```

#### 8.3 Update __init__.py File

**File:** `src/infrastructure/repositories/__init__.py`

**Content:**
```python
from .sqlite_message_repository import SQLiteMessageRepository
from .sqlite_user_repository import SQLiteUserRepository

__all__ = [
    "SQLiteMessageRepository",
    "SQLiteUserRepository",
]
```

**Acceptance Criteria:**
- Both repositories implement their interfaces correctly
- All methods have Google docstrings
- Full typing coverage
- `uv run ruff check` passes
- `uv run black` formatting consistent

---

### Task 9: Create Database Initialization Script

**Status:** Pending

**Description:** Create standalone script to initialize database.

**File:** `scripts/init_db.py`

**Content:**
```python
import asyncio

from infrastructure.database.connection import init_database


async def main() -> None:
    """Initialize the database."""
    print("Initializing database...")

    try:
        init_database()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
```

**Update Makefile:**

Add to `Makefile`:
```makefile
.PHONY: init-db
init-db:
	uv run python scripts/init_db.py

.PHONY: test-db
test-db:
	uv run python -c "from infrastructure.database.connection import get_connection, init_database; init_database(); print('Database OK')"
```

**Acceptance Criteria:**
- Script initializes database correctly
- Can be run with `make init-db`
- All tables and indexes created
- No errors during execution

---

### Task 10: Update Main Application Entry Point

**Status:** Pending

**Description:** Update main.py to use the new structure.

**File:** `main.py`

**Content:**
```python
import chainlit as cl

from infrastructure.database.connection import init_database

# Initialize database on startup
init_database()


@cl.on_chat_start
async def on_chat_start() -> None:
    """Handle chat start event."""
    # Placeholder for user authentication
    # Will be implemented in Phase 1
    pass


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle incoming messages.

    Args:
        message: The incoming message from Chainlit.
    """
    # Placeholder for message handling
    # Will be implemented in Phase 1
    await cl.Message(
        content=f"Echo: {message.content}"
    ).send()
```

**Acceptance Criteria:**
- Application starts without errors
- Database initialized on startup
- Basic echo functionality maintained

---

### Task 11: Create Test Script

**Status:** Pending

**Description:** Create test script to verify Phase 0 completion.

**File:** `tests/test_phase0.py`

**Content:**
```python
import asyncio

from domain.models.chat_message import ChatMessage, MessageRole
from domain.models.user import User
from domain.repositories.message_repository import IMessageRepository
from domain.repositories.user_repository import IUserRepository
from infrastructure.database.connection import get_connection, init_database
from infrastructure.repositories.sqlite_message_repository import SQLiteMessageRepository
from infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository


async def test_database_initialization() -> bool:
    """Test that database can be initialized."""
    try:
        init_database()
        print("✓ Database initialization test passed")
        return True
    except Exception as e:
        print(f"✗ Database initialization test failed: {e}")
        return False


async def test_user_repository() -> bool:
    """Test user repository operations."""
    try:
        repo = SQLiteUserRepository()

        # Test create user
        user = User.create_new("testuser")
        saved_user = await repo.save(user)

        assert saved_user.id > 0, "User ID should be set after save"
        assert saved_user.username == "testuser", "Username should match"

        # Test find by ID
        found_user = await repo.find_by_id(saved_user.id)
        assert found_user is not None, "User should be found by ID"
        assert found_user.username == "testuser", "Username should match"

        # Test find by username
        found_by_username = await repo.find_by_username("testuser")
        assert found_by_username is not None, "User should be found by username"
        assert found_by_username.id == saved_user.id, "User ID should match"

        # Test get_or_create
        existing = await repo.get_or_create("testuser")
        assert existing.id == saved_user.id, "Should return existing user"

        new_user = await repo.get_or_create("newuser")
        assert new_user.id != saved_user.id, "Should create new user"

        # Cleanup
        await repo.delete(saved_user.id)
        await repo.delete(new_user.id)

        print("✓ User repository test passed")
        return True

    except Exception as e:
        print(f"✗ User repository test failed: {e}")
        return False


async def test_message_repository() -> bool:
    """Test message repository operations."""
    try:
        user_repo = SQLiteUserRepository()
        message_repo = SQLiteMessageRepository()

        # Create test user
        user = User.create_new("testuser")
        saved_user = await user_repo.save(user)

        # Test save message
        message = ChatMessage.create(
            user_id=saved_user.id,
            provider="ollama",
            role=MessageRole.USER,
            content="Test message"
        )
        saved_message = await message_repo.save(message)

        assert saved_message.id > 0, "Message ID should be set after save"
        assert saved_message.content == "Test message", "Content should match"

        # Test find by ID
        found_message = await message_repo.find_by_id(saved_message.id)
        assert found_message is not None, "Message should be found by ID"
        assert found_message.content == "Test message", "Content should match"

        # Test find by user
        messages = await message_repo.find_by_user(saved_user.id)
        assert len(messages) > 0, "Should find messages for user"
        assert messages[0].content == "Test message", "Content should match"

        # Cleanup
        await message_repo.delete_by_user(saved_user.id)
        await user_repo.delete(saved_user.id)

        print("✓ Message repository test passed")
        return True

    except Exception as e:
        print(f"✗ Message repository test failed: {e}")
        return False


async def main() -> None:
    """Run all Phase 0 tests."""
    print("Running Phase 0 tests...\n")

    results = []

    results.append(await test_database_initialization())
    results.append(await test_user_repository())
    results.append(await test_message_repository())

    print(f"\nResults: {sum(results)}/{len(results)} tests passed")

    if all(results):
        print("✓ All Phase 0 tests passed!")
    else:
        print("✗ Some tests failed. Please review: output above.")


if __name__ == "__main__":
    asyncio.run(main())
```

**Update Makefile:**

```makefile
.PHONY: test-phase0
test-phase0:
	uv run python tests/test_phase0.py
```

**Acceptance Criteria:**
- All tests pass
- Database operations work correctly
- Repositories function as expected

---

### Task 12: Run Quality Checks

**Status:** Pending

**Description:** Run all quality checks to ensure code meets standards.

**Commands to Run:**
```bash
# Format code
uv run black src/ tests/ scripts/

# Check linting
uv run ruff check src/ tests/ scripts/

# Run tests
uv run python tests/test_phase0.py
```

**Acceptance Criteria:**
- No linting errors
- Code is formatted consistently
- All tests pass

---

### Task 13: Verify Application Runs

**Status:** Pending

**Description:** Verify the application can start and basic functionality works.

**Commands to Run:**
```bash
# Initialize database
make init-db

# Start application (in background)
chainlit run main.py --host 0.0.0.0 --port 8500 &
APP_PID=$!

# Wait a moment
sleep 3

# Check if process is running
if ps -p $APP_PID > /dev/null; then
    echo "✓ Application started successfully"
    kill $APP_PID
else
    echo "✗ Application failed to start"
fi
```

**Acceptance Criteria:**
- Application starts without errors
- Database is initialized
- No exceptions during startup

---

## Execution Order

Execute tasks in the following order:

1. Task 1: Update Dependencies
2. Task 2: Create Folder Structure
3. Task 3: Create Environment Configuration
4. Task 4: Create Domain Models
5. Task 5: Create Repository Interfaces
6. Task 6: Create Domain Exceptions
7. Task 7: Create Database Configuration
8. Task 8: Create SQLite Repository Implementations
9. Task 9: Create Database Initialization Script
10. Task 10: Update Main Application Entry Point
11. Task 11: Create Test Script
12. Task 12: Run Quality Checks
13. Task 13: Verify Application Runs

---

## Validation Checklist

After completing all tasks, verify the following:

- [ ] All directories created with correct structure
- [ ] All `__init__.py` files created
- [ ] `.env.example` contains all required variables
- [ ] `.gitignore` excludes sensitive files
- [ ] Domain models have full typing and docstrings
- [ ] Repository interfaces defined correctly
- [ ] SQLite repositories implement interfaces
- [ ] Database initialization works
- [ ] Test script runs successfully
- [ ] No linting errors
- [ ] Code is formatted with black
- [ ] Application starts without errors
- [ ] Database schema is correct
- [ ] All code follows Python 3.12 standards
- [ ] All code follows AGENTS.md guidelines

---

## Rollback Plan

If issues arise during implementation:

1. **Dependency Issues:** Restore original pyproject.toml and run `uv sync`
2. **Folder Structure Issues:** Remove created directories with `rm -rf src/domain src/application src/infrastructure src/config`
3. **Database Issues:** Delete `chat_history.db` and reinitialize
4. **Code Quality Issues:** Use `git status` to see changes and `git checkout` to restore files

---

## Time Estimate

- Task 1: 5 minutes
- Task 2: 5 minutes
- Task 3: 10 minutes
- Task 4: 20 minutes
- Task 5: 15 minutes
- Task 6: 5 minutes
- Task 7: 15 minutes
- Task 8: 30 minutes
- Task 9: 10 minutes
- Task 10: 5 minutes
- Task 11: 15 minutes
- Task 12: 10 minutes
- Task 13: 5 minutes

**Total Estimated Time:** ~2.5 hours

---

## Notes

- All code must follow Python 3.12 standards with full typing
- All public functions must have Google-style docstrings
- Use `uv run` for all Python command execution
- Run `uv run pre-commit run --all-files` before committing
- Do not commit without explicit user permission
- This is Phase 0 of 6 phases; focus on foundation only
