# Balance Management API

## Overview

The Balance module provides methods to retrieve account balance information.

## Methods

### get_current_balance()

Get current account balance.

**Signature:**
```python
def get_current_balance() -> Balance
```

**Returns:**
- `Balance`: Object with status code and current_balance amount

**Raises:**
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

balance = client.balance.get_current_balance()
print(f"Current balance: {balance.current_balance}")
```

## Balance Object

The Balance object contains:

| Field | Type | Description |
|-------|------|-------------|
| status | int | HTTP status code |
| current_balance | float | Account balance amount |

## Error Handling

```python
from steadfast import SteadastClient, APIError, NetworkError

client = SteadastClient(api_key="key", secret_key="secret")

try:
    balance = client.balance.get_current_balance()
    print(f"Balance: {balance.current_balance}")
except APIError as e:
    print(f"API error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

## Usage Examples

### Check balance before creating orders

```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

balance = client.balance.get_current_balance()

if balance.current_balance >= 1000:
    order = client.orders.create(
        invoice="ORD-2024-001",
        recipient_name="John Smith",
        recipient_phone="01234567890",
        recipient_address="House 123, Dhaka",
        cod_amount=1060,
        delivery_type=0,
    )
    print(f"Order created: {order.consignment_id}")
else:
    print("Insufficient balance")
```

### Monitor balance periodically

```python
import time
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

def monitor_balance(interval: int = 3600):
    """Monitor balance every interval seconds (default 1 hour)"""
    while True:
        try:
            balance = client.balance.get_current_balance()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Balance: {balance.current_balance}")

            if balance.current_balance < 500:
                print("WARNING: Low balance!")

            time.sleep(interval)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

monitor_balance()
```
