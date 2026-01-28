# Steadfast Courier Python SDK

<!-- [![Tests](https://github.com/mojnomiya/steadfast-python/actions/workflows/tests.yml/badge.svg)](https://github.com/mojnomiya/steadfast-python/actions/workflows/tests.yml)
[![Publish](https://github.com/mojnomiya/steadfast-python/actions/workflows/publish.yml/badge.svg)](https://github.com/mojnomiya/steadfast-python/actions/workflows/publish.yml) -->
[![PyPI version](https://badge.fury.io/py/steadfast-python.svg)](https://badge.fury.io/py/steadfast-python)
[![Python versions](https://img.shields.io/pypi/pyversions/steadfast-python.svg)](https://pypi.org/project/steadfast-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://readthedocs.org/projects/steadfast-python/badge/?version=latest)](https://steadfast-python.readthedocs.io/)

A Python SDK for the Steadfast Courier API that provides easy-to-use interfaces for order management, tracking, and other courier services.

## Features

- Simple API Key/Secret Key authentication
- Order creation (single and bulk up to 500 items)
- Multiple tracking methods (by consignment ID, invoice, tracking code)
- Return request management
- Balance and payment tracking
- Police station lookup
- Type hints throughout
- Comprehensive error handling

## Installation

```bash
pip install steadfast-python
```

## Quick Start

```python
from steadfast import SteadfastClient

# Initialize client
client = SteadfastClient(
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
```

## Development

### Setup

```bash
# Clone repository
git clone <repository-url>
cd steadfast-python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Code Quality

This project uses automated code quality checks with pre-commit hooks:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

Run quality checks manually:
```bash
# Run all checks
pre-commit run --all-files

# Or use the convenience script
./scripts/quality-check.sh
```

### Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=steadfast --cov-report=html
```

## Requirements

- Python 3.8+
- requests>=2.28.0
- python-dotenv>=0.21.0

## License

MIT License
