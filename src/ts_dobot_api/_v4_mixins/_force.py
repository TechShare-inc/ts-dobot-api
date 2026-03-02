"""V4 force-control mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Pose

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class V4ForceMixin:
    """Force-control methods available only on V4 robots."""

    _native: V4Robot

    def enable_ft_sensor(self, status: int) -> None:
        """Enable/disable the force-torque sensor.

        Args:
            status: 0 = disable, 1 = enable.
        """
        self._native.dashboard.enable_ft_sensor(status)

    def six_force_home(self) -> None:
        """Zero (tare) the force-torque sensor."""
        self._native.dashboard.six_force_home()

    def get_force(self, tool: int = -1) -> Pose:
        """Read the current 6-axis force/torque values."""
        p = self._native.dashboard.get_force(tool)
        return Pose(x=p.x, y=p.y, z=p.z, rx=p.rx, ry=p.ry, rz=p.rz)

    def force_drive_mode(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int, *, user: int = -1
    ) -> None:
        """Enter force-drive mode for the specified axes."""
        self._native.dashboard.force_drive_mode(x, y, z, rx, ry, rz, user=user)

    def force_drive_speed(self, speed: int) -> None:
        """Set force-drive velocity."""
        self._native.dashboard.force_drive_speed(speed)

    def fc_force_mode(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        fx: int,
        fy: int,
        fz: int,
        frx: int,
        fry: int,
        frz: int,
        *,
        reference: int = -1,
        user: int = -1,
        tool: int = -1,
    ) -> None:
        """Set force compliance mode and target forces."""
        self._native.dashboard.fc_force_mode(
            x,
            y,
            z,
            rx,
            ry,
            rz,
            fx,
            fy,
            fz,
            frx,
            fry,
            frz,
            reference=reference,
            user=user,
            tool=tool,
        )

    def fc_set_deviation(
        self,
        x: int,
        y: int,
        z: int,
        rx: int,
        ry: int,
        rz: int,
        *,
        control_type: int = -1,
    ) -> None:
        """Set maximum allowable deviation."""
        self._native.dashboard.fc_set_deviation(
            x, y, z, rx, ry, rz, control_type=control_type
        )

    def fc_set_force_limit(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int
    ) -> None:
        """Set force limits for compliance mode."""
        self._native.dashboard.fc_set_force_limit(x, y, z, rx, ry, rz)

    def fc_set_mass(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set virtual mass for compliance mode."""
        self._native.dashboard.fc_set_mass(x, y, z, rx, ry, rz)

    def fc_set_stiffness(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int
    ) -> None:
        """Set virtual stiffness for compliance mode."""
        self._native.dashboard.fc_set_stiffness(x, y, z, rx, ry, rz)

    def fc_set_damping(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set virtual damping for compliance mode."""
        self._native.dashboard.fc_set_damping(x, y, z, rx, ry, rz)

    def fc_off(self) -> None:
        """Exit force compliance mode."""
        self._native.dashboard.fc_off()

    def fc_set_force_speed_limit(
        self, x: int, y: int, z: int, rx: int, ry: int, rz: int
    ) -> None:
        """Set speed limits during compliance mode."""
        self._native.dashboard.fc_set_force_speed_limit(x, y, z, rx, ry, rz)

    def fc_set_force(self, x: int, y: int, z: int, rx: int, ry: int, rz: int) -> None:
        """Set target forces directly."""
        self._native.dashboard.fc_set_force(x, y, z, rx, ry, rz)

    def fc_collision_switch(self, enable: int) -> None:
        """Enable or disable collision detection during force control."""
        self._native.dashboard.fc_collision_switch(enable)

    def set_fc_collision(self, force: float, torque: float) -> None:
        """Set force-control collision thresholds."""
        self._native.dashboard.set_fc_collision(force, torque)
