"""
Query robot state
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._base import RobotNamespace

if TYPE_CHECKING:
    from ..types import Pose


class Query(RobotNamespace[object]):
    """Query robot state"""

    def robot_mode(self) -> int:
        """Return the current robot mode."""
        raise NotImplementedError

    def get_pose(self) -> Pose:
        """Return the current Cartesian pose."""
        raise NotImplementedError

    def get_angle(self) -> Pose:
        """Return the current joint angles (as a Pose with j1-j6 in x-rz)."""
        raise NotImplementedError

    def get_error_id(self) -> tuple[int, ...]:
        """Return a tuple of currently-active error IDs."""
        raise NotImplementedError

    def start_drag(self) -> None:
        """Enter drag/teach mode."""
        raise NotImplementedError

    def stop_drag(self) -> None:
        """Exit drag/teach mode."""
        raise NotImplementedError

    def get_current_command_id(self) -> int:
        """Return the queue ID of the currently executing command."""
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError
