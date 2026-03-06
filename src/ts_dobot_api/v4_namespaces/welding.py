"""Concrete Welding namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Welding

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class WeldingV4(Welding):
    """Concrete Welding implementation for V4 API."""

    native: V4Robot

    def weave_start(self) -> None:
        self.native.weave_start()
