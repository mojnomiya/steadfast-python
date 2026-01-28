"""Error handling example."""

import time

from steadfast import (
    SteadfastClient,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    Order,
)

client = SteadfastClient(api_key="your_api_key", secret_key="your_secret_key")

# Example 1: Validation error
print("Example 1: Validation Error")
try:
    order = client.orders.create(
        invoice="invalid@invoice",  # Invalid characters
        recipient_name="John Smith",
        recipient_phone="01234567890",
        recipient_address="House 123, Dhaka",
        cod_amount=1060,
        delivery_type=0,
    )
except ValidationError as e:
    print(f"✗ Validation error: {e}")
    print(f"  Field: {e.field}")

# Example 2: Not found error
print("\nExample 2: Not Found Error")
try:
    status = client.tracking.get_status_by_consignment_id(999)
except NotFoundError as e:
    print(f"✗ Not found: {e}")

# Example 3: API error
print("\nExample 3: API Error")
try:
    # This would fail with API error
    order = client.orders.create(
        invoice="ORD-2024-001",
        recipient_name="John Smith",
        recipient_phone="01234567890",
        recipient_address="House 123, Dhaka",
        cod_amount=1060,
        delivery_type=0,
    )
except APIError as e:
    print(f"✗ API error: {e}")
    print(f"  Status code: {e.status_code}")


def create_order_with_retry(max_retries: int = 3) -> Order:
    """Create order with retry logic."""
    for attempt in range(max_retries):
        try:
            order = client.orders.create(
                invoice="ORD-2024-001",
                recipient_name="John Smith",
                recipient_phone="01234567890",
                recipient_address="House 123, Dhaka",
                cod_amount=1060,
                delivery_type=0,
            )
            return order
        except NetworkError as e:
            if attempt < max_retries - 1:
                wait_time = 2**attempt
                print(f"✗ Network error: {e}")
                print(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
    raise NetworkError("Max retries exceeded")


# Example 4: Network error with retry
print("\nExample 4: Network Error with Retry")
# create_order_with_retry()

# Example 5: Bulk operation with partial failures
print("\nExample 5: Bulk Operation Error Handling")
orders = [
    {
        "invoice": "ORD-2024-001",
        "recipient_name": "John Smith",
        "recipient_phone": "01234567890",
        "recipient_address": "House 123, Dhaka",
        "cod_amount": 1060,
        "delivery_type": 0,
    },
    {
        "invoice": "ORD-2024-002",
        "recipient_name": "Jane Doe",
        "recipient_phone": "01987654321",
        "recipient_address": "Apt 456, Chittagong",
        "cod_amount": 2500,
        "delivery_type": 1,
    },
]

try:
    response = client.orders.create_bulk(orders)

    for result in response.results:
        if result.status == "success":
            print(f"✓ Order {result.invoice}: {result.consignment_id}")
        else:
            print(f"✗ Order {result.invoice}: {result.error}")

except APIError as e:
    print(f"✗ Bulk operation failed: {e}")
