"""Logging configuration utilities."""

import logging
import os


def configure_logging(level: str | None = None) -> None:
    """Configure application logging.

    Args:
        level: Optional log level override.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:
        if level:
            root_logger.setLevel(level)
        return

    resolved_level = level or os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=resolved_level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
