"""Abstract base classes and protocols for unified robot API namespaces."""

from __future__ import annotations

from ._base import RobotNamespace
from .config import Config
from .conveyor import Conveyor
from .error_handling import ErrorHandling
from .feedback import Feedback
from .force_control import ForceControl
from .io import Io
from .lifecycle import Lifecycle
from .modbus import Modbus
from .motion import Motion
from .query import Query
from .raw import Raw
from .relative_motion import RelativeMotion
from .system import System
from .welding import Welding

__all__ = [
    "RobotNamespace",
    "Lifecycle",
    "System",
    "Motion",
    "RelativeMotion",
    "Config",
    "Query",
    "Io",
    "Feedback",
    "ErrorHandling",
    "ForceControl",
    "Modbus",
    "Welding",
    "Conveyor",
    "Raw",
]
