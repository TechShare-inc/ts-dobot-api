"""V3/V4 contract tests for the unified Dobot facade."""

from __future__ import annotations

from typing import Any, ClassVar, cast

import dobot_api_v3
import dobot_api_v4
import numpy as np
import pytest
from numpy.typing import NDArray

from ts_dobot_api import ApiVersion, DobotRobot, DobotRobotV3, DobotRobotV4
from ts_dobot_api.exceptions import NotSupportedError


class _FeedbackPacket:
    """Small structural stand-in for either vendor's typed feedback packet."""

    test_value = 0x123456789ABCDEF
    q_actual = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
    qd_actual = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    m_actual = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


class _FeedbackStream:
    def __init__(self, marker: int) -> None:
        self.packet = _FeedbackPacket()
        self.raw = np.array([marker], dtype=np.int64)

    def feedback_data(self) -> _FeedbackPacket:
        return self.packet

    def raw_feedback_data(self) -> NDArray[np.int64]:
        return self.raw


class _FakeV3Robot:
    last_instance: ClassVar[_FakeV3Robot | None] = None

    def __init__(self, ip: str, *, language: str = "en") -> None:
        self.ip = ip
        self.language = language
        self.dashboard = self
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []
        self.packet = _FeedbackPacket()
        self.raw = np.array([3], dtype=np.int64)
        type(self).last_instance = self

    def enable_robot(self, **kwargs: float) -> None:
        self.calls.append(("enable_robot", (), kwargs))

    def emergency_stop(self) -> int:
        self.calls.append(("emergency_stop", (), {}))
        return 0

    def servo_j(self, *args: float, **kwargs: float) -> int:
        self.calls.append(("servo_j", args, kwargs))
        return 31

    def servo_js(self, *args: float) -> int:
        self.calls.append(("servo_js", args, {}))
        return 32

    def feedback_data(self) -> _FeedbackPacket:
        self.calls.append(("feedback_data", (), {}))
        return self.packet

    def raw_feedback_data(self) -> NDArray[np.int64]:
        self.calls.append(("raw_feedback_data", (), {}))
        return self.raw

    def close(self) -> None:
        self.calls.append(("close", (), {}))

    def ao_execute(self, index: int, value: float) -> int:
        self.calls.append(("ao_execute", (index, value), {}))
        return 0

    def do_execute(self, index: int, status: int) -> int:
        self.calls.append(("do_execute", (index, status), {}))
        return 0

    def tool_do_execute(self, index: int, status: int) -> int:
        self.calls.append(("tool_do_execute", (index, status), {}))
        return 0

    def inverse_solution(self, *args: float | int) -> tuple[float, ...]:
        self.calls.append(("inverse_solution", args, {}))
        return (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

    def positive_solution(self, *args: float | int) -> tuple[float, ...]:
        self.calls.append(("positive_solution", args, {}))
        return (6.0, 5.0, 4.0, 3.0, 2.0, 1.0)

    def get_path_start_pose(self, trace_name: str) -> tuple[float, ...]:
        self.calls.append(("get_path_start_pose", (trace_name,), {}))
        return (10.0, 20.0, 30.0, 40.0, 50.0, 60.0)

    def start_path(self, trace_name: str, const: int, cart: int) -> int:
        self.calls.append(("start_path", (trace_name, const, cart), {}))
        return 33


class _FakeV4Robot:
    last_instance: ClassVar[_FakeV4Robot | None] = None

    def __init__(self, ip: str, *, language: str = "en") -> None:
        self.ip = ip
        self.language = language
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []
        self.feedback = _FeedbackStream(4)
        self.feedback_30005 = _FeedbackStream(5)
        self.feedback_30006 = _FeedbackStream(6)
        type(self).last_instance = self

    def enable_robot(self, **kwargs: float) -> None:
        self.calls.append(("enable_robot", (), kwargs))

    def emergency_stop(self, *, mode: int) -> None:
        self.calls.append(("emergency_stop", (), {"mode": mode}))

    def servo_j(self, *args: float, **kwargs: float) -> int:
        self.calls.append(("servo_j", args, kwargs))
        return 41

    def close(self) -> None:
        self.calls.append(("close", (), {}))


@pytest.fixture(autouse=True)
def _patch_vendor_robots(monkeypatch: pytest.MonkeyPatch) -> None:
    _FakeV3Robot.last_instance = None
    _FakeV4Robot.last_instance = None
    monkeypatch.setattr(dobot_api_v3, "DobotRobot", _FakeV3Robot)
    monkeypatch.setattr(dobot_api_v4, "DobotRobot", _FakeV4Robot)


def test_connect_selects_v3_from_model() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA", language="en")

    assert isinstance(robot, DobotRobotV3)
    assert robot.api_version is ApiVersion.V3
    native = cast(_FakeV3Robot, robot.native)
    assert native is _FakeV3Robot.last_instance
    assert native.ip == "192.0.2.3"
    assert native.language == "en"


def test_connect_selects_v4_from_model() -> None:
    robot = DobotRobot.connect("192.0.2.4", "NOVA_2S", language="ja")

    assert isinstance(robot, DobotRobotV4)
    assert robot.api_version is ApiVersion.V4
    native = cast(_FakeV4Robot, robot.native)
    assert native is _FakeV4Robot.last_instance
    assert native.ip == "192.0.2.4"
    assert native.language == "ja"


def test_v3_enable_estop_and_disconnect_contract() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")
    native = cast(_FakeV3Robot, robot.native)

    robot.system.enable_robot(load=1.5, center_x=1.0, center_y=2.0, center_z=3.0)
    robot.system.emergency_stop()
    robot.lifecycle.disconnect()
    robot.lifecycle.disconnect()

    assert native.calls == [
        (
            "enable_robot",
            (),
            {"load": 1.5, "center_x": 1.0, "center_y": 2.0, "center_z": 3.0},
        ),
        ("emergency_stop", (), {}),
        ("close", (), {}),
    ]


def test_v4_enable_estop_and_disconnect_contract() -> None:
    robot = DobotRobot.connect("192.0.2.4", "NOVA_NG")
    native = cast(_FakeV4Robot, robot.native)

    robot.system.enable_robot(load=1.5, center_x=1.0, center_y=2.0, center_z=3.0)
    robot.system.emergency_stop()
    robot.lifecycle.disconnect()
    robot.lifecycle.disconnect()

    assert native.calls == [
        (
            "enable_robot",
            (),
            {"load": 1.5, "center_x": 1.0, "center_y": 2.0, "center_z": 3.0},
        ),
        ("emergency_stop", (), {"mode": 0}),
        ("close", (), {}),
    ]


def test_v3_feedback_preserves_native_packet_and_raw_data() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")
    native = cast(_FakeV3Robot, robot.native)

    packet = cast(_FeedbackPacket, robot.feedback.feedback_data())
    raw = robot.feedback.raw_feedback_data()

    assert packet is native.packet
    assert packet.q_actual == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
    assert raw is native.raw
    with pytest.raises(ValueError, match="Unsupported feedback port for V3"):
        robot.feedback.feedback_data(port=30005)


@pytest.mark.parametrize("port", [30004, 30005, 30006])
def test_v4_feedback_selects_requested_port(port: int) -> None:
    robot = DobotRobot.connect("192.0.2.4", "CR")
    native = cast(_FakeV4Robot, robot.native)
    stream = {
        30004: native.feedback,
        30005: native.feedback_30005,
        30006: native.feedback_30006,
    }[port]

    packet = cast(_FeedbackPacket, robot.feedback.feedback_data(port=port))
    assert packet is stream.packet
    assert robot.feedback.raw_feedback_data(port=port) is stream.raw


def test_v4_feedback_rejects_unknown_port() -> None:
    robot = DobotRobot.connect("192.0.2.4", "CR")

    with pytest.raises(ValueError, match="Unsupported feedback port: 12345"):
        robot.feedback.feedback_data(port=12345)


def test_v3_servo_contract_and_servojs_compatibility() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")
    native = cast(_FakeV3Robot, robot.native)

    result_j = robot.motion.servo_j(1, 2, 3, 4, 5, 6, t=0.2, lookahead_time=60.0, gain=600.0)
    result_js = robot.motion.servo_js(6, 5, 4, 3, 2, 1)

    assert result_j == 31
    assert result_js == 32
    assert native.calls == [
        (
            "servo_j",
            (1, 2, 3, 4, 5, 6),
            {"t": 0.2, "lookahead_time": 60.0, "gain": 600.0},
        ),
        ("servo_js", (6, 5, 4, 3, 2, 1), {}),
    ]


def test_v4_servo_contract_and_servojs_rejection() -> None:
    robot = DobotRobot.connect("192.0.2.4", "NOVA_2S")
    native = cast(_FakeV4Robot, robot.native)

    result = robot.motion.servo_j(1, 2, 3, 4, 5, 6, t=0.2, lookahead_time=60.0, gain=600.0)

    assert result == 41
    assert native.calls == [
        (
            "servo_j",
            (1, 2, 3, 4, 5, 6),
            {"t": 0.2, "ahead_time": 60.0, "gain": 600.0},
        )
    ]
    with pytest.raises(NotSupportedError, match="only through the V3 protocol"):
        robot.motion.servo_js(1, 2, 3, 4, 5, 6)


def test_v3_renamed_vendor_methods_are_adapted() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")
    native = cast(_FakeV3Robot, robot.native)

    robot.io.ao_instant(1, 2.5)
    robot.io.do_instant(2, 1)
    robot.io.tool_do_instant(1, 0)

    assert native.calls == [
        ("ao_execute", (1, 2.5), {}),
        ("do_execute", (2, 1), {}),
        ("tool_do_execute", (1, 0), {}),
    ]
    with pytest.raises(NotSupportedError, match="AI query"):
        robot.io.ai(1)
    with pytest.raises(NotSupportedError, match="Current command ID"):
        robot.query.get_current_command_id()


def test_v3_pose_and_path_results_use_unified_types() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")

    inverse = robot.query.inverse_kin(1, 2, 3, 4, 5, 6)
    positive = robot.query.positive_kin(1, 2, 3, 4, 5, 6)
    start = robot.motion.get_start_pose("path.csv")
    path_id = robot.motion.start_path("path.csv", is_const=1, cart=0)

    assert inverse.as_tuple() == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
    assert positive.as_tuple() == (6.0, 5.0, 4.0, 3.0, 2.0, 1.0)
    assert start.as_tuple() == (10.0, 20.0, 30.0, 40.0, 50.0, 60.0)
    assert path_id == 33
    with pytest.raises(NotSupportedError, match="multi option"):
        robot.motion.start_path("path.csv", multi=2.0)
