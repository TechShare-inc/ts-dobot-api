"""V3 robot implementation — wraps ``dobot_api_v3.DobotRobot`` directly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .models import ApiVersion
from .robot import DobotRobot
from .types import Pose

if TYPE_CHECKING:
    import numpy as np
    from dobot_api_v3 import DobotApiFeedback as V3Feedback
    from dobot_api_v3 import DobotRobot as V3Robot
    from dobot_api_v3 import FeedbackData as V3FeedbackData

# -- Helpers ---------------------------------------------------------------


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


# -- DobotRobotV3 ---------------------------------------------------------


class DobotRobotV3(DobotRobot):
    """Dobot robot using the V3 protocol (Nova series).

    Wraps ``dobot_api_v3.DobotRobot`` directly — no adapter layer.
    """

    _api_version = ApiVersion.V3

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        super().__init__(ip, model, language=language)

        from dobot_api_v3 import DobotRobot as V3Robot

        self._native: V3Robot = V3Robot(ip, language=language)

    # ==================================================================
    # Lifecycle
    # ==================================================================

    def disconnect(self) -> None:
        """Close all TCP connections."""
        if self._native is not None:
            self._native.close()
            self._native = None  # type: ignore[assignment]

    def reconnect(self) -> None:
        """Re-establish all TCP connections."""
        self._native.reconnect()

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
        """Run the standard V3 startup sequence."""
        self._native.startup(
            speed=speed,
            load=load,
            center_x=center_x,
            center_y=center_y,
            center_z=center_z,
            power_on_wait=power_on_wait,
        )

    def shutdown(self) -> None:
        """Gracefully disable the robot arm."""
        self._native.shutdown()

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
        """Enable the robot."""
        self._native.enable_robot(
            load=load, center_x=center_x, center_y=center_y, center_z=center_z
        )

    def disable_robot(self) -> None:
        """Disable the robot."""
        self._native.disable_robot()

    def clear_error(self) -> None:
        """Clear controller error/alarm information."""
        self._native.clear_error()

    def reset_robot(self) -> None:
        """Reset the robot controller."""
        self._native.reset_robot()

    def power_on(self) -> None:
        """Power on the robot."""
        self._native.power_on()

    def emergency_stop(self) -> None:
        """Trigger an emergency stop."""
        self._native.emergency_stop()

    def speed_factor(self, speed: int) -> None:
        """Set the global speed factor (1–100)."""
        self._native.speed_factor(speed)

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
        """Joint-space move to a Cartesian target."""
        dyn = _build_dyn_params(
            speed_j=speed, accel_j=accel, cp=cp, user=user, tool=tool
        )
        return self._native.mov_j(x, y, z, rx, ry, rz, *dyn)

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
        dyn = _build_dyn_params(
            speed_l=speed, accel_l=accel, cp=cp, user=user, tool=tool
        )
        return self._native.mov_l(x, y, z, rx, ry, rz, *dyn)

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
        return self._native.joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn)

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
        return self._native.servo_j(
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
        """Servo (streaming) move in Cartesian space."""
        return self._native.servo_p(x, y, z, rx, ry, rz)

    def move_jog(self, axis_id: str = "") -> int:
        """Start or stop jog motion."""
        return self._native.move_jog(axis_id)

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
        dyn = _build_dyn_params(
            speed_l=speed, accel_l=accel, cp=cp, user=user, tool=tool
        )
        return self._native.arc(
            x1, y1, z1, rx1, ry1, rz1, x2, y2, z2, rx2, ry2, rz2, *dyn
        )

    def sync(self) -> None:
        """Block until all queued motion commands have completed."""
        self._native.sync()

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
        """Relative joint move in tool coordinate system."""
        tool_val = tool if tool is not None else 0
        return self._native.move.rel_mov_j_tool(
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
        """Relative linear move in tool coordinate system."""
        tool_val = tool if tool is not None else 0
        return self._native.move.rel_mov_l_tool(
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
        """Relative joint move in user coordinate system."""
        user_val = user if user is not None else 0
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel)
        return self._native.move.rel_mov_j_user(
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
        """Relative linear move in user coordinate system."""
        user_val = user if user is not None else 0
        dyn = _build_dyn_params(speed_l=speed, accel_l=accel)
        return self._native.move.rel_mov_l_user(
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
        """Relative move with joint offsets."""
        dyn = _build_dyn_params(speed_j=speed, accel_j=accel)
        return self._native.move.rel_joint_mov_j(j1, j2, j3, j4, j5, j6, *dyn)

    # ==================================================================
    # Config
    # ==================================================================

    def vel_j(self, speed: int) -> None:
        """Set maximum joint velocity (%)."""
        self._native.dashboard.vel_j(speed)

    def vel_l(self, speed: int) -> None:
        """Set maximum Cartesian velocity (mm/s)."""
        self._native.dashboard.vel_l(speed)

    def acc_j(self, speed: int) -> None:
        """Set maximum joint acceleration (%)."""
        self._native.dashboard.acc_j(speed)

    def acc_l(self, speed: int) -> None:
        """Set maximum Cartesian acceleration (mm/s²)."""
        self._native.dashboard.acc_l(speed)

    def cp(self, ratio: int) -> None:
        """Set continuous-path blending ratio."""
        self._native.dashboard.cp(ratio)

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Set the tool payload."""
        self._native.dashboard.set_payload(
            weight, f"CenterX={center_x}", f"CenterY={center_y}", f"CenterZ={center_z}"
        )

    def set_collision_level(self, level: int) -> None:
        """Set collision detection sensitivity level."""
        self._native.dashboard.set_collision_level(level)

    def set_user(self, index: int) -> None:
        """Select the active user coordinate system."""
        self._native.dashboard.set_user(index)

    def set_tool(self, index: int) -> None:
        """Select the active tool coordinate system."""
        self._native.dashboard.set_tool(index)

    # ==================================================================
    # Query
    # ==================================================================

    def robot_mode(self) -> int:
        """Return the current robot mode."""
        return self._native.robot_mode()

    def get_pose(self) -> Pose:
        """Return the current Cartesian pose."""
        return _pose_from_tuple(self._native.get_pose())

    def get_angle(self) -> Pose:
        """Return the current joint angles (as a Pose with j1-j6 in x-rz)."""
        return _pose_from_tuple(self._native.get_angle())

    def get_error_id(self) -> tuple[int, ...]:
        """Return a tuple of currently-active error IDs."""
        return self._native.get_error_id()

    def start_drag(self) -> None:
        """Enter drag/teach mode."""
        self._native.start_drag()

    def stop_drag(self) -> None:
        """Exit drag/teach mode."""
        self._native.stop_drag()

    # ==================================================================
    # I/O
    # ==================================================================

    def do_output(self, index: int, status: int) -> None:
        """Set a digital output."""
        self._native.dashboard.do_output(index, status)

    def tool_do(self, index: int, status: int) -> None:
        """Set a tool digital output."""
        self._native.dashboard.tool_do(index, status)

    def ao(self, index: int, value: float) -> None:
        """Set an analogue output."""
        self._native.dashboard.ao(index, value)

    def di(self, index: int) -> int:
        """Read a digital input."""
        return self._native.dashboard.di(index)

    def tool_di(self, index: int) -> int:
        """Read a tool digital input."""
        return self._native.dashboard.tool_di(index)

    # ==================================================================
    # Feedback
    # ==================================================================

    def feedback_data(self, port: int = 30004) -> V3FeedbackData | None:
        """Return the latest real-time feedback packet."""
        fb = self._get_feedback(port)
        return fb.feedback_data() if fb else None

    def raw_feedback_data(self, port: int = 30004) -> np.ndarray | None:
        """Return the raw numpy feedback array."""
        fb = self._get_feedback(port)
        return fb.raw_feedback_data() if fb else None

    def _get_feedback(self, port: int) -> V3Feedback | None:
        if port == 30004:
            return self._native.feedback
        elif port == 30005:
            return self._native.feedback_30005
        elif port == 30006:
            return self._native.feedback_30006
        return None

    # ==================================================================
    # Error monitoring
    # ==================================================================

    def check_errors(self, language: str = "en") -> bool:
        """Return ``True`` if the controller has active alarms."""
        return self._native.check_errors(language=language)

    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors. Returns ``True`` on success."""
        return self._native.clear_and_recover(language=language)

    # ==================================================================
    # Raw
    # ==================================================================

    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response."""
        return self._native.dashboard.send_recv_msg(command)
