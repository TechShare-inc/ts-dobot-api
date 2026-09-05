"""Concrete Motion namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Motion
from ..exceptions import NotSupportedError
from ._utils import _build_dyn_params, _pose_from_tuple

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot

    from ..types import Pose


class MotionV3(Motion):
    """Concrete Motion implementation for V3 API."""

    native: V3Robot

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
        dyn = _build_dyn_params(speed_l=speed, accel_l=accel, cp=cp, user=user, tool=tool)
        return self.native.arc(x1, y1, z1, rx1, ry1, rz1, x2, y2, z2, rx2, ry2, rz2, *dyn)

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
        raise NotSupportedError()

    def get_start_pose(self, trace_name: str) -> Pose:
        return _pose_from_tuple(self.native.get_path_start_pose(trace_name))

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
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel, cp=cp)
        return self.native.joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn)

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
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel, cp=cp, user=user, tool=tool)
        return self.native.mov_j(x, y, z, rx, ry, rz, *dyn)

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
        dyn = _build_dyn_params(speed_l=speed, accel_l=accel, cp=cp, user=user, tool=tool)
        return self.native.mov_l(x, y, z, rx, ry, rz, *dyn)

    def move_jog(self, axis_id: str = "") -> int:
        """Start or stop jog motion."""
        return self.native.move_jog(axis_id)

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
        return self.native.servo_j(j1, j2, j3, j4, j5, j6, t=t, lookahead_time=lookahead_time, gain=gain)

    def servo_js(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
    ) -> int:
        """Use the V3-only simplified joint-servo command."""
        return self.native.servo_js(j1, j2, j3, j4, j5, j6)

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
        return self.native.servo_p(x, y, z, rx, ry, rz)

    def start_path(
        self,
        trace_name: str,
        *,
        is_const: int = -1,
        multi: float = -1.0,
        cart: int = -1,
    ) -> int:
        if multi != -1.0:
            raise NotSupportedError("The multi option is available only in V4")
        return self.native.start_path(trace_name, is_const, cart)

    def sync(self, timeout: float = 30.0) -> None:
        """Block until all queued motion commands have completed."""
        self.native.sync()
