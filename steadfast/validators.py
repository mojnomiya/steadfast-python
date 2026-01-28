"""Input validators for Steadfast SDK."""

import re
from typing import Union
from .exceptions import ValidationError


def validate_invoice(value: str) -> str:
    """Validate invoice format: alphanumeric, hyphens, underscores."""
    if not value or not isinstance(value, str):
        raise ValidationError("Invoice cannot be empty", "invoice")

    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise ValidationError(
            "Invoice must contain only alphanumeric characters, "
            "hyphens, and underscores",
            "invoice",
        )

    return value.strip()


def validate_phone(value: str) -> str:
    """Validate phone number: exactly 11 digits."""
    if not value or not isinstance(value, str):
        raise ValidationError("Phone number cannot be empty", "phone")

    phone = re.sub(r"\D", "", value)  # Remove non-digits

    if len(phone) != 11:
        raise ValidationError("Phone number must be exactly 11 digits", "phone")

    return phone


def validate_recipient_name(value: str) -> str:
    """Validate recipient name: max 100 characters."""
    if not value or not isinstance(value, str):
        raise ValidationError("Recipient name cannot be empty", "recipient_name")

    name = value.strip()
    if len(name) > 100:
        raise ValidationError(
            "Recipient name cannot exceed 100 characters", "recipient_name"
        )

    return name


def validate_address(value: str) -> str:
    """Validate address: max 250 characters."""
    if not value or not isinstance(value, str):
        raise ValidationError("Address cannot be empty", "address")

    address = value.strip()
    if len(address) > 250:
        raise ValidationError("Address cannot exceed 250 characters", "address")

    return address


def validate_email(value: str) -> str:
    """Validate email format."""
    if not value or not isinstance(value, str):
        raise ValidationError("Email cannot be empty", "email")

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, value):
        raise ValidationError("Invalid email format", "email")

    return value.strip()


def validate_cod_amount(value: Union[int, float]) -> float:
    """Validate COD amount: numeric, >= 0."""
    if value is None:
        raise ValidationError("COD amount cannot be None", "cod_amount")

    try:
        amount = float(value)
    except (ValueError, TypeError):
        raise ValidationError("COD amount must be numeric", "cod_amount")

    if amount < 0:
        raise ValidationError("COD amount cannot be negative", "cod_amount")

    return amount


def validate_delivery_type(value: int) -> int:
    """Validate delivery type: 0 or 1."""
    if value not in [0, 1]:
        raise ValidationError(
            "Delivery type must be 0 (home) or 1 (point)", "delivery_type"
        )

    return value


def validate_consignment_id(value: int) -> int:
    """Validate consignment ID: positive integer."""
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(
            "Consignment ID must be a positive integer", "consignment_id"
        )

    return value


def validate_identifier_type(value: str) -> str:
    """Validate identifier type: valid enum."""
    valid_types = ["consignment_id", "invoice", "tracking_code"]
    if value not in valid_types:
        raise ValidationError(
            f"Identifier type must be one of: {', '.join(valid_types)}",
            "identifier_type",
        )

    return value
