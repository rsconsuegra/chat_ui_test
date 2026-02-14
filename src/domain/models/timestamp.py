"""Domain model for Timestamp value object."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True, frozen=True)
class Timestamp:
    """Value object representing a point in time."""

    value: datetime

    @classmethod
    def now(cls) -> "Timestamp":
        """Create a timestamp for the current time.

        Returns:
            A new Timestamp representing the current time.
        """
        return cls(value=datetime.now())

    def __str__(self) -> str:
        """Return ISO format string representation.

        Returns:
            ISO format string representation of the timestamp.
        """
        return self.value.isoformat()

    def isoformat(self) -> str:
        """Return ISO format string representation of the datetime value.

        Returns:
            ISO format string.
        """
        return self.value.isoformat()

    def __lt__(self, other: "Timestamp") -> bool:
        """Compare timestamps for less than.

        Args:
            other: Another timestamp to compare against.

        Returns:
            True if this timestamp is earlier than the other.
        """
        return self.value < other.value

    def __gt__(self, other: "Timestamp") -> bool:
        """Compare timestamps for greater than.

        Args:
            other: Another timestamp to compare against.

        Returns:
            True if this timestamp is later than the other.
        """
        return self.value > other.value

    def __le__(self, other: "Timestamp") -> bool:
        """Compare timestamps for less than or equal.

        Args:
            other: Another timestamp to compare against.

        Returns:
            True if this timestamp is earlier than or equal to the other.
        """
        return self.value <= other.value

    def __ge__(self, other: "Timestamp") -> bool:
        """Compare timestamps for greater than or equal.

        Args:
            other: Another timestamp to compare against.

        Returns:
            True if this timestamp is later than or equal to the other.
        """
        return self.value >= other.value

    def __eq__(self, other: object) -> bool:
        """Compare timestamps for equality.

        Args:
            other: Another timestamp to compare against.

        Returns:
            True if timestamps are equal.
        """
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        """Return hash value for the timestamp.

        Returns:
            Hash of the underlying datetime.
        """
        return hash(self.value)
