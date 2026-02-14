"""Application bootstrap utilities."""

from logging import getLogger

from src.config import AppConfig, get_config
from src.infrastructure.container import Container
from src.infrastructure.database.connection import init_database
from src.infrastructure.logging import configure_logging

logger = getLogger(__name__)

# Module-level singleton instance (not a constant, hence lowercase)
_container: Container | None = None  # pylint: disable=invalid-name


def build_container(*, config: AppConfig | None = None) -> Container:
    """Build a new application container.

    Args:
        config: Optional configuration override.

    Returns:
        Configured container instance.
    """
    configure_logging()
    resolved_config = config or get_config()
    init_database(resolved_config)
    container = Container(config=resolved_config)
    logger.info("Container initialized")
    return container


def get_container(*, config: AppConfig | None = None) -> Container:  # pylint: disable=global-statement
    """Get a shared container instance.

    Args:
        config: Optional configuration override.

    Returns:
        Shared container instance.
    """
    global _container  # pylint: disable=global-statement
    if _container is None:
        _container = build_container(config=config)
    return _container


def reset_container() -> None:
    """Reset the shared container instance."""
    global _container  # pylint: disable=global-statement
    _container = None
