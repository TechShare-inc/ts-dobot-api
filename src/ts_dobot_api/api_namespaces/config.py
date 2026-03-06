"""
Configuration
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    pass


class Config(RobotNamespace[object]):
    """Configuration"""

    def vel_j(self, speed: int) -> None:
        """Set maximum joint velocity (%)."""
        raise NotImplementedError

    def vel_l(self, speed: int) -> None:
        """Set maximum Cartesian velocity (mm/s)."""
        raise NotImplementedError

    def acc_j(self, speed: int) -> None:
        """Set maximum joint acceleration (%)."""
        raise NotImplementedError

    def acc_l(self, speed: int) -> None:
        """Set maximum Cartesian acceleration (mm/s²)."""
        raise NotImplementedError

    def cp(self, ratio: int) -> None:
        """Set continuous-path blending ratio."""
        raise NotImplementedError

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Set the tool payload."""
        raise NotImplementedError

    def set_collision_level(self, level: int) -> None:
        """Set collision detection sensitivity level."""
        raise NotImplementedError

    def set_user(self, index: int) -> None:
        """Select the active user coordinate system."""
        raise NotImplementedError

    def set_tool(self, index: int) -> None:
        """Select the active tool coordinate system."""
        raise NotImplementedError
