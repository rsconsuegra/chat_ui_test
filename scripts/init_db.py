"""Database initialization script."""

from src.infrastructure.database.connection import init_database


def main() -> None:
    """Initialize the database.

    Raises:
        Exception: If database initialization fails.
    """
    print("Initializing database...")
    try:
        init_database()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    main()
