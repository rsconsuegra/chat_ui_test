# Technical Specifications

## Overview
This document provides detailed technical specifications for the Clean/Hexagonal Architecture LLM Chat Application. These specifications translate the PRD requirements into concrete implementation details.

## 1. Project Structure

```
chat-ui-test/
├── src/
│   ├── __init__.py
│   ├── domain/              # Core domain layer
│   │   ├── __init__.py
│   │   ├── models/          # Entities and value objects
│   │   │   ├── __init__.py
│   │   │   ├── chat_message.py
│   │   │   ├── user.py
│   │   │   ├── prompt.py
│   │   │   └── memory.py
│   │   ├── repositories/    # Repository interfaces (ports)
│   │   │   ├── __init__.py
│   │   │   ├── message_repository.py
│   │   │   ├── user_repository.py
│   │   │   ├── prompt_repository.py
│   │   │   └── memory_repository.py
│   │   └── interfaces/      # Domain interfaces
│   │       └── __init__.py
│   ├── application/         # Application layer
│   │   ├── __init__.py
│   │   ├── use_cases/       # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── send_message_use_case.py
│   │   │   ├── load_history_use_case.py
│   │   │   ├── switch_provider_use_case.py
│   │   │   ├── manage_prompts_use_case.py
│   │   │   ├── get_system_prompt_use_case.py
│   │   │   └── configure_memory_use_case.py
│   │   └── services/        # Application services
│   │       └── __init__.py
│   ├── infrastructure/      # Infrastructure layer (adapters)
│   │   ├── __init__.py
│   │   ├── repositories/    # Repository implementations
│   │   │   ├── __init__.py
│   │   │   ├── sqlite_message_repository.py
│   │   │   ├── sqlite_user_repository.py
│   │   │   └── ... (other repositories)
│   │   └── adapters/        # External service adapters
│   │       ├── __init__.py
│   │       ├── providers/   # LLM provider adapters
│   │       │   ├── __init__.py
│   │       │   ├── base_provider.py
│   │       │   ├── ollama_provider.py
│   │       │   ├── openrouter_provider.py
│   │       │   └── zai_provider.py
│   │       └── agentaai/    # AgentaAI adapter
│   │           ├── __init__.py
│   │           └── agentaai_prompt_adapter.py
│   └── config/              # Configuration
│       ├── __init__.py
│       ├── providers.py     # Provider configuration
│       ├── prompts.py       # Prompt configuration
│       └── memory.py        # Memory configuration
├── chainlit.md              # Chainlit welcome screen
├── main.py                  # Application entry point
├── pyproject.toml           # Python project configuration
├── README.md                # Project documentation
└── AGENTS.md                # Agent guidelines

# Database
chat_history.db              # SQLite database file

# Configuration
.env                         # Environment variables
.env.example                 # Environment variables template
```

## 2. Dependencies

### pyproject.toml
```toml
[project]
name = "chat-ui-test"
version = "0.1.0"
description = "LLM Chat Application with Clean/Hexagonal Architecture"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "chainlit>=2.9.6",
    "langchain>=1.2.8",
    "httpx>=0.27.0",  # Async HTTP client
    "pydantic>=2.0.0",  # Data validation
    "python-dotenv>=1.0.0",  # Environment variables
]

[project.optional-dependencies]
dev = [
    "ruff>=0.6.0",
    "black>=24.0.0",
    "pytest>=8.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 3. Database Schema

### SQLite Schema (chat_history.db)

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
```

#### Chat Messages Table
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    provider TEXT NOT NULL CHECK(provider IN ('ollama', 'openrouter', 'zai')),
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp);
```

#### Indexes Summary
- `users(username)` - Fast username lookup
- `chat_messages(user_id)` - Fast message filtering by user
- `chat_messages(timestamp)` - Fast chronological ordering

### Database Initialization
```python
import sqlite3
from pathlib import Path

def init_database(db_path: str = "./chat_history.db"):
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(db_path)
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp)")

    conn.commit()
    conn.close()
```

## 4. Configuration Management

### Environment Variables (.env.example)
```bash
# LLM Provider Configuration
OPENROUTER_API_KEY=sk-or-v1-your-key-here
ZAI_API_KEY=your-zai-api-key-here
OLLAMA_BASE_URL=http://localhost:11434

# Prompt Management (AgentaAI)
AGENTA_API_KEY=agenta-api-key-here
AGENTA_BASE_URL=https://api.agenta.ai

# Memory Configuration (Optional)
MEM0_ENABLED=false
MEM0_BASE_URL=http://localhost:8080
MEM0_API_KEY=mem0-api-key-here

# Storage Configuration
DATABASE_PATH=./chat_history.db
```

### Configuration Module (config/providers.py)
```python
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class OllamaConfig:
    base_url: str
    model: str = "llama3"

@dataclass
class OpenRouterConfig:
    api_key: str
    base_url: str = "https://openrouter.ai/api/v1"

@dataclass
class ZAIConfig:
    api_key: str
    base_url: str  # To be specified

@dataclass
class ProvidersConfig:
    ollama: OllamaConfig
    openrouter: OpenRouterConfig
    zai: ZAIConfig

    @classmethod
    def from_env(cls) -> "ProvidersConfig":
        """Load configuration from environment variables."""
        return cls(
            ollama=OllamaConfig(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                model=os.getenv("OLLAMA_MODEL", "llama3")
            ),
            openrouter=OpenRouterConfig(
                api_key=os.getenv("OPENROUTER_API_KEY", ""),
                base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            ),
            zai=ZAIConfig(
                api_key=os.getenv("ZAI_API_KEY", ""),
                base_url=os.getenv("ZAI_BASE_URL", "")  # TBD
            )
        )
```

### Configuration Module (config/prompts.py)
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PromptConfig:
    default_system_prompt: str = (
        "You are a helpful AI assistant. "
        "You answer questions accurately and helpfully."
    )

    def get_system_prompt(self, name: str) -> str:
        """Get system prompt by name."""
        prompts = {
            "system": self.default_system_prompt,
            "coding": "You are a coding assistant. Provide clear explanations and working code examples.",
            "general": "You are a helpful assistant. Answer questions clearly and concisely."
        }
        return prompts.get(name, self.default_system_prompt)

    @classmethod
    def from_env(cls) -> "PromptConfig":
        """Load configuration from environment variables."""
        # Could load from AgentaAI here if enabled
        return cls()
```

## 5. Domain Layer

### Domain Models

#### ChatMessage (domain/models/chat_message.py)
```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass(kw_only=True)
class ChatMessage:
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
        """Create a new chat message."""
        return cls(
            id=0,  # Will be set by repository
            user_id=user_id,
            provider=provider,
            role=role,
            content=content,
            timestamp=datetime.now()
        )

    def to_dict(self) -> dict:
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

#### User (domain/models/user.py)
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True)
class User:
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    @property
    def normalized_username(self) -> str:
        """Return username in lowercase for case-insensitive comparison."""
        return self.username.lower()
```

## 6. Infrastructure Layer

### Repository Implementations

#### SQLite Message Repository (infrastructure/repositories/sqlite_message_repository.py)
```python
import sqlite3
from typing import List, Optional
from domain.models.chat_message import ChatMessage, MessageRole
from domain.repositories.message_repository import IMessageRepository

class SQLiteMessageRepository(IMessageRepository):
    def __init__(self, db_path: str = "./chat_history.db"):
        self.db_path = db_path
        self._ensure_connection()

    def _ensure_connection(self):
        """Ensure database connection is available."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    async def save_message(self, message: ChatMessage) -> ChatMessage:
        """Save a new chat message."""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO chat_messages (user_id, provider, role, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            message.user_id,
            message.provider,
            message.role.value,
            message.content,
            message.timestamp
        ))

        message.id = cursor.lastrowid
        self.conn.commit()

        return message

    async def get_messages_by_user(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[ChatMessage]:
        """Get all messages for a user."""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM chat_messages
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()
        return [self._row_to_message(row) for row in rows]

    # ... other methods
```

### Provider Adapters

#### Base Provider Interface (infrastructure/adapters/providers/base_provider.py)
```python
from abc import ABC, abstractmethod
from typing import AsyncGenerator

class IProvider(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    async def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None
    ) -> AsyncGenerator[str, None]:
        """Generate response from LLM provider."""
        pass

    @abstractmethod
    async def get_model_info(self) -> dict:
        """Get information about the provider and model."""
        pass
```

#### Ollama Provider (infrastructure/adapters/providers/ollama_provider.py)
```python
import httpx
from typing import AsyncGenerator, dict, Any
from domain.interfaces.provider import IProvider
from config.providers import get_ollama_config

class OllamaProvider(IProvider):
    def __init__(self):
        self.config = get_ollama_config()
        self.client = httpx.AsyncClient(base_url=self.config.base_url)

    async def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None
    ) -> AsyncGenerator[str, None]:
        """Generate response from Ollama."""
        if system_prompt:
            messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })

        async with self.client.stream(
            "POST",
            "/api/chat",
            json={
                "model": self.config.model,
                "messages": messages,
                "stream": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break

                    import json
                    try:
                        chunk = json.loads(data)
                        delta = chunk.get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        pass

    async def get_model_info(self) -> dict:
        """Get model information."""
        try:
            response = await self.client.get("/api/tags")
            data = response.json()
            models = data.get("models", [])
            if models:
                return {
                    "name": models[0].get("name", "unknown"),
                    "modified_at": models[0].get("modified_at", "")
                }
            return {"name": "unknown", "modified_at": ""}
        except Exception as e:
            return {"error": str(e)}
```

## 7. Application Layer

### Use Case: Send Message (application/use_cases/send_message_use_case.py)
```python
from typing import AsyncGenerator
from domain.interfaces.provider import IProvider
from domain.models.chat_message import ChatMessage, MessageRole
from domain.repositories.message_repository import IMessageRepository
from domain.repositories.user_repository import IUserRepository

class SendMessageUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        message_repo: IMessageRepository,
        provider: IProvider,
        prompt_config: any  # Simplified
    ):
        self.user_repo = user_repo
        self.message_repo = message_repo
        self.provider = provider
        self.prompt_config = prompt_config

    async def execute(
        self,
        username: str,
        message: str,
        conversation_id: int | None = None
    ) -> AsyncGenerator[str, None]:
        """Execute message sending with memory integration."""

        # Get or create user
        user = await self.user_repo.get_or_create_user(username)

        # Generate response
        async for chunk in self.provider.generate_response([{"role": "user", "content": message}]):
            yield chunk

        # Save user message
        user_message = ChatMessage.create(
            user_id=user.id,
            provider=self.provider.__class__.__name__,
            role=MessageRole.USER,
            content=message
        )
        await self.message_repo.save_message(user_message)

        # Save assistant message (if available from provider)
        # This would require modifications to provider interface
        # to return full response
```

## 8. Integration Points

### Chainlit Adapter (infrastructure/adapters/chainlit/chainlit_adapter.py)
```python
import chainlit as cl
from typing import Any
from domain.interfaces.provider import IProvider
from domain.repositories.user_repository import IUserRepository
from application.use_cases.send_message_use_case import SendMessageUseCase
from config.providers import get_ollama_config

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages in Chainlit UI."""

    # Get username from session
    username = cl.user_session.get("username")

    if not username:
        username = input("Enter username: ")
        cl.user_session.set("username", username)

    # Initialize use case
    user_repo = ...  # Need to instantiate
    message_repo = ...  # Need to instantiate
    provider = OllamaProvider()
    prompt_config = ...  # Need to instantiate

    use_case = SendMessageUseCase(
        user_repo=user_repo,
        message_repo=message_repo,
        provider=provider,
        prompt_config=prompt_config
    )

    # Execute use case
    response = ""
    async for chunk in use_case.execute(
        username=username,
        message=message.content
    ):
        response += chunk
        await cl.Message(content=chunk).stream()

    # Save assistant message
    assistant_message = ChatMessage.create(
        user_id=user.id,
        provider=provider.__class__.__name__,
        role=MessageRole.ASSISTANT,
        content=response
    )
    await message_repo.save_message(assistant_message)
```

## 9. Error Handling

### Error Classes (domain/errors/exceptions.py)
```python
from typing import Optional

class ChatAppError(Exception):
    """Base exception for chat application errors."""
    pass

class ProviderError(ChatAppError):
    """Error from LLM provider."""
    pass

class ProviderNotFoundError(ChatAppError):
    """Provider not found."""
    pass

class ConfigurationError(ChatAppError):
    """Configuration error."""
    pass

class AuthenticationError(ChatAppError):
    """Authentication error."""
    pass

class StorageError(ChatAppError):
    """Storage error."""
    pass
```

### Error Handling Strategy
1. **Provider Errors**: Catch and log, fallback to other providers
2. **Database Errors**: Log and notify user
3. **Configuration Errors**: Fail fast with clear message
4. **Authentication Errors**: Clear prompt for new username

## 10. Testing Strategy

### Unit Tests
- Test all repository implementations
- Test all use cases
- Test domain models
- Test validation logic

### Integration Tests
- Test database operations
- Test provider integrations
- Test error handling

### End-to-End Tests
- Test complete message flow
- Test user authentication
- Test multi-provider switching

## 11. Security Considerations

### Input Validation
- Validate username format
- Sanitize message content
- Validate API keys

### Database Security
- Use parameterized queries (no SQL injection)
- Use foreign keys with CASCADE delete
- Proper connection management

### API Security
- Validate API endpoints
- Handle API errors gracefully
- No exposed credentials in logs
