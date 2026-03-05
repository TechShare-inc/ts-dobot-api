"""Unified robot facade - the main user-facing entry point."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from loguru import logger

from .models import ApiVersion, RobotFamily

if TYPE_CHECKING:
    from .api_namespaces import (
        Config,
        Conveyor,
        ErrorHandling,
        Feedback,
        ForceControl,
        Io,
        Lifecycle,
        Modbus,
        Motion,
        Query,
        Raw,
        RelativeMotion,
        System,
        Welding,
    )

_T_Native = TypeVar("_T_Native")


class DobotRobot(Generic[_T_Native]):
    """Base class for all Dobot robots."""

    _api_version: ApiVersion
    _native: _T_Native

    # Namespaces
    lifecycle: Lifecycle
    system: System
    motion: Motion
    relative_motion: RelativeMotion
    config: Config
    query: Query
    io: Io
    feedback: Feedback
    error_handling: ErrorHandling
    force_control: ForceControl
    modbus: Modbus
    welding: Welding
    conveyor: Conveyor
    raw: Raw

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        self._ip = ip
        self._model = model
        self._language = language
        self._family: RobotFamily = RobotFamily.from_model(model)

    @classmethod
    def connect(cls, ip: str, model: str, *, language: str = "en") -> DobotRobot[object]:
        family = RobotFamily.from_model(model)
        version = family.api_version

        robot: DobotRobot[object]
        if version is ApiVersion.V3:
            from .v3 import DobotRobotV3

            robot = DobotRobotV3(ip, model, language=language)  # type: ignore
        elif version is ApiVersion.V4:
            from .v4 import DobotRobotV4

            robot = DobotRobotV4(ip, model, language=language)  # type: ignore
        else:
            raise ValueError(f"Unsupported API: {version}")

        logger.info(f"Connected: {model}")
        return robot

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def model(self) -> str:
        return self._model

    @property
    def family(self) -> RobotFamily:
        return self._family

    @property
    def api_version(self) -> ApiVersion:
        return self._api_version

    @property
    def native(self) -> _T_Native:
        return self._native

    def __enter__(self) -> DobotRobot[_T_Native]:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.lifecycle.disconnect()
