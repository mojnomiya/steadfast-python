"""Tests for return request module."""

from unittest.mock import Mock
import pytest
from steadfast.modules.return_request import ReturnRequestModule
from steadfast.models import ReturnRequest, ReturnRequestList
from steadfast.exceptions import ValidationError, NotFoundError, APIError


@pytest.fixture
def mock_http_client() -> Mock:
    """Create mock HTTP client."""
    return Mock()


@pytest.fixture
def return_request_module(mock_http_client: Mock) -> ReturnRequestModule:
    """Create return request module with mock client."""
    return ReturnRequestModule(mock_http_client)


class TestReturnRequestCreate:
    """Tests for create method."""

    def test_create_with_consignment_id(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating return request with consignment ID."""
        mock_http_client.post.return_value = {
            "id": 1,
            "user_id": 10,
            "consignment_id": 123,
            "reason": "Damaged",
            "status": "pending",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z",
        }

        result = return_request_module.create(123, "consignment_id", "Damaged")

        assert isinstance(result, ReturnRequest)
        assert result.id == 1
        assert result.consignment_id == 123
        assert result.reason == "Damaged"
        assert result.status == "pending"
        mock_http_client.post.assert_called_once_with(
            "/return-request/store",
            {
                "identifier": 123,
                "identifier_type": "consignment_id",
                "reason": "Damaged",
            },
        )

    def test_create_with_invoice(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating return request with invoice."""
        mock_http_client.post.return_value = {
            "id": 2,
            "user_id": 10,
            "consignment_id": 124,
            "reason": "Lost",
            "status": "pending",
        }

        result = return_request_module.create("ORD-2024-001", "invoice", "Lost")

        assert result.id == 2
        assert result.reason == "Lost"
        mock_http_client.post.assert_called_once()

    def test_create_with_tracking_code(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating return request with tracking code."""
        mock_http_client.post.return_value = {
            "id": 3,
            "user_id": 10,
            "consignment_id": 125,
            "status": "pending",
        }

        result = return_request_module.create("TRACK123", "tracking_code")

        assert result.id == 3
        mock_http_client.post.assert_called_once()

    def test_create_without_reason(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating return request without reason."""
        mock_http_client.post.return_value = {
            "id": 4,
            "user_id": 10,
            "consignment_id": 126,
            "status": "pending",
        }

        result = return_request_module.create(126, "consignment_id")

        assert result.id == 4
        call_args = mock_http_client.post.call_args
        assert "reason" not in call_args[0][1]

    def test_create_invalid_identifier_type(
        self, return_request_module: ReturnRequestModule
    ) -> None:
        """Test creating with invalid identifier type."""
        with pytest.raises(ValidationError) as exc_info:
            return_request_module.create(123, "invalid_type")

        assert "identifier_type" in str(exc_info.value)

    def test_create_invalid_consignment_id(
        self, return_request_module: ReturnRequestModule
    ) -> None:
        """Test creating with invalid consignment ID."""
        with pytest.raises(ValidationError) as exc_info:
            return_request_module.create(-1, "consignment_id")

        assert "consignment_id" in str(exc_info.value)

    def test_create_invalid_invoice(
        self, return_request_module: ReturnRequestModule
    ) -> None:
        """Test creating with invalid invoice."""
        with pytest.raises(ValidationError) as exc_info:
            return_request_module.create("@#$%", "invoice")

        assert "invoice" in str(exc_info.value)

    def test_create_not_found(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating when consignment not found."""
        mock_http_client.post.side_effect = NotFoundError("Consignment not found")

        with pytest.raises(NotFoundError):
            return_request_module.create(999, "consignment_id")

    def test_create_api_error(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating with API error."""
        mock_http_client.post.side_effect = APIError("API error", 500)

        with pytest.raises(APIError):
            return_request_module.create(123, "consignment_id")

    def test_create_missing_fields(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test creating with missing response fields."""
        mock_http_client.post.return_value = {"id": 5}

        result = return_request_module.create(127, "consignment_id")

        assert result.id == 5
        assert result.user_id == 0
        assert result.consignment_id == 0
        assert result.status == "pending"


class TestReturnRequestGet:
    """Tests for get method."""

    def test_get_success(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test getting return request successfully."""
        mock_http_client.get.return_value = {
            "id": 1,
            "user_id": 10,
            "consignment_id": 123,
            "reason": "Damaged",
            "status": "approved",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-02T10:00:00Z",
        }

        result = return_request_module.get(1)

        assert isinstance(result, ReturnRequest)
        assert result.id == 1
        assert result.status == "approved"
        mock_http_client.get.assert_called_once_with("/return-request/1")

    def test_get_invalid_id(self, return_request_module: ReturnRequestModule) -> None:
        """Test getting with invalid ID."""
        with pytest.raises(ValidationError) as exc_info:
            return_request_module.get(-1)

        assert "return_request_id" in str(exc_info.value)

    def test_get_zero_id(self, return_request_module: ReturnRequestModule) -> None:
        """Test getting with zero ID."""
        with pytest.raises(ValidationError):
            return_request_module.get(0)

    def test_get_not_found(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test getting non-existent return request."""
        mock_http_client.get.side_effect = NotFoundError("Return request not found")

        with pytest.raises(NotFoundError):
            return_request_module.get(999)

    def test_get_api_error(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test getting with API error."""
        mock_http_client.get.side_effect = APIError("API error", 500)

        with pytest.raises(APIError):
            return_request_module.get(1)

    def test_get_missing_fields(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test getting with missing response fields."""
        mock_http_client.get.return_value = {"id": 1}

        result = return_request_module.get(1)

        assert result.id == 1
        assert result.user_id == 0
        assert result.status == "pending"


class TestReturnRequestList:
    """Tests for list method."""

    def test_list_success(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test listing return requests successfully."""
        mock_http_client.get.return_value = {
            "data": [
                {
                    "id": 1,
                    "user_id": 10,
                    "consignment_id": 123,
                    "reason": "Damaged",
                    "status": "pending",
                },
                {
                    "id": 2,
                    "user_id": 10,
                    "consignment_id": 124,
                    "reason": "Lost",
                    "status": "approved",
                },
            ]
        }

        result = return_request_module.list()

        assert isinstance(result, ReturnRequestList)
        assert len(result.data) == 2
        assert result.data[0].id == 1
        assert result.data[1].id == 2
        mock_http_client.get.assert_called_once_with("/return-request/list")

    def test_list_empty(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test listing with no return requests."""
        mock_http_client.get.return_value = {"data": []}

        result = return_request_module.list()

        assert isinstance(result, ReturnRequestList)
        assert len(result.data) == 0

    def test_list_missing_data_field(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test listing with missing data field."""
        mock_http_client.get.return_value = {}

        result = return_request_module.list()

        assert isinstance(result, ReturnRequestList)
        assert len(result.data) == 0

    def test_list_api_error(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test listing with API error."""
        mock_http_client.get.side_effect = APIError("API error", 500)

        with pytest.raises(APIError):
            return_request_module.list()

    def test_list_partial_fields(
        self, return_request_module: ReturnRequestModule, mock_http_client: Mock
    ) -> None:
        """Test listing with partial fields in response."""
        mock_http_client.get.return_value = {
            "data": [
                {"id": 1, "user_id": 10},
                {"id": 2, "consignment_id": 124},
            ]
        }

        result = return_request_module.list()

        assert len(result.data) == 2
        assert result.data[0].id == 1
        assert result.data[0].status == "pending"
        assert result.data[1].id == 2
