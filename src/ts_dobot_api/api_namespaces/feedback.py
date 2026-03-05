"""
Real-time feedback
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import RobotNamespace

if TYPE_CHECKING:
    import numpy as np



class Feedback(RobotNamespace[object]):
    """Real-time feedback"""

    def feedback_data(self, port: int = 30004) -> object | None:
        """Return the latest real-time feedback packet."""
        raise NotImplementedError

    def raw_feedback_data(self, port: int = 30004) -> np.ndarray | None:
        """Return the raw numpy feedback array."""
        raise NotImplementedError
