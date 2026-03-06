"""Concrete Io namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Io

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class IoV3(Io):
    """Concrete Io implementation for V3 API."""

    native: V3Robot

    def ai(self, index: int) -> int:
        return self.native.ai(index)

    def ao(self, index: int, value: float) -> None:
        """Set an analogue output."""
        self.native.dashboard.ao(index, value)

    def ao_instant(self, index: int, value: float) -> None:
        self.native.ao_instant(index, value)

    def di(self, index: int) -> int:
        """Read a digital input."""
        return self.native.dashboard.di(index)

    def do_instant(self, index: int, status: int) -> None:
        self.native.do_instant(index, status)

    def do_output(self, index: int, status: int) -> None:
        """Set a digital output."""
        self.native.dashboard.do_output(index, status)

    def get_ao(self, index: int) -> float:
        return self.native.get_ao(index)

    def get_do(self, index: int) -> int:
        return self.native.get_do(index)

    def get_tool_do(self, index: int) -> int:
        return self.native.get_tool_do(index)

    def tool_ai(self, index: int) -> int:
        return self.native.tool_ai(index)

    def tool_di(self, index: int) -> int:
        """Read a tool digital input."""
        return self.native.dashboard.tool_di(index)

    def tool_do(self, index: int, status: int) -> None:
        """Set a tool digital output."""
        self.native.dashboard.tool_do(index, status)

    def tool_do_instant(self, index: int, status: int) -> None:
        self.native.tool_do_instant(index, status)
