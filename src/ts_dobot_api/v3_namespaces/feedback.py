"""Concrete Feedback namespace for V3 API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..api_namespaces import Feedback
from ..types import FeedbackData

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot
    from numpy.typing import NDArray


class FeedbackV3(Feedback):
    """Concrete Feedback implementation for V3 API."""

    native: V3Robot

    def feedback_data(self, port: int = 30004) -> FeedbackData | None:
        """Return the latest native V3 feedback packet.

        V3 exposes only its standard feedback stream, so ``port`` is accepted
        for interface compatibility and must remain ``30004``.
        """
        self._validate_port(port)
        packet = self.native.feedback_data()
        if packet is None:
            return None
        return FeedbackData.from_native(packet, angular_values_in_degrees=False)

    def raw_feedback_data(self, port: int = 30004) -> NDArray[Any] | None:
        """Return the raw numpy feedback array."""
        self._validate_port(port)
        return self.native.raw_feedback_data()

    @staticmethod
    def _validate_port(port: int) -> None:
        if port != 30004:
            raise ValueError(f"Unsupported feedback port for V3: {port}")
