"""Domain model for User entity."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class User:
    """User entity representing application users."""

    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    @property
    def normalized_username(self) -> str:
        """Return username in lowercase for case-insensitive comparison.

        Returns:
            The lowercase version of the username.
        """
        return self.username.lower()

    @classmethod
    def create_new(cls, username: str) -> "User":
        """Create a new user with current timestamps.

        Args:
            username: The username for the new user.

        Returns:
            User entity with created_at and updated_at set to now.
        """
        now = datetime.now()
        return cls(
            id=0,
            username=username,
            created_at=now,
            updated_at=now,
        )

    def update_timestamp(self) -> "User":
        """Return a new User instance with updated timestamp.

        Returns:
            User entity with updated_at set to current time.
        """
        return User(
            id=self.id,
            username=self.username,
            created_at=self.created_at,
            updated_at=datetime.now(),
        )
