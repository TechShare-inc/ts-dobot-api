---
title: Connect and Ping
description: Learn the first successful call pattern.
---

# Connect and Ping

This tutorial shows a minimal end-to-end flow and links to runnable example code.

## Prerequisites

- Package installed
- Test endpoint configured

## Steps

1. Initialize a client.
2. Call a health-check method.
3. Print and verify output.

```python
from package_name import Client


def main() -> None:
    client = Client.connect("endpoint")
    print(client.ping())


if __name__ == "__main__":
    main()
```

## Developer Notes

This path prioritizes fast feedback over exhaustive setup.

## Next Steps

- [How to configure authentication](../how-to/)
- [API reference](../reference/api/)
- [Runnable example](../../examples/01_basic_ping.py)
