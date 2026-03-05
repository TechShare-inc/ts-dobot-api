"""Concrete Modbus namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Modbus

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class ModbusV3(Modbus):
    """Concrete Modbus implementation for V3 API."""

    native: V3Robot

    def get_hold_regs(self, index: int, addr: int, count: int, val_type: str = "") -> list | int | float:
        return self.native.get_hold_regs(index, addr, count, val_type)

    def modbus_close(self, index: int) -> None:
        self.native.modbus_close(index)

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int = -1) -> int:
        return self.native.modbus_create(ip, port, slave_id, is_rtu)

    def set_hold_regs(self, index: int, addr: int, count: int, val_tab: str | list, val_type: str = "") -> None:
        self.native.set_hold_regs(index, addr, count, val_tab, val_type)
