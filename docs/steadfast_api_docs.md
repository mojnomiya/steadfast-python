# Steadfast Courier Python SDK - API Documentation

**Version:** 1.0.0
**Last Updated:** January 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Authentication](#authentication)
5. [API Reference](#api-reference)
   - [Client](#client)
   - [Order Management](#order-management)
   - [Order Tracking](#order-tracking)
   - [Balance Management](#balance-management)
   - [Return Requests](#return-requests)
   - [Payments](#payments)
   - [Locations](#locations)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Examples](#examples)

---

## Overview

The Steadfast Courier Python SDK provides a clean, Pythonic interface to the Steadfast Courier API. It handles authentication, request/response serialization, error handling, and provides convenient methods for all supported operations.

### Features

- ✅ Simple API Key/Secret Key authentication
- ✅ Type hints throughout the codebase
- ✅ Comprehensive input validation
- ✅ Detailed error messages
- ✅ Batch order creation (up to 500 items)
- ✅ Multiple order tracking methods
- ✅ Return request management
- ✅ Payment tracking
- ✅ Extensive documentation and examples

---

## Installation

### Via pip

```bash
pip install steadfast
```

### From source

```bash
git clone https://github.com/yourusername/steadfast-python.git
cd steadfast-python
pip install -e .
```

### Requirements

- Python 3.8 or higher
- `requests>=2.28.0`
- `python-dotenv>=0.21.0`

---

## Quick Start

### Basic Usage

```python
from steadfast import SteadastClient

# Initialize the client
client = SteadastClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)

# Create an order
order = client.orders.create(
    invoice="ORD-2024-001",
    recipient_name="John Smith",
    recipient_phone="01234567890",
    recipient_address="House 123, Dhaka",
    cod_amount=1060,
    delivery_type=0  # Home delivery
)

print(f"Order created: {order.consignment_id}")
print(f"Tracking code: {order.tracking_code}")
```

### Using Environment Variables

Create a `.env` file:

```
STEADFAST_API_KEY=your_api_key
STEADFAST_SECRET_KEY=your_secret_key
```

Then initialize without parameters:

```python
from steadfast import SteadastClient

client = SteadastClient()  # Reads from .env
```

---

## Authentication

### SteadastClient Class

```python
class SteadastClient:
    """
    Main client class for Steadfast Courier API interactions.

    Handles authentication and delegates operations to specific modules.
    """
```

#### Constructor

```python
def __init__(
    self,
    api_key: str = None,
    secret_key: str = None,
    timeout: int = 30,
    max_retries: int = 3,
    retry_backoff: float = 0.3
) -> None:
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | str | No | From .env | API Key from Steadfast |
| `secret_key` | str | No | From .env | Secret Key from Steadfast |
| `timeout` | int | No | 30 | Request timeout in seconds |
| `max_retries` | int | No | 3 | Max retry attempts for failed requests |
| `retry_backoff` | float | No | 0.3 | Backoff factor for exponential backoff |

**Example:**

```python
client = SteadastClient(
    api_key="your_api_key",
    secret_key="your_secret_key",
    timeout=30
)
```

---

## API Reference

### Order Management

#### OrderModule

Module for creating and managing orders.

**Access via:** `client.orders`

##### `create(...) -> Order`

Create a single order.

**Parameters:**

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `invoice` | str | Yes | Alphanumeric, hyphens, underscores | Unique order identifier |
| `recipient_name` | str | Yes | Max 100 chars | Recipient's full name |
| `recipient_phone` | str | Yes | Exactly 11 digits | Recipient's phone number |
| `recipient_address` | str | Yes | Max 250 chars | Delivery address |
| `cod_amount` | float/int | Yes | >= 0 | Cash on delivery amount (BDT) |
| `delivery_type` | int | No | 0 or 1 | 0=Home, 1=Point Delivery |
| `alternative_phone` | str | No | Exactly 11 digits | Secondary contact number |
| `recipient_email` | str | No | Valid email | Recipient's email |
| `note` | str | No | - | Delivery instructions |
| `item_description` | str | No | - | Item description |
| `total_lot` | int | No | >= 1 | Total lot of items |

**Returns:** `Order` object

**Raises:**
- `ValidationError` - Invalid parameters
- `APIError` - API request failed

**Example:**

```python
order = client.orders.create(
    invoice="ORD-2024-001",
    recipient_name="John Smith",
    recipient_phone="01234567890",
    recipient_address="House 123, Road 3, Dhaka-1209",
    cod_amount=1060,
    delivery_type=0,  # Home delivery
    note="Deliver before 5 PM"
)

print(f"Created: {order.consignment_id}")
print(f"Tracking: {order.tracking_code}")
print(f"Status: {order.status}")
```

##### `create_bulk(orders: List[Dict]) -> BulkOrderResponse`

Create multiple orders in a single request.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orders` | List[Dict] | Yes | List of order dictionaries (max 500) |

**Returns:** `BulkOrderResponse` object with list of individual results

**Raises:**
- `ValidationError` - Invalid parameters or exceeds 500 items
- `APIError` - API request failed

**Example:**

```python
orders = [
    {
        "invoice": "BULK-001",
        "recipient_name": "Customer 1",
        "recipient_phone": "01711111111",
        "recipient_address": "Address 1, Dhaka",
        "cod_amount": 500,
        "delivery_type": 0
    },
    {
        "invoice": "BULK-002",
        "recipient_name": "Customer 2",
        "recipient_phone": "01712222222",
        "recipient_address": "Address 2, Dhaka",
        "cod_amount": 1000,
        "delivery_type": 1
    }
]

response = client.orders.create_bulk(orders)

for result in response.results:
    if result.status == "success":
        print(f"Created: {result.consignment_id}")
    else:
        print(f"Failed: {result.invoice} - {result.error}")
```

---

### Order Tracking

#### TrackingModule

Module for tracking orders.

**Access via:** `client.tracking`

##### `get_status_by_consignment_id(consignment_id: int) -> OrderStatus`

Get delivery status by consignment ID.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `consignment_id` | int | Yes | Consignment identifier |

**Returns:** `OrderStatus` object with delivery status

**Raises:**
- `NotFoundError` - Consignment not found
- `APIError` - API request failed

**Example:**

```python
status = client.tracking.get_status_by_consignment_id(1424107)
print(f"Status: {status.delivery_status}")
```

##### `get_status_by_invoice(invoice: str) -> OrderStatus`

Get delivery status by invoice ID.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `invoice` | str | Yes | Invoice/order identifier |

**Returns:** `OrderStatus` object with delivery status

**Raises:**
- `NotFoundError` - Invoice not found
- `APIError` - API request failed

**Example:**

```python
status = client.tracking.get_status_by_invoice("ORD-2024-001")
print(f"Status: {status.delivery_status}")
```

##### `get_status_by_tracking_code(tracking_code: str) -> OrderStatus`

Get delivery status by tracking code.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tracking_code` | str | Yes | Tracking code |

**Returns:** `OrderStatus` object with delivery status

**Raises:**
- `NotFoundError` - Tracking code not found
- `APIError` - API request failed

**Example:**

```python
status = client.tracking.get_status_by_tracking_code("15BAEB8A")
print(f"Status: {status.delivery_status}")
```

##### Status Types

Valid delivery statuses:

| Status | Description |
|--------|-------------|
| `pending` | Not delivered or cancelled yet |
| `in_review` | Order placed, waiting for review |
| `delivered` | Successfully delivered |
| `partial_delivered` | Partially delivered |
| `cancelled` | Order cancelled |
| `delivered_approval_pending` | Delivered, awaiting approval |
| `partial_delivered_approval_pending` | Partially delivered, awaiting approval |
| `cancelled_approval_pending` | Cancelled, awaiting approval |
| `hold` | Order on hold |
| `unknown` | Unknown status |

---

### Balance Management

#### BalanceModule

Module for checking account balance.

**Access via:** `client.balance`

##### `get_current_balance() -> Balance`

Get current account balance.

**Returns:** `Balance` object with current balance

**Raises:** `APIError` - API request failed

**Example:**

```python
balance = client.balance.get_current_balance()
print(f"Current balance: {balance.current_balance} BDT")
```

---

### Return Requests

#### ReturnRequestModule

Module for managing return requests.

**Access via:** `client.returns`

##### `create(identifier: str, identifier_type: str = "consignment_id", reason: str = None) -> ReturnRequest`

Create a return request for an order.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `identifier` | str/int | Yes | Consignment ID, invoice, or tracking code |
| `identifier_type` | str | No | "consignment_id", "invoice", or "tracking_code" |
| `reason` | str | No | Reason for return |

**Returns:** `ReturnRequest` object

**Raises:**
- `ValidationError` - Invalid parameters
- `NotFoundError` - Order not found
- `APIError` - API request failed

**Example:**

```python
# By consignment ID
return_req = client.returns.create(
    identifier=1424107,
    identifier_type="consignment_id",
    reason="Item damaged"
)

# By invoice
return_req = client.returns.create(
    identifier="ORD-2024-001",
    identifier_type="invoice"
)

print(f"Return request created: {return_req.id}")
print(f"Status: {return_req.status}")
```

##### `get(return_request_id: int) -> ReturnRequest`

Get details of a specific return request.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `return_request_id` | int | Yes | Return request ID |

**Returns:** `ReturnRequest` object

**Raises:**
- `NotFoundError` - Return request not found
- `APIError` - API request failed

**Example:**

```python
return_req = client.returns.get(1)
print(f"Return ID: {return_req.id}")
print(f"Status: {return_req.status}")
print(f"Reason: {return_req.reason}")
```

##### `list() -> ReturnRequestList`

Get list of all return requests.

**Returns:** `ReturnRequestList` object containing list of return requests

**Raises:** `APIError` - API request failed

**Example:**

```python
returns = client.returns.list()

for ret in returns.data:
    print(f"Return {ret.id}: {ret.status}")
```

---

### Payments

#### PaymentModule

Module for tracking payments.

**Access via:** `client.payments`

##### `list() -> PaymentList`

Get list of all payments.

**Returns:** `PaymentList` object with paginated list of payments

**Raises:** `APIError` - API request failed

**Example:**

```python
payments = client.payments.list()

for payment in payments.data:
    print(f"Payment: {payment.id} - {payment.amount} BDT")
```

##### `get(payment_id: int) -> PaymentDetails`

Get payment details with associated consignments.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `payment_id` | int | Yes | Payment ID |

**Returns:** `PaymentDetails` object with payment info and consignments

**Raises:**
- `NotFoundError` - Payment not found
- `APIError` - API request failed

**Example:**

```python
payment = client.payments.get(123)

print(f"Payment: {payment.id}")
print(f"Amount: {payment.amount} BDT")
print(f"Consignments: {len(payment.consignments)}")

for consignment in payment.consignments:
    print(f"  - {consignment.consignment_id}")
```

---

### Locations

#### LocationModule

Module for location services.

**Access via:** `client.locations`

##### `get_police_stations() -> PoliceStationList`

Get list of all police stations (for return handling).

**Returns:** `PoliceStationList` object with list of police stations

**Raises:** `APIError` - API request failed

**Example:**

```python
stations = client.locations.get_police_stations()

for station in stations.data:
    print(f"Station: {station.name} - {station.location}")
```

---

## Data Models

All responses are returned as dataclass objects for type safety and ease of use.

### Order Models

```python
@dataclass
class Order:
    consignment_id: int
    invoice: str
    tracking_code: str
    recipient_name: str
    recipient_phone: str
    recipient_address: str
    cod_amount: float
    status: str
    note: str = None
    created_at: str
    updated_at: str
```

### OrderStatus

```python
@dataclass
class OrderStatus:
    status: int  # HTTP status code
    delivery_status: str  # Current status
```

### BulkOrderResult

```python
@dataclass
class BulkOrderResult:
    invoice: str
    recipient_name: str
    recipient_address: str
    recipient_phone: str
    cod_amount: float
    note: str = None
    consignment_id: int = None
    tracking_code: str = None
    status: str  # "success" or "error"
    error: str = None
```

### Balance

```python
@dataclass
class Balance:
    status: int
    current_balance: float
```

### ReturnRequest

```python
@dataclass
class ReturnRequest:
    id: int
    user_id: int
    consignment_id: int
    reason: str = None
    status: str  # pending, approved, processing, completed, cancelled
    created_at: str
    updated_at: str
```

### Payment

```python
@dataclass
class Payment:
    id: int
    amount: float
    # ... other payment fields
```

### PaymentDetails

```python
@dataclass
class PaymentDetails:
    id: int
    amount: float
    consignments: List[Dict]
    # ... other details
```

### PoliceStation

```python
@dataclass
class PoliceStation:
    id: int
    name: str
    location: str
    # ... other station details
```

---

## Error Handling

### Exception Hierarchy

```
SteadfastException (base)
├── AuthenticationError
├── ValidationError
├── NotFoundError
├── APIError
├── NetworkError
└── ConfigurationError
```

### Exception Classes

#### SteadfastException

Base exception for all Steadfast SDK errors.

```python
try:
    # SDK operation
except SteadfastException as e:
    print(f"Steadfast error: {e}")
```

#### ValidationError

Raised when input validation fails.

```python
from steadfast.exceptions import ValidationError

try:
    order = client.orders.create(
        invoice="",  # Empty (invalid)
        recipient_name="John",
        # ... other params
    )
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Field: {e.field}")
```

#### NotFoundError

Raised when requested resource is not found.

```python
from steadfast.exceptions import NotFoundError

try:
    status = client.tracking.get_status_by_invoice("NONEXISTENT")
except NotFoundError as e:
    print(f"Not found: {e}")
```

#### APIError

Raised for general API errors.

```python
from steadfast.exceptions import APIError

try:
    order = client.orders.create(...)
except APIError as e:
    print(f"API error code: {e.status_code}")
    print(f"Error message: {e.message}")
```

#### NetworkError

Raised for network-related failures.

```python
from steadfast.exceptions import NetworkError

try:
    balance = client.balance.get_current_balance()
except NetworkError as e:
    print(f"Network error: {e}")
    print(f"Retry after: {e.retry_after} seconds")
```

---

## Examples

### Example 1: Complete Order Workflow

```python
from steadfast import SteadastClient
from steadfast.exceptions import SteadfastException

# Initialize
client = SteadastClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)

try:
    # Create order
    order = client.orders.create(
        invoice="ORDER-001",
        recipient_name="John Doe",
        recipient_phone="01712345678",
        recipient_address="House 123, Dhaka-1209",
        cod_amount=1500,
        delivery_type=0,
        note="Call before delivery"
    )

    print(f"✓ Order created!")
    print(f"  Consignment ID: {order.consignment_id}")
    print(f"  Tracking Code: {order.tracking_code}")

    # Check status
    status = client.tracking.get_status_by_consignment_id(
        order.consignment_id
    )
    print(f"  Current Status: {status.delivery_status}")

except SteadfastException as e:
    print(f"✗ Error: {e}")
```

### Example 2: Bulk Order Creation

```python
from steadfast import SteadastClient

client = SteadastClient()

orders = [
    {
        "invoice": f"BULK-{i:03d}",
        "recipient_name": f"Customer {i}",
        "recipient_phone": f"0171234567{i % 10}",
        "recipient_address": f"Address {i}, Dhaka",
        "cod_amount": 500 * i,
        "delivery_type": 0
    }
    for i in range(1, 11)
]

response = client.orders.create_bulk(orders)

success_count = 0
error_count = 0

for result in response.results:
    if result.status == "success":
        success_count += 1
        print(f"✓ {result.invoice}: {result.consignment_id}")
    else:
        error_count += 1
        print(f"✗ {result.invoice}: {result.error}")

print(f"\nTotal: {success_count} successful, {error_count} failed")
```

### Example 3: Track Multiple Orders

```python
from steadfast import SteadastClient

client = SteadastClient()

invoices = ["ORDER-001", "ORDER-002", "ORDER-003"]

for invoice in invoices:
    try:
        status = client.tracking.get_status_by_invoice(invoice)
        print(f"{invoice}: {status.delivery_status}")
    except Exception as e:
        print(f"{invoice}: Error - {e}")
```

### Example 4: Return Management

```python
from steadfast import SteadastClient

client = SteadastClient()

# Create return request
return_req = client.returns.create(
    identifier="ORDER-001",
    identifier_type="invoice",
    reason="Item not as described"
)

print(f"Return request created: {return_req.id}")
print(f"Status: {return_req.status}")

# Check return status later
return_status = client.returns.get(return_req.id)
print(f"Current status: {return_status.status}")
```

---

## Additional Resources

- [GitHub Repository](https://github.com/yourusername/steadfast-python)
- [PyPI Package](https://pypi.org/project/steadfast/)
- [Official Steadfast API Documentation](https://steadfast.com.bd/docs)
- [Issue Tracker](https://github.com/yourusername/steadfast-python/issues)

---

**Documentation End**
