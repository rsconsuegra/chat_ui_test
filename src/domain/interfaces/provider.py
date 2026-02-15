"""Provider interface defining the contract for LLM providers.

This module defines the abstract interface that all LLM providers must implement,
ensuring a consistent API across different provider implementations.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from src.domain.models.provider_message import ProviderMessage


class Provider(ABC):
    """Abstract base class for LLM providers.

    This interface defines the contract that all LLM provider implementations
    must follow, ensuring consistent behavior across different providers
    (Ollama, OpenRouter, Z.ai, etc.).

    The interface supports both streaming and non-streaming responses,
    allowing implementations to choose the most appropriate approach
    for their underlying API.
    """

    @abstractmethod
    def stream_response(
        self,
        messages: list[ProviderMessage],
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        """Stream response from provider.

        Args:
            messages: List of messages forming conversation context
            system_prompt: Optional system prompt to guide model's behavior

        Yields:
            Chunks of response as they become available

        Raises:
            ProviderError: If provider fails to generate a response
        """
        raise NotImplementedError

    @abstractmethod
    async def complete(
        self,
        messages: list[ProviderMessage],
        system_prompt: str | None = None,
    ) -> str:
        """Get complete response from the provider.

        This method should accumulate the streamed response into a single string.

        Args:
            messages: List of messages forming the conversation context
            system_prompt: Optional system prompt to guide the model's behavior

        Returns:
            The complete response as a single string

        Raises:
            ProviderError: If the provider fails to generate a response
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this provider.

        Returns:
            String identifier for the provider (e.g., 'ollama', 'openrouter')
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> str:
        """Get the model identifier used by this provider.

        Returns:
            String identifier for the model (e.g., 'llama3.1', 'gpt-4')
        """
        raise NotImplementedError


# Backward compatibility alias
IProvider = Provider
