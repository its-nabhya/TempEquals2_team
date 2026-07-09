"""
Logging utilities.

Provides a single place to configure application logging.
"""

from __future__ import annotations

import logging


def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure application-wide logging.

    Parameters
    ----------
    log_level:
        Logging level (INFO, DEBUG, WARNING, ERROR).
    """

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )