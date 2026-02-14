"""Database migration manager for SQL-based migrations."""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.config.database import DatabaseConfig
from src.domain.errors.exceptions import StorageError

DEFAULT_MIGRATIONS_DIR = Path("migrations")


@dataclass(frozen=True, kw_only=True)
class MigrationRecord:
    """Record of applied migration."""

    id: int
    migration_id: str
    applied_at: datetime


class DatabaseMigrator:
    """Handles database migration execution and tracking."""

    def __init__(
        self,
        connection: sqlite3.Connection,
        migrations_dir: Path = DEFAULT_MIGRATIONS_DIR,
    ) -> None:
        """Initialize database migrator.

        Args:
            connection: SQLite database connection.
            migrations_dir: Directory containing SQL migration files.
        """
        self.connection = connection
        self.migrations_dir = migrations_dir
        self._migration_table_name = "schema_migrations"

    def migrate(self) -> None:
        """Apply all pending migrations.

        Raises:
            StorageError: If migration fails.
        """
        try:
            self._ensure_migrations_table()
            applied_migrations = self._get_applied_migrations()
            pending_migrations = self._get_pending_migrations(applied_migrations)

            for migration_file in pending_migrations:
                self._apply_migration(migration_file)
        except sqlite3.Error as e:
            raise StorageError(f"Migration failed: {e}") from e

    def _ensure_migrations_table(self) -> None:
        """Create migrations tracking table if it doesn't exist."""
        cursor = self.connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._migration_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_id TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def _get_applied_migrations(self) -> set[str]:
        """Get set of applied migration IDs.

        Returns:
            Set of migration IDs that have been applied.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT migration_id FROM {self._migration_table_name}")
        return {row[0] for row in cursor.fetchall()}

    def _get_pending_migrations(self, applied_migrations: set[str]) -> list[Path]:
        """Get list of pending migration files.

        Args:
            applied_migrations: Set of already applied migration IDs.

        Returns:
            List of migration file paths in order.
        """
        if not self.migrations_dir.exists():
            return []

        migration_files = sorted(self.migrations_dir.glob("*.sql"))

        pending = []
        for migration_file in migration_files:
            migration_id = migration_file.stem
            if migration_id not in applied_migrations:
                pending.append(migration_file)

        return pending

    def _apply_migration(self, migration_file: Path) -> None:
        """Apply a single migration file.

        Args:
            migration_file: Path to migration SQL file.

        Raises:
            StorageError: If migration execution fails.
        """
        migration_id = migration_file.stem

        try:
            sql_content = migration_file.read_text()

            cursor = self.connection.cursor()
            cursor.executescript(sql_content)

            cursor.execute(
                f"INSERT INTO {self._migration_table_name} (migration_id) VALUES (?)",
                (migration_id,),
            )

            self.connection.commit()

        except (OSError, sqlite3.Error) as e:
            raise StorageError(f"Failed to apply migration {migration_id}: {e}") from e

    def get_migration_history(self) -> list[MigrationRecord]:
        """Get history of applied migrations.

        Returns:
            List of migration records in order of application.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT id, migration_id, applied_at
            FROM {self._migration_table_name}
            ORDER BY id ASC
        """)

        records = []
        for row in cursor.fetchall():
            record = MigrationRecord(
                id=row[0],
                migration_id=row[1],
                applied_at=datetime.fromisoformat(row[2]),
            )
            records.append(record)

        return records


def run_migrations(config: DatabaseConfig, migrations_dir: Path | None = None) -> None:
    """Run all pending migrations for database.

    Args:
        config: Database configuration.
        migrations_dir: Directory containing SQL migration files.

    Raises:
        StorageError: If migration fails.
    """
    if migrations_dir is None:
        migrations_dir = Path("migrations")
    try:
        connection = sqlite3.connect(config.path, check_same_thread=False)
        connection.row_factory = sqlite3.Row

        migrator = DatabaseMigrator(connection, migrations_dir)
        migrator.migrate()

        connection.close()
    except sqlite3.Error as e:
        raise StorageError(f"Migration execution failed: {e}") from e
