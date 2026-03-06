"""Concrete Raw namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Raw

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class RawV3(Raw):
    """Concrete Raw implementation for V3 API."""

    native: V3Robot

    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response."""
        return self.native.dashboard.send_recv_msg(command)
