"""Unified types that the wrapper exposes to callers.

These are **version-agnostic**: adapters translate V3/V4 native types into
these before returning them to user code.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from math import radians
from typing import Any, Protocol

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


class _NativeFeedback(Protocol):
    """Fields shared by the pinned V3 and V4 feedback packets."""

    @property
    def test_value(self) -> int: ...

    @property
    def q_actual(self) -> Sequence[float]: ...

    @property
    def qd_actual(self) -> Sequence[float]: ...

    @property
    def m_actual(self) -> Sequence[float]: ...


@dataclass(frozen=True, slots=True)
class FeedbackData:
    """Protocol-neutral feedback values in radians and radians per second.

    Fields not normalized by this facade remain available through ``native``.
    """

    test_value: int
    q_actual: tuple[float, ...]
    qd_actual: tuple[float, ...]
    m_actual: tuple[float, ...]
    native: object

    @classmethod
    def from_native(cls, native: _NativeFeedback, *, angular_values_in_degrees: bool) -> FeedbackData:
        """Normalize the common joint fields from a vendor feedback packet."""
        convert = radians if angular_values_in_degrees else float
        return cls(
            test_value=int(native.test_value),
            q_actual=tuple(convert(value) for value in native.q_actual),
            qd_actual=tuple(convert(value) for value in native.qd_actual),
            m_actual=tuple(float(value) for value in native.m_actual),
            native=native,
        )

    def __getattr__(self, name: str) -> Any:
        """Expose protocol-specific fields from the original packet."""
        return getattr(self.native, name)


# ---------------------------------------------------------------------------
# Alarm / error info
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AlarmInfo:
    """A single robot alarm entry."""

    error_id: int
    description: str = ""
    level: str | None = None
