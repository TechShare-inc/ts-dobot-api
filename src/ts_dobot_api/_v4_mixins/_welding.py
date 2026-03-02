"""V4 welding mixin — arc tracking, weaving, and weld-speed control."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class V4WeldingMixin:
    """Welding methods available only on V4 robots."""

    _native: V4Robot

    def arc_track_start(self) -> None:
        """Start arc tracking."""
        self._native.dashboard.arc_track_start()

    def arc_track_params(
        self,
        sample_time: int,
        coordinate_type: int,
        up_down_compensation_min: float,
        up_down_compensation_max: float,
        up_down_compensation_offset: float,
        left_right_compensation_min: float,
        left_right_compensation_max: float,
        left_right_compensation_offset: float,
    ) -> None:
        """Configure arc-tracking parameters."""
        self._native.dashboard.arc_track_params(
            sample_time,
            coordinate_type,
            up_down_compensation_min,
            up_down_compensation_max,
            up_down_compensation_offset,
            left_right_compensation_min,
            left_right_compensation_max,
            left_right_compensation_offset,
        )

    def arc_track_end(self) -> None:
        """End arc tracking."""
        self._native.dashboard.arc_track_end()

    def set_arc_track_offset(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
    ) -> None:
        """Set arc-tracking offset."""
        self._native.dashboard.set_arc_track_offset(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
        )

    def rel_point_weld_line(
        self,
        start_x: float,
        end_x: float,
        y: float,
        z: float,
        work_angle: float,
        travel_angle: float,
        p1: Sequence[float],
        p2: Sequence[float],
    ) -> int:
        """Linear weld relative to reference points."""
        return self._native.dashboard.rel_point_weld_line(
            start_x,
            end_x,
            y,
            z,
            work_angle,
            travel_angle,
            p1,
            p2,
        )

    def rel_point_weld_arc(
        self,
        start_x: float,
        end_x: float,
        y: float,
        z: float,
        work_angle: float,
        travel_angle: float,
        p1: Sequence[float],
        p2: Sequence[float],
        p3: Sequence[float],
    ) -> int:
        """Arc weld relative to reference points."""
        return self._native.dashboard.rel_point_weld_arc(
            start_x,
            end_x,
            y,
            z,
            work_angle,
            travel_angle,
            p1,
            p2,
            p3,
        )

    def weave_start(self) -> None:
        """Start weaving pattern."""
        self._native.dashboard.weave_start()

    def weave_params(
        self,
        weld_type: int,
        frequency: float,
        left_amplitude: float,
        right_amplitude: float,
        direction: int,
        stop_mode: int,
        stop_time1: int,
        stop_time2: int,
        stop_time3: int,
        stop_time4: int,
        radius: float,
        radian: float,
        **kwargs: int | float,
    ) -> None:
        """Configure weaving parameters."""
        self._native.dashboard.weave_params(
            weld_type,
            frequency,
            left_amplitude,
            right_amplitude,
            direction,
            stop_mode,
            stop_time1,
            stop_time2,
            stop_time3,
            stop_time4,
            radius,
            radian,
            **kwargs,
        )

    def weave_end(self) -> None:
        """End weaving pattern."""
        self._native.dashboard.weave_end()

    def weld_arc_speed_start(self) -> None:
        """Start weld arc speed section."""
        self._native.dashboard.weld_arc_speed_start()

    def weld_arc_speed(self, speed: float) -> None:
        """Set weld arc speed."""
        self._native.dashboard.weld_arc_speed(speed)

    def weld_arc_speed_end(self) -> None:
        """End weld arc speed section."""
        self._native.dashboard.weld_arc_speed_end()
