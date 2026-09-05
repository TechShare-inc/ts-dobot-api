"""Concrete Feedback namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..api_namespaces import Feedback

if TYPE_CHECKING:
    from dobot_api_v4 import DobotApiFeedback
    from dobot_api_v4 import DobotRobot as V4Robot
    from numpy.typing import NDArray

    from ..types import FeedbackData


class FeedbackV4(Feedback):
    """Concrete Feedback implementation for V4 API."""

    native: V4Robot

    def feedback_data(self, port: int = 30004) -> FeedbackData | None:
        """Return the latest real-time feedback packet."""
        fb = self._get_feedback(port)
        return fb.feedback_data() if fb else None

    def raw_feedback_data(self, port: int = 30004) -> NDArray[Any] | None:
        """Return the raw numpy feedback array."""
        fb = self._get_feedback(port)
        return fb.raw_feedback_data() if fb else None

    def _get_feedback(self, port: int) -> DobotApiFeedback | None:
        """Return the native V4 feedback connection for the requested port."""
        if port == 30004:
            return self.native.feedback
        if port == 30005:
            return self.native.feedback_30005
        if port == 30006:
            return self.native.feedback_30006

        raise ValueError(f"Unsupported feedback port: {port}")
