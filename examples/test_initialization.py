"""Test example - validates SDK initialization and module access."""

import os
from dotenv import load_dotenv
from steadfast import SteadfastClient

load_dotenv()

# Initialize client
client = SteadfastClient(
    api_key=os.getenv("STEADFAST_API_KEY"),
    secret_key=os.getenv("STEADFAST_SECRET_KEY"),
)

print("✓ Steadfast SDK Test Results")
print("=" * 50)
print("✓ Client initialized successfully")
print(f"✓ Orders module accessible: {type(client.orders).__name__}")
print(f"✓ Tracking module accessible: {type(client.tracking).__name__}")
print(f"✓ Balance module accessible: {type(client.balance).__name__}")
print(f"✓ Returns module accessible: {type(client.returns).__name__}")
print(f"✓ Payments module accessible: {type(client.payments).__name__}")
print(f"✓ Locations module accessible: {type(client.locations).__name__}")
print("=" * 50)
print("All modules initialized successfully!")
