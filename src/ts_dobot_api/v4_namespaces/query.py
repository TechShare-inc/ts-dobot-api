"""Concrete Query namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Query

from ._utils import _pose_from_v4

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot

    from ..types import Pose


class QueryV4(Query):
    """Concrete Query implementation for V4 API."""

    native: V4Robot

    def get_angle(self) -> Pose:
        """Return the current joint angles (as a Pose with j1-j6 in x-rz)."""
        return _pose_from_v4(self.native.get_angle())

    def get_current_command_id(self) -> int:
        """Return the queue ID of the currently executing command."""
        return self.native.get_current_command_id()

    def get_error_id(self) -> tuple[int, ...]:
        """Return a tuple of currently-active error IDs."""
        return self.native.get_error_id()

    def get_pose(self) -> Pose:
        """Return the current Cartesian pose."""
        return _pose_from_v4(self.native.get_pose())

    def inverse_kin(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *,
        user: int = -1,
        tool: int = -1,
    ) -> Pose:
        """Inverse kinematics — Cartesian pose to joint angles."""
        return _pose_from_v4(self.native.inverse_kin(x, y, z, rx, ry, rz, user=user, tool=tool))

    def positive_kin(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *,
        user: int = -1,
        tool: int = -1,
    ) -> Pose:
        """Forward kinematics — joint angles to Cartesian pose."""
        return _pose_from_v4(self.native.positive_kin(j1, j2, j3, j4, j5, j6, user=user, tool=tool))

    def robot_mode(self) -> int:
        """Return the current robot mode."""
        return self.native.robot_mode()

    def start_drag(self) -> None:
        """Enter drag/teach mode."""
        self.native.start_drag()

    def stop_drag(self) -> None:
        """Exit drag/teach mode."""
        self.native.stop_drag()
