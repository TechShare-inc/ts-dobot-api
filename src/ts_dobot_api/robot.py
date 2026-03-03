"""Unified robot facade - the main user-facing entry point.

Example::

    from ts_dobot_api import DobotRobot

    with DobotRobot.connect("192.168.1.6", model="CR5") as robot:
        robot.startup(speed=40)
        pose = robot.get_pose()
        robot.mov_j(200, 0, 200, 0, 0, 0)
        robot.sync()
        robot.shutdown()

    # V4-only methods (raise NotImplementedError on V3):
    with DobotRobot.connect("192.168.1.6", model="CR5") as robot:
        robot.startup()
        robot.enable_ft_sensor(1)
        force = robot.get_force()
        robot.fc_off()
        robot.shutdown()

    # Advanced V4-only features — access via the ``.native`` escape hatch:
    with DobotRobot.connect("192.168.1.6", model="CR5") as robot:
        robot.startup()
        # Force compliance (advanced)
        robot.native.dashboard.fc_force_mode(...)
        robot.native.dashboard.fc_set_stiffness(...)
        # Modbus
        robot.native.dashboard.modbus_create(...)
        robot.native.dashboard.get_hold_regs(...)
        # Conveyor tracking
        robot.native.dashboard.cnv_init(1)
        robot.native.dashboard.cnv_mov_l(...)
        # Welding / weave
        robot.native.dashboard.weave_start()
        robot.native.dashboard.weave_params(...)
        # Motion pre-check
        robot.native.dashboard.check_mov_j(...)
        robot.shutdown()
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from loguru import logger

from .models import ApiVersion, RobotFamily

if TYPE_CHECKING:
    import numpy as np

    from .types import Pose

_T_Native = TypeVar("_T_Native")


class DobotRobot(Generic[_T_Native]):
    """Base class for all Dobot robots.

    Use the :meth:`connect` class-method to create an instance — it
    automatically selects the correct subclass (``DobotRobotV3`` or
    ``DobotRobotV4``) based on the *model* string.

    Args:
        ip: Robot controller IP address.
        model: Robot model string (e.g. ``"CR5"``, ``"Nova2s"``, ``"Nova"``).
        language: Default language for alarm messages.
    """

    _api_version: ApiVersion  # set by subclass
    _native: _T_Native

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        self._ip = ip
        self._model = model
        self._language = language
        self._family: RobotFamily = RobotFamily.from_model(model)

    @classmethod
    def connect(
        cls, ip: str, model: str, *, language: str = "en"
    ) -> DobotRobot[object]:
        """Factory: create, connect, and return the correct subclass.

        Args:
            ip: Robot controller IP address.
            model: Robot model string (e.g. ``"CR5"``, ``"Nova"``).
            language: Default language for alarm messages.

        Returns:
            A connected ``DobotRobotV3`` or ``DobotRobotV4`` instance.
        """
        family = RobotFamily.from_model(model)
        version = family.api_version

        robot: DobotRobot[object]
        if version is ApiVersion.V3:
            from .v3 import DobotRobotV3

            robot = DobotRobotV3(ip, model, language=language)  # type: ignore[assignment]
        elif version is ApiVersion.V4:
            from .v4 import DobotRobotV4

            robot = DobotRobotV4(ip, model, language=language)  # type: ignore[assignment]
        else:
            raise ValueError(f"Unsupported API version: {version!r}")

        logger.info(
            f"DobotRobot connected: model={model!r}, family={family.display_name}, api={version.value}, ip={ip}"
        )
        return robot

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
    def native(self) -> _T_Native:
        """Access the underlying SDK's ``DobotRobot`` object directly.

        Useful when you need a method that isn't exposed by the wrapper.
        """
        return self._native

    # ------------------------------------------------------------------
    # Lifecycle (override in subclasses)
    # ------------------------------------------------------------------

    def disconnect(self) -> None:
        """Close all TCP connections."""
        raise NotImplementedError

    def reconnect(self) -> None:
        """Re-establish all TCP connections."""
        raise NotImplementedError

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
        """Run the standard startup sequence."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Gracefully disable the robot arm."""
        raise NotImplementedError

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
        raise NotImplementedError

    def disable_robot(self) -> None:
        """Disable the robot."""
        raise NotImplementedError

    def clear_error(self) -> None:
        """Clear controller error/alarm information."""
        raise NotImplementedError

    def reset_robot(self) -> None:
        """Reset the robot controller."""
        raise NotImplementedError

    def power_on(self) -> None:
        """Power on the robot."""
        raise NotImplementedError

    def emergency_stop(self) -> None:
        """Trigger an emergency stop."""
        raise NotImplementedError

    def speed_factor(self, speed: int) -> None:
        """Set the global speed factor (1-100)."""
        raise NotImplementedError

    def run_script(self, project_name: str) -> None:
        """Run a project/script on the controller.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def stop_script(self) -> None:
        """Stop the running script or motion queue.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def pause_script(self) -> None:
        """Pause the running script or motion queue.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def resume_script(self) -> None:
        """Resume a paused script or motion queue.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

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
        """Full-circle interpolated motion through two via-points.

        V4 only.  On V3, raises ``NotImplementedError``.

        Args:
            x1–rz1: First via-point (Cartesian).
            x2–rz2: Second via-point (Cartesian).
            count: Number of full circles to execute.
        """
        raise NotImplementedError

    def sync(self) -> None:
        """Block until all queued motion commands have completed."""
        raise NotImplementedError

    def start_path(
        self,
        trace_name: str,
        *,
        is_const: int = -1,
        multi: float = -1.0,
    ) -> int:
        """Play back a recorded trajectory file.

        V4 only.  On V3, raises ``NotImplementedError``.

        Args:
            trace_name: Name of the trajectory file on the controller.
            is_const: Constant speed flag (``-1`` = default).
            multi: Speed multiplier (``-1.0`` = default).
        """
        raise NotImplementedError

    def get_start_pose(self, trace_name: str) -> Pose:
        """Return the starting pose of a recorded trajectory.

        V4 only.  On V3, raises ``NotImplementedError``.

        Args:
            trace_name: Name of the trajectory file on the controller.
        """
        raise NotImplementedError

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
        """Relative joint move in tool coordinate system."""
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------

    def vel_j(self, speed: int) -> None:
        """Set maximum joint velocity (%)."""
        raise NotImplementedError

    def vel_l(self, speed: int) -> None:
        """Set maximum Cartesian velocity (mm/s)."""
        raise NotImplementedError

    def acc_j(self, speed: int) -> None:
        """Set maximum joint acceleration (%)."""
        raise NotImplementedError

    def acc_l(self, speed: int) -> None:
        """Set maximum Cartesian acceleration (mm/s\u00b2)."""
        raise NotImplementedError

    def cp(self, ratio: int) -> None:
        """Set continuous-path blending ratio."""
        raise NotImplementedError

    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Set the tool payload."""
        raise NotImplementedError

    def set_collision_level(self, level: int) -> None:
        """Set collision detection sensitivity level."""
        raise NotImplementedError

    def set_user(self, index: int) -> None:
        """Select the active user coordinate system."""
        raise NotImplementedError

    def set_tool(self, index: int) -> None:
        """Select the active tool coordinate system."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

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
        """Return the queue ID of the currently executing command.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
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
        """Forward kinematics — joint angles to Cartesian pose.

        V4 only.  On V3, raises ``NotImplementedError``.

        Args:
            j1–j6: Joint angles in degrees.
            user: User coordinate system index (``-1`` = current).
            tool: Tool coordinate system index (``-1`` = current).
        """
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
        """Inverse kinematics — Cartesian pose to joint angles.

        V4 only.  On V3, raises ``NotImplementedError``.

        Args:
            x–rz: Target Cartesian pose.
            user: User coordinate system index (``-1`` = current).
            tool: Tool coordinate system index (``-1`` = current).
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # I/O
    # ------------------------------------------------------------------

    def do_output(self, index: int, status: int) -> None:
        """Set a digital output."""
        raise NotImplementedError

    def tool_do(self, index: int, status: int) -> None:
        """Set a tool digital output."""
        raise NotImplementedError

    def ao(self, index: int, value: float) -> None:
        """Set an analogue output."""
        raise NotImplementedError

    def di(self, index: int) -> int:
        """Read a digital input."""
        raise NotImplementedError

    def tool_di(self, index: int) -> int:
        """Read a tool digital input."""
        raise NotImplementedError

    def do_instant(self, index: int, status: int) -> None:
        """Set a digital output immediately (bypasses the motion queue).

        V4 only.  On V3, raises ``NotImplementedError``.
        For queued output, use :meth:`do_output`.
        """
        raise NotImplementedError

    def tool_do_instant(self, index: int, status: int) -> None:
        """Set a tool digital output immediately (bypasses the motion queue).

        V4 only.  On V3, raises ``NotImplementedError``.
        For queued output, use :meth:`tool_do`.
        """
        raise NotImplementedError

    def ao_instant(self, index: int, value: float) -> None:
        """Set an analogue output immediately (bypasses the motion queue).

        V4 only.  On V3, raises ``NotImplementedError``.
        For queued output, use :meth:`ao`.
        """
        raise NotImplementedError

    def ai(self, index: int) -> int:
        """Read an analogue input.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def tool_ai(self, index: int) -> int:
        """Read a tool analogue input.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def get_do(self, index: int) -> int:
        """Read the current status of a digital output.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def get_tool_do(self, index: int) -> int:
        """Read the current status of a tool digital output.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def get_ao(self, index: int) -> float:
        """Read the current value of an analogue output.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------

    def feedback_data(self, port: int = 30004) -> object | None:
        """Return the latest real-time feedback packet."""
        raise NotImplementedError

    def raw_feedback_data(self, port: int = 30004) -> np.ndarray | None:
        """Return the raw numpy feedback array."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Error monitoring
    # ------------------------------------------------------------------

    def check_errors(self, language: str = "en") -> bool:
        """Return ``True`` if the controller has active alarms."""
        raise NotImplementedError

    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors. Returns ``True`` on success."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Force control (V4 only)
    # ------------------------------------------------------------------

    def enable_ft_sensor(self, status: int) -> None:
        """Enable or disable the force/torque sensor.

        V4 only.  On V3, raises ``NotImplementedError``.

        Args:
            status: ``0`` to disable, ``1`` to enable.

        For advanced force-compliance configuration, use the native API::

            robot.native.dashboard.fc_force_mode(...)
            robot.native.dashboard.fc_set_stiffness(...)
            robot.native.dashboard.fc_set_damping(...)
            robot.native.dashboard.fc_set_mass(...)
            robot.native.dashboard.fc_set_force(...)
        """
        raise NotImplementedError

    def six_force_home(self) -> None:
        """Zero (home) the six-axis force/torque sensor.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    def get_force(self) -> Pose:
        """Return force/torque readings from the sensor.

        V4 only.  On V3, raises ``NotImplementedError``.

        Returns:
            A :class:`Pose` where *x–rz* hold Fx, Fy, Fz, Tx, Ty, Tz.
        """
        raise NotImplementedError

    def fc_off(self) -> None:
        """Turn off force-compliance mode.

        V4 only.  On V3, raises ``NotImplementedError``.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Raw
    # ------------------------------------------------------------------

    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Advanced V4 features — native access only
    # ------------------------------------------------------------------
    #
    # The features below are **V4 only** and too specialised for the
    # unified wrapper.  Access them through the ``.native`` escape hatch:
    #
    # **Modbus / Registers**::
    #
    #     robot.native.dashboard.modbus_create(ip, port, slave_id)
    #     robot.native.dashboard.get_hold_regs(index, addr, count)
    #     robot.native.dashboard.set_hold_regs(index, addr, count, val_tab)
    #     robot.native.dashboard.get_coils(index, addr, count)
    #     robot.native.dashboard.set_coils(index, addr, count, val_tab)
    #     robot.native.dashboard.modbus_close(index)
    #
    # **Conveyor tracking**::
    #
    #     robot.native.dashboard.cnv_init(index)
    #     robot.native.dashboard.cnv_mov_l(...)
    #     robot.native.dashboard.start_sync_cnv()
    #     robot.native.dashboard.stop_sync_cnv()
    #
    # **Welding / Weave**::
    #
    #     robot.native.dashboard.weave_start()
    #     robot.native.dashboard.weave_params(...)
    #     robot.native.dashboard.weave_end()
    #     robot.native.dashboard.arc_track_start()
    #     robot.native.dashboard.arc_track_params(...)
    #     robot.native.dashboard.arc_track_end()
    #
    # **Motion pre-check**::
    #
    #     robot.native.dashboard.check_mov_j(...)
    #     robot.native.dashboard.check_mov_l(...)
    #     robot.native.dashboard.check_mov_c(...)
    #
    # **Advanced force compliance**::
    #
    #     robot.native.dashboard.fc_force_mode(...)
    #     robot.native.dashboard.fc_set_stiffness(...)
    #     robot.native.dashboard.fc_set_damping(...)
    #     robot.native.dashboard.fc_set_mass(...)
    #     robot.native.dashboard.fc_set_force(...)
    #     robot.native.dashboard.fc_set_deviation(...)
    #     robot.native.dashboard.force_drive_mode(...)
    #     robot.native.dashboard.force_drive_speed(speed)
    #
    # **I/O groups & Modbus RTU**::
    #
    #     robot.native.dashboard.do_group(...)
    #     robot.native.dashboard.di_group(...)
    #     robot.native.dashboard.modbus_rtu_create(...)
    #     robot.native.dashboard.set_tool_power(status)
    #     robot.native.dashboard.set_tool_mode(mode, port_type)
    #
    # **Advanced config**::
    #
    #     robot.native.dashboard.set_user(index, table)   # define 6-DOF frame
    #     robot.native.dashboard.set_tool(index, table)   # define 6-DOF frame
    #     robot.native.dashboard.calc_user(index, ...)
    #     robot.native.dashboard.calc_tool(index, ...)
    #     robot.native.dashboard.enable_safe_skin(status)
    #     robot.native.dashboard.set_safe_skin(part, status)
    #     robot.native.dashboard.drag_sensitivity(index, value)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> DobotRobot[_T_Native]:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.disconnect()

    # ------------------------------------------------------------------
    # repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"DobotRobot(ip={self._ip!r}, model={self._model!r}, "
            f"family={self._family.display_name!r}, api={self._api_version.value!r})"
        )
