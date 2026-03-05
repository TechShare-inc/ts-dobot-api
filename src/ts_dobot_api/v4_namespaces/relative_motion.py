"""Concrete RelativeMotion namespace for V4 API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..api_namespaces import RelativeMotion
from ._utils import _opt

if TYPE_CHECKING:
    from dobot_api_v4 import DobotRobot as V4Robot


class RelativeMotionV4(RelativeMotion):
    """Concrete RelativeMotion implementation for V4 API."""

    native: V4Robot

    def rel_joint_mov_j(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        *,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        """Relative move with joint offsets."""
        return self.native.dashboard.rel_joint_mov_j(
            j1,
            j2,
            j3,
            j4,
            j5,
            j6,
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_j_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        tool: int | None = None,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        """Relative joint move in tool coordinate system."""
        return self.native.dashboard.rel_mov_j_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_j_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        """Relative joint move in user coordinate system."""
        return self.native.dashboard.rel_mov_j_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_l_tool(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        tool: int | None = None,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        """Relative linear move in tool coordinate system."""
        return self.native.dashboard.rel_mov_l_tool(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            tool=_opt(tool),
            a=_opt(accel),
            v=_opt(speed),
        )

    def rel_mov_l_user(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
        *,
        user: int | None = None,
        speed: int | None = None,
        accel: int | None = None,
    ) -> int:
        """Relative linear move in user coordinate system."""
        return self.native.dashboard.rel_mov_l_user(
            offset_x,
            offset_y,
            offset_z,
            offset_rx,
            offset_ry,
            offset_rz,
            user=_opt(user),
            a=_opt(accel),
            v=_opt(speed),
        )
