"""Repository interfaces defining ports for data persistence."""

from src.domain.repositories.message_repository import IMessageRepository
from src.domain.repositories.user_repository import IUserRepository

__all__ = [
    "IMessageRepository",
    "IUserRepository",
]
