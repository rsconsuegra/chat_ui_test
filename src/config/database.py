"""Database configuration settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """Configuration for database connection with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    path: str = Field(
        default="./chat_history.db",
        description="Path to the SQLite database file",
    )

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Create configuration from environment variables.

        Returns:
            DatabaseConfig instance loaded from environment.
        """
        return cls()
