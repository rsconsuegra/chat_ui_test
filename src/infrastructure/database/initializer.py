"""Database initialization wrapper for migration-based approach.

This module provides backward compatibility while delegating to the migration system.
"""

from logging import getLogger
from pathlib import Path

from src.config.app import AppConfig
from src.domain.errors.exceptions import StorageError
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.migrator import AsyncDatabaseMigrator

_DEFAULT_MIGRATIONS_DIR: Path = Path("migrations")
logger = getLogger(__name__)


async def initialize_database(
    config: AppConfig,
    migrations_dir: Path | None = None,
) -> DatabaseConnection:
    """Initialize database connection and run migrations.

    Args:
        config: Database configuration.
        migrations_dir: Directory containing SQL migration files.

    Returns:
        Initialized database connection.

    Raises:
        StorageError: If initialization or migration fails.
    """
    migrations_path = migrations_dir if migrations_dir is not None else _DEFAULT_MIGRATIONS_DIR

    try:
        connection = DatabaseConnection(config)
        await connection.init()

        async with connection.get_connection() as conn:
            migrator = AsyncDatabaseMigrator(conn, migrations_path)
            await migrator.migrate()

        return connection
    except Exception as exc:
        logger.exception("Database initialization failed")
        raise StorageError(f"Database initialization failed: {exc}") from exc
