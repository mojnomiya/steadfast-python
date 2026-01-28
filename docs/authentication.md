# Authentication Guide

## Overview

The Steadfast SDK uses API key and secret key authentication. Credentials can be provided via parameters or environment variables.

## Getting Credentials

1. Log in to your Steadfast account
2. Navigate to API Settings
3. Generate API Key and Secret Key
4. Store them securely

## Authentication Methods

### Method 1: Direct Parameters

```python
from steadfast import SteadfastClient

client = SteadfastClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)
```

### Method 2: Environment Variables

Set environment variables:

```bash
export STEADFAST_API_KEY="your_api_key"
export STEADFAST_SECRET_KEY="your_secret_key"
```

Then initialize without parameters:

```python
from steadfast import SteadfastClient

client = SteadfastClient()
```

### Method 3: .env File

Create `.env` file in your project root:

```
STEADFAST_API_KEY=your_api_key
STEADFAST_SECRET_KEY=your_secret_key
```

Load with python-dotenv:

```python
from dotenv import load_dotenv
from steadfast import SteadfastClient

load_dotenv()
client = SteadfastClient()
```

## Configuration

### Custom Base URL

```python
from steadfast import SteadfastClient

client = SteadfastClient(
    api_key="your_api_key",
    secret_key="your_secret_key",
    base_url="https://custom.api.com"
)
```

### Environment-Specific Configuration

```python
import os
from steadfast import SteadfastClient

env = os.getenv("ENVIRONMENT", "production")

if env == "development":
    base_url = "https://dev.api.steadfast.io"
else:
    base_url = "https://api.steadfast.io"

client = SteadfastClient(
    api_key=os.getenv("STEADFAST_API_KEY"),
    secret_key=os.getenv("STEADFAST_SECRET_KEY"),
    base_url=base_url
)
```

## Security Best Practices

### 1. Never Hardcode Credentials

❌ **Bad:**
```python
client = SteadfastClient(
    api_key="abc123def456",
    secret_key="xyz789uvw012"
)
```

✅ **Good:**
```python
import os
from steadfast import SteadfastClient

client = SteadfastClient(
    api_key=os.getenv("STEADFAST_API_KEY"),
    secret_key=os.getenv("STEADFAST_SECRET_KEY")
)
```

### 2. Use .env Files

Create `.env` file:
```
STEADFAST_API_KEY=your_api_key
STEADFAST_SECRET_KEY=your_secret_key
```

Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

### 3. Rotate Credentials Regularly

- Change API keys periodically
- Revoke old keys after rotation
- Monitor key usage

### 4. Use Separate Keys for Different Environments

```python
import os

if os.getenv("ENVIRONMENT") == "production":
    api_key = os.getenv("PROD_STEADFAST_API_KEY")
    secret_key = os.getenv("PROD_STEADFAST_SECRET_KEY")
else:
    api_key = os.getenv("DEV_STEADFAST_API_KEY")
    secret_key = os.getenv("DEV_STEADFAST_SECRET_KEY")

from steadfast import SteadfastClient
client = SteadfastClient(api_key=api_key, secret_key=secret_key)
```

### 5. Restrict Key Permissions

- Use read-only keys where possible
- Limit key scope to specific operations
- Monitor key activity

## Error Handling

### Missing Credentials

```python
from steadfast import SteadfastClient, ConfigurationError

try:
    client = SteadfastClient()  # No credentials provided
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Set STEADFAST_API_KEY and STEADFAST_SECRET_KEY environment variables
```

### Invalid Credentials

```python
from steadfast import SteadfastClient, AuthenticationError

client = SteadfastClient(
    api_key="invalid_key",
    secret_key="invalid_secret"
)

try:
    order = client.orders.create(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check API key and secret key
```

## Testing

### Using Mock Credentials

```python
import os
from unittest.mock import patch
from steadfast import SteadfastClient

# Mock environment variables
with patch.dict(os.environ, {
    "STEADFAST_API_KEY": "test_key",
    "STEADFAST_SECRET_KEY": "test_secret"
}):
    client = SteadfastClient()
    # Use client for testing
```

### Using Test Credentials

```python
from steadfast import SteadfastClient

# Use test/sandbox credentials
client = SteadfastClient(
    api_key="test_api_key",
    secret_key="test_secret_key",
    base_url="https://sandbox.api.steadfast.io"
)
```

## Troubleshooting

### "API key is required" Error

**Cause:** API key not provided or not found in environment

**Solution:**
1. Check environment variables are set
2. Verify .env file exists and is loaded
3. Pass api_key parameter directly

### "Secret key is required" Error

**Cause:** Secret key not provided or not found in environment

**Solution:**
1. Check environment variables are set
2. Verify .env file exists and is loaded
3. Pass secret_key parameter directly

### "Authentication failed" Error

**Cause:** Invalid API key or secret key

**Solution:**
1. Verify credentials are correct
2. Check credentials haven't expired
3. Regenerate credentials if needed
4. Ensure using correct environment (dev/prod)

## Example: Complete Setup

```python
import os
from dotenv import load_dotenv
from steadfast import SteadfastClient, ConfigurationError

# Load environment variables
load_dotenv()

try:
    # Initialize client
    client = SteadfastClient(
        api_key=os.getenv("STEADFAST_API_KEY"),
        secret_key=os.getenv("STEADFAST_SECRET_KEY")
    )

    # Test connection
    balance = client.balance.get_current_balance()
    print(f"Connected! Balance: {balance.current_balance}")

except ConfigurationError as e:
    print(f"Configuration error: {e}")
    print("Please set STEADFAST_API_KEY and STEADFAST_SECRET_KEY")
except Exception as e:
    print(f"Error: {e}")
```
