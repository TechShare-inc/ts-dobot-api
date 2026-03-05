"""V4 robot implementation - wraps ``dobot_api_v4.DobotRobot`` directly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .models import ApiVersion
from .robot import DobotRobot
from .v4_namespaces.config import ConfigV4
from .v4_namespaces.conveyor import ConveyorV4
from .v4_namespaces.error_handling import ErrorHandlingV4
from .v4_namespaces.feedback import FeedbackV4
from .v4_namespaces.force_control import ForceControlV4
from .v4_namespaces.io import IoV4
from .v4_namespaces.lifecycle import LifecycleV4
from .v4_namespaces.modbus import ModbusV4
from .v4_namespaces.motion import MotionV4
from .v4_namespaces.query import QueryV4
from .v4_namespaces.raw import RawV4
from .v4_namespaces.relative_motion import RelativeMotionV4
from .v4_namespaces.system import SystemV4
from .v4_namespaces.welding import WeldingV4

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class DobotRobotV4(DobotRobot["V4Robot"]):
    """Dobot robot using the V4 protocol (CR / Nova 2s / Nova NG series)."""

    _api_version = ApiVersion.V4

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        super().__init__(ip, model, language=language)

        from dobot_api_v4 import DobotRobot as V4Robot

        self._native: V4Robot = V4Robot(ip, language=language)

        # Initialize namespaces
        self.lifecycle = LifecycleV4(self._native)
        self.system = SystemV4(self._native)
        self.motion = MotionV4(self._native)
        self.relative_motion = RelativeMotionV4(self._native)
        self.config = ConfigV4(self._native)
        self.query = QueryV4(self._native)
        self.io = IoV4(self._native)
        self.feedback = FeedbackV4(self._native)
        self.error_handling = ErrorHandlingV4(self._native)
        self.raw = RawV4(self._native)
        self.modbus = ModbusV4(self._native)
        self.welding = WeldingV4(self._native)
        self.conveyor = ConveyorV4(self._native)
        self.force_control = ForceControlV4(self._native)
