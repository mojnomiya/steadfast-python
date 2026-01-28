"""Bulk orders example."""

from steadfast import SteadastClient

client = SteadastClient(api_key="your_api_key", secret_key="your_secret_key")

# Prepare bulk orders
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
    {
        "invoice": "ORD-2024-003",
        "recipient_name": "Bob Johnson",
        "recipient_phone": "01555555555",
        "recipient_address": "Office 789, Sylhet",
        "cod_amount": 3000,
        "delivery_type": 0,
    },
]

# Create bulk orders
response = client.orders.create_bulk(orders)

# Process results
successful = []
failed = []

for result in response.results:
    if result.status == "success":
        successful.append(result)
        print(f"✓ Order {result.invoice}: {result.consignment_id}")
    else:
        failed.append(result)
        print(f"✗ Order {result.invoice}: {result.error}")

print("Summary:")
print(f"  Successful: {len(successful)}")
print(f"  Failed: {len(failed)}")
