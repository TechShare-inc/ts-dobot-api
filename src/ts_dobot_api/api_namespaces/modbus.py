"""
Modbus Operations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._base import RobotNamespace

if TYPE_CHECKING:
    pass


class Modbus(RobotNamespace[object]):
    """Modbus Operations"""

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int = -1) -> int:
        """Create a Modbus master station."""
        raise NotImplementedError

    def modbus_close(self, index: int) -> None:
        """Close Modbus master station."""
        raise NotImplementedError

    def get_hold_regs(self, index: int, addr: int, count: int, val_type: str = "") -> tuple[float, ...] | str:
        """Read holding registers in the native protocol response format."""
        raise NotImplementedError

    def set_hold_regs(
        self,
        index: int,
        addr: int,
        count: int,
        val_tab: str,
        val_type: str = "",
    ) -> None:
        """Write holding registers."""
        raise NotImplementedError
