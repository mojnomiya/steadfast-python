"""Balance management module for Steadfast SDK."""

from ..http_client import HTTPClient
from ..models import Balance


class BalanceModule:
    """Module for account balance management."""

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize balance module.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def get_current_balance(self) -> Balance:
        """Get current account balance.

        Returns:
            Balance object with current balance

        Raises:
            APIError: If API request fails
            NetworkError: If network request fails
        """
        # Make API call
        response = self.http_client.get("/get_balance")

        # Parse and return response
        return Balance(
            status=response.get("status", 200),
            current_balance=response.get("current_balance", 0.0),
        )
