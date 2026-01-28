"""Tests for Tracking module."""

from typing import Dict, Any
from unittest.mock import Mock

import pytest

from steadfast.modules.tracking import TrackingModule
from steadfast.models import OrderStatus
from steadfast.exceptions import ValidationError, APIError, NotFoundError


class TestTrackingModule:
    """Test TrackingModule class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_http_client = Mock()
        self.tracking_module = TrackingModule(self.mock_http_client)

    def test_get_status_by_consignment_id_success(self) -> None:
        """Test successful status retrieval by consignment ID."""
        # Mock API response
        mock_response = {"status": 200, "delivery_status": "delivered"}
        self.mock_http_client.get.return_value = mock_response

        # Get status
        status = self.tracking_module.get_status_by_consignment_id(1424107)

        # Verify result
        assert isinstance(status, OrderStatus)
        assert status.status == 200
        assert status.delivery_status == "delivered"

        # Verify API call
        self.mock_http_client.get.assert_called_once_with("/status_by_cid/1424107")

    def test_get_status_by_consignment_id_validation_error(self) -> None:
        """Test validation error for invalid consignment ID."""
        # Test negative ID
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_consignment_id(-1)
        assert exc_info.value.field == "consignment_id"

        # Test zero ID
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_consignment_id(0)
        assert exc_info.value.field == "consignment_id"

        # Test non-integer ID
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_consignment_id("123")  # type: ignore
        assert exc_info.value.field == "consignment_id"

    def test_get_status_by_consignment_id_not_found(self) -> None:
        """Test NotFoundError for non-existent consignment ID."""
        self.mock_http_client.get.side_effect = NotFoundError("Consignment not found")

        with pytest.raises(NotFoundError):
            self.tracking_module.get_status_by_consignment_id(999999)

    def test_get_status_by_invoice_success(self) -> None:
        """Test successful status retrieval by invoice."""
        # Mock API response
        mock_response = {"status": 200, "delivery_status": "pending"}
        self.mock_http_client.get.return_value = mock_response

        # Get status
        status = self.tracking_module.get_status_by_invoice("ORD-2024-001")

        # Verify result
        assert isinstance(status, OrderStatus)
        assert status.status == 200
        assert status.delivery_status == "pending"

        # Verify API call
        self.mock_http_client.get.assert_called_once_with(
            "/status_by_invoice/ORD-2024-001"
        )

    def test_get_status_by_invoice_validation_error(self) -> None:
        """Test validation error for invalid invoice."""
        # Test empty invoice
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_invoice("")
        assert exc_info.value.field == "invoice"

        # Test None invoice
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_invoice(None)  # type: ignore
        assert exc_info.value.field == "invoice"

        # Test invalid characters
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_invoice("ORD@2024")
        assert exc_info.value.field == "invoice"

    def test_get_status_by_invoice_not_found(self) -> None:
        """Test NotFoundError for non-existent invoice."""
        self.mock_http_client.get.side_effect = NotFoundError("Invoice not found")

        with pytest.raises(NotFoundError):
            self.tracking_module.get_status_by_invoice("NONEXISTENT")

    def test_get_status_by_tracking_code_success(self) -> None:
        """Test successful status retrieval by tracking code."""
        # Mock API response
        mock_response = {"status": 200, "delivery_status": "in_transit"}
        self.mock_http_client.get.return_value = mock_response

        # Get status
        status = self.tracking_module.get_status_by_tracking_code("15BAEB8A")

        # Verify result
        assert isinstance(status, OrderStatus)
        assert status.status == 200
        assert status.delivery_status == "in_transit"

        # Verify API call
        self.mock_http_client.get.assert_called_once_with(
            "/status_by_trackingcode/15BAEB8A"
        )

    def test_get_status_by_tracking_code_with_whitespace(self) -> None:
        """Test tracking code with leading/trailing whitespace."""
        mock_response = {"status": 200, "delivery_status": "delivered"}
        self.mock_http_client.get.return_value = mock_response

        # Get status with whitespace
        status = self.tracking_module.get_status_by_tracking_code("  15BAEB8A  ")

        # Verify result
        assert status.delivery_status == "delivered"

        # Verify API call with trimmed code
        self.mock_http_client.get.assert_called_once_with(
            "/status_by_trackingcode/15BAEB8A"
        )

    def test_get_status_by_tracking_code_validation_error(self) -> None:
        """Test validation error for invalid tracking code."""
        # Test empty tracking code
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_tracking_code("")
        assert exc_info.value.field == "tracking_code"

        # Test None tracking code
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_tracking_code(None)  # type: ignore
        assert exc_info.value.field == "tracking_code"

        # Test whitespace-only tracking code
        with pytest.raises(ValidationError) as exc_info:
            self.tracking_module.get_status_by_tracking_code("   ")
        assert exc_info.value.field == "tracking_code"

    def test_get_status_by_tracking_code_not_found(self) -> None:
        """Test NotFoundError for non-existent tracking code."""
        self.mock_http_client.get.side_effect = NotFoundError("Tracking code not found")

        with pytest.raises(NotFoundError):
            self.tracking_module.get_status_by_tracking_code("INVALID")

    def test_api_error_handling(self) -> None:
        """Test API error handling for all methods."""
        self.mock_http_client.get.side_effect = APIError("API Error", 500)

        # Test consignment ID method
        with pytest.raises(APIError):
            self.tracking_module.get_status_by_consignment_id(123)

        # Test invoice method
        with pytest.raises(APIError):
            self.tracking_module.get_status_by_invoice("ORD-001")

        # Test tracking code method
        with pytest.raises(APIError):
            self.tracking_module.get_status_by_tracking_code("TRACK001")

    def test_response_with_missing_fields(self) -> None:
        """Test response parsing with missing fields."""
        # Mock response with missing fields
        mock_response: Dict[str, Any] = {}
        self.mock_http_client.get.return_value = mock_response

        status = self.tracking_module.get_status_by_consignment_id(123)

        # Should use default values
        assert status.status == 200
        assert status.delivery_status == "unknown"

    def test_response_with_partial_fields(self) -> None:
        """Test response parsing with partial fields."""
        # Mock response with only status
        mock_response: Dict[str, Any] = {"status": 404}
        self.mock_http_client.get.return_value = mock_response

        status = self.tracking_module.get_status_by_invoice("ORD-001")

        # Should use provided status and default delivery_status
        assert status.status == 404
        assert status.delivery_status == "unknown"

        # Mock response with only delivery_status
        mock_response = {"delivery_status": "cancelled"}
        self.mock_http_client.get.return_value = mock_response

        status = self.tracking_module.get_status_by_tracking_code("TRACK001")

        # Should use default status and provided delivery_status
        assert status.status == 200
        assert status.delivery_status == "cancelled"

    def test_different_delivery_statuses(self) -> None:
        """Test different delivery status values."""
        statuses = [
            "pending",
            "in_review",
            "delivered",
            "partial_delivered",
            "cancelled",
            "delivered_approval_pending",
            "partial_delivered_approval_pending",
            "cancelled_approval_pending",
            "hold",
            "unknown",
        ]

        for delivery_status in statuses:
            mock_response: Dict[str, Any] = {
                "status": 200,
                "delivery_status": delivery_status,
            }
            self.mock_http_client.get.return_value = mock_response

            status = self.tracking_module.get_status_by_consignment_id(123)
            assert status.delivery_status == delivery_status
