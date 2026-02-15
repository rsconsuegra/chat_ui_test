"""Chainlit message adapter implementation."""

import chainlit as cl

from src.domain.interfaces.frontend_adapter import IMessageAdapter, IStreamingMessage


class ChainlitStreamingMessage(IStreamingMessage):
    """Chainlit-specific streaming message implementation.

    Wraps Chainlit's Message class to provide incremental output.
    """

    def __init__(self) -> None:
        """Initialize the streaming message."""
        self._message = cl.Message(content="")

    async def stream_token(self, token: str) -> None:
        """Append a token to the streaming message.

        Args:
            token: Text chunk to append.
        """
        await self._message.stream_token(token)

    async def send(self) -> None:
        """Finalize and send the message."""
        await self._message.send()


class ChainlitMessageAdapter(IMessageAdapter):
    """Chainlit-specific message handling implementation.

    This adapter wraps Chainlit's message APIs to provide a
    frontend-agnostic interface for message display.
    """

    async def send_message(self, content: str) -> None:
        """Send a complete message to the user.

        Args:
            content: Message content to display.
        """
        await cl.Message(content=content).send()

    def create_streaming_message(self) -> ChainlitStreamingMessage:
        """Create a new streaming message for incremental output.

        Returns:
            ChainlitStreamingMessage instance.
        """
        return ChainlitStreamingMessage()
