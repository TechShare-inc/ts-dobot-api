"""V4 robot implementation - wraps ``dobot_api_v4.DobotRobot`` directly."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from .models import ApiVersion
from .robot import DobotRobot
from .types import Pose

from .v4_namespaces import (
    ConfigV4, ConveyorV4, ErrorHandlingV4, FeedbackV4, ForceControlV4,
    IoV4, LifecycleV4, ModbusV4, MotionV4, QueryV4, RawV4, RelativeMotionV4,
    SystemV4, WeldingV4
)

if TYPE_CHECKING:
    import numpy as np
    from dobot_api_v4 import DobotApiDashboard as V4Dashboard
    from dobot_api_v4 import DobotApiFeedback as V4Feedback
    from dobot_api_v4 import DobotRobot as V4Robot
    from dobot_api_v4 import FeedbackData as V4FeedbackData
    from dobot_api_v4 import Pose as V4Pose


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