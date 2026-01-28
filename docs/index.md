# Steadfast Courier Python SDK Documentation

Welcome to the Steadfast Courier Python SDK documentation. This guide will help you integrate Steadfast courier services into your Python applications.

## Getting Started

- **[Installation](installation.md)** - Install the SDK and verify setup
- **[Authentication](authentication.md)** - Configure API credentials
- **[Quick Start](#quick-start)** - Create your first order

## API Reference

- **[Order Management](order_management.md)** - Create and manage orders
- **[Order Tracking](order_tracking.md)** - Track order status
- **[Balance Management](balance_management.md)** - Check account balance
- **[Return Requests](return_requests.md)** - Manage return requests
- **[Payments](payments.md)** - View payment information

## Guides

- **[Error Handling](error_handling.md)** - Handle errors and exceptions
- **[Examples](../examples/)** - Code examples and use cases

## Quick Start

### 1. Install the SDK

```bash
pip install steadfast
```

### 2. Set Up Credentials

Create a `.env` file:

```
STEADFAST_API_KEY=your_api_key
STEADFAST_SECRET_KEY=your_secret_key
```

### 3. Initialize Client

```python
from steadfast import SteadfastClient

client = SteadfastClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)
```

### 4. Create an Order

```python
order = client.orders.create(
    invoice="ORD-2024-001",
    recipient_name="John Smith",
    recipient_phone="01234567890",
    recipient_address="House 123, Dhaka",
    cod_amount=1060,
    delivery_type=0
)

print(f"Order created: {order.consignment_id}")
print(f"Tracking code: {order.tracking_code}")
```

### 5. Track Order

```python
status = client.tracking.get_status_by_consignment_id(order.consignment_id)
print(f"Status: {status.delivery_status}")
```

## Core Modules

### Orders Module

Create and manage courier orders.

```python
# Create single order
order = client.orders.create(...)

# Create bulk orders
response = client.orders.create_bulk([...])
```

### Tracking Module

Track order status using different identifiers.

```python
# By consignment ID
status = client.tracking.get_status_by_consignment_id(123)

# By invoice
status = client.tracking.get_status_by_invoice("ORD-2024-001")

# By tracking code
status = client.tracking.get_status_by_tracking_code("TRACK123")
```

### Balance Module

Check account balance.

```python
balance = client.balance.get_current_balance()
print(f"Balance: {balance.current_balance}")
```

### Return Requests Module

Manage return requests.

```python
# Create return
return_req = client.returns.create(
    identifier=123,
    identifier_type="consignment_id",
    reason="Damaged"
)

# Get return
return_req = client.returns.get(1)

# List returns
returns = client.returns.list()
```

### Payments Module

View payment information.

```python
# List payments
payments = client.payments.list()

# Get payment details
payment = client.payments.get(1)
```

## Exception Handling

The SDK provides specific exceptions for different error scenarios:

```python
from steadfast import (
    SteadfastClient,
    ValidationError,
    NotFoundError,
    AuthenticationError,
    APIError,
    NetworkError,
)

try:
    order = client.orders.create(...)
except ValidationError as e:
    print(f"Invalid input: {e}")
except NotFoundError as e:
    print(f"Not found: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

## Common Tasks

### Create Order and Track

```python
from steadfast import SteadfastClient

client = SteadfastClient(api_key="key", secret_key="secret")

# Create order
order = client.orders.create(
    invoice="ORD-2024-001",
    recipient_name="John Smith",
    recipient_phone="01234567890",
    recipient_address="House 123, Dhaka",
    cod_amount=1060,
    delivery_type=0
)

# Track order
status = client.tracking.get_status_by_consignment_id(order.consignment_id)
print(f"Status: {status.delivery_status}")
```

### Bulk Order Creation

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

### Check Balance Before Order

```python
balance = client.balance.get_current_balance()

if balance.current_balance >= 1000:
    order = client.orders.create(...)
else:
    print("Insufficient balance")
```

## Support

For issues and questions:

- Check the [Error Handling Guide](error_handling.md)
- Review [Examples](../examples/)
- Contact Steadfast support

## License

MIT License - See LICENSE file for details

## Version

Current version: 0.3.0

See [CHANGELOG](../CHANGELOG.md) for version history.
