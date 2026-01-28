"""HTTP client for Steadfast SDK with retry logic and error handling."""

import time
from typing import Dict, Any, Optional

import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    RequestException,
    JSONDecodeError,
)

from .exceptions import APIError, NetworkError
from .logger import get_logger, sanitize_log_message


class HTTPClient:
    """HTTP client wrapper with retry logic and error handling."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff: float = 0.3,
    ) -> None:
        """Initialize HTTP client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            retry_backoff: Backoff factor for exponential backoff
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.logger = get_logger(__name__)

    def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make GET request.

        Args:
            endpoint: API endpoint
            headers: Request headers
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            APIError: For API-related errors
            NetworkError: For network-related errors
        """
        return self._make_request("GET", endpoint, headers=headers, params=params)

    def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make POST request.

        Args:
            endpoint: API endpoint
            headers: Request headers
            data: Request payload

        Returns:
            Parsed JSON response

        Raises:
            APIError: For API-related errors
            NetworkError: For network-related errors
        """
        return self._make_request("POST", endpoint, headers=headers, data=data)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic.

        Args:
            method: HTTP method
            endpoint: API endpoint
            headers: Request headers
            params: Query parameters
            data: Request payload

        Returns:
            Parsed JSON response

        Raises:
            APIError: For API-related errors
            NetworkError: For network-related errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = headers or {}

        # Set default headers
        if "Content-Type" not in headers and data is not None:
            headers["Content-Type"] = "application/json"

        for attempt in range(self.max_retries + 1):
            try:
                self.logger.debug(
                    sanitize_log_message(
                        f"Making {method} request to {url} "
                        f"(attempt {attempt + 1}/{self.max_retries + 1})"
                    )
                )

                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=self.timeout,
                )

                # Handle HTTP errors
                if not response.ok:
                    error_msg = f"HTTP {response.status_code}"
                    try:
                        error_data = response.json()
                        if "message" in error_data:
                            error_msg = error_data["message"]
                        elif "error" in error_data:
                            error_msg = error_data["error"]
                    except (JSONDecodeError, ValueError):
                        error_msg = response.text or error_msg

                    if response.status_code == 404:
                        from .exceptions import NotFoundError

                        raise NotFoundError(error_msg)
                    elif response.status_code == 401:
                        from .exceptions import AuthenticationError

                        raise AuthenticationError(error_msg)
                    else:
                        raise APIError(error_msg, response.status_code)

                # Parse JSON response
                try:
                    response_data: Dict[str, Any] = response.json()
                    return response_data
                except (JSONDecodeError, ValueError) as e:
                    raise APIError(f"Invalid JSON response: {str(e)}")

            except (ConnectionError, Timeout) as e:
                if not self._should_retry(e, attempt):
                    raise NetworkError(f"Network error: {str(e)}")

                if attempt < self.max_retries:
                    self._exponential_backoff(attempt)

            except RequestException as e:
                raise NetworkError(f"Request failed: {str(e)}")

        # This should never be reached due to the retry logic
        raise NetworkError("Max retries exceeded")

    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if request should be retried.

        Args:
            exception: Exception that occurred
            attempt: Current attempt number

        Returns:
            True if should retry, False otherwise
        """
        if attempt >= self.max_retries:
            return False

        # Retry on connection errors and timeouts
        return isinstance(exception, (ConnectionError, Timeout))

    def _exponential_backoff(self, attempt: int) -> None:
        """Apply exponential backoff delay.

        Args:
            attempt: Current attempt number
        """
        delay = self.retry_backoff * (2**attempt)
        self.logger.debug(f"Retrying in {delay:.2f} seconds...")
        time.sleep(delay)
