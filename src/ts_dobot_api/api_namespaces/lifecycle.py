"""
Lifecycle management
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._base import RobotNamespace

if TYPE_CHECKING:
    pass


class Lifecycle(RobotNamespace[object]):
    """Lifecycle management"""

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
        power_on_wait: float = 20.0,
    ) -> None:
        """Run the standard startup sequence."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Gracefully disable the robot arm."""
        raise NotImplementedError
