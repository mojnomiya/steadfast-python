"""Tests for Balance module."""

from typing import Dict, Any
from unittest.mock import Mock

import pytest

from steadfast.modules.balance import BalanceModule
from steadfast.models import Balance
from steadfast.exceptions import APIError, NetworkError


class TestBalanceModule:
    """Test BalanceModule class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_http_client = Mock()
        self.balance_module = BalanceModule(self.mock_http_client)

    def test_get_current_balance_success(self) -> None:
        """Test successful balance retrieval."""
        # Mock API response
        mock_response = {"status": 200, "current_balance": 1500.50}
        self.mock_http_client.get.return_value = mock_response

        # Get balance
        balance = self.balance_module.get_current_balance()

        # Verify result
        assert isinstance(balance, Balance)
        assert balance.status == 200
        assert balance.current_balance == 1500.50

        # Verify API call
        self.mock_http_client.get.assert_called_once_with("/get_balance")

    def test_get_current_balance_zero(self) -> None:
        """Test balance retrieval with zero balance."""
        mock_response = {"status": 200, "current_balance": 0.0}
        self.mock_http_client.get.return_value = mock_response

        balance = self.balance_module.get_current_balance()

        assert balance.current_balance == 0.0

    def test_get_current_balance_large_amount(self) -> None:
        """Test balance retrieval with large amount."""
        mock_response = {"status": 200, "current_balance": 999999.99}
        self.mock_http_client.get.return_value = mock_response

        balance = self.balance_module.get_current_balance()

        assert balance.current_balance == 999999.99

    def test_get_current_balance_api_error(self) -> None:
        """Test API error handling."""
        self.mock_http_client.get.side_effect = APIError("API Error", 500)

        with pytest.raises(APIError):
            self.balance_module.get_current_balance()

    def test_get_current_balance_network_error(self) -> None:
        """Test network error handling."""
        self.mock_http_client.get.side_effect = NetworkError("Network Error")

        with pytest.raises(NetworkError):
            self.balance_module.get_current_balance()

    def test_get_current_balance_missing_fields(self) -> None:
        """Test response with missing fields."""
        # Mock response with missing fields
        mock_response: Dict[str, Any] = {}
        self.mock_http_client.get.return_value = mock_response

        balance = self.balance_module.get_current_balance()

        # Should use default values
        assert balance.status == 200
        assert balance.current_balance == 0.0

    def test_get_current_balance_partial_fields(self) -> None:
        """Test response with partial fields."""
        # Only status provided
        mock_response: Dict[str, Any] = {"status": 404}
        self.mock_http_client.get.return_value = mock_response

        balance = self.balance_module.get_current_balance()

        assert balance.status == 404
        assert balance.current_balance == 0.0

        # Only balance provided
        mock_response = {"current_balance": 2500.75}
        self.mock_http_client.get.return_value = mock_response

        balance = self.balance_module.get_current_balance()

        assert balance.status == 200
        assert balance.current_balance == 2500.75
