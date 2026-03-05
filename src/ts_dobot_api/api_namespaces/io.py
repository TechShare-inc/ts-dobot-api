"""
Digital/analog I/O
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    pass


class Io(RobotNamespace[object]):
    """Digital/analog I/O"""

    def do_output(self, index: int, status: int) -> None:
        """Set a digital output."""
        raise NotImplementedError

    def tool_do(self, index: int, status: int) -> None:
        """Set a tool digital output."""
        raise NotImplementedError

    def ao(self, index: int, value: float) -> None:
        """Set an analogue output."""
        raise NotImplementedError

    def di(self, index: int) -> int:
        """Read a digital input."""
        raise NotImplementedError

    def tool_di(self, index: int) -> int:
        """Read a tool digital input."""
        raise NotImplementedError

    def do_instant(self, index: int, status: int) -> None:
        """Set a digital output immediately (bypasses the motion queue)."""
        raise NotImplementedError

    def tool_do_instant(self, index: int, status: int) -> None:
        """Set a tool digital output immediately."""
        raise NotImplementedError

    def ao_instant(self, index: int, value: float) -> None:
        """Set an analogue output immediately."""
        raise NotImplementedError

    def ai(self, index: int) -> int:
        """Read an analogue input."""
        raise NotImplementedError

    def tool_ai(self, index: int) -> int:
        """Read a tool analogue input."""
        raise NotImplementedError

    def get_do(self, index: int) -> int:
        """Read the current status of a digital output."""
        raise NotImplementedError

    def get_tool_do(self, index: int) -> int:
        """Read the current status of a tool digital output."""
        raise NotImplementedError

    def get_ao(self, index: int) -> float:
        """Read the current value of an analogue output."""
        raise NotImplementedError
