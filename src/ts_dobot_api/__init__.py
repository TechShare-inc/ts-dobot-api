"""TechShare Dobot API wrapper — unified interface for all Dobot robots."""

__version__ = "1.0.0-alpha.1"

from .exceptions import NotSupportedError, TsDobotError
from .models import ApiVersion, RobotFamily
from .robot import DobotRobot
from .types import AlarmInfo, Pose

__all__ = [
    "DobotRobot",
    "ApiVersion",
    "RobotFamily",
    "Pose",
    "AlarmInfo",
    "TsDobotError",
    "NotSupportedError",
    "__version__",
]
