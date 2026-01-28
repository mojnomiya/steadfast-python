# Payment Management API

## Overview

The Payment module provides methods to retrieve payment information and transaction details.

## Methods

### list()

List all payments.

**Signature:**
```python
def list() -> PaymentList
```

**Returns:**
- `PaymentList`: List of Payment objects

**Raises:**
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

payments = client.payments.list()

for payment in payments.data:
    print(f"Payment {payment.id}: {payment.amount}")
```

### get()

Get payment details with associated consignments.

**Signature:**
```python
def get(payment_id: int) -> PaymentDetails
```

**Parameters:**
- `payment_id` (int): Payment ID

**Returns:**
- `PaymentDetails`: Payment object with consignments list

**Raises:**
- `ValidationError`: If payment_id is invalid
- `NotFoundError`: If payment not found
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
payment = client.payments.get(1)
print(f"Payment amount: {payment.amount}")
print(f"Consignments: {len(payment.consignments)}")

for consignment in payment.consignments:
    print(f"  - Consignment {consignment['consignment_id']}: {consignment['amount']}")
```

## Payment Objects

### Payment

| Field | Type | Description |
|-------|------|-------------|
| id | int | Payment ID |
| amount | float | Payment amount |
| created_at | str | Creation timestamp |
| updated_at | str | Last update timestamp |

### PaymentDetails

| Field | Type | Description |
|-------|------|-------------|
| id | int | Payment ID |
| amount | float | Payment amount |
| consignments | list | List of consignment objects |
| created_at | str | Creation timestamp |
| updated_at | str | Last update timestamp |

## Error Handling

```python
from steadfast import SteadastClient, ValidationError, NotFoundError, APIError

client = SteadastClient(api_key="key", secret_key="secret")

try:
    payment = client.payments.get(1)
    print(f"Amount: {payment.amount}")
except ValidationError as e:
    print(f"Invalid input: {e}")
except NotFoundError as e:
    print(f"Payment not found: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Usage Examples

### Get total payments

```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

payments = client.payments.list()
total = sum(p.amount for p in payments.data)
print(f"Total payments: {total}")
```

### Find payments by amount range

```python
payments = client.payments.list()

large_payments = [p for p in payments.data if p.amount >= 5000]
print(f"Large payments (>= 5000): {len(large_payments)}")

for payment in large_payments:
    print(f"Payment {payment.id}: {payment.amount}")
```

### Analyze payment details

```python
payment = client.payments.get(1)

print(f"Payment ID: {payment.id}")
print(f"Total Amount: {payment.amount}")
print(f"Number of Consignments: {len(payment.consignments)}")

total_consignment_amount = sum(c['amount'] for c in payment.consignments)
print(f"Total Consignment Amount: {total_consignment_amount}")

if total_consignment_amount == payment.amount:
    print("Payment amount matches consignments")
else:
    print("Payment amount mismatch!")
```
