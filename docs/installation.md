# Installation Guide

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### From PyPI (Recommended)

```bash
pip install steadfast-python
```

<!--
### From Source

```bash
git clone https://github.com/mojnomiya/steadfast-python.git
cd steadfast-python
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/mojnomiya/steadfast-python.git
cd steadfast-python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```
-->

## Verification

Verify installation:

```python
from steadfast import SteadfastClient

print("Steadfast SDK installed successfully!")
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
    delivery_type=0
)

print(f"Order created: {order.consignment_id}")
```

## Virtual Environment Setup

### Using venv

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install steadfast-python

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n steadfast python=3.9

# Activate environment
conda activate steadfast

# Install package
pip install steadfast-python

# Deactivate when done
conda deactivate
```

## Dependencies

The SDK requires:

- `requests>=2.28.0` - HTTP client library
- `python-dotenv>=0.21.0` - Environment variable management

These are automatically installed with the package.

## Troubleshooting

### "ModuleNotFoundError: No module named 'steadfast'"

**Solution:**
```bash
pip install steadfast-python
```

### "ImportError: cannot import name 'SteadfastClient'"

**Solution:**
```bash
# Verify installation
pip show steadfast-python

# Reinstall if needed
pip install --upgrade steadfast-python
```

### Virtual Environment Issues

**Solution:**
```bash
# Deactivate current environment
deactivate

# Create new environment
python3 -m venv venv

# Activate new environment
source venv/bin/activate

# Install package
pip install steadfast-python
```

## Upgrading

### Upgrade to Latest Version

```bash
pip install --upgrade steadfast-python
```

### Upgrade to Specific Version

```bash
pip install steadfast-python==0.2.0
```

### Check Installed Version

```bash
pip show steadfast-python
```

Or in Python:

```python
import steadfast
print(steadfast.__version__)
```

## Uninstallation

```bash
pip uninstall steadfast-python
```

## Next Steps

1. Read the [Authentication Guide](authentication.md)
2. Check [Order Management API](order_management.md)
3. Review [Error Handling Guide](error_handling.md)
4. Explore [Examples](../examples/)
