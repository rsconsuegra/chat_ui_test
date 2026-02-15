"""Ollama provider implementation using LangChain."""

from langchain_ollama import ChatOllama

from src.infrastructure.adapters.providers.base.langchain_base import (
    BaseLangChainProvider,
)


class OllamaLangChainProvider(BaseLangChainProvider):
    """Ollama provider using LangChain's ChatOllama.

    This provider connects to a local Ollama instance using LangChain's
    native Ollama integration.
    """

    def __init__(self, base_url: str, model: str) -> None:
        """Initialize the Ollama LangChain provider.

        Args:
            base_url: Base URL for Ollama API (e.g., http://localhost:11434)
            model: Model name to use (e.g., llama3.1)
        """
        llm = ChatOllama(base_url=base_url, model=model)
        super().__init__(llm)
        self._model_name = model

    @property
    def name(self) -> str:
        """Provider name identifier.

        Returns:
            str: The name of the provider
        """
        return "ollama"

    @property
    def model(self) -> str:
        """Model identifier.

        Returns:
            str: The model name used by the provider
        """
        return self._model_name
