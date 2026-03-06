"""Concrete ErrorHandling namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import ErrorHandling

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class ErrorHandlingV3(ErrorHandling):
    """Concrete ErrorHandling implementation for V3 API."""

    native: V3Robot

    def check_errors(self, language: str = "en") -> bool:
        """Return ``True`` if the controller has active alarms."""
        return self.native.check_errors(language=language)

    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors. Returns ``True`` on success."""
        return self.native.clear_and_recover(language=language)
