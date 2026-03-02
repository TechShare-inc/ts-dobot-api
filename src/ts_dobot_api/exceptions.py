"""Custom exceptions for the ts-dobot-api wrapper."""

from __future__ import annotations


class TsDobotError(Exception):
    """Base exception for all ts-dobot-api errors."""


class NotSupportedError(TsDobotError):
    """Raised when an operation is not supported by the robot's API version.

    For example, calling force-control methods on a V3 (Nova) robot.
    """


class ConnectionError(TsDobotError):  # noqa: A001
    """Raised when the wrapper cannot establish or maintain a connection."""


class StartupError(TsDobotError):
    """Raised when the robot startup sequence fails."""
