"""Tests for payment module."""

from unittest.mock import Mock
import pytest
from steadfast.modules.payment import PaymentModule
from steadfast.models import PaymentDetails, PaymentList
from steadfast.exceptions import ValidationError, NotFoundError, APIError


@pytest.fixture
def mock_http_client() -> Mock:
    """Create mock HTTP client."""
    return Mock()


@pytest.fixture
def payment_module(mock_http_client: Mock) -> PaymentModule:
    """Create payment module with mock client."""
    return PaymentModule(mock_http_client)


class TestPaymentList:
    """Tests for list method."""

    def test_list_success(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test listing payments successfully."""
        mock_http_client.get.return_value = {
            "data": [
                {
                    "id": 1,
                    "amount": 5000.50,
                    "created_at": "2024-01-01T10:00:00Z",
                    "updated_at": "2024-01-01T10:00:00Z",
                },
                {
                    "id": 2,
                    "amount": 3000.00,
                    "created_at": "2024-01-02T10:00:00Z",
                    "updated_at": "2024-01-02T10:00:00Z",
                },
            ]
        }

        result = payment_module.list()

        assert isinstance(result, PaymentList)
        assert len(result.data) == 2
        assert result.data[0].id == 1
        assert result.data[0].amount == 5000.50
        assert result.data[1].id == 2
        assert result.data[1].amount == 3000.00
        mock_http_client.get.assert_called_once_with("/payment/list")

    def test_list_empty(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test listing with no payments."""
        mock_http_client.get.return_value = {"data": []}

        result = payment_module.list()

        assert isinstance(result, PaymentList)
        assert len(result.data) == 0

    def test_list_missing_data_field(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test listing with missing data field."""
        mock_http_client.get.return_value = {}

        result = payment_module.list()

        assert isinstance(result, PaymentList)
        assert len(result.data) == 0

    def test_list_api_error(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test listing with API error."""
        mock_http_client.get.side_effect = APIError("API error", 500)

        with pytest.raises(APIError):
            payment_module.list()

    def test_list_partial_fields(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test listing with partial fields in response."""
        mock_http_client.get.return_value = {
            "data": [
                {"id": 1, "amount": 1000},
                {"id": 2},
            ]
        }

        result = payment_module.list()

        assert len(result.data) == 2
        assert result.data[0].id == 1
        assert result.data[0].amount == 1000.0
        assert result.data[1].id == 2
        assert result.data[1].amount == 0.0

    def test_list_string_amounts(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test listing with string amounts."""
        mock_http_client.get.return_value = {
            "data": [
                {"id": 1, "amount": "2500.75"},
            ]
        }

        result = payment_module.list()

        assert result.data[0].amount == 2500.75


class TestPaymentGet:
    """Tests for get method."""

    def test_get_success(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test getting payment details successfully."""
        mock_http_client.get.return_value = {
            "id": 1,
            "amount": 5000.50,
            "consignments": [
                {"consignment_id": 123, "amount": 2500.25},
                {"consignment_id": 124, "amount": 2500.25},
            ],
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z",
        }

        result = payment_module.get(1)

        assert isinstance(result, PaymentDetails)
        assert result.id == 1
        assert result.amount == 5000.50
        assert len(result.consignments) == 2
        assert result.consignments[0]["consignment_id"] == 123
        mock_http_client.get.assert_called_once_with("/payment/1")

    def test_get_no_consignments(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test getting payment with no consignments."""
        mock_http_client.get.return_value = {
            "id": 2,
            "amount": 1000.00,
            "consignments": [],
        }

        result = payment_module.get(2)

        assert result.id == 2
        assert len(result.consignments) == 0

    def test_get_invalid_id(self, payment_module: PaymentModule) -> None:
        """Test getting with invalid ID."""
        with pytest.raises(ValidationError) as exc_info:
            payment_module.get(-1)

        assert "payment_id" in str(exc_info.value)

    def test_get_zero_id(self, payment_module: PaymentModule) -> None:
        """Test getting with zero ID."""
        with pytest.raises(ValidationError):
            payment_module.get(0)

    def test_get_not_found(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test getting non-existent payment."""
        mock_http_client.get.side_effect = NotFoundError("Payment not found")

        with pytest.raises(NotFoundError):
            payment_module.get(999)

    def test_get_api_error(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test getting with API error."""
        mock_http_client.get.side_effect = APIError("API error", 500)

        with pytest.raises(APIError):
            payment_module.get(1)

    def test_get_missing_fields(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test getting with missing response fields."""
        mock_http_client.get.return_value = {"id": 1}

        result = payment_module.get(1)

        assert result.id == 1
        assert result.amount == 0.0
        assert result.consignments == []

    def test_get_string_amount(
        self, payment_module: PaymentModule, mock_http_client: Mock
    ) -> None:
        """Test getting with string amount."""
        mock_http_client.get.return_value = {
            "id": 1,
            "amount": "7500.99",
            "consignments": [],
        }

        result = payment_module.get(1)

        assert result.amount == 7500.99
