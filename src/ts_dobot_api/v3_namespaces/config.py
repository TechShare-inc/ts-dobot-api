"""Concrete Config namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Config

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class ConfigV3(Config):
    """Concrete Config implementation for V3 API."""

    native: V3Robot

    def acc_j(self, speed: int) -> None:
        """Set maximum joint acceleration (%)."""
        self.native.dashboard.acc_j(speed)

    def acc_l(self, speed: int) -> None:
        """Set maximum Cartesian acceleration (mm/s²)."""
        self.native.dashboard.acc_l(speed)

    def cp(self, ratio: int) -> None:
        """Set continuous-path blending ratio."""
        self.native.dashboard.cp(ratio)

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
        self.native.dashboard.set_payload(weight, f"CenterX={center_x}", f"CenterY={center_y}", f"CenterZ={center_z}")

    def set_tool(self, index: int) -> None:
        """Select the active tool coordinate system."""
        self.native.dashboard.set_tool(index)

    def set_user(self, index: int) -> None:
        """Select the active user coordinate system."""
        self.native.dashboard.set_user(index)

    def vel_j(self, speed: int) -> None:
        """Set maximum joint velocity (%)."""
        self.native.dashboard.vel_j(speed)

    def vel_l(self, speed: int) -> None:
        """Set maximum Cartesian velocity (mm/s)."""
        self.native.dashboard.vel_l(speed)
