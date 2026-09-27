"""Structured logging setup for AQUARYS."""

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Configure standard structured logging."""
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=log_format,
        stream=sys.stdout,
        force=True,
    )


logger = logging.getLogger("aquarys")
