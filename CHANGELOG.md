# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- aiosqlite dependency for true async SQLite support
- pytest-asyncio for async test support
- Centralized pylint configuration in `.code_quality/.pylintrc`
- Frontend adapter architecture for UI decoupling
  - ISessionAdapter: abstract session management interface
  - IMessageAdapter: abstract message handling interface
  - IStreamingMessage: protocol for incremental output
  - ChainlitSessionAdapter: Chainlit-specific session implementation
  - ChainlitMessageAdapter: Chainlit-specific message implementation
- LoadHistoryUseCase: load and format chat history for provider context
- GetSystemPromptUseCase: resolve system prompt (async for Phase 3 AgentaAI)
- FrontendError exception for adapter-related errors

### Changed
- Migrated from sync sqlite3 to aiosqlite for true async database operations
- All repository methods now use proper async/await with aiosqlite
- Connection management now uses aiosqlite.Connection
- Database migrator updated for async migrations
- Tests updated to use pytest-asyncio with auto mode
- SendMessageUseCase now delegates to LoadHistoryUseCase and GetSystemPromptUseCase
- main.py simplified to use adapters via Container (better separation of concerns)
- Container updated with factory methods for all use cases and adapters
- All `__all__` declarations removed for explicit imports (approach B)
- All `__init__.py` files simplified to module docstrings only
- All imports are now direct (no re-exports)
- Provider imports updated to use direct module paths
- Pre-commit pylint now uses centralized `.pylintrc` config
- Removed inline pylint disables (moved to centralized config)

### Removed
- async_sqlite_base.py (replaced by proper aiosqlite in sqlite_base_repository.py)
- memory_repository.py (dead code, not used anywhere)
>>>>>>> 85e5660 (refactor: migrate from sync sqlite3 to aiosqlite)

### Architecture
- Frontend is now decoupled from Chainlit via adapter interfaces
- Replacing frontend would only require implementing ISessionAdapter/IMessageAdapter
- Clear separation between application layer use cases

---

## [0.2.0] - 2026-02-14

### Phase 1 Complete - MVP Core Chat Functionality

### Added
- Initial project setup with Clean/Hexagonal architecture
- Domain models: User, ChatMessage, MessageRole
- Repository interfaces: IUserRepository, IMessageRepository
- Domain exceptions: ChatAppError, ValidationError, StorageError, ConfigurationError, RepositoryError, ProviderError
- SQLite database with proper schema and indexes
- Database migration system with pure SQL files
- Database configuration with environment variable support
- Connection management with async context manager
- Comprehensive test suite with pytest (49 unit tests)
- Pre-commit hooks with black, isort, ruff, pylint, mypy, pydocstyle
- Provider interface abstraction for LLM providers
- Ollama provider adapter implementation
- Dependency management with uv (Python 3.12)

### Changed
- Migrated from Python-based database initialization to SQL migration system
- Converted old test suite to pytest-based unit tests with mocking
- Removed hardcoded SQL from Python code
- Replaced Timestamp value object with datetime directly (simplification)

### Documentation
- Product Requirements Document (PRD) created
- Architecture documentation with Clean/Hexagonal patterns
- Roadmap with 6 development phases
- Technical specifications and implementation details
- 5 detailed user stories with acceptance criteria

### Development
- AGENTS.md guidelines for AI agents and contributors
- Makefile with convenient commands (init-db, test, format, lint, pre-commit)
- pyproject.toml with comprehensive dependency management
- Environment configuration template (.env.example)
- Test fixtures and shared configuration in conftest.py

---

## [0.1.0] - 2026-02-08

### Initial Release
- Project foundation with Clean/Hexagonal architecture
- Core domain models and repository patterns
- SQLite database with migration support
- Comprehensive test suite (49 tests, 37% coverage)
- Pre-commit hooks with perfect code quality scores
