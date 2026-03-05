"""Abstract base classes and Protocols for the unified robot API namespaces."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from ..types import Pose

_T_Native = TypeVar("_T_Native")


class RobotNamespace(ABC, Generic[_T_Native]):
    """Base class for functional namespaces on a robot."""

    def __init__(self, native: _T_Native) -> None:
        self.native: _T_Native = native


# Export namespace classes
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
