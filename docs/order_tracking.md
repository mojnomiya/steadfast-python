# Order Tracking API

## Overview

The Tracking module provides methods to retrieve the current status and delivery information of orders using different identifiers.

## Methods

### get_status_by_consignment_id()

Get order status by consignment ID.

**Signature:**
```python
def get_status_by_consignment_id(consignment_id: int) -> OrderStatus
```

**Parameters:**
- `consignment_id` (int): Positive integer consignment ID

**Returns:**
- `OrderStatus`: Object with status code and delivery_status

**Raises:**
- `ValidationError`: If consignment_id is invalid
- `NotFoundError`: If order not found
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

status = client.tracking.get_status_by_consignment_id(123)
print(f"Status: {status.delivery_status}")
```

### get_status_by_invoice()

Get order status by invoice number.

**Signature:**
```python
def get_status_by_invoice(invoice: str) -> OrderStatus
```

**Parameters:**
- `invoice` (str): Invoice identifier (alphanumeric, hyphens, underscores)

**Returns:**
- `OrderStatus`: Object with status code and delivery_status

**Raises:**
- `ValidationError`: If invoice format is invalid
- `NotFoundError`: If order not found
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
status = client.tracking.get_status_by_invoice("ORD-2024-001")
print(f"Status: {status.delivery_status}")
```

### get_status_by_tracking_code()

Get order status by tracking code.

**Signature:**
```python
def get_status_by_tracking_code(tracking_code: str) -> OrderStatus
```

**Parameters:**
- `tracking_code` (str): Tracking code from order response

**Returns:**
- `OrderStatus`: Object with status code and delivery_status

**Raises:**
- `ValidationError`: If tracking_code is empty
- `NotFoundError`: If order not found
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
status = client.tracking.get_status_by_tracking_code("TRACK123")
print(f"Status: {status.delivery_status}")
```

## Delivery Status Values

Common delivery status values:

| Status | Description |
|--------|-------------|
| pending | Order created, awaiting pickup |
| in_transit | Order picked up and in transit |
| out_for_delivery | Order out for delivery |
| delivered | Order delivered |
| failed | Delivery failed |
| returned | Order returned |
| cancelled | Order cancelled |

## Error Handling

```python
from steadfast import SteadastClient, ValidationError, NotFoundError, APIError

client = SteadastClient(api_key="key", secret_key="secret")

try:
    status = client.tracking.get_status_by_consignment_id(123)
    print(f"Delivery status: {status.delivery_status}")
except ValidationError as e:
    print(f"Invalid input: {e}")
except NotFoundError as e:
    print(f"Order not found: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Polling for Updates

```python
import time
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

def wait_for_delivery(consignment_id: int, max_attempts: int = 10):
    for attempt in range(max_attempts):
        status = client.tracking.get_status_by_consignment_id(consignment_id)

        if status.delivery_status == "delivered":
            print("Order delivered!")
            return True

        if status.delivery_status == "failed":
            print("Delivery failed!")
            return False

        print(f"Attempt {attempt + 1}: {status.delivery_status}")
        time.sleep(60)  # Wait 1 minute before next check

    return False

wait_for_delivery(123)
```
