"""Concrete Config namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Config

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class ConfigV4(Config):
    """Concrete Config implementation for V4 API."""

    native: V4Robot

    def acc_j(self, speed: int) -> None:
        """Set maximum joint acceleration (%)."""
        self.native.acc_j(speed)

    def acc_l(self, speed: int) -> None:
        """Set maximum Cartesian acceleration (mm/s²)."""
        self.native.acc_l(speed)

    def cp(self, ratio: int) -> None:
        """Set continuous-path blending ratio."""
        self.native.cp(ratio)

    def set_collision_level(self, level: int) -> None:
        """Set collision detection sensitivity level."""
        self.native.dashboard.set_collision_level(level)

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Set the tool payload."""
        self.native.dashboard.set_payload(load=weight, x=center_x, y=center_y, z=center_z)

    def set_tool(self, index: int) -> None:
        """Select the active tool coordinate system."""
        self.native.dashboard.tool(index)

    def set_user(self, index: int) -> None:
        """Select the active user coordinate system."""
        self.native.dashboard.user(index)

    def vel_j(self, speed: int) -> None:
        """Set maximum joint velocity (%)."""
        self.native.vel_j(speed)

    def vel_l(self, speed: int) -> None:
        """Set maximum Cartesian velocity (mm/s)."""
        self.native.vel_l(speed)
