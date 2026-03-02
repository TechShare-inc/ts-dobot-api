# ts-dobot-api

TechShare Dobot API wrapper.

## Prerequisites

- Python >= 3.10

## Setup

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>

# Or initialize submodules after cloning
git submodule update --init --recursive

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

## Submodules

| Submodule | Path | Branch |
|-----------|------|--------|
| TCP-IP-Python-V4 | `vendor/TCP-IP-Python-V4` | `ts-main` |
| TCP-IP-Python-V3 | `vendor/TCP-IP-Python-V3` | `ts-main` |
