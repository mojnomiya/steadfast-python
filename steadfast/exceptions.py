"""Custom exceptions for Steadfast SDK."""

from typing import Optional


class SteadfastException(Exception):
    """Base exception for all Steadfast SDK errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class AuthenticationError(SteadfastException):
    """Raised when authentication fails."""

    pass


class ValidationError(SteadfastException):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message)
        self.field = field

    def __str__(self) -> str:
        if self.field:
            return (
                f"Validation error for field '{self.field}': {self.message}"
            )
        return f"Validation error: {self.message}"


class NotFoundError(SteadfastException):
    """Raised when requested resource is not found."""

    pass


class APIError(SteadfastException):
    """Raised for general API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    def __str__(self) -> str:
        if self.status_code:
            return f"API error ({self.status_code}): {self.message}"
        return f"API error: {self.message}"


class NetworkError(SteadfastException):
    """Raised for network-related failures."""

    def __init__(self, message: str, retry_after: Optional[int] = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after

    def __str__(self) -> str:
        if self.retry_after:
            return (
                f"Network error: {self.message} "
                f"(retry after {self.retry_after}s)"
            )
        return f"Network error: {self.message}"


class ConfigurationError(SteadfastException):
    """Raised for configuration-related errors."""

    pass
