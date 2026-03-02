"""V4 conveyor-tracking mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class V4ConveyorMixin:
    """Conveyor-tracking methods available only on V4 robots."""

    _native: V4Robot

    def cnv_init(self, index: int) -> None:
        """Initialise a conveyor belt."""
        self._native.dashboard.cnv_init(index)

    def cnv_mov_l(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> int:
        """Linear conveyor-tracking move."""
        return self._native.dashboard.cnv_mov_l(
            j1,
            j2,
            j3,
            j4,
            j5,
            j6,
            user=user,
            tool=tool,
            a=a,
            v=v,
            cp=cp,
            r=r,
        )

    def cnv_mov_c(
        self,
        j1a: float,
        j2a: float,
        j3a: float,
        j4a: float,
        j5a: float,
        j6a: float,
        j1b: float,
        j2b: float,
        j3b: float,
        j4b: float,
        j5b: float,
        j6b: float,
        *,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
        r: int = -1,
        mode: int = 1,
    ) -> int:
        """Circular conveyor-tracking move."""
        return self._native.dashboard.cnv_mov_c(
            j1a,
            j2a,
            j3a,
            j4a,
            j5a,
            j6a,
            j1b,
            j2b,
            j3b,
            j4b,
            j5b,
            j6b,
            user=user,
            tool=tool,
            a=a,
            v=v,
            cp=cp,
            r=r,
            mode=mode,
        )

    def get_cnv_object(self, obj_id: int) -> str:
        """Query the position of a conveyor object."""
        return self._native.dashboard.get_cnv_object(obj_id)

    def set_cnv_point_offset(self, x_offset: float, y_offset: float) -> None:
        """Set conveyor point offset."""
        self._native.dashboard.set_cnv_point_offset(x_offset, y_offset)

    def set_cnv_time_compensation(self, time: int) -> None:
        """Set conveyor time compensation value."""
        self._native.dashboard.set_cnv_time_compensation(time)

    def start_sync_cnv(self) -> None:
        """Start conveyor synchronisation."""
        self._native.dashboard.start_sync_cnv()

    def stop_sync_cnv(self) -> None:
        """Stop conveyor synchronisation."""
        self._native.dashboard.stop_sync_cnv()
