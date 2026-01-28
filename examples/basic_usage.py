"""Basic usage example of Steadfast SDK."""

from steadfast import SteadastClient

# Initialize client
client = SteadastClient(api_key="your_api_key", secret_key="your_secret_key")

# Check balance
balance = client.balance.get_current_balance()
print(f"Current balance: {balance.current_balance}")

# Create an order
order = client.orders.create(
    invoice="ORD-2024-001",
    recipient_name="John Smith",
    recipient_phone="01234567890",
    recipient_address="House 123, Dhaka",
    cod_amount=1060,
    delivery_type=0,
    note="Handle with care",
)

print("Order created!")
print(f"  Consignment ID: {order.consignment_id}")
print(f"  Tracking Code: {order.tracking_code}")
print(f"  Status: {order.status}")

# Track the order
status = client.tracking.get_status_by_consignment_id(order.consignment_id)
print(f"\nOrder status: {status.delivery_status}")
