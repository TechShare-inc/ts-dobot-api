"""V3 adapter — wraps ``dobot_api_v3.DobotRobot`` behind :class:`DobotProtocol`."""

from __future__ import annotations

from typing import Any

from ..protocol import DobotProtocol
from ..types import Pose


def _pose_from_tuple(t: tuple[float, ...]) -> Pose:
    """Convert a V3 Pose (plain tuple) to our unified Pose dataclass."""
    return Pose(x=t[0], y=t[1], z=t[2], rx=t[3], ry=t[4], rz=t[5])


def _build_dyn_params(
    *,
    speed_j: int | None = None,
    speed_l: int | None = None,
    accel_j: int | None = None,
    accel_l: int | None = None,
    speed: int | None = None,
    accel: int | None = None,
    cp: int | None = None,
    user: int | None = None,
    tool: int | None = None,
) -> list[str]:
    """Build a list of V3-style DynParam strings from keyword arguments."""
    params: list[str] = []
    if speed_j is not None:
        params.append(f"SpeedJ={speed_j}")
    if speed_l is not None:
        params.append(f"SpeedL={speed_l}")
    if accel_j is not None:
        params.append(f"AccJ={accel_j}")
    if accel_l is not None:
        params.append(f"AccL={accel_l}")
    if speed is not None:
        params.append(f"SpeedJ={speed}")
    if accel is not None:
        params.append(f"AccJ={accel}")
    if cp is not None:
        params.append(f"CP={cp}")
    if user is not None:
        params.append(f"User={user}")
    if tool is not None:
        params.append(f"Tool={tool}")
    return params


class V3Adapter(DobotProtocol):
    """Adapter that wraps the ``dobot_api_v3`` SDK.

    Supports: Nova series robots.
    """

    def __init__(self, ip: str, *, language: str = "en") -> None:
        self._ip = ip
        self._language = language
        self._robot: Any = None  # Lazy — created in connect()

    @property
    def native(self) -> Any:
        """Access the underlying ``dobot_api_v3.DobotRobot`` instance."""
        if self._robot is None:
            raise RuntimeError("Not connected. Call connect() first.")
        return self._robot

    # ==================================================================
    # Lifecycle
    # ==================================================================

    def connect(self) -> None:
        from dobot_api_v3 import DobotRobot as V3Robot

        self._robot = V3Robot(self._ip, language=self._language)

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
        self.native.startup(
            speed=speed,
            load=load,
            center_x=center_x,
            center_y=center_y,
            center_z=center_z,
            power_on_wait=power_on_wait,
        )

    def shutdown(self) -> None:
        self.native.shutdown()

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
        self.native.emergency_stop()

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
        dyn = _build_dyn_params(
            speed_j=speed, accel_j=accel, cp=cp, user=user, tool=tool
        )
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
        dyn = _build_dyn_params(
            speed_l=speed, accel_l=accel, cp=cp, user=user, tool=tool
        )
        return self.native.mov_l(x, y, z, rx, ry, rz, *dyn)

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
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel, cp=cp)
        return self.native.joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn)

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
            j1, j2, j3, j4, j5, j6, t=t, lookahead_time=lookahead_time, gain=gain
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
        return self.native.move_jog(axis_id)

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
        dyn = _build_dyn_params(
            speed_l=speed, accel_l=accel, cp=cp, user=user, tool=tool
        )
        return self.native.arc(
            x1, y1, z1, rx1, ry1, rz1, x2, y2, z2, rx2, ry2, rz2, *dyn
        )

    def sync(self) -> None:
        self.native.sync()

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
        # V3 requires tool as positional arg
        tool_val = tool if tool is not None else 0
        return self.native.move.rel_mov_j_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            tool_val,
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
        tool_val = tool if tool is not None else 0
        return self.native.move.rel_mov_l_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            tool_val,
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
        user_val = user if user is not None else 0
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel)
        return self.native.move.rel_mov_j_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user_val,
            *dyn,
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
        user_val = user if user is not None else 0
        dyn = _build_dyn_params(speed_l=speed, accel_l=accel)
        return self.native.move.rel_mov_l_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user_val,
            *dyn,
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
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel)
        return self.native.move.rel_joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn)

    # ==================================================================
    # Config
    # ==================================================================

    def vel_j(self, speed: int) -> None:
        self.native.dashboard.vel_j(speed)

    def vel_l(self, speed: int) -> None:
        self.native.dashboard.vel_l(speed)

    def acc_j(self, speed: int) -> None:
        self.native.dashboard.acc_j(speed)

    def acc_l(self, speed: int) -> None:
        self.native.dashboard.acc_l(speed)

    def cp(self, ratio: int) -> None:
        self.native.dashboard.cp(ratio)

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        self.native.dashboard.set_payload(
            weight, f"CenterX={center_x}", f"CenterY={center_y}", f"CenterZ={center_z}"
        )

    def set_collision_level(self, level: int) -> None:
        self.native.dashboard.set_collision_level(level)

    def set_user(self, index: int) -> None:
        self.native.dashboard.set_user(index)

    def set_tool(self, index: int) -> None:
        self.native.dashboard.set_tool(index)

    # ==================================================================
    # Query
    # ==================================================================

    def robot_mode(self) -> int:
        return self.native.robot_mode()

    def get_pose(self) -> Pose:
        return _pose_from_tuple(self.native.get_pose())

    def get_angle(self) -> Pose:
        return _pose_from_tuple(self.native.get_angle())

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
        self.native.dashboard.do_output(index, status)

    def tool_do(self, index: int, status: int) -> None:
        self.native.dashboard.tool_do(index, status)

    def ao(self, index: int, value: float) -> None:
        self.native.dashboard.ao(index, value)

    def di(self, index: int) -> int:
        return self.native.dashboard.di(index)

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
        return self.native.clear_and_recover(language=language)

    # ==================================================================
    # Raw
    # ==================================================================

    def send_raw(self, command: str) -> str:
        return self.native.dashboard.send_recv_msg(command)
