"""Shared helpers for V4 namespace implementations."""

from __future__ import annotations

from dobot_api_v4 import Pose as V4Pose

from ..types import Pose


def _opt(val: int | None) -> int:
    """Convert ``None`` to ``-1`` for optional V4 API parameters."""
    return val if val is not None else -1


def _pose_from_v4(v4_pose: V4Pose) -> Pose:
    """Convert a V4 ``dobot_api_v4.Pose`` to our unified :class:`Pose`."""
    return Pose(
        x=v4_pose.x,
        y=v4_pose.y,
        z=v4_pose.z,
        rx=v4_pose.rx,
        ry=v4_pose.ry,
        rz=v4_pose.rz,
    )
