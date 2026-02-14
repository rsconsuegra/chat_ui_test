"""Use case for sending a message through a provider."""

from collections.abc import AsyncIterator

from src.config.prompts import PromptConfig
from src.domain.errors.exceptions import ProviderError
from src.domain.interfaces.provider import Provider, ProviderMessage
from src.domain.models.chat_message import ChatMessage
from src.domain.models.message_role import MessageRole
from src.domain.repositories.message_repository import IMessageRepository


class SendMessageUseCase:  # pylint: disable=too-few-public-methods
    """Handle sending a message and streaming provider responses."""

    def __init__(
        self,
        *,
        message_repository: IMessageRepository,
        provider: Provider,
        prompt_config: PromptConfig,
    ) -> None:
        """Initialize the use case.

        Args:
            message_repository: Repository for chat messages.
            provider: Provider used to generate responses.
            prompt_config: Prompt configuration.
        """
        self._message_repository = message_repository
        self._provider = provider
        self._prompt_config = prompt_config

    async def stream_response(
        self,
        *,
        user_id: int,
        user_input: str,
        prompt_variant: str | None = None,
        history_limit: int = 50,
    ) -> AsyncIterator[str]:
        """Persist user input, stream provider response, and persist output.

        Args:
            user_id: The ID of the user sending the message.
            user_input: The content of the user's message.
            prompt_variant: Optional prompt variant name.
            history_limit: Max number of historical messages to include.

        Yields:
            Streamed response tokens from the provider.

        Raises:
            ProviderError: If the provider fails to stream a response.
        """
        user_message = ChatMessage.create(
            user_id=user_id,
            provider=self._provider.name,
            role=MessageRole.USER,
            content=user_input,
        )
        await self._message_repository.save(user_message)

        history = await self._message_repository.find_by_user_id(
            user_id,
            limit=history_limit,
            offset=0,
        )

        system_prompt = self._prompt_config.resolve_system_prompt(prompt_variant)
        provider_messages = [ProviderMessage(role=MessageRole.SYSTEM, content=system_prompt)]

        for message in reversed(history):
            provider_messages.append(ProviderMessage(role=message.role, content=message.content))

        response_chunks: list[str] = []

        try:
            async for token in self._provider.stream_response(provider_messages):
                response_chunks.append(token)
                yield token
        except ProviderError:
            raise
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise ProviderError(f"Provider stream failed: {exc}") from exc

        response_text = "".join(response_chunks)

        assistant_message = ChatMessage.create(
            user_id=user_id,
            provider=self._provider.name,
            role=MessageRole.ASSISTANT,
            content=response_text,
        )
        await self._message_repository.save(assistant_message)
