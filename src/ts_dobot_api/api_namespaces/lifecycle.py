"""
Lifecycle management
"""

from __future__ import annotations

from typing import Protocol

from ._base import RobotNamespace


class _Reconnectable(Protocol):
    def close(self) -> None: ...

    def reconnect(self) -> None: ...


def _disconnect_once(native: _Reconnectable, connected: bool) -> bool:
    """Close a native client at most once and return its new state."""
    if connected:
        native.close()
    return False


def _reconnect(native: _Reconnectable) -> bool:
    """Reconnect a native client and return its new state."""
    native.reconnect()
    return True


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
