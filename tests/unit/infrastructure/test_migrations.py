"""Tests for database migrations."""

import sqlite3
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import pytest

from src.config.database import DatabaseConfig
from src.domain.errors.exceptions import StorageError
from src.infrastructure.database.migrator import (
    DatabaseMigrator,
    MigrationRecord,
    run_migrations,
)


@pytest.fixture(name="in_memory_db")
def fixture_in_memory_db() -> Generator[sqlite3.Connection, None, None]:
    """Create in-memory database for testing.

    Yields:
        In-memory SQLite connection.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


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


def test_migrator_creates_tracking_table(
    in_memory_db: sqlite3.Connection,
) -> None:
    """Test that migrator creates schema_migrations tracking table.

    Args:
        in_memory_db: In-memory SQLite connection.
    """
    migrator = DatabaseMigrator(in_memory_db)
    migrator.migrate()

    cursor = in_memory_db.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_migrations'").fetchone()

    assert result is not None


def test_migrator_applies_sql_files(  # pylint: disable=redefined-outer-name
    in_memory_db: sqlite3.Connection,
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

    migrator = DatabaseMigrator(in_memory_db, migrations_dir)
    migrator.migrate()

    cursor = in_memory_db.cursor()
    result = cursor.execute("SELECT name FROM sqlite_master WHERE name='test_table'").fetchone()

    assert result is not None


def test_migrator_tracks_applied_migrations(  # pylint: disable=redefined-outer-name
    in_memory_db: sqlite3.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator tracks which migrations have been applied.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    migration_file = migrations_dir / "002_test_tracking.sql"
    migration_file.write_text("CREATE TABLE test_tracking (id INTEGER);")

    migrator = DatabaseMigrator(in_memory_db, migrations_dir)
    migrator.migrate()

    history = migrator.get_migration_history()

    assert len(history) > 0
    assert any(m.migration_id == "002_test_tracking" for m in history)


def test_migrator_skips_already_applied(  # pylint: disable=redefined-outer-name
    in_memory_db: sqlite3.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator skips migrations that are already applied.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    migration_file = migrations_dir / "003_skip_test.sql"
    migration_file.write_text("CREATE TABLE skip_test (id INTEGER);")

    migrator = DatabaseMigrator(in_memory_db, migrations_dir)

    migrator.migrate()
    migrator.migrate()

    history = migrator.get_migration_history()

    skip_count = sum(1 for m in history if m.migration_id == "003_skip_test")
    assert skip_count == 1


def test_migrator_applies_migrations_in_order(  # pylint: disable=redefined-outer-name
    in_memory_db: sqlite3.Connection,
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

    migrator = DatabaseMigrator(in_memory_db, migrations_dir)
    migrator.migrate()

    history = migrator.get_migration_history()

    migration_ids = [m.migration_id for m in history]
    expected_order = ["001_first", "002_second", "003_third"]

    assert migration_ids == expected_order


def test_migrator_handles_invalid_sql(  # pylint: disable=redefined-outer-name
    in_memory_db: sqlite3.Connection,
    migrations_dir: Path,
) -> None:
    """Test that migrator raises StorageError on invalid SQL.

    Args:
        in_memory_db: In-memory SQLite connection.
        migrations_dir: Path to temporary migrations directory.
    """
    invalid_file = migrations_dir / "004_invalid.sql"
    invalid_file.write_text("INVALID SQL SYNTAX;")

    migrator = DatabaseMigrator(in_memory_db, migrations_dir)

    with pytest.raises(StorageError, match="Failed to apply migration 004_invalid"):
        migrator.migrate()


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


def test_run_migrations_with_config(  # pylint: disable=redefined-outer-name,unused-argument
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
    run_migrations(config, migrations_dir)

    conn = sqlite3.connect(str(db_path))
    result = conn.execute("SELECT name FROM sqlite_master WHERE name='test_run'").fetchone()
    conn.close()

    assert result is not None


def test_migrator_handles_missing_migrations_dir(
    in_memory_db: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    """Test that migrator handles missing migrations directory gracefully.

    Args:
        in_memory_db: In-memory SQLite connection.
        tmp_path: Pytest temporary path fixture.
    """
    nonexistent_dir = tmp_path / "nonexistent"

    migrator = DatabaseMigrator(in_memory_db, nonexistent_dir)

    migrator.migrate()

    history = migrator.get_migration_history()
    assert len(history) == 0
