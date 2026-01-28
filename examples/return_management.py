"""Return management example."""

from steadfast import SteadfastClient

client = SteadfastClient(api_key="your_api_key", secret_key="your_secret_key")

# Create return by consignment ID
return_req = client.returns.create(
    identifier=123, identifier_type="consignment_id", reason="Item damaged"
)
print(f"Return created: {return_req.id}")
print(f"Status: {return_req.status}")

# Create return by invoice
return_req = client.returns.create(
    identifier="ORD-2024-001", identifier_type="invoice", reason="Wrong item sent"
)
print(f"Return created: {return_req.id}")

# Get return details
return_req = client.returns.get(1)
print("Return details:")
print(f"  ID: {return_req.id}")
print(f"  Status: {return_req.status}")
print(f"  Reason: {return_req.reason}")
print(f"  Created: {return_req.created_at}")

# List all returns
returns = client.returns.list()
print(f"\nTotal returns: {len(returns.data)}")

# Filter by status
pending = [r for r in returns.data if r.status == "pending"]
print(f"Pending returns: {len(pending)}")

for return_req in pending:
    print(f"  - Return {return_req.id}: {return_req.reason}")
