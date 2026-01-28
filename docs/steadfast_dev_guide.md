# Steadfast Courier Python SDK - Development Guide

**For Agentic AI Code Development**

---

## Project Structure and Setup

### Directory Tree

```
steadfast-python/
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .env.example
│
├── steadfast/
│   ├── __init__.py
│   ├── client.py
│   ├── exceptions.py
│   ├── models.py
│   ├── http_client.py
│   ├── validators.py
│   ├── logger.py
│   └── modules/
│       ├── __init__.py
│       ├── order.py
│       ├── tracking.py
│       ├── balance.py
│       ├── return_request.py
│       ├── payment.py
│       └── location.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_order.py
│   ├── test_tracking.py
│   ├── test_balance.py
│   ├── test_return_request.py
│   ├── test_payment.py
│   ├── test_location.py
│   ├── test_validators.py
│   └── fixtures/
│       └── mock_responses.py
│
├── examples/
│   ├── basic_usage.py
│   ├── create_order.py
│   ├── bulk_orders.py
│   ├── tracking_orders.py
│   ├── return_management.py
│   └── error_handling.py
│
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── authentication.md
│   ├── order_management.md
│   ├── order_tracking.md
│   ├── balance_management.md
│   ├── return_requests.md
│   ├── payments.md
│   └── error_handling.md
│
└── .github/
    └── workflows/
        ├── tests.yml
        └── publish.yml
```

---

## Implementation Guide

### Phase 1: Setup and Configuration Files

#### 1.1 setup.py

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="steadfast",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python SDK for Steadfast Courier API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/steadfast-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.21.0",
    ],
)
```

#### 1.2 .env.example

```
STEADFAST_API_KEY=your_api_key_here
STEADFAST_SECRET_KEY=your_secret_key_here
STEADFAST_TIMEOUT=30
STEADFAST_MAX_RETRIES=3
```

---

## Phase 2: Core Infrastructure

### 2.1 Exceptions

Create `steadfast/exceptions.py` with these classes:

```python
class SteadfastException(Exception)
class AuthenticationError(SteadfastException)
class ValidationError(SteadfastException)
class NotFoundError(SteadfastException)
class APIError(SteadfastException)
class NetworkError(SteadfastException)
class ConfigurationError(SteadfastException)
```

Each exception should have:
- Clear error message
- Context information (field name for ValidationError, status code for APIError)
- Custom `__str__()` method

### 2.2 Data Models

Create `steadfast/models.py` with dataclasses:

**Order Models:**
- `Order` - Single order response
- `BulkOrderResult` - Individual result in bulk response
- `BulkOrderResponse` - List of bulk results

**Tracking Models:**
- `OrderStatus` - Order status response

**Balance Models:**
- `Balance` - Account balance response

**Return Request Models:**
- `ReturnRequest` - Return request details
- `ReturnRequestList` - List of return requests

**Payment Models:**
- `Payment` - Payment information
- `PaymentDetails` - Payment with consignments
- `PaymentList` - List of payments

**Location Models:**
- `PoliceStation` - Police station information
- `PoliceStationList` - List of police stations

### 2.3 Validators

Create `steadfast/validators.py` with functions:

```python
def validate_invoice(value: str) -> str
def validate_phone(value: str) -> str
def validate_address(value: str) -> str
def validate_email(value: str) -> str
def validate_recipient_name(value: str) -> str
def validate_cod_amount(value: float) -> float
def validate_delivery_type(value: int) -> int
def validate_consignment_id(value: int) -> int
def validate_identifier_type(value: str) -> str
```

Each validator should:
- Check for None/empty
- Check constraints
- Raise ValidationError with field name
- Return normalized value

### 2.4 Logger

Create `steadfast/logger.py`:

```python
def get_logger(name: str) -> logging.Logger
def setup_logging(level: str = "INFO") -> None
```

---

## Phase 3: HTTP Client

Create `steadfast/http_client.py`:

```python
class HTTPClient:
    """Wrapper around requests library with retry logic."""

    def __init__(self, base_url: str, timeout: int = 30,
                 max_retries: int = 3, retry_backoff: float = 0.3)
    def get(self, endpoint: str, headers: dict = None, params: dict = None) -> dict
    def post(self, endpoint: str, headers: dict = None, data: dict = None) -> dict
    def _make_request(self, method: str, endpoint: str, ...) -> dict
    def _should_retry(self, exception: Exception, attempt: int) -> bool
    def _exponential_backoff(self, attempt: int) -> None
```

Features:
- Base URL management
- Authentication headers
- Error handling and response parsing
- Exponential backoff retry logic
- Request timeout handling
- Logging (without sensitive data)

---

## Phase 4: Order Module

Create `steadfast/modules/order.py`:

```python
class OrderModule:
    def __init__(self, http_client: HTTPClient)
    def create(self, invoice: str, recipient_name: str, ...) -> Order
    def create_bulk(self, orders: List[Dict]) -> BulkOrderResponse
    def _validate_order(self, **kwargs) -> dict
    def _prepare_order_payload(self, **kwargs) -> dict
```

Validation:
- Invoice: alphanumeric, hyphens, underscores, not empty
- Recipient name: max 100 chars
- Phone: exactly 11 digits
- Address: max 250 chars
- COD amount: numeric, >= 0
- Delivery type: 0 or 1
- Bulk orders: max 500 items

---

## Phase 5: Tracking Module

Create `steadfast/modules/tracking.py`:

```python
class TrackingModule:
    def __init__(self, http_client: HTTPClient)
    def get_status_by_consignment_id(self, consignment_id: int) -> OrderStatus
    def get_status_by_invoice(self, invoice: str) -> OrderStatus
    def get_status_by_tracking_code(self, tracking_code: str) -> OrderStatus
```

Features:
- Three different tracking methods
- Error handling for invalid inputs
- Return OrderStatus with delivery status

---

## Phase 6: Balance Module

Create `steadfast/modules/balance.py`:

```python
class BalanceModule:
    def __init__(self, http_client: HTTPClient)
    def get_current_balance(self) -> Balance
```

Simple implementation returning current balance.

---

## Phase 7: Return Request Module

Create `steadfast/modules/return_request.py`:

```python
class ReturnRequestModule:
    def __init__(self, http_client: HTTPClient)
    def create(self, identifier: str, identifier_type: str = "consignment_id",
               reason: str = None) -> ReturnRequest
    def get(self, return_request_id: int) -> ReturnRequest
    def list(self) -> ReturnRequestList
    def _validate_identifier(self, identifier: str, identifier_type: str)
```

Features:
- Support three identifier types
- Validate identifier and type
- Create, retrieve, and list return requests

---

## Phase 8: Payment Module

Create `steadfast/modules/payment.py`:

```python
class PaymentModule:
    def __init__(self, http_client: HTTPClient)
    def list(self) -> PaymentList
    def get(self, payment_id: int) -> PaymentDetails
```

Simple payment tracking operations.

---

## Phase 9: Location Module

Create `steadfast/modules/location.py`:

```python
class LocationModule:
    def __init__(self, http_client: HTTPClient)
    def get_police_stations(self) -> PoliceStationList
```

Police station lookup for return handling.

---

## Phase 10: Main Client Class

Create `steadfast/client.py`:

```python
class SteadfastClient:
    def __init__(self, api_key: str = None, secret_key: str = None,
                 timeout: int = 30, max_retries: int = 3,
                 retry_backoff: float = 0.3)

    @property
    def orders(self) -> OrderModule
    @property
    def tracking(self) -> TrackingModule
    @property
    def balance(self) -> BalanceModule
    @property
    def returns(self) -> ReturnRequestModule
    @property
    def payments(self) -> PaymentModule
    @property
    def locations(self) -> LocationModule

    def _load_credentials_from_env(self) -> dict
    def _validate_credentials(self) -> None
    def _initialize_modules(self) -> None
```

Responsibilities:
- Load credentials from parameters or .env
- Initialize HTTPClient with authentication
- Initialize all modules
- Provide module access via properties

---

## Phase 11: Package Initialization

Create `steadfast/__init__.py`:

```python
from steadfast.client import SteadfastClient
from steadfast.exceptions import (
    SteadfastException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    APIError,
    NetworkError,
    ConfigurationError,
)

__version__ = "0.1.0"
__all__ = [
    "SteadfastClient",
    # ... exceptions
    # ... models
]
```

---

## Phase 12: Testing Suite

### Test Files to Create:

1. **tests/conftest.py** - Shared fixtures
2. **tests/test_order.py** - Order module tests
3. **tests/test_tracking.py** - Tracking module tests
4. **tests/test_balance.py** - Balance module tests
5. **tests/test_return_request.py** - Return request tests
6. **tests/test_payment.py** - Payment tests
7. **tests/test_location.py** - Location tests
8. **tests/test_validators.py** - Validator tests
9. **tests/fixtures/mock_responses.py** - Mock API responses

### Test Pattern Example:

```python
def test_create_order_success(mock_http_client):
    """Test successful order creation."""
    module = OrderModule(mock_http_client)
    expected_response = {
        "consignment_id": 1424107,
        "tracking_code": "15BAEB8A",
        # ... other fields
    }
    mock_http_client.post.return_value = expected_response

    result = module.create(
        invoice="ORD-001",
        recipient_name="John Smith",
        # ... other params
    )

    assert result.consignment_id == 1424107
    mock_http_client.post.assert_called_once()
```

Target coverage: **80%+**

---

## Phase 13: Documentation

Create in `docs/` directory:
- `index.md` - Documentation home
- `installation.md` - Installation guide
- `authentication.md` - Authentication guide
- `order_management.md` - Order management
- `order_tracking.md` - Order tracking
- `balance_management.md` - Balance operations
- `return_requests.md` - Return request guide
- `payments.md` - Payment tracking
- `error_handling.md` - Error handling guide

---

## Phase 14: Examples

Create in `examples/` directory:

1. **basic_usage.py** - Hello world example
2. **create_order.py** - Single order creation
3. **bulk_orders.py** - Bulk order creation
4. **tracking_orders.py** - Order tracking examples
5. **return_management.py** - Return request examples
6. **error_handling.py** - Error handling patterns

---

## Phase 15: CI/CD Configuration

### .github/workflows/tests.yml

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    - name: Lint
      run: |
        flake8 steadfast
        black --check steadfast
    - name: Type check
      run: mypy steadfast
    - name: Test
      run: pytest --cov=steadfast tests/
```

---

## Key Implementation Differences from Pathao

### Authentication
- **Pathao:** OAuth 2.0 with token refresh
- **Steadfast:** Simple API Key + Secret Key headers (no refresh needed)

### Order Creation
- **Pathao:** More detailed (delivery_type: 48 or 12)
- **Steadfast:** Simpler (delivery_type: 0 or 1)

### Tracking
- **Pathao:** Single endpoint, different query types
- **Steadfast:** Three separate endpoints

### Features
- **Pathao:** Store management, location hierarchy
- **Steadfast:** Return requests, payments, police stations

### Return Handling
- **Pathao:** No built-in return feature
- **Steadfast:** Dedicated return request management

---

## Code Quality Standards

- **PEP 8 Compliance:** Use Black formatter
- **Type Hints:** All public methods
- **Docstrings:** Google style format
- **Testing:** Pytest with 80%+ coverage
- **Linting:** Flake8
- **Type Checking:** MyPy

---

## Development Commands

```bash
# Format code
black steadfast/ tests/

# Check formatting
black --check steadfast/ tests/

# Lint
flake8 steadfast/ tests/

# Type check
mypy steadfast/

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=steadfast --cov-report=html

# Install in development mode
pip install -e .

# Build package
python -m build
```

---

## Security Considerations

- Never log API keys or secret keys
- Validate SSL certificates
- Use HTTPS only
- Sanitize error messages
- Input validation before API calls

---

## Common Patterns

### Module Implementation Pattern

```python
class ModuleClass:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def method_name(self, param: Type) -> ReturnType:
        # Validate input
        validated_param = validate_param(param)

        # Prepare payload
        payload = {"key": validated_param}

        # Make API call
        response = self.http_client.post(
            "/endpoint",
            data=payload
        )

        # Parse response
        return ModelClass.from_dict(response)
```

### Error Handling Pattern

```python
try:
    # API call
    response = self.http_client.post(endpoint, data=payload)
except requests.Timeout:
    raise NetworkError("Request timeout")
except requests.RequestException as e:
    raise NetworkError(str(e))
except Exception as e:
    if response.status_code == 404:
        raise NotFoundError(...)
    else:
        raise APIError(...)
```

---

**Development Guide Complete**
