"""Use case for resolving system prompts."""

# pylint: disable=too-few-public-methods

from src.config.prompts import PromptConfig


class GetSystemPromptUseCase:
    """Resolve system prompt for chat context.

    This use case is async to support future AgentaAI integration
    in Phase 3, where prompts may be fetched from a remote service.
    """

    def __init__(self, *, prompt_config: PromptConfig) -> None:
        """Initialize the use case.

        Args:
            prompt_config: Configuration for system prompts.
        """
        self._prompt_config = prompt_config

    async def execute(self, *, variant: str | None = None) -> str:
        """Resolve the system prompt.

        Args:
            variant: Optional prompt variant key.

        Returns:
            Resolved system prompt string.
        """
        return self._prompt_config.resolve_system_prompt(variant)
