"""Concrete ForceControl namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import ForceControl
from ._utils import _pose_from_v4

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot

    from ..types import Pose


class ForceControlV4(ForceControl):
    """Concrete ForceControl implementation for V4 API."""

    native: V4Robot

    def enable_ft_sensor(self, status: int) -> None:
        """Enable or disable the force/torque sensor."""
        self.native.dashboard.enable_ft_sensor(status)

    def fc_off(self) -> None:
        """Turn off force-compliance mode."""
        self.native.fc_off()

    def get_force(self) -> Pose:
        """Return force/torque readings from the sensor."""
        return _pose_from_v4(self.native.get_force())

    def six_force_home(self) -> None:
        """Zero (home) the six-axis force/torque sensor."""
        self.native.dashboard.six_force_home()
