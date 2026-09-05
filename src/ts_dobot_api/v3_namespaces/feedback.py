"""Concrete Feedback namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..api_namespaces import Feedback

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot
    from numpy.typing import NDArray

    from ..types import FeedbackData


class FeedbackV3(Feedback):
    """Concrete Feedback implementation for V3 API."""

    native: V3Robot

    def feedback_data(self, port: int = 30004) -> FeedbackData | None:
        """Return the latest native V3 feedback packet.

        V3 exposes only its standard feedback stream, so ``port`` is accepted
        for interface compatibility and must remain ``30004``.
        """
        if port != 30004:
            raise ValueError(f"Unsupported feedback port for V3: {port}")
        return self.native.feedback_data()

    def raw_feedback_data(self, port: int = 30004) -> NDArray[Any] | None:
        """Return the raw numpy feedback array."""
        if port != 30004:
            raise ValueError(f"Unsupported feedback port for V3: {port}")
        return self.native.raw_feedback_data()
