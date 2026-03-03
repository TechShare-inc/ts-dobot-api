"""Tests for the unified types (Pose and AlarmInfo)."""

import pytest

from ts_dobot_api.types import AlarmInfo, Pose

# ── Pose ──────────────────────────────────────────────────────────────────


class TestPose:
    """Tests for the Pose frozen dataclass."""

    def test_creation(self) -> None:
        p = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        assert p.x == 1.0
        assert p.y == 2.0
        assert p.z == 3.0
        assert p.rx == 4.0
        assert p.ry == 5.0
        assert p.rz == 6.0

    def test_as_tuple(self) -> None:
        p = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        assert p.as_tuple() == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

    def test_iterable(self) -> None:
        p = Pose(x=10.0, y=20.0, z=30.0, rx=40.0, ry=50.0, rz=60.0)
        assert list(p) == [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]

    def test_frozen(self) -> None:
        p = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        with pytest.raises(AttributeError):
            p.x = 99.0  # type: ignore[misc]

    def test_equality(self) -> None:
        a = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        b = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        assert a == b

    def test_inequality(self) -> None:
        a = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        b = Pose(x=9.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
        assert a != b


# ── AlarmInfo ─────────────────────────────────────────────────────────────


class TestAlarmInfo:
    """Tests for the AlarmInfo frozen dataclass."""

    def test_creation_defaults(self) -> None:
        a = AlarmInfo(error_id=42)
        assert a.error_id == 42
        assert a.description == ""
        assert a.level is None

    def test_creation_all_fields(self) -> None:
        a = AlarmInfo(error_id=1, description="motor fault", level="warning")
        assert a.error_id == 1
        assert a.description == "motor fault"
        assert a.level == "warning"

    def test_frozen(self) -> None:
        a = AlarmInfo(error_id=7)
        with pytest.raises(AttributeError):
            a.error_id = 99  # type: ignore[misc]

    def test_equality(self) -> None:
        a = AlarmInfo(error_id=1, description="x", level="error")
        b = AlarmInfo(error_id=1, description="x", level="error")
        assert a == b

    def test_inequality(self) -> None:
        a = AlarmInfo(error_id=1)
        b = AlarmInfo(error_id=2)
        assert a != b
