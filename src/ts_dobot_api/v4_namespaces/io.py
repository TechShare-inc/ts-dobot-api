"""Concrete Io namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Io

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class IoV4(Io):
    """Concrete Io implementation for V4 API."""

    native: V4Robot

    def ai(self, index: int) -> int:
        """Read an analogue input."""
        return self.native.dashboard.ai(index)

    def ao(self, index: int, value: float) -> None:
        """Set an analogue output."""
        self.native.ao(index, value)

    def ao_instant(self, index: int, value: float) -> None:
        """Set an analogue output immediately."""
        self.native.dashboard.ao_instant(index, value)

    def di(self, index: int) -> int:
        """Read a digital input."""
        return self.native.di(index)

    def do_instant(self, index: int, status: int) -> None:
        """Set a digital output immediately (bypasses the motion queue)."""
        self.native.dashboard.do_instant(index, status)

    def do_output(self, index: int, status: int) -> None:
        """Set a digital output."""
        self.native.do_output(index, status)

    def get_ao(self, index: int) -> float:
        """Read the current value of an analogue output."""
        return float(self.native.dashboard.get_ao(index))

    def get_do(self, index: int) -> int:
        """Read the current status of a digital output."""
        return self.native.get_do(index)

    def get_tool_do(self, index: int) -> int:
        """Read the current status of a tool digital output."""
        return self.native.dashboard.get_tool_do(index)

    def tool_ai(self, index: int) -> int:
        """Read a tool analogue input."""
        return self.native.dashboard.tool_ai(index)

    def tool_di(self, index: int) -> int:
        """Read a tool digital input."""
        return self.native.dashboard.tool_di(index)

    def tool_do(self, index: int, status: int) -> None:
        """Set a tool digital output."""
        self.native.dashboard.tool_do(index, status)

    def tool_do_instant(self, index: int, status: int) -> None:
        """Set a tool digital output immediately."""
        self.native.dashboard.tool_do_instant(index, status)
