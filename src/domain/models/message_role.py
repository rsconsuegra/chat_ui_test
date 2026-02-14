"""Enumeration for message roles in chat conversations."""

from enum import Enum


class MessageRole(Enum):
    """Enumeration for message roles in chat conversations."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
