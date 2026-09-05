"""Concrete Query namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Query
from ..exceptions import NotSupportedError
from ._utils import _pose_from_tuple

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot

    from ..types import Pose


class QueryV3(Query):
    """Concrete Query implementation for V3 API."""

    native: V3Robot

    def get_angle(self) -> Pose:
        """Return the current joint angles (as a Pose with j1-j6 in x-rz)."""
        return _pose_from_tuple(self.native.get_angle())

    def get_current_command_id(self) -> int:
        raise NotSupportedError("Current command ID is not available in the V3 vendor API")

    def get_error_id(self) -> tuple[int, ...]:
        """Return a tuple of currently-active error IDs."""
        return self.native.get_error_id()

    def get_pose(self) -> Pose:
        """Return the current Cartesian pose."""
        return _pose_from_tuple(self.native.get_pose())

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
        return _pose_from_tuple(self.native.inverse_solution(x, y, z, rx, ry, rz, user, tool))

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
        return _pose_from_tuple(self.native.positive_solution(j1, j2, j3, j4, j5, j6, user, tool))

    def robot_mode(self) -> int:
        """Return the current robot mode."""
        return self.native.robot_mode()

    def start_drag(self) -> None:
        """Enter drag/teach mode."""
        self.native.start_drag()

    def stop_drag(self) -> None:
        """Exit drag/teach mode."""
        self.native.stop_drag()
