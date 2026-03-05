"""Concrete Raw namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Raw

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class RawV4(Raw):
    """Concrete Raw implementation for V4 API."""

    native: V4Robot

    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response."""
        return self.native.dashboard.send_recv_msg(command)
