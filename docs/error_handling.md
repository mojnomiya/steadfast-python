# Error Handling Guide

## Exception Hierarchy

```
SteadfastException (base)
├── AuthenticationError
├── ValidationError
├── NotFoundError
├── APIError
├── NetworkError
└── ConfigurationError
```

## Exception Types

### SteadfastException

Base exception for all Steadfast SDK errors.

```python
from steadfast import SteadfastException

try:
    # SDK operation
    pass
except SteadfastException as e:
    print(f"Steadfast error: {e}")
```

### AuthenticationError

Raised when authentication fails (HTTP 401).

```python
from steadfast import AuthenticationError

try:
    order = client.orders.create(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check API key and secret key
```

### ValidationError

Raised when input validation fails.

```python
from steadfast import ValidationError

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
    print(f"Validation error: {e}")
    print(f"Field: {e.field}")  # Access field name
```

### NotFoundError

Raised when resource is not found (HTTP 404).

```python
from steadfast import NotFoundError

try:
    status = client.tracking.get_status_by_consignment_id(999)
except NotFoundError as e:
    print(f"Order not found: {e}")
```

### APIError

Raised for general API errors.

```python
from steadfast import APIError

try:
    order = client.orders.create(...)
except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")  # Access HTTP status code
```

### NetworkError

Raised for network-related errors with retry information.

```python
from steadfast import NetworkError

try:
    order = client.orders.create(...)
except NetworkError as e:
    print(f"Network error: {e}")
    if e.retry_after:
        print(f"Retry after: {e.retry_after} seconds")
```

### ConfigurationError

Raised when SDK is not properly configured.

```python
from steadfast import ConfigurationError

try:
    # Missing API key
    client = SteadastClient(secret_key="secret")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Error Handling Patterns

### Basic Try-Catch

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
    print(f"Order created: {order.consignment_id}")
except ValidationError as e:
    print(f"Invalid input: {e}")
except APIError as e:
    print(f"API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

### Retry Logic

```python
import time
from steadfast import SteadastClient, NetworkError

client = SteadastClient(api_key="key", secret_key="secret")

def create_order_with_retry(max_retries: int = 3):
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
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise

order = create_order_with_retry()
```

### Specific Error Handling

```python
from steadfast import (
    SteadastClient,
    ValidationError,
    NotFoundError,
    AuthenticationError,
    APIError,
    NetworkError,
)

client = SteadastClient(api_key="key", secret_key="secret")

try:
    status = client.tracking.get_status_by_consignment_id(123)
except ValidationError as e:
    # Handle validation errors
    print(f"Invalid input: {e}")
except NotFoundError as e:
    # Handle not found
    print(f"Order not found: {e}")
except AuthenticationError as e:
    # Handle authentication
    print(f"Authentication failed: {e}")
except APIError as e:
    # Handle API errors
    print(f"API error ({e.status_code}): {e}")
except NetworkError as e:
    # Handle network errors
    print(f"Network error: {e}")
```

### Bulk Operation Error Handling

```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

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

    successful = []
    failed = []

    for result in response.results:
        if result.status == "success":
            successful.append(result)
        else:
            failed.append(result)

    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    for result in failed:
        print(f"Order {result.invoice}: {result.error}")

except Exception as e:
    print(f"Bulk operation failed: {e}")
```

## Common Error Scenarios

### Invalid Credentials

```python
from steadfast import SteadastClient, ConfigurationError

try:
    client = SteadastClient()  # No credentials provided
except ConfigurationError as e:
    print(f"Error: {e}")
    # Solution: Provide api_key and secret_key or set environment variables
```

### Invalid Input

```python
from steadfast import ValidationError

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
    print(f"Error: {e}")
    # Solution: Use valid invoice format (alphanumeric, hyphens, underscores)
```

### Network Timeout

```python
from steadfast import NetworkError

try:
    order = client.orders.create(...)
except NetworkError as e:
    print(f"Error: {e}")
    # Solution: Check network connection and retry
```

### Order Not Found

```python
from steadfast import NotFoundError

try:
    status = client.tracking.get_status_by_consignment_id(999)
except NotFoundError as e:
    print(f"Error: {e}")
    # Solution: Verify consignment ID is correct
```

## Best Practices

1. **Always catch specific exceptions first**, then general ones
2. **Log errors with context** for debugging
3. **Implement retry logic** for network errors
4. **Validate input early** to catch ValidationError
5. **Handle bulk operations** with partial failure support
6. **Use environment variables** for credentials
7. **Never log sensitive data** (API keys, secret keys)
