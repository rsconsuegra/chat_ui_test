# LLM Chat Application

A chat application built with Clean/Hexagonal Architecture principles, demonstrating SOLID design patterns and modern Python practices.

## Features

- Chat with Ollama (local LLM)
- Persistent chat history (SQLite with aiosqlite)
- Simple username authentication
- Streaming responses
- Clean Architecture with dependency injection
- Async/await throughout

## Architecture

This application follows Clean/Hexagonal Architecture with clear layer separation:

- **Domain Layer** - Entities, value objects, repository interfaces
- **Application Layer** - Use cases and application services
- **Infrastructure Layer** - Adapters, repositories, database

See [specs/architecture/architecture.md](specs/architecture/architecture.md) for detailed documentation.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.ai/) (optional, for local LLM)

## Quick Start

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
uv run python scripts/init_db.py

# Run the application
uv run chainlit run src/main.py -w
```

## Project Structure

```
src/
├── domain/
│   ├── models/           # Entities (User, ChatMessage, MessageRole)
│   ├── repositories/     # Repository interfaces
│   ├── interfaces/       # Provider and adapter interfaces
│   └── errors/           # Domain exceptions
├── application/
│   ├── use_cases/        # Business logic (SendMessage, LoadHistory)
│   └── services/         # Application services (SessionService)
├── infrastructure/
│   ├── adapters/         # External integrations (Chainlit, Ollama)
│   ├── repositories/     # SQLite implementations
│   ├── database/         # Connection and migrations
│   └── container.py      # Dependency injection container
├── config/               # Configuration modules
├── bootstrap.py          # Application bootstrap
└── main.py               # Entry point
```

## Configuration

Key environment variables (see `.env.example` for all options):

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_PROVIDER` | LLM provider (ollama, openrouter, zai) | `ollama` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model to use | `llama3` |
| `DATABASE_PATH` | SQLite database path | `./chat_history.db` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Lint code
uv run ruff check src/ tests/ scripts/

# Format code
uv run black src/ tests/ scripts/

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

## Project Status

Currently in **Phase 1 (MVP)** with core chat functionality complete.

- [x] Clean Architecture structure
- [x] Ollama provider integration
- [x] SQLite with aiosqlite (async)
- [x] Chainlit frontend
- [x] Username authentication
- [x] Chat history persistence

See [specs/roadmap/roadmap.md](specs/roadmap/roadmap.md) for the full roadmap.
