"""Shared helpers for V3 namespace implementations."""

from __future__ import annotations

from ..types import Pose


def _pose_from_tuple(t: tuple[float, ...]) -> Pose:
    """Convert a V3 Pose (plain tuple) to our unified :class:`Pose`."""
    return Pose(x=t[0], y=t[1], z=t[2], rx=t[3], ry=t[4], rz=t[5])


def _build_dyn_params(
    *,
    speed_j: int | None = None,
    speed_l: int | None = None,
    accel_j: int | None = None,
    accel_l: int | None = None,
    speed: int | None = None,
    accel: int | None = None,
    cp: int | None = None,
    user: int | None = None,
    tool: int | None = None,
) -> list[str]:
    """Build a list of V3-style DynParam strings from keyword arguments."""
    params: list[str] = []
    if speed_j is not None:
        params.append(f"SpeedJ={speed_j}")
    if speed_l is not None:
        params.append(f"SpeedL={speed_l}")
    if accel_j is not None:
        params.append(f"AccJ={accel_j}")
    if accel_l is not None:
        params.append(f"AccL={accel_l}")
    if speed is not None:
        params.append(f"SpeedJ={speed}")
    if accel is not None:
        params.append(f"AccJ={accel}")
    if cp is not None:
        params.append(f"CP={cp}")
    if user is not None:
        params.append(f"User={user}")
    if tool is not None:
        params.append(f"Tool={tool}")
    return params
