# ts-dobot-api

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-1.0.0--alpha.1-orange)](https://github.com/TechShare-inc/ts-dobot-api)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

TechShare's unified interface for Dobot V3 and V4 robot APIs. The model passed
to `DobotRobot.connect()` selects the protocol-specific implementation.

## Prerequisites

- Python >= 3.10

## Setup

```bash
# Clone the repository
git clone https://github.com/TechShare-inc/ts-dobot-api.git

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Development

```bash
# Run tests
pytest

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Protocol selection

```python
from ts_dobot_api import DobotRobot

v3_robot = DobotRobot.connect("192.168.5.1", "NOVA")
v4_robot = DobotRobot.connect("192.168.5.1", "NOVA_2S")
```

`NOVA` uses V3. `CR`, `NOVA_2S`, and `NOVA_NG` use V4. The pinned V3 and V4
vendor packages are internal runtime dependencies and are installed
automatically.

Both protocols expose `motion.servo_j()`. The simplified `motion.servo_js()`
command is preserved for V3 callers and raises `NotSupportedError` for V4,
whose vendor protocol does not expose ServoJS. Feedback packets remain the
native typed packet for the selected protocol; higher-level adapters normalize
protocol-specific units.
