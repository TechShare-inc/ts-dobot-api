"""
Raw protocol access
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._base import RobotNamespace

if TYPE_CHECKING:
    pass


class Raw(RobotNamespace[object]):
    """Raw protocol access"""

    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response."""
        raise NotImplementedError
