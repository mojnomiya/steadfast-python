"""Order tracking example."""

import time

from steadfast import SteadastClient, NotFoundError

client = SteadastClient(api_key="your_api_key", secret_key="your_secret_key")

# Track by consignment ID
try:
    status = client.tracking.get_status_by_consignment_id(123)
    print(f"Status by consignment ID: {status.delivery_status}")
except NotFoundError:
    print("Order not found by consignment ID")

# Track by invoice
try:
    status = client.tracking.get_status_by_invoice("ORD-2024-001")
    print(f"Status by invoice: {status.delivery_status}")
except NotFoundError:
    print("Order not found by invoice")

# Track by tracking code
try:
    status = client.tracking.get_status_by_tracking_code("TRACK123")
    print(f"Status by tracking code: {status.delivery_status}")
except NotFoundError:
    print("Order not found by tracking code")


def wait_for_delivery(consignment_id: int, max_attempts: int = 5) -> bool:
    """Wait for order to be delivered."""
    for attempt in range(max_attempts):
        status = client.tracking.get_status_by_consignment_id(consignment_id)

        if status.delivery_status == "delivered":
            print("✓ Order delivered!")
            return True

        if status.delivery_status == "failed":
            print("✗ Delivery failed!")
            return False

        print(f"Attempt {attempt + 1}: {status.delivery_status}")
        if attempt < max_attempts - 1:
            time.sleep(2)

    print("Max attempts reached")
    return False


# Example usage
# wait_for_delivery(123)
