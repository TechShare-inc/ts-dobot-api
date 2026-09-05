"""
Real-time feedback
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._base import RobotNamespace

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from ..types import FeedbackData


class Feedback(RobotNamespace[object]):
    """Real-time feedback"""

    def feedback_data(self, port: int = 30004) -> FeedbackData | None:
        """Return the native typed feedback packet for the selected protocol."""
        raise NotImplementedError

    def raw_feedback_data(self, port: int = 30004) -> NDArray[Any] | None:
        """Return the raw numpy feedback array."""
        raise NotImplementedError
