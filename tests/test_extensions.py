"""Tests for extension namespaces raising NotSupportedError on V3."""

import pytest

from ts_dobot_api.exceptions import NotSupportedError
from ts_dobot_api.extensions.check import MotionCheck
from ts_dobot_api.extensions.conveyor import ConveyorTracking
from ts_dobot_api.extensions.force import ForceControl
from ts_dobot_api.extensions.weld import Welding
from ts_dobot_api.models import ApiVersion


class TestExtensionsOnV3:
    """All extensions must raise NotSupportedError when api_version is V3."""

    def test_force_raises_on_v3(self) -> None:
        ext = ForceControl(dashboard=None, api_version=ApiVersion.V3)
        with pytest.raises(NotSupportedError, match="Force control"):
            ext.fc_off()

    def test_conveyor_raises_on_v3(self) -> None:
        ext = ConveyorTracking(dashboard=None, api_version=ApiVersion.V3)
        with pytest.raises(NotSupportedError, match="Conveyor tracking"):
            ext.cnv_init(0)

    def test_weld_raises_on_v3(self) -> None:
        ext = Welding(dashboard=None, api_version=ApiVersion.V3)
        with pytest.raises(NotSupportedError, match="Welding"):
            ext.arc_track_start()

    def test_check_raises_on_v3(self) -> None:
        ext = MotionCheck(dashboard=None, api_version=ApiVersion.V3)
        with pytest.raises(NotSupportedError, match="Motion check"):
            ext.check_mov_j(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
