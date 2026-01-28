# Software Requirements Specification (SRS)
## Steadfast Courier Python SDK

**Document Version:** 1.0
**Date:** January 2026
**Author:** Development Team
**Status:** Draft

---

## 1. Executive Summary

This document specifies the requirements for developing a comprehensive Python SDK for the Steadfast Courier API. The SDK will provide developers with an easy-to-use, well-documented interface to integrate Steadfast's courier services into their Python applications. The package will be published on PyPI and made available as open-source software.

---

## 2. Project Overview

### 2.1 Purpose
Create a user-friendly Python wrapper around Steadfast Courier's REST API that abstracts away HTTP complexities and provides Pythonic interfaces for all Steadfast operations.

### 2.2 Scope
- **In Scope:**
  - API Key and Secret Key authentication
  - Order creation (single and bulk)
  - Delivery status tracking (by consignment ID, invoice, tracking code)
  - Balance checking
  - Return request management (create, view, list)
  - Payment tracking
  - Police station lookup
  - Support for both home and point delivery
  - Comprehensive error handling and logging
  - Type hints throughout the codebase
  - Unit and integration tests
  - Complete API documentation
  - Usage examples and tutorials

- **Out of Scope:**
  - Web UI/Dashboard
  - Real-time tracking websocket support (initial release)
  - Advanced analytics features
  - Multi-language documentation (English only for v1.0)
  - Webhook support (can be added in v2.0)

### 2.3 Target Users
- Python developers integrating Steadfast services
- E-commerce platforms
- Logistics management systems
- Third-party shipping integrators

---

## 3. Functional Requirements

### 3.1 Authentication Module

#### FR-3.1.1: API Key Authentication
- **Description:** System shall authenticate requests using API Key and Secret Key headers
- **Acceptance Criteria:**
  - Accept API Key and Secret Key from configuration
  - Add authentication headers to all requests
  - Handle invalid credentials gracefully
  - Store credentials securely (not in logs)

### 3.2 Order Management Module

#### FR-3.2.1: Create Single Order
- **Description:** Create a new order for shipment
- **Acceptance Criteria:**
  - Accept order parameters: invoice, recipient details, delivery type, COD amount
  - Validate all required fields
  - Support optional fields (alternative_phone, recipient_email, note, etc.)
  - Support both home delivery (0) and point delivery (1)
  - Return order confirmation with consignment_id and tracking_code
  - Handle validation errors gracefully

#### FR-3.2.2: Validate Invoice Format
- **Description:** Validate invoice is unique and properly formatted
- **Acceptance Criteria:**
  - Accept alphanumeric, hyphens, and underscores
  - Validate invoice is not empty
  - Enforce uniqueness at application level (optional server-side check)

#### FR-3.2.3: Create Bulk Orders
- **Description:** Create multiple orders in a single request
- **Acceptance Criteria:**
  - Accept up to 500 orders per request
  - Validate each order in the batch
  - Handle partial failures (some succeed, some fail)
  - Return per-order status (success/error)
  - Support batch processing

#### FR-3.2.4: Validate Order Parameters
- **Description:** Validate all order parameters before sending to API
- **Acceptance Criteria:**
  - Recipient name: max 100 characters
  - Recipient phone: exactly 11 digits
  - Alternative phone: exactly 11 digits (if provided)
  - Recipient address: max 250 characters
  - COD amount: numeric, >= 0
  - Delivery type: 0 or 1
  - All required fields present

### 3.3 Order Tracking Module

#### FR-3.3.1: Get Delivery Status by Consignment ID
- **Description:** Retrieve delivery status using consignment ID
- **Acceptance Criteria:**
  - Accept consignment_id as parameter
  - Return current delivery status
  - Support all status types (pending, delivered, cancelled, etc.)

#### FR-3.3.2: Get Delivery Status by Invoice
- **Description:** Retrieve delivery status using user-defined invoice ID
- **Acceptance Criteria:**
  - Accept invoice as parameter
  - Return current delivery status
  - Handle non-existent invoices gracefully

#### FR-3.3.3: Get Delivery Status by Tracking Code
- **Description:** Retrieve delivery status using tracking code
- **Acceptance Criteria:**
  - Accept tracking_code as parameter
  - Return current delivery status
  - Handle invalid tracking codes gracefully

### 3.4 Balance Management Module

#### FR-3.4.1: Check Current Balance
- **Description:** Retrieve current account balance
- **Acceptance Criteria:**
  - Return current balance in BDT
  - Handle authentication errors
  - Provide balance as numeric value

### 3.5 Return Request Management Module

#### FR-3.5.1: Create Return Request
- **Description:** Create a return request for an order
- **Acceptance Criteria:**
  - Accept consignment_id, invoice, or tracking_code
  - Accept optional reason for return
  - Return return request details with ID and status
  - Initial status should be 'pending'

#### FR-3.5.2: Get Return Request Details
- **Description:** Retrieve details of a specific return request
- **Acceptance Criteria:**
  - Accept return request ID
  - Return complete return request information
  - Include status, reason, timestamps

#### FR-3.5.3: List Return Requests
- **Description:** Retrieve all return requests
- **Acceptance Criteria:**
  - Return list of all return requests
  - Support optional filtering (optional, for future)
  - Include pagination (optional, for future)

### 3.6 Payment Management Module

#### FR-3.6.1: Get Payments List
- **Description:** Retrieve list of all payments
- **Acceptance Criteria:**
  - Return paginated list of payments
  - Include payment details and amounts

#### FR-3.6.2: Get Payment Details with Consignments
- **Description:** Retrieve payment details with associated consignments
- **Acceptance Criteria:**
  - Accept payment_id as parameter
  - Return payment details and related consignments
  - Validate payment_id exists

### 3.7 Location Services Module

#### FR-3.7.1: Get Police Stations
- **Description:** Retrieve list of police stations (for return handling)
- **Acceptance Criteria:**
  - Return list of all police stations
  - Include station details

### 3.8 Error Handling and Validation

#### FR-3.8.1: Input Validation
- **Description:** Validate all input parameters before API calls
- **Acceptance Criteria:**
  - Validate string lengths according to API specs
  - Validate phone number formats (11 digits)
  - Validate numeric ranges
  - Validate enum values (delivery_type: 0 or 1)
  - Raise appropriate validation errors

#### FR-3.8.2: API Error Handling
- **Description:** Handle all API error responses gracefully
- **Acceptance Criteria:**
  - Catch and parse API error responses
  - Create custom exception classes for different error types
  - Provide meaningful error messages
  - Support error logging and debugging

#### FR-3.8.3: Network Error Handling
- **Description:** Handle network-related failures
- **Acceptance Criteria:**
  - Handle connection timeouts
  - Handle network unreachability
  - Support configurable retry logic
  - Implement exponential backoff for retries

---

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-4.1.1:** API response times should be processed within 2 seconds
- **NFR-4.1.2:** Bulk order creation should support up to 500 orders per request
- **NFR-4.1.3:** SDK should minimize memory footprint

### 4.2 Reliability
- **NFR-4.2.1:** SDK should have 99% successful API call rate (excluding network failures)
- **NFR-4.2.2:** SDK should recover gracefully from transient failures
- **NFR-4.2.3:** Retry logic should prevent cascading failures

### 4.3 Usability
- **NFR-4.3.1:** API should follow Python best practices and PEP 8 standards
- **NFR-4.3.2:** All public methods should have comprehensive docstrings
- **NFR-4.3.3:** Type hints should be used throughout the codebase
- **NFR-4.3.4:** Error messages should be clear and actionable

### 4.4 Security
- **NFR-4.4.1:** Credentials should not be logged or exposed in error messages
- **NFR-4.4.2:** SDK should support HTTPS only
- **NFR-4.4.3:** API Keys and Secret Keys should be handled securely
- **NFR-4.4.4:** SDK should validate SSL certificates

### 4.5 Maintainability
- **NFR-4.5.1:** Code should have 80% minimum test coverage
- **NFR-4.5.2:** All complex functions should have comments explaining logic
- **NFR-4.5.3:** SDK should be version-compatible with Python 3.8+
- **NFR-4.5.4:** Dependencies should be minimal and well-maintained

### 4.6 Documentation
- **NFR-4.6.1:** Comprehensive README with quick start guide
- **NFR-4.6.2:** API reference documentation for all classes and methods
- **NFR-4.6.3:** Multiple examples for different use cases
- **NFR-4.6.4:** Contributing guidelines for open-source collaboration

---

## 5. System Architecture

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────┐
│     User Application                    │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Steadfast Python SDK                  │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐   │
│  │  Public API Layer               │   │
│  │ (Client Class - Main Interface) │   │
│  └────────────┬────────────────────┘   │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  Module Layer                    │ │
│  │ ├─ Order Module                  │ │
│  │ ├─ Tracking Module               │ │
│  │ ├─ Balance Module                │ │
│  │ ├─ Return Request Module         │ │
│  │ ├─ Payment Module                │ │
│  │ └─ Location Module               │ │
│  └────────────┬─────────────────────┘ │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  HTTP Client Layer               │ │
│  │ (Requests wrapper with retry)    │ │
│  └────────────┬─────────────────────┘ │
│               │                        │
│  ┌────────────▼──────────────────────┐ │
│  │  Utilities Layer                 │ │
│  │ ├─ Validators                    │ │
│  │ ├─ Exception Classes             │ │
│  │ ├─ Data Models (Dataclasses)     │ │
│  │ └─ Logging                       │ │
│  └──────────────────────────────────┘ │
└─────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Steadfast Courier API                 │
│  (Production)                           │
│  https://portal.packzy.com/api/v1      │
└─────────────────────────────────────────┘
```

### 5.2 Directory Structure

```
steadfast-python/
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── publish.yml
├── steadfast/
│   ├── __init__.py
│   ├── client.py                 # Main client class
│   ├── exceptions.py             # Custom exceptions
│   ├── models.py                 # Data models
│   ├── http_client.py            # HTTP wrapper
│   ├── validators.py             # Input validators
│   ├── logger.py                 # Logging setup
│   └── modules/
│       ├── __init__.py
│       ├── order.py              # Order operations
│       ├── tracking.py           # Tracking operations
│       ├── balance.py            # Balance operations
│       ├── return_request.py     # Return request operations
│       ├── payment.py            # Payment operations
│       └── location.py           # Location services
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_order.py
│   ├── test_tracking.py
│   ├── test_balance.py
│   ├── test_return_request.py
│   ├── test_payment.py
│   ├── test_location.py
│   ├── test_validators.py
│   └── fixtures/
│       └── mock_responses.py
├── examples/
│   ├── basic_usage.py
│   ├── create_order.py
│   ├── bulk_orders.py
│   ├── tracking_orders.py
│   ├── return_management.py
│   └── error_handling.py
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
└── .env.example
```

---

## 6. Technical Specifications

### 6.1 Technology Stack
- **Language:** Python 3.8+
- **HTTP Client:** requests library
- **Data Serialization:** JSON
- **Testing:** pytest
- **Documentation:** MkDocs / Sphinx
- **Package Management:** pip/setuptools
- **Version Control:** Git
- **CI/CD:** GitHub Actions

### 6.2 Dependencies
- `requests>=2.28.0` - HTTP client
- `python-dotenv>=0.21.0` - Environment variable management

### 6.3 Development Dependencies
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `pytest-mock>=3.10` - Mocking utilities
- `black>=22.0` - Code formatting
- `flake8>=4.0` - Linting
- `mypy>=0.990` - Type checking
- `sphinx>=5.0` - Documentation generation

---

## 7. API Interface Specification

### 7.1 Client Initialization

```python
from steadfast import SteadfastClient

# Initialize with credentials
client = SteadastClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)

# Or with .env file
client = SteadastClient()  # Reads from .env
```

### 7.2 Core Classes

#### SteadastClient
Main entry point for all SDK operations.

#### Module Classes
- `OrderModule` - Order creation and validation
- `TrackingModule` - Order status tracking
- `BalanceModule` - Account balance management
- `ReturnRequestModule` - Return request operations
- `PaymentModule` - Payment tracking
- `LocationModule` - Location services

---

## 8. Testing Strategy

### 8.1 Testing Scope
- Unit tests for all modules (target: 80% coverage)
- Integration tests for API calls (using mocks)
- Validation tests for input parameters
- Error handling tests

### 8.2 Testing Approach
- Use pytest framework
- Mock HTTP responses using responses library
- Fixture-based test data
- Parametrized tests for multiple scenarios

### 8.3 Test Categories
- Order creation (single and bulk)
- Order status tracking (all three methods)
- Balance checking
- Return request management
- Payment operations
- Error handling and edge cases
- Input validation

---

## 9. Release and Deployment

### 9.1 Version Strategy
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- Initial release: v0.1.0 (alpha)
- Stable release: v1.0.0

### 9.2 PyPI Publication
- Create PyPI account
- Configure setup.py/pyproject.toml
- Automated publishing via GitHub Actions
- Support for multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)

---

## 10. Project Milestones

### Phase 1: Core Development (Weeks 1-2)
- Project setup and configuration
- Implement validators
- Create data models
- Set up testing infrastructure

### Phase 2: Feature Implementation (Weeks 2-4)
- Implement order management
- Implement tracking services
- Implement balance management
- Implement return requests
- Implement payments and locations

### Phase 3: Testing & Documentation (Weeks 4-5)
- Comprehensive unit and integration tests
- Write API documentation
- Create usage examples
- Performance optimization

### Phase 4: Release Preparation (Week 5-6)
- Code review and refactoring
- Final testing and QA
- Prepare for PyPI publication
- Create release notes

---

## 11. Constraints and Assumptions

### 11.1 Constraints
- Must maintain compatibility with Python 3.8+
- API rate limits may apply from Steadfast
- Depends on Steadfast API availability
- SSL/TLS encryption required
- Maximum 500 items per bulk order

### 11.2 Assumptions
- Steadfast API structure remains stable
- Users have valid Steadfast credentials
- Internet connectivity is available
- Users have basic Python knowledge

---

## 12. Success Criteria

- [ ] All functional requirements implemented
- [ ] 80%+ test coverage achieved
- [ ] All tests passing (unit and integration)
- [ ] Code follows PEP 8 standards
- [ ] Documentation complete and reviewed
- [ ] Package successfully published on PyPI
- [ ] At least 50 downloads in first month
- [ ] No critical security vulnerabilities
- [ ] GitHub repository established with contributing guidelines
- [ ] Community feedback mechanisms in place

---

## 13. Glossary

- **API Key:** Authentication credential for Steadfast API
- **Secret Key:** Secondary authentication credential for Steadfast API
- **Consignment ID:** Unique identifier for a shipment
- **Tracking Code:** User-friendly identifier for tracking a shipment
- **COD:** Cash On Delivery payment method
- **Invoice:** User-defined unique order identifier
- **Delivery Type:** 0 for home delivery, 1 for point delivery
- **Return Request:** Request to return a delivered shipment
- **Police Station:** Designated locations for returns handling

---

## 14. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Dev Team | Initial SRS |

---

**Document End**
