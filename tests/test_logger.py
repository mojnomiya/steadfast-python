"""Tests for logger utilities."""

import logging
from steadfast.logger import get_logger, setup_logging, sanitize_log_message


class TestGetLogger:
    """Test logger creation."""

    def test_get_logger(self) -> None:
        """Test logger creation with name."""
        logger = get_logger("test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_logger_has_handler(self) -> None:
        """Test logger has handler configured."""
        logger = get_logger("test_handler")
        assert len(logger.handlers) > 0
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    def test_logger_level(self) -> None:
        """Test logger default level."""
        logger = get_logger("test_level")
        assert logger.level == logging.INFO


class TestSetupLogging:
    """Test logging setup."""

    def test_setup_logging_warning(self) -> None:
        """Test setup logging with WARNING level."""
        setup_logging("WARNING")
        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING


class TestSanitizeLogMessage:
    """Test credential sanitization."""

    def test_sanitize_api_key(self) -> None:
        """Test API key sanitization."""
        message = "Request with api_key=abc123def456"
        sanitized = sanitize_log_message(message)
        assert "abc123def456" not in sanitized
        assert "api_key=***" in sanitized

    def test_sanitize_secret_key(self) -> None:
        """Test secret key sanitization."""
        message = "Config: secret_key=xyz789abc123"
        sanitized = sanitize_log_message(message)
        assert "xyz789abc123" not in sanitized
        assert "secret_key=***" in sanitized

    def test_sanitize_authorization_header(self) -> None:
        """Test authorization header sanitization."""
        message = "Headers: authorization=Bearer token123"
        sanitized = sanitize_log_message(message)
        assert "token123" not in sanitized
        assert "authorization=***" in sanitized

    def test_sanitize_multiple_credentials(self) -> None:
        """Test multiple credential sanitization."""
        message = "api_key=key123 secret_key=secret456 authorization=auth789"
        sanitized = sanitize_log_message(message)
        assert "key123" not in sanitized
        assert "secret456" not in sanitized
        assert "auth789" not in sanitized
        assert sanitized.count("***") == 3

    def test_sanitize_no_credentials(self) -> None:
        """Test message without credentials remains unchanged."""
        message = "Normal log message without credentials"
        sanitized = sanitize_log_message(message)
        assert sanitized == message

    def test_sanitize_case_insensitive(self) -> None:
        """Test sanitization is case insensitive."""
        message = "API_KEY=key123 Secret_Key=secret456"
        sanitized = sanitize_log_message(message)
        assert "key123" not in sanitized
        assert "secret456" not in sanitized
