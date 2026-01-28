"""Order tracking module for Steadfast SDK."""

from ..http_client import HTTPClient
from ..models import OrderStatus
from ..validators import validate_consignment_id, validate_invoice
from ..exceptions import ValidationError


class TrackingModule:
    """Module for order status tracking."""

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize tracking module.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def get_status_by_consignment_id(self, consignment_id: int) -> OrderStatus:
        """Get delivery status by consignment ID.

        Args:
            consignment_id: Consignment identifier

        Returns:
            OrderStatus with delivery status

        Raises:
            ValidationError: If consignment_id is invalid
            NotFoundError: If consignment not found
            APIError: If API request fails
        """
        # Validate input
        validated_id = validate_consignment_id(consignment_id)

        # Make API call
        response = self.http_client.get(f"/status_by_cid/{validated_id}")

        # Parse and return response
        return OrderStatus(
            status=response.get("status", 200),
            delivery_status=response.get("delivery_status", "unknown"),
        )

    def get_status_by_invoice(self, invoice: str) -> OrderStatus:
        """Get delivery status by invoice ID.

        Args:
            invoice: Invoice/order identifier

        Returns:
            OrderStatus with delivery status

        Raises:
            ValidationError: If invoice format is invalid
            NotFoundError: If invoice not found
            APIError: If API request fails
        """
        # Validate input
        validated_invoice = validate_invoice(invoice)

        # Make API call
        response = self.http_client.get(f"/status_by_invoice/{validated_invoice}")

        # Parse and return response
        return OrderStatus(
            status=response.get("status", 200),
            delivery_status=response.get("delivery_status", "unknown"),
        )

    def get_status_by_tracking_code(self, tracking_code: str) -> OrderStatus:
        """Get delivery status by tracking code.

        Args:
            tracking_code: Tracking code identifier

        Returns:
            OrderStatus with delivery status

        Raises:
            ValidationError: If tracking_code is invalid
            NotFoundError: If tracking code not found
            APIError: If API request fails
        """
        # Validate input
        if not tracking_code or not isinstance(tracking_code, str):
            raise ValidationError("Tracking code cannot be empty", "tracking_code")

        tracking_code = tracking_code.strip()
        if not tracking_code:
            raise ValidationError("Tracking code cannot be empty", "tracking_code")

        # Make API call
        response = self.http_client.get(f"/status_by_trackingcode/{tracking_code}")

        # Parse and return response
        return OrderStatus(
            status=response.get("status", 200),
            delivery_status=response.get("delivery_status", "unknown"),
        )
