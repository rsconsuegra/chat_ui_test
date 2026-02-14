"""Provider-related configuration settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProviderConfig(BaseSettings):
    """Configuration for LLM providers with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

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


class AgentaAIConfig(BaseSettings):
    """Configuration for AgentaAI integration with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str | None = Field(
        default=None,
        description="API key for AgentaAI (optional)",
    )
    base_url: str = Field(
        default="https://api.agenta.ai",
        description="Base URL for AgentaAI API",
    )


class Mem0Config(BaseSettings):
    """Configuration for Mem0 integration with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = Field(
        default="http://localhost:8080",
        description="Base URL for Mem0 API",
    )
    enabled: bool = Field(
        default=False,
        description="Whether Mem0 memory integration is enabled",
    )


__all__ = ["ProviderConfig", "AgentaAIConfig", "Mem0Config"]
