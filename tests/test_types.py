"""Tests for the Pose type."""

from ts_dobot_api.types import Pose


def test_pose_creation() -> None:
    p = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
    assert p.x == 1.0
    assert p.y == 2.0
    assert p.z == 3.0
    assert p.rx == 4.0
    assert p.ry == 5.0
    assert p.rz == 6.0


def test_pose_as_tuple() -> None:
    p = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
    assert p.as_tuple() == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)


def test_pose_iterable() -> None:
    p = Pose(x=10.0, y=20.0, z=30.0, rx=40.0, ry=50.0, rz=60.0)
    assert list(p) == [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]


def test_pose_is_frozen() -> None:
    import pytest

    p = Pose(x=1.0, y=2.0, z=3.0, rx=4.0, ry=5.0, rz=6.0)
    with pytest.raises(AttributeError):
        p.x = 99.0  # type: ignore[misc]
