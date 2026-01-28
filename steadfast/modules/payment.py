"""Payment module for Steadfast SDK."""

from ..http_client import HTTPClient
from ..models import Payment, PaymentDetails, PaymentList


class PaymentModule:
    """Module for managing payments."""

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize payment module.

        Args:
            http_client: HTTPClient instance for API calls
        """
        self.http_client = http_client

    def list(self) -> PaymentList:
        """List all payments.

        Returns:
            PaymentList object with paginated results

        Raises:
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        response = self.http_client.get("/payment/list")

        payments = []
        for item in response.get("data", []):
            payments.append(
                Payment(
                    id=item.get("id", 0),
                    amount=float(item.get("amount", 0)),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at"),
                )
            )

        return PaymentList(data=payments)

    def get(self, payment_id: int) -> PaymentDetails:
        """Get payment details with consignments.

        Args:
            payment_id: ID of the payment

        Returns:
            PaymentDetails object with consignments list

        Raises:
            ValidationError: If payment_id is invalid
            NotFoundError: If payment not found
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        if not isinstance(payment_id, int) or payment_id <= 0:
            from ..exceptions import ValidationError

            raise ValidationError("Payment ID must be a positive integer", "payment_id")

        response = self.http_client.get(f"/payment/{payment_id}")

        return PaymentDetails(
            id=response.get("id", 0),
            amount=float(response.get("amount", 0)),
            consignments=response.get("consignments", []),
            created_at=response.get("created_at"),
            updated_at=response.get("updated_at"),
        )
