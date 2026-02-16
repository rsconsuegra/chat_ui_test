## Summary

Migrate from fake async (ThreadPoolExecutor + sqlite3) to true async using **aiosqlite** for proper non-blocking database operations aligned with Chainlit's async architecture.

## Changes

### Dependencies Added
- `aiosqlite` - Async SQLite driver
- `pytest-asyncio` - Async test support

### Files Modified
| File | Change |
|------|--------|
| `src/infrastructure/repositories/sqlite_base_repository.py` | Rewritten for aiosqlite |
| `src/infrastructure/database/connection.py` | True async connection management |
| `src/infrastructure/database/migrator.py` | Async migrations |
| `src/infrastructure/database/initializer.py` | Async initialization |
| `src/infrastructure/repositories/sqlite_user_repository.py` | Use async base |
| `src/infrastructure/repositories/sqlite_message_repository.py` | Use async base |
| `src/infrastructure/container.py` | Async connection factory |
| `src/bootstrap.py` | Async database setup |
| `src/main.py` | Async initialization |
| `tests/conftest.py` | Async mock fixtures |
| `tests/unit/infrastructure/test_repositories.py` | Async tests |
| `tests/unit/infrastructure/test_migrations.py` | Async tests |

### Files Deleted
| File | Reason |
|------|--------|
| `async_sqlite_base.py` | Replaced by proper aiosqlite in base |
| `memory_repository.py` | Dead code, not used anywhere |

## Technical Details

**Before (fake async):**
```python
async def _fetchone(self, sql: str, params: tuple = ()) -> Any | None:
    def _fetch():
        cursor = self._connection.execute(sql, params)
        return cursor.fetchone()
    return await loop.run_in_executor(self._executor, _fetch)  # Blocking in thread
```

**After (true async):**
```python
async def _fetchone(self, sql: str, params: Sequence[Any] = ()) -> Any | None:
    cursor = await self._connection.execute(sql, params)
    return await cursor.fetchone()  # Truly non-blocking
```

## Verification

- ✅ All 45 tests pass
- ✅ Pylint rating: 10.00/10
- ✅ Pre-commit hooks pass
- ✅ Type checking (mypy) passes

## Rationale

Chainlit is built on async/await patterns. Using sync SQLite operations in async methods was blocking the event loop. This migration ensures proper non-blocking database operations throughout the application.
