"""
Motion control
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    from ..types import Pose


class Motion(RobotNamespace[object]):
    """Motion control"""

    def mov_j(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *,
        speed: int | None = None,
        accel: int | None = None,
        cp: int | None = None,
        user: int | None = None,
        tool: int | None = None,
    ) -> int:
        """Joint-space move to a Cartesian target."""
        raise NotImplementedError

    def mov_l(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
        *,
        speed: int | None = None,
        accel: int | None = None,
        cp: int | None = None,
        user: int | None = None,
        tool: int | None = None,
    ) -> int:
        """Linear move."""
        raise NotImplementedError

    def joint_mov_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *,
        speed: int | None = None,
        accel: int | None = None,
        cp: int | None = None,
    ) -> int:
        """Joint-space move with joint-angle targets."""
        raise NotImplementedError

    def servo_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *,
        t: float = 0.1,
        lookahead_time: float = 50.0,
        gain: float = 500.0,
    ) -> int:
        """Servo (streaming) move in joint space."""
        raise NotImplementedError

    def servo_p(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
    ) -> int:
        """Servo (streaming) move in Cartesian space."""
        raise NotImplementedError

    def move_jog(self, axis_id: str = "") -> int:
        """Start or stop jog motion."""
        raise NotImplementedError

    def arc(
        self,
        x1: float,
        y1: float,
        z1: float,
        rx1: float,
        ry1: float,
        rz1: float,
        x2: float,
        y2: float,
        z2: float,
        rx2: float,
        ry2: float,
        rz2: float,
        *,
        speed: int | None = None,
        accel: int | None = None,
        cp: int | None = None,
        user: int | None = None,
        tool: int | None = None,
    ) -> int:
        """Circular arc move through two via-points."""
        raise NotImplementedError

    def sync(self, timeout: float = 30.0) -> None:
        """Block until all queued motion commands have completed."""
        raise NotImplementedError

    def circle(
        self,
        x1: float,
        y1: float,
        z1: float,
        rx1: float,
        ry1: float,
        rz1: float,
        x2: float,
        y2: float,
        z2: float,
        rx2: float,
        ry2: float,
        rz2: float,
        *,
        count: int = 1,
        speed: int | None = None,
        accel: int | None = None,
        cp: int | None = None,
        user: int | None = None,
        tool: int | None = None,
    ) -> int:
        """Full-circle interpolated motion through two via-points."""
        raise NotImplementedError

    def start_path(
        self,
        trace_name: str,
        *,
        is_const: int = -1,
        multi: float = -1.0,
    ) -> int:
        """Play back a recorded trajectory file."""
        raise NotImplementedError

    def get_start_pose(self, trace_name: str) -> Pose:
        """Return the starting pose of a recorded trajectory."""
        raise NotImplementedError
