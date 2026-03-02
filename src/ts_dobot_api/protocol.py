"""Abstract protocol defining the common API surface.

Every adapter (V3, V4, …) must implement this interface so that
:class:`~ts_dobot_api.robot.DobotRobot` can delegate uniformly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .types import Pose


class DobotProtocol(ABC):
    """Abstract base for version-specific adapters.

    Methods are grouped by subsystem.  Return types are unified:

    * **Ack commands** (enable, disable, clear, …) return ``None``.
    * **Motion commands** (mov_j, mov_l, …) return ``int`` (command queue ID).
    * **Query commands** (get_pose, get_angle, …) return the value directly.
    """

    # ==================================================================
    # Lifecycle
    # ==================================================================

    @abstractmethod
    def connect(self) -> None:
        """Open all required TCP connections to the robot."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close all TCP connections gracefully."""

    @abstractmethod
    def reconnect(self) -> None:
        """Re-establish all TCP connections."""

    @abstractmethod
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
        """Run the standard startup sequence (clear → power → enable → speed)."""

    @abstractmethod
    def shutdown(self) -> None:
        """Gracefully disable the robot arm."""

    # ==================================================================
    # System
    # ==================================================================

    @abstractmethod
    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None: ...

    @abstractmethod
    def disable_robot(self) -> None: ...

    @abstractmethod
    def clear_error(self) -> None: ...

    @abstractmethod
    def reset_robot(self) -> None: ...

    @abstractmethod
    def power_on(self) -> None: ...

    @abstractmethod
    def emergency_stop(self) -> None: ...

    @abstractmethod
    def speed_factor(self, speed: int) -> None: ...

    # ==================================================================
    # Motion
    # ==================================================================

    @abstractmethod
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
        """Joint-space move (pose target)."""

    @abstractmethod
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

    @abstractmethod
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
        """Joint-space move (joint target)."""

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def move_jog(self, axis_id: str = "") -> int:
        """Start or stop jog motion along an axis."""

    @abstractmethod
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

    @abstractmethod
    def sync(self) -> None:
        """Block until all queued motion commands have completed.

        V3: native ``sync()`` command. V4: polls ``get_current_command_id()``.
        """

    # ==================================================================
    # Relative motion
    # ==================================================================

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    # ==================================================================
    # Config
    # ==================================================================

    @abstractmethod
    def vel_j(self, speed: int) -> None: ...

    @abstractmethod
    def vel_l(self, speed: int) -> None: ...

    @abstractmethod
    def acc_j(self, speed: int) -> None: ...

    @abstractmethod
    def acc_l(self, speed: int) -> None: ...

    @abstractmethod
    def cp(self, ratio: int) -> None: ...

    @abstractmethod
    def set_payload(
        self,
        weight: float,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None: ...

    @abstractmethod
    def set_collision_level(self, level: int) -> None: ...

    @abstractmethod
    def set_user(self, index: int) -> None: ...

    @abstractmethod
    def set_tool(self, index: int) -> None: ...

    # ==================================================================
    # Query
    # ==================================================================

    @abstractmethod
    def robot_mode(self) -> int: ...

    @abstractmethod
    def get_pose(self) -> Pose: ...

    @abstractmethod
    def get_angle(self) -> Pose: ...

    @abstractmethod
    def get_error_id(self) -> tuple[int, ...]: ...

    @abstractmethod
    def start_drag(self) -> None: ...

    @abstractmethod
    def stop_drag(self) -> None: ...

    # ==================================================================
    # I/O
    # ==================================================================

    @abstractmethod
    def do_output(self, index: int, status: int) -> None: ...

    @abstractmethod
    def tool_do(self, index: int, status: int) -> None: ...

    @abstractmethod
    def ao(self, index: int, value: float) -> None: ...

    @abstractmethod
    def di(self, index: int) -> int: ...

    @abstractmethod
    def tool_di(self, index: int) -> int: ...

    # ==================================================================
    # Feedback
    # ==================================================================

    @abstractmethod
    def feedback_data(self, port: int = 30004) -> Any | None:
        """Return the latest real-time feedback packet, or ``None``."""

    @abstractmethod
    def raw_feedback_data(self, port: int = 30004) -> Any | None:
        """Return the raw numpy feedback array, or ``None``."""

    # ==================================================================
    # Error monitoring
    # ==================================================================

    @abstractmethod
    def check_errors(self, language: str = "en") -> bool:
        """Return ``True`` if the controller currently has active alarms."""

    @abstractmethod
    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors and return ``True`` if successful."""

    # ==================================================================
    # Raw access
    # ==================================================================

    @abstractmethod
    def send_raw(self, command: str) -> str:
        """Send a raw TCP command string and return the raw response."""
