# Return Request Management API

## Overview

The Return Request module handles creation and management of return requests for orders.

## Methods

### create()

Create a return request for an order.

**Signature:**
```python
def create(
    identifier: Union[int, str],
    identifier_type: str = "consignment_id",
    reason: str = ""
) -> ReturnRequest
```

**Parameters:**
- `identifier` (int or str): Order identifier (consignment_id, invoice, or tracking_code)
- `identifier_type` (str): Type of identifier - "consignment_id", "invoice", or "tracking_code"
- `reason` (str, optional): Reason for return

**Returns:**
- `ReturnRequest`: Return request object with id, status, and timestamps

**Raises:**
- `ValidationError`: If inputs are invalid
- `NotFoundError`: If order not found
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

# Create return by consignment ID
return_req = client.returns.create(
    identifier=123,
    identifier_type="consignment_id",
    reason="Damaged package"
)
print(f"Return request created: {return_req.id}")

# Create return by invoice
return_req = client.returns.create(
    identifier="ORD-2024-001",
    identifier_type="invoice",
    reason="Wrong item sent"
)

# Create return by tracking code
return_req = client.returns.create(
    identifier="TRACK123",
    identifier_type="tracking_code"
)
```

### get()

Get a specific return request.

**Signature:**
```python
def get(return_request_id: int) -> ReturnRequest
```

**Parameters:**
- `return_request_id` (int): Return request ID

**Returns:**
- `ReturnRequest`: Return request object

**Raises:**
- `ValidationError`: If return_request_id is invalid
- `NotFoundError`: If return request not found
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
return_req = client.returns.get(1)
print(f"Status: {return_req.status}")
print(f"Reason: {return_req.reason}")
```

### list()

List all return requests.

**Signature:**
```python
def list() -> ReturnRequestList
```

**Returns:**
- `ReturnRequestList`: List of return requests

**Raises:**
- `APIError`: If API returns an error
- `NetworkError`: If network error occurs

**Example:**
```python
return_list = client.returns.list()

for return_req in return_list.data:
    print(f"Return {return_req.id}: {return_req.status}")
```

## Return Request Status

| Status | Description |
|--------|-------------|
| pending | Return request created, awaiting approval |
| approved | Return approved |
| processing | Return in process |
| completed | Return completed |
| cancelled | Return cancelled |

## Error Handling

```python
from steadfast import SteadastClient, ValidationError, NotFoundError, APIError

client = SteadastClient(api_key="key", secret_key="secret")

try:
    return_req = client.returns.create(
        identifier=123,
        identifier_type="consignment_id",
        reason="Damaged"
    )
    print(f"Return created: {return_req.id}")
except ValidationError as e:
    print(f"Invalid input: {e}")
except NotFoundError as e:
    print(f"Order not found: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Usage Examples

### Create return and track status

```python
from steadfast import SteadastClient

client = SteadastClient(api_key="key", secret_key="secret")

# Create return request
return_req = client.returns.create(
    identifier=123,
    identifier_type="consignment_id",
    reason="Item defective"
)

# Check status
updated = client.returns.get(return_req.id)
print(f"Return status: {updated.status}")
```

### List and filter returns

```python
return_list = client.returns.list()

pending_returns = [r for r in return_list.data if r.status == "pending"]
print(f"Pending returns: {len(pending_returns)}")

for return_req in pending_returns:
    print(f"Return {return_req.id}: {return_req.reason}")
```
