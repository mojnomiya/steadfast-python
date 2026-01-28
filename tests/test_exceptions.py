"""Tests for exception classes."""

from steadfast.exceptions import (
    SteadfastException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
)


class TestSteadfastException:
    """Test base exception class."""

    def test_exception_instantiation(self) -> None:
        """Test exception can be instantiated with message."""
        exc = SteadfastException("Test message")
        assert exc.message == "Test message"
        assert str(exc) == "Test message"

    def test_exception_inheritance(self) -> None:
        """Test exception inherits from Exception."""
        exc = SteadfastException("Test")
        assert isinstance(exc, Exception)


class TestAuthenticationError:
    """Test authentication error."""

    def test_inheritance(self) -> None:
        """Test inherits from SteadfastException."""
        exc = AuthenticationError("Auth failed")
        assert isinstance(exc, SteadfastException)
        assert str(exc) == "Auth failed"


class TestValidationError:
    """Test validation error with field support."""

    def test_without_field(self) -> None:
        """Test validation error without field."""
        exc = ValidationError("Invalid input")
        assert exc.field is None
        assert str(exc) == "Validation error: Invalid input"

    def test_with_field(self) -> None:
        """Test validation error with field."""
        exc = ValidationError("Invalid format", "email")
        assert exc.field == "email"
        assert str(exc) == "Validation error for field 'email': Invalid format"

    def test_inheritance(self) -> None:
        """Test inherits from SteadfastException."""
        exc = ValidationError("Test")
        assert isinstance(exc, SteadfastException)


class TestNotFoundError:
    """Test not found error."""

    def test_inheritance(self) -> None:
        """Test inherits from SteadfastException."""
        exc = NotFoundError("Not found")
        assert isinstance(exc, SteadfastException)
        assert str(exc) == "Not found"


class TestAPIError:
    """Test API error with status code support."""

    def test_without_status_code(self) -> None:
        """Test API error without status code."""
        exc = APIError("API failed")
        assert exc.status_code is None
        assert str(exc) == "API error: API failed"

    def test_with_status_code(self) -> None:
        """Test API error with status code."""
        exc = APIError("Bad request", 400)
        assert exc.status_code == 400
        assert str(exc) == "API error (400): Bad request"

    def test_inheritance(self) -> None:
        """Test inherits from SteadfastException."""
        exc = APIError("Test")
        assert isinstance(exc, SteadfastException)


class TestNetworkError:
    """Test network error with retry support."""

    def test_without_retry_after(self) -> None:
        """Test network error without retry info."""
        exc = NetworkError("Connection failed")
        assert exc.retry_after is None
        assert str(exc) == "Network error: Connection failed"

    def test_with_retry_after(self) -> None:
        """Test network error with retry info."""
        exc = NetworkError("Rate limited", 60)
        assert exc.retry_after == 60
        assert str(exc) == "Network error: Rate limited (retry after 60s)"

    def test_inheritance(self) -> None:
        """Test inherits from SteadfastException."""
        exc = NetworkError("Test")
        assert isinstance(exc, SteadfastException)


class TestConfigurationError:
    """Test configuration error."""

    def test_inheritance(self) -> None:
        """Test inherits from SteadfastException."""
        exc = ConfigurationError("Config error")
        assert isinstance(exc, SteadfastException)
        assert str(exc) == "Config error"
