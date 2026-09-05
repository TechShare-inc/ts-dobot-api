"""Concrete Motion namespace for V4 API."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ..api_namespaces import Motion
from ..exceptions import NotSupportedError
from ._utils import _opt, _pose_from_v4

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot

    from ..types import Pose


class MotionV4(Motion):
    """Concrete Motion implementation for V4 API."""

    native: V4Robot

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
        return self.native.arc(
            x1,
            y1,
            z1,
            rx1,
            ry1,
            rz1,
            x2,
            y2,
            z2,
            rx2,
            ry2,
            rz2,
            coordinate_mode=0,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
            cp=_opt(cp),
        )

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
        return self.native.circle(
            x1,
            y1,
            z1,
            rx1,
            ry1,
            rz1,
            x2,
            y2,
            z2,
            rx2,
            ry2,
            rz2,
            coordinate_mode=0,
            count=count,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
            cp=_opt(cp),
        )

    def get_start_pose(self, trace_name: str) -> Pose:
        """Return the starting pose of a recorded trajectory."""
        return _pose_from_v4(self.native.dashboard.get_start_pose(trace_name))

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
        return self.native.mov_j(
            j1,
            j2,
            j3,
            j4,
            j5,
            j6,
            coordinate_mode=1,
            a=_opt(accel),
            v=_opt(speed),
            cp=_opt(cp),
        )

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
        return self.native.mov_j(
            x,
            y,
            z,
            rx,
            ry,
            rz,
            coordinate_mode=0,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
            cp=_opt(cp),
        )

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
        return self.native.mov_l(
            x,
            y,
            z,
            rx,
            ry,
            rz,
            coordinate_mode=0,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
            cp=_opt(cp),
        )

    def move_jog(self, axis_id: str = "") -> int:
        """Start or stop jog motion."""
        self.native.move_jog(axis_id=axis_id)
        return 0  # V4 move_jog returns None

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
        return self.native.servo_j(j1, j2, j3, j4, j5, j6, t=t, ahead_time=lookahead_time, gain=gain)

    def servo_js(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
    ) -> int:
        """Reject the V3-only simplified joint-servo command."""
        raise NotSupportedError("ServoJS is available only through the V3 protocol")

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
        """Play back a recorded trajectory file."""
        if cart != -1:
            raise NotSupportedError("The cart option is available only in V3")
        return self.native.dashboard.start_path(trace_name, is_const=is_const, multi=multi)

    def sync(self, timeout: float = 30.0) -> None:
        """Block until the robot finishes moving and returns to ENABLE state.

        V4 has no native ``sync()`` — polls ``robot_mode()`` every 50 ms.
        Waits for the robot to enter RUNNING or SINGLE_MOVE mode, then waits
        for it to drop back to ENABLE (idle).

        Args:
            timeout: Maximum seconds to wait before giving up.

        Raises:
            TimeoutError: If the motion does not complete within *timeout* seconds.
            RuntimeError: If the robot enters ERROR state.
        """
        mode_enable = 5
        mode_running = 7
        mode_single_move = 8
        mode_error = 9

        deadline = time.monotonic() + timeout
        saw_moving = False
        while time.monotonic() < deadline:
            mode = self.native.robot_mode()
            if mode in (mode_running, mode_single_move):
                saw_moving = True
            elif saw_moving and mode == mode_enable:
                return
            elif mode == mode_error:
                raise RuntimeError("Robot entered ERROR state during sync().")
            time.sleep(0.05)
        raise TimeoutError(f"sync() timed out after {timeout}s — motion did not complete.")
