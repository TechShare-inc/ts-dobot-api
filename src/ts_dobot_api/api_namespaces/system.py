"""
System control and monitoring
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    pass


class System(RobotNamespace[object]):
    """System control and monitoring"""

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
        """Run a project/script on the controller."""
        raise NotImplementedError

    def stop_script(self) -> None:
        """Stop the running script or motion queue."""
        raise NotImplementedError

    def pause_script(self) -> None:
        """Pause the running script or motion queue."""
        raise NotImplementedError

    def resume_script(self) -> None:
        """Resume a paused script or motion queue."""
        raise NotImplementedError
