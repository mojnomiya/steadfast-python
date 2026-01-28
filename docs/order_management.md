# Order Management API

## Overview

The Order module handles creation and management of courier orders. It supports both single order creation and bulk operations (up to 500 orders).

## Methods

### create()

Create a single order.

**Signature:**
```python
def create(
    invoice: str,
    recipient_name: str,
    recipient_phone: str,
    recipient_address: str,
    cod_amount: float,
    delivery_type: int,
    note: Optional[str] = None
) -> Order
```

**Parameters:**
- `invoice` (str): Unique invoice identifier (alphanumeric, hyphens, underscores)
- `recipient_name` (str): Recipient name (max 100 characters)
- `recipient_phone` (str): Phone number (exactly 11 digits)
- `recipient_address` (str): Delivery address (max 250 characters)
- `cod_amount` (float): Cash on delivery amount (>= 0)
- `delivery_type` (int): 0 for home delivery, 1 for point delivery
- `note` (str, optional): Additional notes

**Returns:**
- `Order`: Order object with consignment_id, tracking_code, and status

**Raises:**
- `ValidationError`: If any input validation fails
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
from steadfast import SteadastClient

client = SteadastClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)

order = client.orders.create(
    invoice="ORD-2024-001",
    recipient_name="John Smith",
    recipient_phone="01234567890",
    recipient_address="House 123, Dhaka",
    cod_amount=1060,
    delivery_type=0,
    note="Handle with care"
)

print(f"Order created: {order.consignment_id}")
print(f"Tracking code: {order.tracking_code}")
```

### create_bulk()

Create multiple orders in a single request (up to 500).

**Signature:**
```python
def create_bulk(orders: List[Dict[str, Any]]) -> BulkOrderResponse
```

**Parameters:**
- `orders` (list): List of order dictionaries with same fields as create()

**Returns:**
- `BulkOrderResponse`: Contains list of BulkOrderResult with individual success/error status

**Raises:**
- `ValidationError`: If validation fails (empty list, > 500 items, invalid fields)
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
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

response = client.orders.create_bulk(orders)

for result in response.results:
    if result.status == "success":
        print(f"Order {result.invoice}: {result.consignment_id}")
    else:
        print(f"Order {result.invoice} failed: {result.error}")
```

## Validation Rules

| Field | Rule | Example |
|-------|------|---------|
| invoice | Alphanumeric, hyphens, underscores | ORD-2024-001 |
| recipient_name | Max 100 characters | John Smith |
| recipient_phone | Exactly 11 digits | 01234567890 |
| recipient_address | Max 250 characters | House 123, Dhaka |
| cod_amount | Numeric, >= 0 | 1060 |
| delivery_type | 0 or 1 | 0 |

## Error Handling

```python
from steadfast import SteadastClient, ValidationError, APIError, NetworkError

client = SteadastClient(api_key="key", secret_key="secret")

try:
    order = client.orders.create(
        invoice="ORD-2024-001",
        recipient_name="John Smith",
        recipient_phone="01234567890",
        recipient_address="House 123, Dhaka",
        cod_amount=1060,
        delivery_type=0,
    )
except ValidationError as e:
    print(f"Validation error: {e}")
except APIError as e:
    print(f"API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```
