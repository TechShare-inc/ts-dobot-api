"""V4 adapter — wraps ``dobot_api_v4.DobotRobot`` behind :class:`DobotProtocol`."""

from __future__ import annotations

import time
from typing import Any

from loguru import logger

from ..protocol import DobotProtocol
from ..types import Pose


def _pose_from_v4(p: Any) -> Pose:
    """Convert a V4 ``Pose`` dataclass to our unified Pose."""
    return Pose(x=p.x, y=p.y, z=p.z, rx=p.rx, ry=p.ry, rz=p.rz)


def _opt(value: Any, default: int = -1) -> int:
    """Convert ``None`` → V4's sentinel default (``-1``)."""
    return default if value is None else value


class V4Adapter(DobotProtocol):
    """Adapter that wraps the ``dobot_api_v4`` SDK.

    Supports: CR series, Nova 2s, Nova NG series robots.
    """

    def __init__(self, ip: str, *, language: str = "en") -> None:
        self._ip = ip
        self._language = language
        self._robot: Any = None  # Lazy — created in connect()

    @property
    def native(self) -> Any:
        """Access the underlying ``dobot_api_v4.DobotRobot`` instance."""
        if self._robot is None:
            raise RuntimeError("Not connected. Call connect() first.")
        return self._robot

    # ==================================================================
    # Lifecycle
    # ==================================================================

    def connect(self) -> None:
        from dobot_api_v4 import DobotRobot as V4Robot

        self._robot = V4Robot(self._ip, language=self._language)

    def disconnect(self) -> None:
        if self._robot is not None:
            self._robot.close()
            self._robot = None

    def reconnect(self) -> None:
        self.native.reconnect()

    def startup(
        self,
        speed: int = 40,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
        *,
        power_on_wait: float = 15.0,
    ) -> None:
        """V4 startup — composed manually since there's no built-in startup()."""
        logger.info("V4 startup sequence starting")
        has_errors = self.native.check_errors(language=self._language)
        if has_errors:
            logger.info("Errors detected — clearing and powering on")
            self.native.clear_error()
            self.native.power_on()
            logger.info(f"Waiting {power_on_wait}s for controller to power on")
            time.sleep(power_on_wait)
        else:
            logger.info("No errors detected — skipping clear_error and power_on")
        self.native.disable_robot()
        self.native.enable_robot(
            load=load,
            center_x=center_x,
            center_y=center_y,
            center_z=center_z,
        )
        self.native.speed_factor(speed)
        logger.info("V4 startup sequence complete")

    def shutdown(self) -> None:
        logger.info("V4 shutdown: disabling robot")
        self.native.disable_robot()

    # ==================================================================
    # System
    # ==================================================================

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        self.native.enable_robot(
            load=load, center_x=center_x, center_y=center_y, center_z=center_z
        )

    def disable_robot(self) -> None:
        self.native.disable_robot()

    def clear_error(self) -> None:
        self.native.clear_error()

    def reset_robot(self) -> None:
        self.native.reset_robot()

    def power_on(self) -> None:
        self.native.power_on()

    def emergency_stop(self) -> None:
        # V4 requires a mode param; 0 = standard stop
        self.native.emergency_stop(mode=0)

    def speed_factor(self, speed: int) -> None:
        self.native.speed_factor(speed)

    # ==================================================================
    # Motion
    # ==================================================================

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
            speed=_opt(speed),
            cp=_opt(cp),
        )

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
        # V4 uses coordinate_mode=1 for joint targets
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
        return self.native.servo_j(
            j1, j2, j3, j4, j5, j6, t=t, ahead_time=lookahead_time, gain=gain
        )

    def servo_p(
        self,
        x: float,
        y: float,
        z: float,
        rx: float,
        ry: float,
        rz: float,
    ) -> int:
        return self.native.servo_p(x, y, z, rx, ry, rz)

    def move_jog(self, axis_id: str = "") -> int:
        self.native.move_jog(axis_id=axis_id)
        return 0  # V4 move_jog returns None

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

    def sync(self) -> None:
        """V4 has no native sync(). Poll ``get_current_command_id()`` instead."""
        # Simple polling approach — wait until the robot is idle.
        # get_current_command_id() returns 0 when no command is active.
        logger.debug("V4 sync: polling get_current_command_id()")
        while True:
            cmd_id = self.native.get_current_command_id()
            if cmd_id == 0:
                break
            time.sleep(0.1)

    # ==================================================================
    # Relative motion
    # ==================================================================

    def rel_mov_j_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        tool: int | None = None,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        return self.native.dashboard.rel_mov_j_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_l_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        tool: int | None = None,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        return self.native.dashboard.rel_mov_l_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_j_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        return self.native.dashboard.rel_mov_j_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_l_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        return self.native.dashboard.rel_mov_l_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_joint_mov_j(
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
    ) -> int:
        return self.native.dashboard.rel_joint_mov_j(
            j1,
            j2,
            j3,
            j4,
            j5,
            j6,
            a=_opt(accel),
            v=_opt(speed),
        )

    # ==================================================================
    # Config
    # ==================================================================

    def vel_j(self, speed: int) -> None:
        self.native.vel_j(speed)

    def vel_l(self, speed: int) -> None:
        self.native.vel_l(speed)

    def acc_j(self, speed: int) -> None:
        self.native.acc_j(speed)

    def acc_l(self, speed: int) -> None:
        self.native.acc_l(speed)

    def cp(self, ratio: int) -> None:
        self.native.cp(ratio)

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        self.native.dashboard.set_payload(
            load=weight, x=center_x, y=center_y, z=center_z
        )

    def set_collision_level(self, level: int) -> None:
        self.native.dashboard.set_collision_level(level)

    def set_user(self, index: int) -> None:
        self.native.dashboard.user(index)

    def set_tool(self, index: int) -> None:
        self.native.dashboard.tool(index)

    # ==================================================================
    # Query
    # ==================================================================

    def robot_mode(self) -> int:
        return self.native.robot_mode()

    def get_pose(self) -> Pose:
        return _pose_from_v4(self.native.get_pose())

    def get_angle(self) -> Pose:
        return _pose_from_v4(self.native.get_angle())

    def get_error_id(self) -> tuple[int, ...]:
        return self.native.get_error_id()

    def start_drag(self) -> None:
        self.native.start_drag()

    def stop_drag(self) -> None:
        self.native.stop_drag()

    # ==================================================================
    # I/O
    # ==================================================================

    def do_output(self, index: int, status: int) -> None:
        self.native.do_output(index, status)

    def tool_do(self, index: int, status: int) -> None:
        self.native.dashboard.tool_do(index, status)

    def ao(self, index: int, value: float) -> None:
        self.native.ao(index, value)

    def di(self, index: int) -> int:
        return self.native.di(index)

    def tool_di(self, index: int) -> int:
        return self.native.dashboard.tool_di(index)

    # ==================================================================
    # Feedback
    # ==================================================================

    def feedback_data(self, port: int = 30004) -> Any | None:
        fb = self._get_feedback(port)
        return fb.feedback_data() if fb else None

    def raw_feedback_data(self, port: int = 30004) -> Any | None:
        fb = self._get_feedback(port)
        return fb.raw_feedback_data() if fb else None

    def _get_feedback(self, port: int) -> Any | None:
        if port == 30004:
            return self.native.feedback
        elif port == 30005:
            return self.native.feedback_30005
        elif port == 30006:
            return self.native.feedback_30006
        return None

    # ==================================================================
    # Error monitoring
    # ==================================================================

    def check_errors(self, language: str = "en") -> bool:
        return self.native.check_errors(language=language)

    def clear_and_recover(self, language: str = "en") -> bool:
        return self.native.clear_robot_error(language=language)

    # ==================================================================
    # Raw
    # ==================================================================

    def send_raw(self, command: str) -> str:
        return self.native.dashboard.send_recv_msg(command)
