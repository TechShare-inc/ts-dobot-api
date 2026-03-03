#!/usr/bin/env python3
"""Placeholder helper for docs workflows.

Replace command bodies with project-specific Sphinx/VitePress commands.
"""

from __future__ import annotations

import subprocess
import sys


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    return subprocess.call(cmd)


def main() -> int:
    # Example placeholders:
    # run(["sphinx-build", "-b", "markdown", "docs", "docs/reference/api"])
    # run(["npm", "run", "docs:build"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
