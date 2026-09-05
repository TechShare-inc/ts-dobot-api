"""
Conveyor Operations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._base import RobotNamespace

if TYPE_CHECKING:
    pass


class Conveyor(RobotNamespace[object]):
    """Conveyor Operations"""

    def cnv_init(self, index: int) -> None:
        """Initialize conveyor."""
        raise NotImplementedError
