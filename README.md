# Steadfast Courier Python SDK

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
pip install steadfast
```

## Quick Start

```python
from steadfast import SteadastClient

# Initialize client
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
```

## Requirements

- Python 3.8+
- requests>=2.28.0
- python-dotenv>=0.21.0

## License

MIT License