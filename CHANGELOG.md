# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
