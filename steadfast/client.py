"""Main Steadfast client for SDK."""

import os
from typing import Optional
from .http_client import HTTPClient
from .modules.order import OrderModule
from .modules.tracking import TrackingModule
from .modules.balance import BalanceModule
from .modules.return_request import ReturnRequestModule
from .modules.payment import PaymentModule
from .modules.location import LocationModule
from .exceptions import ConfigurationError


class SteadastClient:
    """Main client for Steadfast Courier API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """Initialize Steadfast client.

        Args:
            api_key: API key for authentication (or from .env)
            secret_key: Secret key for authentication (or from .env)
            base_url: Base URL for API (optional, defaults to production)

        Raises:
            ConfigurationError: If credentials are missing
        """
        self._api_key = api_key or os.getenv("STEADFAST_API_KEY")
        self._secret_key = secret_key or os.getenv("STEADFAST_SECRET_KEY")

        self._validate_credentials()

        self._base_url = base_url or "https://api.steadfast.io/v1"
        self._http_client = HTTPClient(base_url=self._base_url)

        self._orders: Optional[OrderModule] = None
        self._tracking: Optional[TrackingModule] = None
        self._balance: Optional[BalanceModule] = None
        self._returns: Optional[ReturnRequestModule] = None
        self._payments: Optional[PaymentModule] = None
        self._locations: Optional[LocationModule] = None

    def _validate_credentials(self) -> None:
        """Validate that credentials are provided.

        Raises:
            ConfigurationError: If credentials are missing
        """
        if not self._api_key:
            raise ConfigurationError(
                "API key is required. Provide via api_key parameter or "
                "STEADFAST_API_KEY environment variable"
            )

        if not self._secret_key:
            raise ConfigurationError(
                "Secret key is required. Provide via secret_key parameter or "
                "STEADFAST_SECRET_KEY environment variable"
            )

    @property
    def orders(self) -> OrderModule:
        """Get orders module.

        Returns:
            OrderModule instance
        """
        if self._orders is None:
            self._orders = OrderModule(self._http_client)
        return self._orders

    @property
    def tracking(self) -> TrackingModule:
        """Get tracking module.

        Returns:
            TrackingModule instance
        """
        if self._tracking is None:
            self._tracking = TrackingModule(self._http_client)
        return self._tracking

    @property
    def balance(self) -> BalanceModule:
        """Get balance module.

        Returns:
            BalanceModule instance
        """
        if self._balance is None:
            self._balance = BalanceModule(self._http_client)
        return self._balance

    @property
    def returns(self) -> ReturnRequestModule:
        """Get return request module.

        Returns:
            ReturnRequestModule instance
        """
        if self._returns is None:
            self._returns = ReturnRequestModule(self._http_client)
        return self._returns

    @property
    def payments(self) -> PaymentModule:
        """Get payment module.

        Returns:
            PaymentModule instance
        """
        if self._payments is None:
            self._payments = PaymentModule(self._http_client)
        return self._payments

    @property
    def locations(self) -> LocationModule:
        """Get location module.

        Returns:
            LocationModule instance
        """
        if self._locations is None:
            self._locations = LocationModule(self._http_client)
        return self._locations
