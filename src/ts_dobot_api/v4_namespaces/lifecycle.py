"""Concrete Lifecycle namespace for V4 API."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from loguru import logger

from ..api_namespaces import Lifecycle
from ..api_namespaces.lifecycle import _disconnect_once, _reconnect

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class LifecycleV4(Lifecycle):
    """Concrete Lifecycle implementation for V4 API."""

    native: V4Robot

    def __init__(self, native: V4Robot, *, language: str = "en") -> None:
        super().__init__(native)
        self._language = language
        self._connected = True

    def disconnect(self) -> None:
        """Close all TCP connections."""
        self._connected = _disconnect_once(self.native, self._connected)

    def reconnect(self) -> None:
        """Re-establish all TCP connections."""
        self._connected = _reconnect(self.native)

    def shutdown(self) -> None:
        """Gracefully disable the robot arm."""
        logger.info("V4 shutdown: disabling robot")
        self.native.disable_robot()

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
        """V4 startup — composed manually since there's no built-in startup()."""
        logger.info("V4 startup sequence starting")
        has_errors = self.native.check_errors(language=self._language)
        if has_errors:
            logger.info("Errors detected — clearing and powering on")
            self.native.clear_error()
            self.native.power_on()
            logger.info(f"Waiting {power_on_wait}s for controller to power on")
            time.sleep(power_on_wait)
        else:
            logger.info("No errors detected — skipping clear_error and power_on")
        self.native.disable_robot()
        self.native.enable_robot(
            load=load,
            center_x=center_x,
            center_y=center_y,
            center_z=center_z,
        )
        self.native.speed_factor(speed)
        logger.info("V4 startup sequence complete")
