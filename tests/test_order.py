"""Tests for Order module."""

from unittest.mock import Mock

import pytest

from steadfast.modules.order import OrderModule
from steadfast.models import Order, BulkOrderResponse
from steadfast.exceptions import ValidationError, APIError


class TestOrderModule:
    """Test OrderModule class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_http_client = Mock()
        self.order_module = OrderModule(self.mock_http_client)

    def test_create_order_success(self) -> None:
        """Test successful order creation."""
        # Mock API response
        mock_response = {
            "consignment_id": 1424107,
            "invoice": "ORD-001",
            "tracking_code": "15BAEB8A",
            "recipient_name": "John Smith",
            "recipient_phone": "01234567890",
            "recipient_address": "House 123, Dhaka",
            "cod_amount": 1060.0,
            "status": "pending",
            "note": "Test note",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }
        self.mock_http_client.post.return_value = mock_response

        # Create order
        order = self.order_module.create(
            invoice="ORD-001",
            recipient_name="John Smith",
            recipient_phone="01234567890",
            recipient_address="House 123, Dhaka",
            cod_amount=1060,
            delivery_type=0,
            note="Test note",
        )

        # Verify result
        assert isinstance(order, Order)
        assert order.consignment_id == 1424107
        assert order.invoice == "ORD-001"
        assert order.tracking_code == "15BAEB8A"
        assert order.recipient_name == "John Smith"
        assert order.cod_amount == 1060.0
        assert order.status == "pending"
        assert order.note == "Test note"

        # Verify API call
        self.mock_http_client.post.assert_called_once_with(
            "/create_order",
            data={
                "invoice": "ORD-001",
                "recipient_name": "John Smith",
                "recipient_phone": "01234567890",
                "recipient_address": "House 123, Dhaka",
                "cod_amount": 1060.0,
                "delivery_type": 0,
                "note": "Test note",
            },
        )

    def test_create_order_with_optional_fields(self) -> None:
        """Test order creation with all optional fields."""
        mock_response = {
            "consignment_id": 1424107,
            "invoice": "ORD-002",
            "tracking_code": "15BAEB8B",
            "recipient_name": "Jane Doe",
            "recipient_phone": "01234567891",
            "recipient_address": "House 456, Dhaka",
            "cod_amount": 2000.0,
            "status": "pending",
        }
        self.mock_http_client.post.return_value = mock_response

        order = self.order_module.create(
            invoice="ORD-002",
            recipient_name="Jane Doe",
            recipient_phone="01234567891",
            recipient_address="House 456, Dhaka",
            cod_amount=2000,
            delivery_type=1,
            alternative_phone="01987654321",
            recipient_email="jane@example.com",
            note="Fragile items",
            item_description="Electronics",
            total_lot=2,
        )

        assert order.consignment_id == 1424107
        assert order.invoice == "ORD-002"

        # Verify all optional fields were included in payload
        call_args = self.mock_http_client.post.call_args[1]["data"]
        assert call_args["alternative_phone"] == "01987654321"
        assert call_args["recipient_email"] == "jane@example.com"
        assert call_args["note"] == "Fragile items"
        assert call_args["item_description"] == "Electronics"
        assert call_args["total_lot"] == 2

    def test_create_order_validation_errors(self) -> None:
        """Test order creation validation errors."""
        # Test empty invoice
        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create(
                invoice="",
                recipient_name="John Smith",
                recipient_phone="01234567890",
                recipient_address="House 123, Dhaka",
                cod_amount=1060,
            )
        assert exc_info.value.field == "invoice"

        # Test invalid phone number
        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create(
                invoice="ORD-001",
                recipient_name="John Smith",
                recipient_phone="123",  # Too short
                recipient_address="House 123, Dhaka",
                cod_amount=1060,
            )
        assert exc_info.value.field == "phone"

        # Test negative COD amount
        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create(
                invoice="ORD-001",
                recipient_name="John Smith",
                recipient_phone="01234567890",
                recipient_address="House 123, Dhaka",
                cod_amount=-100,
            )
        assert exc_info.value.field == "cod_amount"

        # Test invalid delivery type
        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create(
                invoice="ORD-001",
                recipient_name="John Smith",
                recipient_phone="01234567890",
                recipient_address="House 123, Dhaka",
                cod_amount=1060,
                delivery_type=2,  # Invalid
            )
        assert exc_info.value.field == "delivery_type"

    def test_create_order_api_error(self) -> None:
        """Test API error handling in order creation."""
        self.mock_http_client.post.side_effect = APIError("API Error", 400)

        with pytest.raises(APIError):
            self.order_module.create(
                invoice="ORD-001",
                recipient_name="John Smith",
                recipient_phone="01234567890",
                recipient_address="House 123, Dhaka",
                cod_amount=1060,
            )

    def test_create_bulk_orders_success(self) -> None:
        """Test successful bulk order creation."""
        orders = [
            {
                "invoice": "BULK-001",
                "recipient_name": "Customer 1",
                "recipient_phone": "01711111111",
                "recipient_address": "Address 1, Dhaka",
                "cod_amount": 500,
                "delivery_type": 0,
            },
            {
                "invoice": "BULK-002",
                "recipient_name": "Customer 2",
                "recipient_phone": "01712222222",
                "recipient_address": "Address 2, Dhaka",
                "cod_amount": 1000,
                "delivery_type": 1,
            },
        ]

        mock_response = {
            "results": [
                {
                    "invoice": "BULK-001",
                    "recipient_name": "Customer 1",
                    "recipient_address": "Address 1, Dhaka",
                    "recipient_phone": "01711111111",
                    "cod_amount": 500,
                    "consignment_id": 1001,
                    "tracking_code": "TRACK001",
                    "status": "success",
                },
                {
                    "invoice": "BULK-002",
                    "recipient_name": "Customer 2",
                    "recipient_address": "Address 2, Dhaka",
                    "recipient_phone": "01712222222",
                    "cod_amount": 1000,
                    "status": "error",
                    "error": "Invalid address",
                },
            ]
        }
        self.mock_http_client.post.return_value = mock_response

        response = self.order_module.create_bulk(orders)

        assert isinstance(response, BulkOrderResponse)
        assert len(response.results) == 2

        # Check successful result
        success_result = response.results[0]
        assert success_result.status == "success"
        assert success_result.consignment_id == 1001
        assert success_result.tracking_code == "TRACK001"
        assert success_result.error is None

        # Check failed result
        error_result = response.results[1]
        assert error_result.status == "error"
        assert error_result.error == "Invalid address"
        assert error_result.consignment_id is None

    def test_create_bulk_orders_empty_list(self) -> None:
        """Test bulk order creation with empty list."""
        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create_bulk([])
        assert exc_info.value.field == "orders"
        assert "cannot be empty" in str(exc_info.value)

    def test_create_bulk_orders_exceed_limit(self) -> None:
        """Test bulk order creation exceeding 500 items."""
        orders = [{"invoice": f"ORD-{i:03d}"} for i in range(501)]

        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create_bulk(orders)
        assert exc_info.value.field == "orders"
        assert "500 orders" in str(exc_info.value)

    def test_create_bulk_orders_validation_error(self) -> None:
        """Test bulk order creation with validation error in individual order."""
        orders = [
            {
                "invoice": "BULK-001",
                "recipient_name": "Customer 1",
                "recipient_phone": "01711111111",
                "recipient_address": "Address 1, Dhaka",
                "cod_amount": 500,
            },
            {
                "invoice": "",  # Invalid empty invoice
                "recipient_name": "Customer 2",
                "recipient_phone": "01712222222",
                "recipient_address": "Address 2, Dhaka",
                "cod_amount": 1000,
            },
        ]

        with pytest.raises(ValidationError) as exc_info:
            self.order_module.create_bulk(orders)
        assert "Order 2" in str(exc_info.value)

    def test_validate_order_missing_required_fields(self) -> None:
        """Test order validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            self.order_module._validate_order(invoice="ORD-001")
        assert "Missing required fields" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            self.order_module._validate_order(
                invoice="ORD-001",
                recipient_name="John",
                recipient_phone="01234567890",
                recipient_address="Address",
                # Missing cod_amount
            )
        assert exc_info.value.field == "cod_amount"

    def test_validate_order_success(self) -> None:
        """Test successful order validation."""
        order_data = {
            "invoice": "ORD-001",
            "recipient_name": "John Smith",
            "recipient_phone": "01234567890",
            "recipient_address": "House 123, Dhaka",
            "cod_amount": 1060,
            "delivery_type": 0,
            "alternative_phone": "01987654321",
            "recipient_email": "john@example.com",
            "note": "Test note",
            "item_description": "Electronics",
            "total_lot": 1,
        }

        validated = self.order_module._validate_order(**order_data)

        assert validated["invoice"] == "ORD-001"
        assert validated["recipient_name"] == "John Smith"
        assert validated["recipient_phone"] == "01234567890"
        assert validated["cod_amount"] == 1060.0
        assert validated["delivery_type"] == 0
        assert validated["alternative_phone"] == "01987654321"
        assert validated["recipient_email"] == "john@example.com"
        assert validated["note"] == "Test note"
        assert validated["item_description"] == "Electronics"
        assert validated["total_lot"] == 1
