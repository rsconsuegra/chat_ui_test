"""Database initialization script."""

import asyncio

from src.config.database import DatabaseConfig
from src.infrastructure.database.connection import init_database


async def async_main() -> None:
    """Initialize the database asynchronously.

    Raises:
        Exception: If database initialization fails.
    """
    print("Initializing database...")
    try:
        config = DatabaseConfig()
        await init_database(config)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise


def main() -> None:
    """Entry point for database initialization."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
