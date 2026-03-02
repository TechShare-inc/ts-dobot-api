"""Unified robot facade — the main user-facing entry point.

Example::

    from ts_dobot_api import DobotRobot

    with DobotRobot("192.168.1.6", model="CR5") as robot:
        robot.startup(speed=40)
        pose = robot.get_pose()
        robot.mov_j(200, 0, 200, 0, 0, 0)
        robot.sync()
        robot.shutdown()

    # V4-only extensions
    with DobotRobot("192.168.1.6", model="CR5") as robot:
        robot.startup()
        robot.force.enable_ft_sensor(1)
        force = robot.force.get_force()
        robot.force.fc_off()
        robot.shutdown()
"""

from __future__ import annotations

from typing import Any

from loguru import logger

from .adapters import create_adapter
from .extensions.check import MotionCheck
from .extensions.conveyor import ConveyorTracking
from .extensions.force import ForceControl
from .extensions.weld import Welding
from .models import ApiVersion, RobotFamily
from .protocol import DobotProtocol
from .types import Pose


class DobotRobot:
    """Unified interface for all Dobot robots.

    Automatically selects the correct underlying API (V3 or V4) based on the
    *model* string and presents a single, version-agnostic interface.

    Args:
        ip: Robot controller IP address.
        model: Robot model string (e.g. ``"CR5"``, ``"Nova2s"``, ``"Nova"``).
            Used to determine the correct API version.
        language: Default language for alarm messages.
    """

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        self._ip = ip
        self._model = model
        self._language = language

        # Resolve model → family → API version
        self._family: RobotFamily = RobotFamily.from_model(model)
        self._api_version: ApiVersion = self._family.api_version

        # Create the version-specific adapter
        self._adapter: DobotProtocol = create_adapter(
            self._api_version, ip, language=language
        )

        # Connect immediately
        self._adapter.connect()

        # Extension namespaces — wired to real dashboard on V4, raise on V3
        dashboard = self._get_v4_dashboard()
        self.force: ForceControl = ForceControl(dashboard, self._api_version)
        self.conveyor: ConveyorTracking = ConveyorTracking(dashboard, self._api_version)
        self.weld: Welding = Welding(dashboard, self._api_version)
        self.check: MotionCheck = MotionCheck(dashboard, self._api_version)

        logger.info(
            f"DobotRobot initialized: model={model!r}, family={self._family.display_name}, "
            f"api={self._api_version.value}, ip={ip}"
        )

    def _get_v4_dashboard(self) -> Any | None:
        """Return the underlying V4 dashboard, or None if not V4."""
        if self._api_version is ApiVersion.V4:
            from .adapters.v4_adapter import V4Adapter

            adapter = self._adapter
            if isinstance(adapter, V4Adapter) and adapter._robot is not None:
                return adapter._robot.dashboard
        return None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def ip(self) -> str:
        """Robot controller IP address."""
        return self._ip

    @property
    def model(self) -> str:
        """Robot model string as provided by the user."""
        return self._model

    @property
    def family(self) -> RobotFamily:
        """Resolved robot family."""
        return self._family

    @property
    def api_version(self) -> ApiVersion:
        """Resolved API version."""
        return self._api_version

    @property
    def adapter(self) -> DobotProtocol:
        """The underlying version-specific adapter (for advanced use)."""
        return self._adapter

    @property
    def native(self) -> Any:
        """Access the underlying SDK's ``DobotRobot`` object directly.

        Useful when you need a method that isn't exposed by the wrapper.
        """
        return self._adapter.native  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> DobotRobot:
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.disconnect()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        """Open TCP connections to the robot (called automatically on init)."""
        self._adapter.connect()

    def disconnect(self) -> None:
        """Close all TCP connections."""
        self._adapter.disconnect()

    def reconnect(self) -> None:
        """Re-establish all TCP connections."""
        self._adapter.reconnect()

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
        """Run the standard startup sequence.

        Clears errors (if any), powers on, enables the robot, and sets
        the global speed factor.  The exact sequence depends on the API
        version but the end result is the same: the robot is enabled and
        ready to accept motion commands.

        Args:
            speed: Global speed factor (1–100).
            load: Payload weight (kg).
            center_x: Payload centre-of-gravity X offset (mm).
            center_y: Payload centre-of-gravity Y offset (mm).
            center_z: Payload centre-of-gravity Z offset (mm).
            power_on_wait: Seconds to wait after power-on (only when errors
                were detected and ``power_on`` is called).
        """
        self._adapter.startup(
            speed=speed,
            load=load,
            center_x=center_x,
            center_y=center_y,
            center_z=center_z,
            power_on_wait=power_on_wait,
        )

    def shutdown(self) -> None:
        """Gracefully disable the robot arm.

        Does **not** close TCP connections — call :meth:`disconnect` or
        use the context manager for that.
        """
        self._adapter.shutdown()

    # ------------------------------------------------------------------
    # System
    # ------------------------------------------------------------------

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Enable the robot."""
        self._adapter.enable_robot(
            load=load, center_x=center_x, center_y=center_y, center_z=center_z
        )

    def disable_robot(self) -> None:
        """Disable the robot."""
        self._adapter.disable_robot()

    def clear_error(self) -> None:
        """Clear controller error/alarm information."""
        self._adapter.clear_error()

    def reset_robot(self) -> None:
        """Reset the robot controller."""
        self._adapter.reset_robot()

    def power_on(self) -> None:
        """Power on the robot."""
        self._adapter.power_on()

    def emergency_stop(self) -> None:
        """Trigger an emergency stop."""
        self._adapter.emergency_stop()

    def speed_factor(self, speed: int) -> None:
        """Set the global speed factor (1–100)."""
        self._adapter.speed_factor(speed)

    # ------------------------------------------------------------------
    # Motion
    # ------------------------------------------------------------------

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
        """Joint-space move to a Cartesian target.

        Args:
            x, y, z: Target position (mm).
            rx, ry, rz: Target orientation (degrees).
            speed: Override velocity (%).
            accel: Override acceleration (%).
            cp: Continuous-path blending radius.
            user: User coordinate system index.
            tool: Tool coordinate system index.

        Returns:
            Command queue ID.
        """
        return self._adapter.mov_j(
            x, y, z, rx, ry, rz, speed=speed, accel=accel, cp=cp, user=user, tool=tool
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
        """Linear move.

        Args:
            x, y, z: Target position (mm).
            rx, ry, rz: Target orientation (degrees).
            speed: Override velocity (%).
            accel: Override acceleration (%).
            cp: Continuous-path blending radius.
            user: User coordinate system index.
            tool: Tool coordinate system index.

        Returns:
            Command queue ID.
        """
        return self._adapter.mov_l(
            x, y, z, rx, ry, rz, speed=speed, accel=accel, cp=cp, user=user, tool=tool
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
        """Joint-space move with joint-angle targets.

        Returns:
            Command queue ID.
        """
        return self._adapter.joint_mov_j(
            j1, j2, j3, j4, j5, j6, speed=speed, accel=accel, cp=cp
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
        """Servo (streaming) move in joint space.

        Returns:
            Command queue ID.
        """
        return self._adapter.servo_j(
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
        """Servo (streaming) move in Cartesian space.

        Returns:
            Command queue ID.
        """
        return self._adapter.servo_p(x, y, z, rx, ry, rz)

    def move_jog(self, axis_id: str = "") -> int:
        """Start or stop jog motion.

        Args:
            axis_id: Axis identifier (e.g. ``"J1+"``, ``"X-"``).
                Empty string stops all jog motion.

        Returns:
            Command queue ID.
        """
        return self._adapter.move_jog(axis_id)

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
        """Circular arc move through two via-points.

        Returns:
            Command queue ID.
        """
        return self._adapter.arc(
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
            speed=speed,
            accel=accel,
            cp=cp,
            user=user,
            tool=tool,
        )

    def sync(self) -> None:
        """Block until all queued motion commands have completed.

        V3: uses the native ``sync()`` command on port 30003.
        V4: polls ``get_current_command_id()`` until the queue is empty.
        """
        self._adapter.sync()

    # ------------------------------------------------------------------
    # Relative motion
    # ------------------------------------------------------------------

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
        """Relative joint move in tool coordinate system.

        Returns:
            Command queue ID.
        """
        return self._adapter.rel_mov_j_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            tool=tool,
            user=user,
            speed=speed,
            accel=accel,
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
        """Relative linear move in tool coordinate system.

        Returns:
            Command queue ID.
        """
        return self._adapter.rel_mov_l_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            tool=tool,
            user=user,
            speed=speed,
            accel=accel,
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
        """Relative joint move in user coordinate system.

        Returns:
            Command queue ID.
        """
        return self._adapter.rel_mov_j_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=user,
            speed=speed,
            accel=accel,
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
        """Relative linear move in user coordinate system.

        Returns:
            Command queue ID.
        """
        return self._adapter.rel_mov_l_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=user,
            speed=speed,
            accel=accel,
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
        """Relative move with joint offsets.

        Returns:
            Command queue ID.
        """
        return self._adapter.rel_joint_mov_j(
            j1, j2, j3, j4, j5, j6, speed=speed, accel=accel
        )

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------

    def vel_j(self, speed: int) -> None:
        """Set maximum joint velocity (%)."""
        self._adapter.vel_j(speed)

    def vel_l(self, speed: int) -> None:
        """Set maximum Cartesian velocity (mm/s)."""
        self._adapter.vel_l(speed)

    def acc_j(self, speed: int) -> None:
        """Set maximum joint acceleration (%)."""
        self._adapter.acc_j(speed)

    def acc_l(self, speed: int) -> None:
        """Set maximum Cartesian acceleration (mm/s²)."""
        self._adapter.acc_l(speed)

    def cp(self, ratio: int) -> None:
        """Set continuous-path blending ratio."""
        self._adapter.cp(ratio)

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Set the tool payload."""
        self._adapter.set_payload(weight, center_x, center_y, center_z)

    def set_collision_level(self, level: int) -> None:
        """Set collision detection sensitivity level."""
        self._adapter.set_collision_level(level)

    def set_user(self, index: int) -> None:
        """Select the active user coordinate system."""
        self._adapter.set_user(index)

    def set_tool(self, index: int) -> None:
        """Select the active tool coordinate system."""
        self._adapter.set_tool(index)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def robot_mode(self) -> int:
        """Return the current robot mode."""
        return self._adapter.robot_mode()

    def get_pose(self) -> Pose:
        """Return the current Cartesian pose."""
        return self._adapter.get_pose()

    def get_angle(self) -> Pose:
        """Return the current joint angles (as a Pose with j1-j6 in x-rz)."""
        return self._adapter.get_angle()

    def get_error_id(self) -> tuple[int, ...]:
        """Return a tuple of currently-active error IDs."""
        return self._adapter.get_error_id()

    def start_drag(self) -> None:
        """Enter drag/teach mode."""
        self._adapter.start_drag()

    def stop_drag(self) -> None:
        """Exit drag/teach mode."""
        self._adapter.stop_drag()

    # ------------------------------------------------------------------
    # I/O
    # ------------------------------------------------------------------

    def do_output(self, index: int, status: int) -> None:
        """Set a digital output.

        Args:
            index: DO port index.
            status: 0 = OFF, 1 = ON.
        """
        self._adapter.do_output(index, status)

    def tool_do(self, index: int, status: int) -> None:
        """Set a tool digital output."""
        self._adapter.tool_do(index, status)

    def ao(self, index: int, value: float) -> None:
        """Set an analogue output."""
        self._adapter.ao(index, value)

    def di(self, index: int) -> int:
        """Read a digital input."""
        return self._adapter.di(index)

    def tool_di(self, index: int) -> int:
        """Read a tool digital input."""
        return self._adapter.tool_di(index)

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------

    def feedback_data(self, port: int = 30004) -> Any | None:
        """Return the latest real-time feedback packet.

        Args:
            port: Feedback port (30004, 30005, or 30006).

        Returns:
            A ``FeedbackData`` dataclass, or ``None`` if not available.
        """
        return self._adapter.feedback_data(port)

    def raw_feedback_data(self, port: int = 30004) -> Any | None:
        """Return the raw numpy feedback array.

        Args:
            port: Feedback port (30004, 30005, or 30006).
        """
        return self._adapter.raw_feedback_data(port)

    # ------------------------------------------------------------------
    # Error monitoring
    # ------------------------------------------------------------------

    def check_errors(self, language: str = "en") -> bool:
        """Return ``True`` if the controller has active alarms."""
        return self._adapter.check_errors(language)

    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors. Returns ``True`` on success."""
        return self._adapter.clear_and_recover(language)

    # ------------------------------------------------------------------
    # Raw
    # ------------------------------------------------------------------

    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response.

        Useful for accessing commands not yet covered by the wrapper.
        """
        return self._adapter.send_raw(command)

    # ------------------------------------------------------------------
    # repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"DobotRobot(ip={self._ip!r}, model={self._model!r}, "
            f"family={self._family.display_name!r}, api={self._api_version.value!r})"
        )
