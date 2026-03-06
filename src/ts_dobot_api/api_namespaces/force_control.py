"""
Force control (V4+ only)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    from ..types import Pose


class ForceControl(RobotNamespace[object]):
    """Force control (V4+ only)"""

    def enable_ft_sensor(self, status: int) -> None:
        """Enable or disable the force/torque sensor."""
        raise NotImplementedError

    def six_force_home(self) -> None:
        """Zero (home) the six-axis force/torque sensor."""
        raise NotImplementedError

    def get_force(self) -> Pose:
        """Return force/torque readings from the sensor."""
        raise NotImplementedError

    def fc_off(self) -> None:
        """Turn off force-compliance mode."""
        raise NotImplementedError
