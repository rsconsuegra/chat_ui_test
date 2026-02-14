"""Base LangChain provider implementation."""

from abc import abstractmethod
from collections.abc import AsyncIterator

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    HumanMessage,
    SystemMessage,
)

from src.domain.interfaces.provider import Provider, ProviderMessage
from src.domain.models.message_role import MessageRole


class BaseLangChainProvider(Provider):
    """Base class for LangChain-based LLM providers.

    This abstract base class provides common functionality for all providers
    that use LangChain's chat model interface, handling message conversion
    and streaming.

    Subclasses must provide the LangChain chat model instance and implement
    the name and model properties.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        """Initialize the provider with a LangChain chat model.

        Args:
            llm: Configured LangChain chat model instance
        """
        self._llm = llm

    async def stream_response(  # pylint: disable=W0236
        self,
        messages: list[ProviderMessage],
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        """Stream response from the LangChain model.

        Args:
            messages: List of messages forming conversation context
            system_prompt: Optional system prompt to guide model's behavior

        Yields:
            Chunks of response as they become available

        """
        lc_messages = self._convert_messages(messages, system_prompt)
        async for chunk in self._llm.astream(lc_messages):
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield str(chunk.content)

    async def complete(
        self,
        messages: list[ProviderMessage],
        system_prompt: str | None = None,
    ) -> str:
        """Get complete response from the LangChain model.

        Args:
            messages: List of messages forming the conversation context
            system_prompt: Optional system prompt to guide the model's behavior

        Returns:
            The complete response as a single string

        """
        lc_messages = self._convert_messages(messages, system_prompt)
        response = await self._llm.ainvoke(lc_messages)
        return str(response.content)

    def _convert_messages(
        self,
        messages: list[ProviderMessage],
        system_prompt: str | None = None,
    ) -> list[HumanMessage | SystemMessage | AIMessage]:
        """Convert provider messages to LangChain message format.

        Args:
            messages: List of provider messages to convert
            system_prompt: Optional system prompt to prepend

        Returns:
            List of LangChain message objects
        """
        lc_messages: list[HumanMessage | SystemMessage | AIMessage] = []

        if system_prompt:
            lc_messages.append(SystemMessage(content=system_prompt))

        for msg in messages:
            match msg.role:
                case MessageRole.USER:
                    lc_messages.append(HumanMessage(content=msg.content))
                case MessageRole.ASSISTANT:
                    lc_messages.append(AIMessage(content=msg.content))
                case MessageRole.SYSTEM:
                    lc_messages.append(SystemMessage(content=msg.content))

        return lc_messages

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this provider."""

    @property
    @abstractmethod
    def model(self) -> str:
        """Get the model identifier used by this provider."""
