"""TechShare Dobot API wrapper - unified interface for all Dobot robots."""

__version__ = "1.0.0-alpha.1"

from .exceptions import NotSupportedError, TsDobotError
from .models import ApiVersion, RobotFamily
from .robot import DobotRobot
from .types import AlarmInfo, FeedbackData, Pose
from .v3 import DobotRobotV3
from .v4 import DobotRobotV4

__all__ = [
    "DobotRobot",
    "DobotRobotV3",
    "DobotRobotV4",
    "ApiVersion",
    "RobotFamily",
    "Pose",
    "FeedbackData",
    "AlarmInfo",
    "TsDobotError",
    "NotSupportedError",
    "__version__",
]
