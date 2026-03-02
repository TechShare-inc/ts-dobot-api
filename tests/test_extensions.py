"""Tests verifying V4-only methods are only on DobotRobotV4."""

from ts_dobot_api.v3 import DobotRobotV3
from ts_dobot_api.v4 import DobotRobotV4


# -- Force control ---------------------------------------------------------

V4_ONLY_FORCE_METHODS = [
    "enable_ft_sensor",
    "six_force_home",
    "get_force",
    "force_drive_mode",
    "force_drive_speed",
    "fc_force_mode",
    "fc_off",
    "fc_collision_switch",
    "set_fc_collision",
]


class TestV4OnlyMethods:
    """V4-only methods must exist on DobotRobotV4 but not DobotRobotV3."""

    def test_force_methods_on_v4(self) -> None:
        for name in V4_ONLY_FORCE_METHODS:
            assert hasattr(DobotRobotV4, name), f"DobotRobotV4 missing {name}"

    def test_force_methods_not_on_v3(self) -> None:
        for name in V4_ONLY_FORCE_METHODS:
            assert not hasattr(DobotRobotV3, name), f"DobotRobotV3 should not have {name}"

    def test_welding_methods_on_v4(self) -> None:
        for name in ["arc_track_start", "weave_start", "weld_arc_speed"]:
            assert hasattr(DobotRobotV4, name), f"DobotRobotV4 missing {name}"

    def test_welding_methods_not_on_v3(self) -> None:
        for name in ["arc_track_start", "weave_start", "weld_arc_speed"]:
            assert not hasattr(DobotRobotV3, name), f"DobotRobotV3 should not have {name}"

    def test_conveyor_methods_on_v4(self) -> None:
        for name in ["cnv_init", "cnv_mov_l", "start_sync_cnv"]:
            assert hasattr(DobotRobotV4, name), f"DobotRobotV4 missing {name}"

    def test_conveyor_methods_not_on_v3(self) -> None:
        for name in ["cnv_init", "cnv_mov_l", "start_sync_cnv"]:
            assert not hasattr(DobotRobotV3, name), f"DobotRobotV3 should not have {name}"

    def test_check_methods_on_v4(self) -> None:
        for name in ["check_mov_j", "check_mov_l", "check_odd_mov_j"]:
            assert hasattr(DobotRobotV4, name), f"DobotRobotV4 missing {name}"

    def test_check_methods_not_on_v3(self) -> None:
        for name in ["check_mov_j", "check_mov_l", "check_odd_mov_j"]:
            assert not hasattr(DobotRobotV3, name), f"DobotRobotV3 should not have {name}"
