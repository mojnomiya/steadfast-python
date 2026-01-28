"""Tests for data models."""

from steadfast.models import (
    Order,
    BulkOrderResult,
    BulkOrderResponse,
    OrderStatus,
    Balance,
    ReturnRequest,
    ReturnRequestList,
    Payment,
    PaymentDetails,
    PaymentList,
    PoliceStation,
    PoliceStationList,
)


class TestOrder:
    """Test Order dataclass."""

    def test_order_instantiation(self) -> None:
        """Test Order can be instantiated with required fields."""
        order = Order(
            consignment_id=123,
            invoice="ORD-001",
            tracking_code="ABC123",
            recipient_name="John Doe",
            recipient_phone="01234567890",
            recipient_address="123 Main St",
            cod_amount=100.0,
            status="pending",
        )
        assert order.consignment_id == 123
        assert order.invoice == "ORD-001"
        assert order.tracking_code == "ABC123"
        assert order.recipient_name == "John Doe"
        assert order.recipient_phone == "01234567890"
        assert order.recipient_address == "123 Main St"
        assert order.cod_amount == 100.0
        assert order.status == "pending"
        assert order.note is None

    def test_order_with_optional_fields(self) -> None:
        """Test Order with optional fields."""
        order = Order(
            consignment_id=123,
            invoice="ORD-001",
            tracking_code="ABC123",
            recipient_name="John Doe",
            recipient_phone="01234567890",
            recipient_address="123 Main St",
            cod_amount=100.0,
            status="pending",
            note="Test note",
            created_at="2024-01-01",
            updated_at="2024-01-02",
        )
        assert order.note == "Test note"
        assert order.created_at == "2024-01-01"
        assert order.updated_at == "2024-01-02"


class TestBulkOrderResult:
    """Test BulkOrderResult dataclass."""

    def test_bulk_order_result_success(self) -> None:
        """Test successful bulk order result."""
        result = BulkOrderResult(
            invoice="ORD-001",
            recipient_name="John Doe",
            recipient_address="123 Main St",
            recipient_phone="01234567890",
            cod_amount=100.0,
            consignment_id=123,
            tracking_code="ABC123",
            status="success",
        )
        assert result.status == "success"
        assert result.consignment_id == 123
        assert result.error is None

    def test_bulk_order_result_error(self) -> None:
        """Test failed bulk order result."""
        result = BulkOrderResult(
            invoice="ORD-001",
            recipient_name="John Doe",
            recipient_address="123 Main St",
            recipient_phone="01234567890",
            cod_amount=100.0,
            status="error",
            error="Invalid phone number",
        )
        assert result.status == "error"
        assert result.error == "Invalid phone number"
        assert result.consignment_id is None


class TestBulkOrderResponse:
    """Test BulkOrderResponse dataclass."""

    def test_bulk_order_response(self) -> None:
        """Test bulk order response with results."""
        result1 = BulkOrderResult(
            invoice="ORD-001",
            recipient_name="John Doe",
            recipient_address="123 Main St",
            recipient_phone="01234567890",
            cod_amount=100.0,
            status="success",
            consignment_id=123,
        )
        result2 = BulkOrderResult(
            invoice="ORD-002",
            recipient_name="Jane Doe",
            recipient_address="456 Oak St",
            recipient_phone="01234567891",
            cod_amount=200.0,
            status="error",
            error="Invalid address",
        )
        response = BulkOrderResponse(results=[result1, result2])
        assert len(response.results) == 2
        assert response.results[0].status == "success"
        assert response.results[1].status == "error"


class TestOrderStatus:
    """Test OrderStatus dataclass."""

    def test_order_status(self) -> None:
        """Test OrderStatus instantiation."""
        status = OrderStatus(status=200, delivery_status="delivered")
        assert status.status == 200
        assert status.delivery_status == "delivered"


class TestBalance:
    """Test Balance dataclass."""

    def test_balance(self) -> None:
        """Test Balance instantiation."""
        balance = Balance(status=200, current_balance=1500.50)
        assert balance.status == 200
        assert balance.current_balance == 1500.50


class TestReturnRequest:
    """Test ReturnRequest dataclass."""

    def test_return_request(self) -> None:
        """Test ReturnRequest instantiation."""
        return_req = ReturnRequest(
            id=1,
            user_id=100,
            consignment_id=123,
            reason="Damaged item",
            status="pending",
        )
        assert return_req.id == 1
        assert return_req.user_id == 100
        assert return_req.consignment_id == 123
        assert return_req.reason == "Damaged item"
        assert return_req.status == "pending"


class TestReturnRequestList:
    """Test ReturnRequestList dataclass."""

    def test_return_request_list(self) -> None:
        """Test ReturnRequestList instantiation."""
        return_req = ReturnRequest(id=1, user_id=100, consignment_id=123)
        return_list = ReturnRequestList(data=[return_req])
        assert len(return_list.data) == 1
        assert return_list.data[0].id == 1


class TestPayment:
    """Test Payment dataclass."""

    def test_payment(self) -> None:
        """Test Payment instantiation."""
        payment = Payment(id=1, amount=500.0)
        assert payment.id == 1
        assert payment.amount == 500.0


class TestPaymentDetails:
    """Test PaymentDetails dataclass."""

    def test_payment_details(self) -> None:
        """Test PaymentDetails instantiation."""
        consignments = [{"consignment_id": 123, "amount": 100.0}]
        payment_details = PaymentDetails(id=1, amount=500.0, consignments=consignments)
        assert payment_details.id == 1
        assert payment_details.amount == 500.0
        assert len(payment_details.consignments) == 1


class TestPaymentList:
    """Test PaymentList dataclass."""

    def test_payment_list(self) -> None:
        """Test PaymentList instantiation."""
        payment = Payment(id=1, amount=500.0)
        payment_list = PaymentList(data=[payment])
        assert len(payment_list.data) == 1
        assert payment_list.data[0].id == 1


class TestPoliceStation:
    """Test PoliceStation dataclass."""

    def test_police_station(self) -> None:
        """Test PoliceStation instantiation."""
        station = PoliceStation(id=1, name="Dhanmondi PS", location="Dhaka")
        assert station.id == 1
        assert station.name == "Dhanmondi PS"
        assert station.location == "Dhaka"


class TestPoliceStationList:
    """Test PoliceStationList dataclass."""

    def test_police_station_list(self) -> None:
        """Test PoliceStationList instantiation."""
        station = PoliceStation(id=1, name="Dhanmondi PS", location="Dhaka")
        station_list = PoliceStationList(data=[station])
        assert len(station_list.data) == 1
        assert station_list.data[0].name == "Dhanmondi PS"
