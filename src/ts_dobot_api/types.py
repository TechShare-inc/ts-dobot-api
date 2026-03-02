"""Unified types that the wrapper exposes to callers.

These are **version-agnostic**: adapters translate V3/V4 native types into
these before returning them to user code.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

# ---------------------------------------------------------------------------
# Pose – always a dataclass, even though V3 uses plain tuples internally.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Pose:
    """Six-DOF pose (Cartesian or joint angles)."""

    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    # Convenience: unpack as a tuple.
    def as_tuple(self) -> tuple[float, float, float, float, float, float]:
        return (self.x, self.y, self.z, self.rx, self.ry, self.rz)

    def __iter__(self) -> Iterator[float]:
        return iter(self.as_tuple())


# ---------------------------------------------------------------------------
# FeedbackData – thin re-export placeholder.  The actual data structure is
# version-specific and quite large (~70 fields).  We re-export whichever
# the active adapter provides under this alias.
# ---------------------------------------------------------------------------
# The concrete FeedbackData from either SDK is compatible: both are frozen
# dataclasses with ``from_numpy`` classmethod.  We intentionally do NOT
# merge them into a single schema – the adapters return the native object
# and we type-alias it here for documentation purposes.

if TYPE_CHECKING:
    from dobot_api_v3 import FeedbackData as V3FeedbackData
    from dobot_api_v4 import FeedbackData as V4FeedbackData

FeedbackData: TypeAlias = "V3FeedbackData | V4FeedbackData"


# ---------------------------------------------------------------------------
# Alarm / error info
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AlarmInfo:
    """A single robot alarm entry."""

    error_id: int
    description: str = ""
    level: str | None = None
