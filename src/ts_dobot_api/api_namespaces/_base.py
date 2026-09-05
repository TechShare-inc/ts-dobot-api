"""Base class for unified robot API namespaces."""

from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

_T_Native = TypeVar("_T_Native")


class RobotNamespace(ABC, Generic[_T_Native]):
    """Base class for functional namespaces on a robot."""

    def __init__(self, native: _T_Native) -> None:
        self.native = native
