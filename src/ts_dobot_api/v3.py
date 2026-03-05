"""V3 robot implementation — wraps ``dobot_api_v3.DobotRobot`` directly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .models import ApiVersion
from .robot import DobotRobot
from .types import Pose

from .v3_namespaces import (
    ConfigV3, ErrorHandlingV3, FeedbackV3, IoV3, LifecycleV3,
    MotionV3, QueryV3, RawV3, RelativeMotionV3, SystemV3
)

if TYPE_CHECKING:
    import numpy as np
    from dobot_api_v3 import DobotApiFeedback as V3Feedback
    from dobot_api_v3 import DobotRobot as V3Robot
    from dobot_api_v3 import FeedbackData as V3FeedbackData


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
        self.raw = RawV3(self._native)

        # V4 Only namespaces mapped to error on V3
        from .v3_namespaces import ModbusV3, WeldingV3, ConveyorV3, ForceControlV3
        self.modbus = ModbusV3(self._native)
        self.welding = WeldingV3(self._native)
        self.conveyor = ConveyorV3(self._native)
        self.force_control = ForceControlV3(self._native)
