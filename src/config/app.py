"""Application configuration aggregation."""

# pylint: disable=duplicate-code
# TECH-DEBT-001: Duplicate provider field definitions with providers.py

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.database import DatabaseConfig
from src.config.providers import AgentaAIConfig, Mem0Config, ProviderConfig


class AppConfig(BaseSettings):
    """Root application configuration aggregating all settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database settings
    database_path: str = Field(
        default="./chat_history.db",
        description="Path to the SQLite database file",
    )

    # Provider settings
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for Ollama API",
    )
    ollama_model: str = Field(
        default="llama3.1",
        description="Default Ollama model to use",
    )
    openrouter_api_key: str | None = Field(
        default=None,
        description="API key for OpenRouter (optional)",
    )
    zai_api_key: str | None = Field(
        default=None,
        description="API key for ZAI (optional)",
    )

    # AgentaAI settings
    agenta_api_key: str | None = Field(
        default=None,
        description="API key for AgentaAI (optional)",
    )
    agenta_base_url: str = Field(
        default="https://api.agenta.ai",
        description="Base URL for AgentaAI API",
    )

    # Mem0 settings
    mem0_base_url: str = Field(
        default="http://localhost:8080",
        description="Base URL for Mem0 API",
    )
    mem0_enabled: bool = Field(
        default=False,
        description="Whether Mem0 memory integration is enabled",
    )

    @property
    def database_config(self) -> DatabaseConfig:
        """Get database configuration subset.

        Returns:
            Database configuration with path.
        """
        return DatabaseConfig(path=self.database_path)

    @property
    def provider_config(self) -> ProviderConfig:
        """Get provider configuration subset.

        Returns:
            Provider configuration with URLs and API keys.
        """
        return ProviderConfig(
            ollama_base_url=self.ollama_base_url,
            ollama_model=self.ollama_model,
            openrouter_api_key=self.openrouter_api_key,
            zai_api_key=self.zai_api_key,
        )

    @property
    def agenta_config(self) -> AgentaAIConfig:
        """Get AgentaAI configuration subset.

        Returns:
            AgentaAI configuration with API key and base URL.
        """
        return AgentaAIConfig(
            api_key=self.agenta_api_key,
            base_url=self.agenta_base_url,
        )

    @property
    def mem0_config(self) -> Mem0Config:
        """Get Mem0 configuration subset.

        Returns:
            Mem0 configuration with base URL and enabled flag.
        """
        return Mem0Config(
            base_url=self.mem0_base_url,
            enabled=self.mem0_enabled,
        )


def get_config() -> AppConfig:
    """Get the application configuration singleton.

    Returns:
        AppConfig instance loaded from environment variables.
    """
    return AppConfig()


__all__ = ["AppConfig", "get_config"]
