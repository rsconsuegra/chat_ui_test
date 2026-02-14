"""Factory for creating provider instances."""

from src.config.providers import ProviderConfig
from src.domain.interfaces.provider import Provider
from src.infrastructure.adapters.providers.ollama import OllamaLangChainProvider


def build_provider(config: ProviderConfig, name: str | None = None) -> Provider:  # pylint: disable=unused-argument
    """Build a provider instance based on configuration.

    Args:
        config: Provider configuration containing provider type and settings.
        name: Optional provider name identifier (for future provider selection).

    Returns:
        Configured provider instance.

    Note:
        Currently only Ollama provider is supported. The name parameter
        is reserved for future provider selection capabilities.
    """
    return OllamaLangChainProvider(
        base_url=config.ollama_base_url,
        model=config.ollama_model,
    )
