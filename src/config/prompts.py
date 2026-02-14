"""Prompt configuration for chat interactions."""

from dataclasses import dataclass

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant in a cleanly layered chat application. Answer clearly, be concise, and avoid unsafe content."
)


@dataclass(frozen=True, kw_only=True)
class PromptConfig:
    """Configuration for system prompts and variants.

    Args:
        system_prompt: The default system prompt used for conversations.
        variants: Named prompt variants for specialized behaviors.
    """

    system_prompt: str
    variants: dict[str, str]

    @classmethod
    def default(cls) -> "PromptConfig":
        """Create a default prompt configuration.

        Returns:
            PromptConfig with default prompts.
        """
        return cls(
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            variants={
                "concise": "Be direct and keep responses brief.",
                "explanatory": "Explain reasoning step by step with examples.",
            },
        )

    def resolve_system_prompt(self, variant: str | None = None) -> str:
        """Resolve the system prompt for a given variant.

        Args:
            variant: Optional prompt variant key.

        Returns:
            The resolved system prompt string.
        """
        if variant is None:
            return self.system_prompt

        return self.variants.get(variant, self.system_prompt)
