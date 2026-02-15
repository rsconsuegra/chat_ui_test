"""Session services for user initialization."""

from src.domain.models.user import User
from src.domain.repositories.user_repository import IUserRepository


class SessionService:
    """Service for session-level user operations."""

    def __init__(self, *, user_repository: IUserRepository) -> None:
        """Initialize the session service.

        Args:
            user_repository: Repository for user persistence.
        """
        self._user_repository = user_repository

    async def get_or_create_user(self, *, username: str) -> User:
        """Get or create a user for the provided username.

        Args:
            username: Username to resolve.

        Returns:
            The existing or newly created user.
        """
        return await self._user_repository.get_or_create(username)
