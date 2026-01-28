"""Tests for input validators."""

import pytest
from steadfast.validators import (
    validate_invoice,
    validate_phone,
    validate_recipient_name,
    validate_address,
    validate_email,
    validate_cod_amount,
    validate_delivery_type,
    validate_consignment_id,
    validate_identifier_type,
)
from steadfast.exceptions import ValidationError


class TestValidateInvoice:
    """Test invoice validation."""

    def test_valid_invoice(self) -> None:
        """Test valid invoice formats."""
        assert validate_invoice("ORD-001") == "ORD-001"
        assert validate_invoice("ORDER_123") == "ORDER_123"
        assert validate_invoice("ABC123") == "ABC123"
        assert validate_invoice("test-order_001") == "test-order_001"

    def test_invalid_invoice_empty(self) -> None:
        """Test empty invoice raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_invoice("")
        assert exc_info.value.field == "invoice"
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_invoice_none(self) -> None:
        """Test None invoice raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_invoice(None)  # type: ignore
        assert exc_info.value.field == "invoice"

    def test_invalid_invoice_special_chars(self) -> None:
        """Test invoice with invalid characters."""
        with pytest.raises(ValidationError) as exc_info:
            validate_invoice("ORD@001")
        assert exc_info.value.field == "invoice"
        assert "alphanumeric" in str(exc_info.value)


class TestValidatePhone:
    """Test phone validation."""

    def test_valid_phone(self) -> None:
        """Test valid phone numbers."""
        assert validate_phone("01234567890") == "01234567890"
        assert validate_phone("01-234-567-890") == "01234567890"
        assert validate_phone("01 234 567 890") == "01234567890"

    def test_invalid_phone_empty(self) -> None:
        """Test empty phone raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_phone("")
        assert exc_info.value.field == "phone"

    def test_invalid_phone_length(self) -> None:
        """Test phone with wrong length."""
        with pytest.raises(ValidationError) as exc_info:
            validate_phone("0123456789")  # 10 digits
        assert exc_info.value.field == "phone"
        assert "exactly 11 digits" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            validate_phone("012345678901")  # 12 digits
        assert exc_info.value.field == "phone"


class TestValidateRecipientName:
    """Test recipient name validation."""

    def test_valid_name(self) -> None:
        """Test valid recipient names."""
        assert validate_recipient_name("John Doe") == "John Doe"
        assert validate_recipient_name("  John Doe  ") == "John Doe"

    def test_invalid_name_empty(self) -> None:
        """Test empty name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_recipient_name("")
        assert exc_info.value.field == "recipient_name"

    def test_invalid_name_too_long(self) -> None:
        """Test name exceeding 100 characters."""
        long_name = "A" * 101
        with pytest.raises(ValidationError) as exc_info:
            validate_recipient_name(long_name)
        assert exc_info.value.field == "recipient_name"
        assert "100 characters" in str(exc_info.value)


class TestValidateAddress:
    """Test address validation."""

    def test_valid_address(self) -> None:
        """Test valid addresses."""
        assert validate_address("123 Main St") == "123 Main St"
        assert validate_address("  123 Main St  ") == "123 Main St"

    def test_invalid_address_empty(self) -> None:
        """Test empty address raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_address("")
        assert exc_info.value.field == "address"

    def test_invalid_address_too_long(self) -> None:
        """Test address exceeding 250 characters."""
        long_address = "A" * 251
        with pytest.raises(ValidationError) as exc_info:
            validate_address(long_address)
        assert exc_info.value.field == "address"
        assert "250 characters" in str(exc_info.value)


class TestValidateEmail:
    """Test email validation."""

    def test_valid_email(self) -> None:
        """Test valid email formats."""
        assert validate_email("test@example.com") == "test@example.com"
        assert validate_email("user.name@domain.co.uk") == "user.name@domain.co.uk"

    def test_invalid_email_empty(self) -> None:
        """Test empty email raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_email("")
        assert exc_info.value.field == "email"

    def test_invalid_email_format(self) -> None:
        """Test invalid email formats."""
        invalid_emails = [
            "invalid",
            "test@",
            "@example.com",
            "test.example.com",
        ]
        for email in invalid_emails:
            with pytest.raises(ValidationError) as exc_info:
                validate_email(email)
            assert exc_info.value.field == "email"
            assert "Invalid email format" in str(exc_info.value)


class TestValidateCodAmount:
    """Test COD amount validation."""

    def test_valid_cod_amount(self) -> None:
        """Test valid COD amounts."""
        assert validate_cod_amount(100) == 100.0
        assert validate_cod_amount(100.5) == 100.5
        assert validate_cod_amount("100") == 100.0  # type: ignore
        assert validate_cod_amount(0) == 0.0

    def test_invalid_cod_amount_none(self) -> None:
        """Test None COD amount raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_cod_amount(None)  # type: ignore
        assert exc_info.value.field == "cod_amount"

    def test_invalid_cod_amount_negative(self) -> None:
        """Test negative COD amount raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_cod_amount(-10)
        assert exc_info.value.field == "cod_amount"
        assert "cannot be negative" in str(exc_info.value)

    def test_invalid_cod_amount_non_numeric(self) -> None:
        """Test non-numeric COD amount raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_cod_amount("invalid")  # type: ignore
        assert exc_info.value.field == "cod_amount"
        assert "must be numeric" in str(exc_info.value)


class TestValidateDeliveryType:
    """Test delivery type validation."""

    def test_valid_delivery_type(self) -> None:
        """Test valid delivery types."""
        assert validate_delivery_type(0) == 0
        assert validate_delivery_type(1) == 1

    def test_invalid_delivery_type(self) -> None:
        """Test invalid delivery types."""
        invalid_types = [2, -1, "0", None]  # type: ignore
        for delivery_type in invalid_types:
            with pytest.raises(ValidationError) as exc_info:
                validate_delivery_type(delivery_type)  # type: ignore
            assert exc_info.value.field == "delivery_type"
            assert "must be 0 (home) or 1 (point)" in str(exc_info.value)


class TestValidateConsignmentId:
    """Test consignment ID validation."""

    def test_valid_consignment_id(self) -> None:
        """Test valid consignment IDs."""
        assert validate_consignment_id(123) == 123
        assert validate_consignment_id(1) == 1

    def test_invalid_consignment_id(self) -> None:
        """Test invalid consignment IDs."""
        invalid_ids = [0, -1, "123", None, 1.5]  # type: ignore
        for consignment_id in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                validate_consignment_id(consignment_id)  # type: ignore
            assert exc_info.value.field == "consignment_id"
            assert "positive integer" in str(exc_info.value)


class TestValidateIdentifierType:
    """Test identifier type validation."""

    def test_valid_identifier_type(self) -> None:
        """Test valid identifier types."""
        valid_types = ["consignment_id", "invoice", "tracking_code"]
        for identifier_type in valid_types:
            assert validate_identifier_type(identifier_type) == identifier_type

    def test_invalid_identifier_type(self) -> None:
        """Test invalid identifier types."""
        with pytest.raises(ValidationError) as exc_info:
            validate_identifier_type("invalid")
        assert exc_info.value.field == "identifier_type"
        assert "must be one of" in str(exc_info.value)
