"""
Error and alarm handling
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._base import RobotNamespace

if TYPE_CHECKING:
    pass


class ErrorHandling(RobotNamespace[object]):
    """Error and alarm handling"""

    def check_errors(self, language: str = "en") -> bool:
        """Return True if the controller has active alarms."""
        raise NotImplementedError

    def clear_and_recover(self, language: str = "en") -> bool:
        """Attempt to clear errors. Returns True on success."""
        raise NotImplementedError
