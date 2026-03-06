"""Concrete System namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import System

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class SystemV4(System):
    """Concrete System implementation for V4 API."""

    native: V4Robot

    def clear_error(self) -> None:
        """Clear controller error/alarm information."""
        self.native.clear_error()

    def disable_robot(self) -> None:
        """Disable the robot."""
        self.native.disable_robot()

    def emergency_stop(self) -> None:
        """Trigger an emergency stop."""
        self.native.emergency_stop(mode=0)

    def enable_robot(
        self,
        load: float = 0.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        center_z: float = 0.0,
    ) -> None:
        """Enable the robot."""
        self.native.enable_robot(load=load, center_x=center_x, center_y=center_y, center_z=center_z)

    def pause_script(self) -> None:
        """Pause the running script or motion queue."""
        self.native.dashboard.pause_script()

    def power_on(self) -> None:
        """Power on the robot."""
        self.native.power_on()

    def reset_robot(self) -> None:
        """Reset the robot controller."""
        self.native.reset_robot()

    def resume_script(self) -> None:
        """Resume a paused script or motion queue."""
        self.native.dashboard.resume()

    def run_script(self, project_name: str) -> None:
        """Run a project/script on the controller."""
        self.native.dashboard.run_script(project_name)

    def speed_factor(self, speed: int) -> None:
        """Set the global speed factor (1–100)."""
        self.native.speed_factor(speed)

    def stop_script(self) -> None:
        """Stop the running script or motion queue."""
        self.native.dashboard.stop_script()
