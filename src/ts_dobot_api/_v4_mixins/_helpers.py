"""Shared helpers for V4 mixin modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Pose

if TYPE_CHECKING:
    from dobot_api_v4 import Pose as V4Pose


def _pose_from_v4(p: V4Pose) -> Pose:
    """Convert a V4 ``Pose`` dataclass to our unified Pose."""
    return Pose(x=p.x, y=p.y, z=p.z, rx=p.rx, ry=p.ry, rz=p.rz)


def _opt(value: int | None, default: int = -1) -> int:
    """Convert ``None`` → V4's sentinel default (``-1``)."""
    return default if value is None else value
