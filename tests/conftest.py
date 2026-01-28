"""Pytest configuration and shared fixtures."""

from unittest.mock import Mock
import pytest


@pytest.fixture
def mock_http_client() -> Mock:
    """Create mock HTTP client for testing."""
    return Mock()


@pytest.fixture
def sample_order_data() -> dict:
    """Sample order data for testing."""
    return {
        "invoice": "ORD-2024-001",
        "recipient_name": "John Smith",
        "recipient_phone": "01234567890",
        "recipient_address": "House 123, Dhaka",
        "cod_amount": 1060,
        "delivery_type": 0,
    }


@pytest.fixture
def sample_order_response() -> dict:
    """Sample order response from API."""
    return {
        "consignment_id": 123,
        "invoice": "ORD-2024-001",
        "tracking_code": "TRACK123",
        "recipient_name": "John Smith",
        "recipient_phone": "01234567890",
        "recipient_address": "House 123, Dhaka",
        "cod_amount": 1060,
        "status": "pending",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
    }


@pytest.fixture
def sample_tracking_data() -> dict:
    """Sample tracking response from API."""
    return {
        "status": 200,
        "delivery_status": "in_transit",
    }


@pytest.fixture
def sample_balance_data() -> dict:
    """Sample balance response from API."""
    return {
        "status": 200,
        "current_balance": 5000.50,
    }


@pytest.fixture
def sample_return_request_data() -> dict:
    """Sample return request response from API."""
    return {
        "id": 1,
        "user_id": 10,
        "consignment_id": 123,
        "reason": "Damaged",
        "status": "pending",
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
    }


@pytest.fixture
def sample_payment_data() -> dict:
    """Sample payment response from API."""
    return {
        "id": 1,
        "amount": 5000.50,
        "consignments": [
            {"consignment_id": 123, "amount": 2500.25},
            {"consignment_id": 124, "amount": 2500.25},
        ],
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
    }


@pytest.fixture
def sample_police_station_data() -> dict:
    """Sample police station response from API."""
    return {
        "data": [
            {
                "id": 1,
                "name": "Dhaka Central Police Station",
                "location": "Dhaka",
            },
            {
                "id": 2,
                "name": "Chittagong Police Station",
                "location": "Chittagong",
            },
        ]
    }
