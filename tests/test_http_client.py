"""Tests for HTTP client."""

import json
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import ConnectionError, Timeout, RequestException

from steadfast.http_client import HTTPClient
from steadfast.exceptions import (
    APIError,
    NetworkError,
    NotFoundError,
    AuthenticationError,
)


class TestHTTPClient:
    """Test HTTPClient class."""

    def setup_method(self) -> None:
        """Set up test client."""
        self.client = HTTPClient(
            base_url="https://api.example.com",
            timeout=30,
            max_retries=2,
            retry_backoff=0.1,
        )

    def test_init(self) -> None:
        """Test HTTPClient initialization."""
        client = HTTPClient("https://api.example.com/", timeout=60, max_retries=5)
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 60
        assert client.max_retries == 5

    @patch("requests.request")
    def test_get_success(self, mock_request: Mock) -> None:
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response

        result = self.client.get("/test", headers={"Auth": "token"})

        assert result == {"status": "success"}
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.example.com/test",
            headers={"Auth": "token"},
            params=None,
            json=None,
            timeout=30,
        )

    @patch("requests.request")
    def test_post_success(self, mock_request: Mock) -> None:
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"id": 123}
        mock_request.return_value = mock_response

        data = {"name": "test"}
        result = self.client.post("/create", data=data)

        assert result == {"id": 123}
        mock_request.assert_called_once_with(
            method="POST",
            url="https://api.example.com/create",
            headers={"Content-Type": "application/json"},
            params=None,
            json=data,
            timeout=30,
        )

    @patch("requests.request")
    def test_get_with_params(self, mock_request: Mock) -> None:
        """Test GET request with query parameters."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"data": []}
        mock_request.return_value = mock_response

        params = {"page": 1, "limit": 10}
        result = self.client.get("/list", params=params)

        assert result == {"data": []}
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.example.com/list",
            headers={},
            params=params,
            json=None,
            timeout=30,
        )

    @patch("requests.request")
    def test_404_error(self, mock_request: Mock) -> None:
        """Test 404 Not Found error."""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Resource not found"}
        mock_request.return_value = mock_response

        with pytest.raises(NotFoundError) as exc_info:
            self.client.get("/nonexistent")

        assert "Resource not found" in str(exc_info.value)

    @patch("requests.request")
    def test_401_error(self, mock_request: Mock) -> None:
        """Test 401 Authentication error."""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid credentials"}
        mock_request.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            self.client.get("/protected")

        assert "Invalid credentials" in str(exc_info.value)

    @patch("requests.request")
    def test_api_error_with_status_code(self, mock_request: Mock) -> None:
        """Test API error with status code."""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad request"}
        mock_request.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            self.client.get("/invalid")

        assert exc_info.value.status_code == 400
        assert "Bad request" in str(exc_info.value)

    @patch("requests.request")
    def test_api_error_no_json(self, mock_request: Mock) -> None:
        """Test API error when response is not JSON."""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)
        mock_response.text = "Internal Server Error"
        mock_request.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            self.client.get("/error")

        assert "Internal Server Error" in str(exc_info.value)

    @patch("requests.request")
    def test_invalid_json_response(self, mock_request: Mock) -> None:
        """Test invalid JSON response."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)
        mock_request.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            self.client.get("/invalid-json")

        assert "Invalid JSON response" in str(exc_info.value)

    @patch("requests.request")
    def test_connection_error_no_retry(self, mock_request: Mock) -> None:
        """Test connection error without retry."""
        mock_request.side_effect = ConnectionError("Connection failed")

        with pytest.raises(NetworkError) as exc_info:
            self.client.get("/test")

        assert "Network error" in str(exc_info.value)
        assert mock_request.call_count == 3  # Initial + 2 retries

    @patch("requests.request")
    def test_timeout_error_with_retry(self, mock_request: Mock) -> None:
        """Test timeout error with retry logic."""
        mock_request.side_effect = [
            Timeout("Request timeout"),
            Timeout("Request timeout"),
            Mock(ok=True, json=lambda: {"success": True}),
        ]

        with patch("time.sleep"):  # Mock sleep to speed up test
            result = self.client.get("/test")

        assert result == {"success": True}
        assert mock_request.call_count == 3

    @patch("requests.request")
    def test_request_exception(self, mock_request: Mock) -> None:
        """Test general request exception."""
        mock_request.side_effect = RequestException("Request failed")

        with pytest.raises(NetworkError) as exc_info:
            self.client.get("/test")

        assert "Request failed" in str(exc_info.value)

    @patch("time.sleep")
    def test_exponential_backoff(self, mock_sleep: Mock) -> None:
        """Test exponential backoff calculation."""
        client = HTTPClient("https://api.example.com", retry_backoff=0.5)

        client._exponential_backoff(0)
        mock_sleep.assert_called_with(0.5)

        client._exponential_backoff(1)
        mock_sleep.assert_called_with(1.0)

        client._exponential_backoff(2)
        mock_sleep.assert_called_with(2.0)

    def test_should_retry_logic(self) -> None:
        """Test retry decision logic."""
        # Should retry on connection errors
        assert self.client._should_retry(ConnectionError(), 0) is True
        assert self.client._should_retry(Timeout(), 1) is True

        # Should not retry after max attempts
        assert self.client._should_retry(ConnectionError(), 2) is False

        # Should not retry on other exceptions
        assert self.client._should_retry(ValueError(), 0) is False

    @patch("requests.request")
    def test_url_construction(self, mock_request: Mock) -> None:
        """Test URL construction with different endpoint formats."""
        mock_response = Mock(ok=True, json=lambda: {})
        mock_request.return_value = mock_response

        # Test with leading slash
        self.client.get("/api/test")
        mock_request.assert_called_with(
            method="GET",
            url="https://api.example.com/api/test",
            headers={},
            params=None,
            json=None,
            timeout=30,
        )

        # Test without leading slash
        self.client.get("api/test")
        mock_request.assert_called_with(
            method="GET",
            url="https://api.example.com/api/test",
            headers={},
            params=None,
            json=None,
            timeout=30,
        )

    @patch("requests.request")
    def test_content_type_header(self, mock_request: Mock) -> None:
        """Test Content-Type header is set for POST with data."""
        mock_response = Mock(ok=True, json=lambda: {})
        mock_request.return_value = mock_response

        # POST with data should set Content-Type
        self.client.post("/test", data={"key": "value"})
        args, kwargs = mock_request.call_args
        assert kwargs["headers"]["Content-Type"] == "application/json"

        # GET should not set Content-Type
        self.client.get("/test")
        args, kwargs = mock_request.call_args
        assert "Content-Type" not in kwargs["headers"]

        # Custom Content-Type should not be overridden
        self.client.post(
            "/test", headers={"Content-Type": "custom"}, data={"key": "value"}
        )
        args, kwargs = mock_request.call_args
        assert kwargs["headers"]["Content-Type"] == "custom"
