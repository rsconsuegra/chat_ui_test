# Technical Debt Register

This file tracks known technical debt items and their justification.

---

## Pylint Disables

### R0903: Too Few Public Methods

Classes with only one public method are flagged by pylint. These are acceptable patterns:

| Location | Class | Justification |
|----------|-------|---------------|
| `src/application/services/session_service.py` | `SessionService` | Single-responsibility service, may grow |
| `src/application/use_cases/send_message.py` | `SendMessageUseCase` | Clean architecture use case, intentionally focused |
| `src/infrastructure/repositories/async_sqlite_base.py` | `AsyncSQLiteBaseRepository` | Base class with protected helper methods |
| `src/infrastructure/repositories/sqlite_base_repository.py` | `SQLiteBaseRepository` | Base class with protected helper methods |
| `tests/unit/domain/test_exceptions.py:53` | `TestExceptionMapping` | Test fixture class |
| `tests/unit/domain/test_exceptions.py:65` | `TestExceptionChaining` | Test fixture class |
| `tests/unit/domain/test_exceptions.py:97` | `TestExceptionMessages` | Test fixture class |

### W0603: Global Statement

| Location | Variable | Justification |
|----------|----------|---------------|
| `src/bootstrap.py:42` | `_container` | Singleton pattern for dependency injection |
| `src/bootstrap.py:50` | `_container` | Singleton pattern for dependency injection |

**Future fix:** Consider using a proper DI framework or module-level singleton pattern.

### C0415: Import Outside Toplevel

| Location | Import | Justification |
|----------|--------|---------------|
| `src/infrastructure/repositories/async_sqlite_base.py:124` | `RepositoryError` | Lazy import to avoid circular dependency |

**Future fix:** Restructure imports or use TYPE_CHECKING block.

### R0801: Duplicate Code

| Location | Duplicate With | Justification |
|----------|----------------|---------------|
| `src/config/app.py` | `src.config.providers` | Config fields naturally similar (ollama settings) |
| `src/infrastructure/repositories/async_sqlite_base.py` | `sqlite_base_repository.py` | Sync/async implementations share error handling |

**Future fix:** Extract common error handling to shared module; consolidate provider config.

---

## Dead Code (Phase 2 Candidates)

These files are not imported anywhere but kept for future multi-provider support:

| File | Lines | Purpose |
|------|-------|---------|
| `src/infrastructure/repositories/async_sqlite_base.py` | 148 | Async repository for future use |
| `src/infrastructure/repositories/memory_repository.py` | 272 | In-memory repository for testing |

**Action:** Delete when Phase 2 confirms they won't be needed, or integrate if they are.

---

## Other Known Issues

### Provider Config Duplication

`src.config.app` and `src.config.providers` have overlapping provider configuration fields.

**Future fix:** Consolidate into single configuration class.

---

## Resolution Log

| Date | Item | Resolution |
|------|------|------------|
| 2026-02-14 | `retry.py` overengineering | Deleted - using LangChain's built-in retry |
| 2026-02-14 | `ollama_provider.py` httpx impl | Deleted - replaced with LangChain provider |
