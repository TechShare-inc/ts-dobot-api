"""Concrete Feedback namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import Feedback

if TYPE_CHECKING:
    import numpy as np

    from dobot_api_v3 import DobotRobot as V3Robot


class FeedbackV3(Feedback):
    """Concrete Feedback implementation for V3 API."""

    native: V3Robot

    def feedback_data(self, port: int = 30004) -> object | None:
        """Return the latest real-time feedback packet."""
        fb = self._get_feedback(port)
        return fb.feedback_data() if fb else None

    def raw_feedback_data(self, port: int = 30004) -> np.ndarray | None:
        """Return the raw numpy feedback array."""
        fb = self._get_feedback(port)
        return fb.raw_feedback_data() if fb else None
