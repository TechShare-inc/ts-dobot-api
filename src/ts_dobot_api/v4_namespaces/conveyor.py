"""Concrete Conveyor namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Conveyor

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class ConveyorV4(Conveyor):
    """Concrete Conveyor implementation for V4 API."""

    native: V4Robot

    def cnv_init(self, index: int) -> None:
        self.native.cnv_init(index)
