"""
Welding Operations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    pass


class Welding(RobotNamespace[object]):
    """Welding Operations"""

    def weave_start(self) -> None:
        """Start weave operation."""
        raise NotImplementedError
