"""V3 robot implementation — wraps ``dobot_api_v3.DobotRobot`` directly."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .api_namespaces import Conveyor, ForceControl, Welding
from .exceptions import NotSupportedError
from .models import ApiVersion
from .robot import DobotRobot
from .v3_namespaces.config import ConfigV3
from .v3_namespaces.error_handling import ErrorHandlingV3
from .v3_namespaces.feedback import FeedbackV3
from .v3_namespaces.io import IoV3
from .v3_namespaces.lifecycle import LifecycleV3
from .v3_namespaces.modbus import ModbusV3
from .v3_namespaces.motion import MotionV3
from .v3_namespaces.query import QueryV3
from .v3_namespaces.raw import RawV3
from .v3_namespaces.relative_motion import RelativeMotionV3
from .v3_namespaces.system import SystemV3

if TYPE_CHECKING:
    from dobot_api_v3 import DobotRobot as V3Robot


class _UnsupportedNamespace:
    """Raise a protocol-specific error when an unavailable namespace is used."""

    def __init__(self, name: str) -> None:
        self._name = name

    def __getattr__(self, attribute: str) -> object:
        raise NotSupportedError(f"{self._name} namespace is not available in the V3 protocol")


class DobotRobotV3(DobotRobot["V3Robot"]):
    """Dobot robot using the V3 protocol (Nova series)."""

    _api_version = ApiVersion.V3

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        super().__init__(ip, model, language=language)

        from dobot_api_v3 import DobotRobot as V3Robot

        self._native: V3Robot = V3Robot(ip, language=language)

        # Initialize namespaces
        self.lifecycle = LifecycleV3(self._native)
        self.system = SystemV3(self._native)
        self.motion = MotionV3(self._native)
        self.relative_motion = RelativeMotionV3(self._native)
        self.config = ConfigV3(self._native)
        self.query = QueryV3(self._native)
        self.io = IoV3(self._native)
        self.feedback = FeedbackV3(self._native)
        self.error_handling = ErrorHandlingV3(self._native)
        self.modbus = ModbusV3(self._native)
        self.raw = RawV3(self._native)

        # V4-only namespaces fail explicitly when accessed on a V3 robot.
        self.welding = cast(Welding, _UnsupportedNamespace("Welding"))
        self.conveyor = cast(Conveyor, _UnsupportedNamespace("Conveyor"))
        self.force_control = cast(ForceControl, _UnsupportedNamespace("ForceControl"))
