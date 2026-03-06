"""Concrete ErrorHandling namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import ErrorHandling

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class ErrorHandlingV4(ErrorHandling):
    """Concrete ErrorHandling implementation for V4 API."""

    native: V4Robot

    def check_errors(self, language: str = "en") -> bool:
        """Return ``True`` if the controller has active alarms."""
        return self.native.check_errors(language=language)

    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors. Returns ``True`` on success."""
        return self.native.clear_robot_error(language=language)
