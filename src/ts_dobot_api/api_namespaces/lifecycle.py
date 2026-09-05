"""
Lifecycle management
"""

from __future__ import annotations

from typing import Protocol, cast

from ._base import RobotNamespace


class _Reconnectable(Protocol):
    def close(self) -> None: ...

    def reconnect(self) -> None: ...


class Lifecycle(RobotNamespace[object]):
    """Lifecycle management"""

    def __init__(self, native: object) -> None:
        super().__init__(native)
        self._connected = True

    def disconnect(self) -> None:
        """Close all TCP connections."""
        if self._connected:
            cast(_Reconnectable, self.native).close()
            self._connected = False

    def reconnect(self) -> None:
        """Re-establish all TCP connections."""
        cast(_Reconnectable, self.native).reconnect()
        self._connected = True

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
