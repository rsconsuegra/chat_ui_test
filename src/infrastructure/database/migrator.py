"""Database migration manager for SQL-based migrations."""

from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from pathlib import Path

import aiosqlite

from src.config.database import DatabaseConfig
from src.domain.errors.exceptions import StorageError

logger = getLogger(__name__)

DEFAULT_MIGRATIONS_DIR = Path("migrations")


@dataclass(frozen=True, kw_only=True)
class MigrationRecord:
    """Record of applied migration."""

    id: int
    migration_id: str
    applied_at: datetime


class AsyncDatabaseMigrator:
    """Handles async database migration execution and tracking."""

    def __init__(
        self,
        connection: aiosqlite.Connection,
        migrations_dir: Path = DEFAULT_MIGRATIONS_DIR,
    ) -> None:
        """Initialize database migrator.

        Args:
            connection: aiosqlite database connection.
            migrations_dir: Directory containing SQL migration files.
        """
        self.connection = connection
        self.migrations_dir = migrations_dir
        self._migration_table_name = "schema_migrations"

    async def migrate(self) -> None:
        """Apply all pending migrations.

        Raises:
            StorageError: If migration fails.
        """
        try:
            await self._ensure_migrations_table()
            applied_migrations = await self._get_applied_migrations()
            pending_migrations = self._get_pending_migrations(applied_migrations)

            for migration_file in pending_migrations:
                await self._apply_migration(migration_file)
                logger.info("Applied migration: %s", migration_file.stem)
        except aiosqlite.Error as e:
            raise StorageError(f"Migration failed: {e}") from e

    async def _ensure_migrations_table(self) -> None:
        """Create migrations tracking table if it doesn't exist."""
        await self.connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._migration_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_id TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self.connection.commit()

    async def _get_applied_migrations(self) -> set[str]:
        """Get set of applied migration IDs.

        Returns:
            Set of migration IDs that have been applied.
        """
        cursor = await self.connection.execute(f"SELECT migration_id FROM {self._migration_table_name}")
        rows = await cursor.fetchall()
        return {row[0] for row in rows}

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

    async def _apply_migration(self, migration_file: Path) -> None:
        """Apply a single migration file.

        Args:
            migration_file: Path to migration SQL file.

        Raises:
            StorageError: If migration execution fails.
        """
        migration_id = migration_file.stem

        try:
            sql_content = migration_file.read_text()

            await self.connection.executescript(sql_content)

            await self.connection.execute(
                f"INSERT INTO {self._migration_table_name} (migration_id) VALUES (?)",
                (migration_id,),
            )

            await self.connection.commit()

        except (OSError, aiosqlite.Error) as e:
            raise StorageError(f"Failed to apply migration {migration_id}: {e}") from e

    async def get_migration_history(self) -> list[MigrationRecord]:
        """Get history of applied migrations.

        Returns:
            List of migration records in order of application.
        """
        cursor = await self.connection.execute(f"""
            SELECT id, migration_id, applied_at
            FROM {self._migration_table_name}
            ORDER BY id ASC
        """)
        rows = await cursor.fetchall()

        records = []
        for row in rows:
            record = MigrationRecord(
                id=row[0],
                migration_id=row[1],
                applied_at=datetime.fromisoformat(row[2]),
            )
            records.append(record)

        return records


async def run_migrations(
    config: DatabaseConfig,
    migrations_dir: Path | None = None,
) -> None:
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
        connection = await aiosqlite.connect(config.path)
        connection.row_factory = aiosqlite.Row

        migrator = AsyncDatabaseMigrator(connection, migrations_dir)
        await migrator.migrate()

        await connection.close()
    except aiosqlite.Error as e:
        raise StorageError(f"Migration execution failed: {e}") from e
