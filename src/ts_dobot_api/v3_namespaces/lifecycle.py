"""Concrete Lifecycle namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Lifecycle

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class LifecycleV3(Lifecycle):
    """Concrete Lifecycle implementation for V3 API."""

    native: V3Robot

    def shutdown(self) -> None:
        """Gracefully disable the robot arm."""
        self.native.shutdown()

    def startup(
        self,
        speed: int = 40,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        *,
        power_on_wait: float = 20.0,
    ) -> None:
        """Run the standard V3 startup sequence."""
        self.native.startup(
            speed=speed,
            load=load,
            center_x=center_x,
            center_y=center_y,
            center_z=center_z,
            power_on_wait=power_on_wait,
        )
