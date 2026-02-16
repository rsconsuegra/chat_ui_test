"""Tests for database migrations."""

from collections.abc import AsyncGenerator
from datetime import datetime
from pathlib import Path

import aiosqlite
import pytest

from src.config.database import DatabaseConfig
from src.domain.errors.exceptions import StorageError
from src.infrastructure.database.migrator import (
    AsyncDatabaseMigrator,
    MigrationRecord,
    run_migrations,
)


@pytest.fixture(name="in_memory_db")
async def fixture_in_memory_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Create in-memory database for testing.

    Yields:
        In-memory SQLite connection.
    """
    conn = await aiosqlite.connect(":memory:")
    conn.row_factory = aiosqlite.Row
    yield conn
    await conn.close()


@pytest.fixture(name="migrations_dir")
def fixture_migrations_dir(tmp_path: Path) -> Path:
    """Create temporary migrations directory.

    Args:
        tmp_path: Pytest temporary path fixture.

    Returns:
        Path to temporary migrations directory.
    """
    migrations_dir = tmp_path / "migrations"
    migrations_dir.mkdir()
    return migrations_dir


async def test_migrator_creates_tracking_table(
    in_memory_db: aiosqlite.Connection,
) -> None:
    """Test that migrator creates schema_migrations tracking table.

    Args:
        in_memory_db: In-memory SQLite connection.
    """
    migrator = AsyncDatabaseMigrator(in_memory_db)
    await migrator.migrate()

    cursor = await in_memory_db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_migrations'")
    result = await cursor.fetchone()

    assert result is not None


async def test_migrator_applies_sql_files(
    in_memory_db: aiosqlite.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator applies SQL migration files.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    migration_file = migrations_dir / "001_test_migration.sql"
    migration_file.write_text(
        """
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        """
    )

    migrator = AsyncDatabaseMigrator(in_memory_db, migrations_dir)
    await migrator.migrate()

    cursor = await in_memory_db.execute("SELECT name FROM sqlite_master WHERE name='test_table'")
    result = await cursor.fetchone()

    assert result is not None


async def test_migrator_tracks_applied_migrations(
    in_memory_db: aiosqlite.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator tracks which migrations have been applied.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    migration_file = migrations_dir / "002_test_tracking.sql"
    migration_file.write_text("CREATE TABLE test_tracking (id INTEGER);")

    migrator = AsyncDatabaseMigrator(in_memory_db, migrations_dir)
    await migrator.migrate()

    history = await migrator.get_migration_history()

    assert len(history) > 0
    assert any(m.migration_id == "002_test_tracking" for m in history)


async def test_migrator_skips_already_applied(
    in_memory_db: aiosqlite.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator skips migrations that are already applied.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    migration_file = migrations_dir / "003_skip_test.sql"
    migration_file.write_text("CREATE TABLE skip_test (id INTEGER);")

    migrator = AsyncDatabaseMigrator(in_memory_db, migrations_dir)

    await migrator.migrate()
    await migrator.migrate()

    history = await migrator.get_migration_history()

    skip_count = sum(1 for m in history if m.migration_id == "003_skip_test")
    assert skip_count == 1


async def test_migrator_applies_migrations_in_order(
    in_memory_db: aiosqlite.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrations are applied in alphabetical order.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    migration_files = [
        ("002_second.sql", "CREATE TABLE second (id INTEGER);"),
        ("001_first.sql", "CREATE TABLE first (id INTEGER);"),
        ("003_third.sql", "CREATE TABLE third (id INTEGER);"),
    ]

    for filename, sql in migration_files:
        (migrations_dir / filename).write_text(sql)

    migrator = AsyncDatabaseMigrator(in_memory_db, migrations_dir)
    await migrator.migrate()

    history = await migrator.get_migration_history()

    migration_ids = [m.migration_id for m in history]
    expected_order = ["001_first", "002_second", "003_third"]

    assert migration_ids == expected_order


async def test_migrator_handles_invalid_sql(
    in_memory_db: aiosqlite.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator raises StorageError on invalid SQL.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    invalid_file = migrations_dir / "004_invalid.sql"
    invalid_file.write_text("INVALID SQL SYNTAX;")

    migrator = AsyncDatabaseMigrator(in_memory_db, migrations_dir)

    with pytest.raises(StorageError, match="Failed to apply migration 004_invalid"):
        await migrator.migrate()


def test_migration_record_dataclass() -> None:
    """Test MigrationRecord dataclass creation."""
    record = MigrationRecord(
        id=1,
        migration_id="001_initial",
        applied_at=datetime(2025, 1, 1, 12, 0, 0),
    )

    assert record.id == 1
    assert record.migration_id == "001_initial"
    assert record.applied_at == datetime(2025, 1, 1, 12, 0, 0)


async def test_run_migrations_with_config(
    migrations_dir: Path,
) -> None:
    """Test run_migrations function with DatabaseConfig.

    Args:
        migrations_dir: Path to temporary migrations directory.
    """
    migration_file = migrations_dir / "001_test_run.sql"
    migration_file.write_text("CREATE TABLE test_run (id INTEGER);")

    db_path = migrations_dir / "test.db"

    config = DatabaseConfig(path=str(db_path))
    await run_migrations(config, migrations_dir)

    async with aiosqlite.connect(str(db_path)) as conn:
        cursor = await conn.execute("SELECT name FROM sqlite_master WHERE name='test_run'")
        result = await cursor.fetchone()

    assert result is not None


async def test_migrator_handles_missing_migrations_dir(
    in_memory_db: aiosqlite.Connection,
    tmp_path: Path,
) -> None:
    """Test that migrator handles missing migrations directory gracefully.

    Args:
        in_memory_db: In-memory SQLite connection.
        tmp_path: Pytest temporary path fixture.
    """
    nonexistent_dir = tmp_path / "nonexistent"

    migrator = AsyncDatabaseMigrator(in_memory_db, nonexistent_dir)

    await migrator.migrate()

    history = await migrator.get_migration_history()
    assert len(history) == 0
