"""V3/V4 contract tests for the unified Dobot facade."""

from __future__ import annotations

from typing import Any, ClassVar, cast

import dobot_api_v3
import dobot_api_v4
import numpy as np
import pytest
from numpy.typing import NDArray

from ts_dobot_api import (
    ApiVersion,
    DobotRobot,
    DobotRobotV3,
    DobotRobotV4,
    FeedbackData,
)
from ts_dobot_api.exceptions import NotSupportedError


class _FeedbackPacket:
    """Small structural stand-in for either vendor's typed feedback packet."""

    def __init__(self, q_actual: tuple[float, ...], qd_actual: tuple[float, ...]) -> None:
        self.test_value = 0x123456789ABCDEF
        self.q_actual = q_actual
        self.qd_actual = qd_actual
        self.m_actual = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)


class _FeedbackStream:
    def __init__(self, marker: int) -> None:
        self.packet = _FeedbackPacket(
            (0.0, 90.0, -90.0, 180.0, -180.0, 45.0),
            (0.0, 9.0, -9.0, 18.0, -18.0, 4.5),
        )
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
        self.packet = _FeedbackPacket(
            (0.0, np.pi / 2, -np.pi / 2, np.pi, -np.pi, np.pi / 4),
            (0.0, np.pi / 20, -np.pi / 20, np.pi / 10, -np.pi / 10, np.pi / 40),
        )
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

    def reconnect(self) -> None:
        self.calls.append(("reconnect", (), {}))

    def resume(self) -> int:
        self.calls.append(("resume", (), {}))
        return 0

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

    def modbus_create(self, ip: str, port: int, slave_id: int, is_rtu: int) -> int:
        self.calls.append(("modbus_create", (ip, port, slave_id, is_rtu), {}))
        return 7

    def modbus_close(self, index: int) -> int:
        self.calls.append(("modbus_close", (index,), {}))
        return 0

    def get_hold_regs(self, index: int, addr: int, count: int, val_type: str) -> tuple[float, ...]:
        self.calls.append(("get_hold_regs", (index, addr, count, val_type), {}))
        return (1.0, 2.0)

    def set_hold_regs(self, index: int, addr: int, count: int, values: str, val_type: str) -> int:
        self.calls.append(("set_hold_regs", (index, addr, count, values, val_type), {}))
        return 0


class _FakeV4Robot:
    last_instance: ClassVar[_FakeV4Robot | None] = None

    def __init__(self, ip: str, *, language: str = "en") -> None:
        self.ip = ip
        self.language = language
        self.dashboard = self
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

    def reconnect(self) -> None:
        self.calls.append(("reconnect", (), {}))

    def start_path(self, trace_name: str, *, is_const: int, multi: float) -> int:
        self.calls.append(("start_path", (trace_name,), {"is_const": is_const, "multi": multi}))
        return 43

    def get_hold_regs(self, index: int, addr: int, count: int, val_type: str) -> str:
        self.calls.append(("get_hold_regs", (index, addr, count, val_type), {}))
        return "0,{1,2},GetHoldRegs();"

    def set_hold_regs(self, index: int, addr: int, count: int, values: str, val_type: str) -> None:
        self.calls.append(("set_hold_regs", (index, addr, count, values, val_type), {}))


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

    packet = cast(FeedbackData, robot.feedback.feedback_data())
    raw = robot.feedback.raw_feedback_data()

    assert packet.native is native.packet
    assert packet.q_actual == pytest.approx((0.0, np.pi / 2, -np.pi / 2, np.pi, -np.pi, np.pi / 4))
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

    packet = cast(FeedbackData, robot.feedback.feedback_data(port=port))
    assert packet.native is stream.packet
    assert packet.q_actual == pytest.approx((0.0, np.pi / 2, -np.pi / 2, np.pi, -np.pi, np.pi / 4))
    assert robot.feedback.raw_feedback_data(port=port) is stream.raw


def test_v4_feedback_rejects_unknown_port() -> None:
    robot = DobotRobot.connect("192.0.2.4", "CR")

    with pytest.raises(ValueError, match="Unsupported feedback port: 12345"):
        robot.feedback.feedback_data(port=12345)


def test_v3_and_v4_feedback_share_normalized_units() -> None:
    v3 = DobotRobot.connect("192.0.2.3", "NOVA")
    v4 = DobotRobot.connect("192.0.2.4", "NOVA_2S")

    v3_packet = cast(FeedbackData, v3.feedback.feedback_data())
    v4_packet = cast(FeedbackData, v4.feedback.feedback_data())

    assert v4_packet.q_actual == pytest.approx(v3_packet.q_actual)
    assert v4_packet.qd_actual == pytest.approx(v3_packet.qd_actual)
    assert v4_packet.m_actual == v3_packet.m_actual


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


@pytest.mark.parametrize("model", ["NOVA", "NOVA_2S"])
def test_lifecycle_reconnect_allows_a_later_disconnect(model: str) -> None:
    robot = DobotRobot.connect("192.0.2.5", model)
    native = cast(_FakeV3Robot | _FakeV4Robot, robot.native)

    robot.lifecycle.disconnect()
    robot.lifecycle.reconnect()
    robot.lifecycle.disconnect()

    assert [name for name, _, _ in native.calls] == ["close", "reconnect", "close"]


def test_v3_unsupported_queries_and_namespaces_fail_explicitly() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")

    for query in (
        robot.io.get_ao,
        robot.io.get_do,
        robot.io.get_tool_do,
        robot.io.tool_ai,
    ):
        with pytest.raises(NotSupportedError):
            query(1)
    with pytest.raises(NotSupportedError, match="Welding namespace"):
        robot.welding.weave_start()


def test_v3_resume_and_modbus_use_pinned_vendor_contract() -> None:
    robot = DobotRobot.connect("192.0.2.3", "NOVA")
    native = cast(_FakeV3Robot, robot.native)

    robot.system.resume_script()
    index = robot.modbus.modbus_create("192.0.2.10", 502, 1, 0)
    values = robot.modbus.get_hold_regs(index, 100, 2, "F32")
    robot.modbus.set_hold_regs(index, 100, 2, "{1,2}", "F32")
    robot.modbus.modbus_close(index)

    assert index == 7
    assert values == (1.0, 2.0)
    assert [name for name, _, _ in native.calls] == [
        "resume",
        "modbus_create",
        "get_hold_regs",
        "set_hold_regs",
        "modbus_close",
    ]


def test_v4_modbus_and_path_options_use_pinned_vendor_contract() -> None:
    robot = DobotRobot.connect("192.0.2.4", "CR")

    assert robot.modbus.get_hold_regs(2, 100, 2, "U16") == "0,{1,2},GetHoldRegs();"
    robot.modbus.set_hold_regs(2, 100, 2, "{1,2}", "U16")
    assert robot.motion.start_path("path.csv", is_const=1, multi=2.0) == 43
    with pytest.raises(NotSupportedError, match="cart option"):
        robot.motion.start_path("path.csv", cart=1)
