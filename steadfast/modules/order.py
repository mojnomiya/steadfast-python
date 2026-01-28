"""Order management module for Steadfast SDK."""

from typing import List, Dict, Any, Optional, Union

from ..http_client import HTTPClient
from ..models import Order, BulkOrderResult, BulkOrderResponse
from ..validators import (
    validate_invoice,
    validate_recipient_name,
    validate_phone,
    validate_address,
    validate_email,
    validate_cod_amount,
    validate_delivery_type,
)
from ..exceptions import ValidationError


class OrderModule:
    """Module for order creation and management."""

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize order module.

        Args:
            http_client: HTTP client instance
        """
        self.http_client = http_client

    def create(
        self,
        invoice: str,
        recipient_name: str,
        recipient_phone: str,
        recipient_address: str,
        cod_amount: Union[int, float],
        delivery_type: int = 0,
        alternative_phone: Optional[str] = None,
        recipient_email: Optional[str] = None,
        note: Optional[str] = None,
        item_description: Optional[str] = None,
        total_lot: Optional[int] = None,
    ) -> Order:
        """Create a single order.

        Args:
            invoice: Unique order identifier
            recipient_name: Recipient's full name
            recipient_phone: Recipient's phone number (11 digits)
            recipient_address: Delivery address
            cod_amount: Cash on delivery amount
            delivery_type: 0 for home delivery, 1 for point delivery
            alternative_phone: Secondary contact number
            recipient_email: Recipient's email address
            note: Delivery instructions
            item_description: Description of items
            total_lot: Total lot of items

        Returns:
            Order object with consignment details

        Raises:
            ValidationError: If input validation fails
            APIError: If API request fails
        """
        # Validate required fields
        validated_invoice = validate_invoice(invoice)
        validated_name = validate_recipient_name(recipient_name)
        validated_phone = validate_phone(recipient_phone)
        validated_address = validate_address(recipient_address)
        validated_cod_amount = validate_cod_amount(cod_amount)
        validated_delivery_type = validate_delivery_type(delivery_type)

        # Validate optional fields
        validated_alt_phone = None
        if alternative_phone:
            validated_alt_phone = validate_phone(alternative_phone)

        validated_email = None
        if recipient_email:
            validated_email = validate_email(recipient_email)

        # Build payload
        payload = {
            "invoice": validated_invoice,
            "recipient_name": validated_name,
            "recipient_phone": validated_phone,
            "recipient_address": validated_address,
            "cod_amount": validated_cod_amount,
            "delivery_type": validated_delivery_type,
        }

        # Add optional fields
        if validated_alt_phone:
            payload["alternative_phone"] = validated_alt_phone
        if validated_email:
            payload["recipient_email"] = validated_email
        if note:
            payload["note"] = note
        if item_description:
            payload["item_description"] = item_description
        if total_lot is not None:
            payload["total_lot"] = total_lot

        # Make API call
        response = self.http_client.post("/create_order", data=payload)

        # Parse response and return Order object
        return Order(
            consignment_id=response["consignment_id"],
            invoice=response["invoice"],
            tracking_code=response["tracking_code"],
            recipient_name=response["recipient_name"],
            recipient_phone=response["recipient_phone"],
            recipient_address=response["recipient_address"],
            cod_amount=response["cod_amount"],
            status=response.get("status", "pending"),
            note=response.get("note"),
            created_at=response.get("created_at"),
            updated_at=response.get("updated_at"),
        )

    def create_bulk(self, orders: List[Dict[str, Any]]) -> BulkOrderResponse:
        """Create multiple orders in a single request.

        Args:
            orders: List of order dictionaries (max 500)

        Returns:
            BulkOrderResponse with individual results

        Raises:
            ValidationError: If validation fails
            APIError: If API request fails
        """
        # Validate orders list
        if not orders:
            raise ValidationError("Orders list cannot be empty", "orders")

        if len(orders) > 500:
            raise ValidationError(
                "Cannot create more than 500 orders at once", "orders"
            )

        # Validate each order
        validated_orders = []
        for i, order in enumerate(orders):
            try:
                validated_order = self._validate_order(**order)
                validated_orders.append(validated_order)
            except ValidationError as e:
                # Add order index to error message
                raise ValidationError(
                    f"Order {i + 1}: {e.message}", e.field or "orders"
                )

        # Build payload
        payload = {"orders": validated_orders}

        # Make API call
        response = self.http_client.post("/create_bulk_order", data=payload)

        # Parse response
        results = []
        for result_data in response.get("results", []):
            result = BulkOrderResult(
                invoice=result_data["invoice"],
                recipient_name=result_data["recipient_name"],
                recipient_address=result_data["recipient_address"],
                recipient_phone=result_data["recipient_phone"],
                cod_amount=result_data["cod_amount"],
                note=result_data.get("note"),
                consignment_id=result_data.get("consignment_id"),
                tracking_code=result_data.get("tracking_code"),
                status=result_data.get("status", "error"),
                error=result_data.get("error"),
            )
            results.append(result)

        return BulkOrderResponse(results=results)

    def _validate_order(self, **kwargs: Any) -> Dict[str, Any]:
        """Validate a single order's parameters.

        Args:
            **kwargs: Order parameters

        Returns:
            Validated order dictionary

        Raises:
            ValidationError: If validation fails
        """
        # Extract required fields
        invoice = kwargs.get("invoice")
        recipient_name = kwargs.get("recipient_name")
        recipient_phone = kwargs.get("recipient_phone")
        recipient_address = kwargs.get("recipient_address")
        cod_amount = kwargs.get("cod_amount")

        if not all([invoice, recipient_name, recipient_phone, recipient_address]):
            raise ValidationError("Missing required fields")

        if cod_amount is None:
            raise ValidationError("COD amount is required", "cod_amount")

        # Validate required fields
        validated_order = {
            "invoice": validate_invoice(str(invoice)),
            "recipient_name": validate_recipient_name(str(recipient_name)),
            "recipient_phone": validate_phone(str(recipient_phone)),
            "recipient_address": validate_address(str(recipient_address)),
            "cod_amount": validate_cod_amount(cod_amount),
            "delivery_type": validate_delivery_type(kwargs.get("delivery_type", 0)),
        }

        # Validate and add optional fields
        alternative_phone = kwargs.get("alternative_phone")
        if alternative_phone:
            validated_order["alternative_phone"] = validate_phone(alternative_phone)

        recipient_email = kwargs.get("recipient_email")
        if recipient_email:
            validated_order["recipient_email"] = validate_email(recipient_email)

        # Add other optional fields without validation
        for field in ["note", "item_description", "total_lot"]:
            if field in kwargs and kwargs[field] is not None:
                validated_order[field] = kwargs[field]

        return validated_order
