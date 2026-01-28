"""Tests for main Steadfast client."""

import os
from unittest.mock import patch
import pytest
from steadfast.client import SteadastClient
from steadfast.modules.order import OrderModule
from steadfast.modules.tracking import TrackingModule
from steadfast.modules.balance import BalanceModule
from steadfast.modules.return_request import ReturnRequestModule
from steadfast.modules.payment import PaymentModule
from steadfast.modules.location import LocationModule
from steadfast.exceptions import ConfigurationError


class TestSteadastClientInitialization:
    """Tests for client initialization."""

    def test_init_with_credentials(self) -> None:
        """Test initializing client with credentials."""
        client = SteadastClient(api_key="test_api_key", secret_key="test_secret_key")

        assert client._api_key == "test_api_key"
        assert client._secret_key == "test_secret_key"
        assert client._base_url == "https://api.steadfast.io/v1"

    def test_init_with_custom_base_url(self) -> None:
        """Test initializing client with custom base URL."""
        client = SteadastClient(
            api_key="test_api_key",
            secret_key="test_secret_key",
            base_url="https://custom.api.com",
        )

        assert client._base_url == "https://custom.api.com"

    def test_init_missing_api_key(self) -> None:
        """Test initializing without API key."""
        with pytest.raises(ConfigurationError) as exc_info:
            SteadastClient(secret_key="test_secret_key")

        assert "API key is required" in str(exc_info.value)

    def test_init_missing_secret_key(self) -> None:
        """Test initializing without secret key."""
        with pytest.raises(ConfigurationError) as exc_info:
            SteadastClient(api_key="test_api_key")

        assert "Secret key is required" in str(exc_info.value)

    @patch.dict(os.environ, {"STEADFAST_API_KEY": "env_api_key"})
    def test_init_with_env_api_key(self) -> None:
        """Test initializing with API key from environment."""
        client = SteadastClient(secret_key="test_secret_key")

        assert client._api_key == "env_api_key"

    @patch.dict(os.environ, {"STEADFAST_SECRET_KEY": "env_secret_key"})
    def test_init_with_env_secret_key(self) -> None:
        """Test initializing with secret key from environment."""
        client = SteadastClient(api_key="test_api_key")

        assert client._secret_key == "env_secret_key"

    @patch.dict(
        os.environ,
        {
            "STEADFAST_API_KEY": "env_api_key",
            "STEADFAST_SECRET_KEY": "env_secret_key",
        },
    )
    def test_init_with_all_env_credentials(self) -> None:
        """Test initializing with all credentials from environment."""
        client = SteadastClient()

        assert client._api_key == "env_api_key"
        assert client._secret_key == "env_secret_key"

    def test_init_parameter_overrides_env(self) -> None:
        """Test that parameters override environment variables."""
        with patch.dict(
            os.environ,
            {
                "STEADFAST_API_KEY": "env_api_key",
                "STEADFAST_SECRET_KEY": "env_secret_key",
            },
        ):
            client = SteadastClient(
                api_key="param_api_key", secret_key="param_secret_key"
            )

            assert client._api_key == "param_api_key"
            assert client._secret_key == "param_secret_key"


class TestSteadastClientModuleProperties:
    """Tests for module property access."""

    @pytest.fixture
    def client(self) -> SteadastClient:
        """Create client for testing."""
        return SteadastClient(api_key="test_api_key", secret_key="test_secret_key")

    def test_orders_property(self, client: SteadastClient) -> None:
        """Test accessing orders module."""
        orders = client.orders

        assert isinstance(orders, OrderModule)
        assert orders is client.orders  # Same instance on second access

    def test_tracking_property(self, client: SteadastClient) -> None:
        """Test accessing tracking module."""
        tracking = client.tracking

        assert isinstance(tracking, TrackingModule)
        assert tracking is client.tracking

    def test_balance_property(self, client: SteadastClient) -> None:
        """Test accessing balance module."""
        balance = client.balance

        assert isinstance(balance, BalanceModule)
        assert balance is client.balance

    def test_returns_property(self, client: SteadastClient) -> None:
        """Test accessing returns module."""
        returns = client.returns

        assert isinstance(returns, ReturnRequestModule)
        assert returns is client.returns

    def test_payments_property(self, client: SteadastClient) -> None:
        """Test accessing payments module."""
        payments = client.payments

        assert isinstance(payments, PaymentModule)
        assert payments is client.payments

    def test_locations_property(self, client: SteadastClient) -> None:
        """Test accessing locations module."""
        locations = client.locations

        assert isinstance(locations, LocationModule)
        assert locations is client.locations

    def test_all_modules_share_http_client(self, client: SteadastClient) -> None:
        """Test that all modules share the same HTTP client."""
        orders_client = client.orders.http_client
        tracking_client = client.tracking.http_client
        balance_client = client.balance.http_client
        returns_client = client.returns.http_client
        payments_client = client.payments.http_client
        locations_client = client.locations.http_client

        assert orders_client is tracking_client
        assert tracking_client is balance_client
        assert balance_client is returns_client
        assert returns_client is payments_client
        assert payments_client is locations_client

    def test_module_lazy_initialization(self, client: SteadastClient) -> None:
        """Test that modules are lazily initialized."""
        assert client._orders is None
        assert client._tracking is None
        assert client._balance is None
        assert client._returns is None
        assert client._payments is None
        assert client._locations is None

        _ = client.orders
        assert client._orders is not None
        assert client._tracking is None

        _ = client.tracking
        assert client._tracking is not None
