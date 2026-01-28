"""Logging utilities for Steadfast SDK."""

import logging
import re


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def sanitize_log_message(message: str) -> str:
    """Remove sensitive information from log messages."""
    # Remove API keys and secrets
    message = re.sub(
        r'api_key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]+["\']?',
        "api_key=***",
        message,
        flags=re.IGNORECASE,
    )
    message = re.sub(
        r'secret_key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]+["\']?',
        "secret_key=***",
        message,
        flags=re.IGNORECASE,
    )

    # Remove authorization headers
    message = re.sub(
        r'authorization["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\s-]+["\']?',
        "authorization=***",
        message,
        flags=re.IGNORECASE,
    )

    return message
