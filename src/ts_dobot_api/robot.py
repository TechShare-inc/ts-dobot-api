"""Unified robot facade - the main user-facing entry point.

Example::

    from ts_dobot_api import DobotRobot

    with DobotRobot.connect("192.168.1.6", model="CR5") as robot:
        robot.startup(speed=40)
        pose = robot.get_pose()
        robot.mov_j(200, 0, 200, 0, 0, 0)
        robot.sync()
        robot.shutdown()

    # V4-only methods — access via the ``.native`` escape hatch:
    with DobotRobot.connect("192.168.1.6", model="CR5") as robot:
        robot.startup()
        robot.native.dashboard.enable_ft_sensor(1)
        force = robot.native.dashboard.get_force()
        robot.native.dashboard.fc_off()
        robot.shutdown()
"""

from typing import Generic, TypeVar

from loguru import logger

from .models import ApiVersion, RobotFamily

_T_Native = TypeVar("_T_Native")


class DobotRobot(Generic[_T_Native]):
    """Base class for all Dobot robots.

    Use the :meth:`connect` class-method to create an instance — it
    automatically selects the correct subclass (``DobotRobotV3`` or
    ``DobotRobotV4``) based on the *model* string.

    Args:
        ip: Robot controller IP address.
        model: Robot model string (e.g. ``"CR5"``, ``"Nova2s"``, ``"Nova"``).
        language: Default language for alarm messages.
    """

    _api_version: ApiVersion  # set by subclass
    _native: _T_Native

    def __init__(self, ip: str, model: str, *, language: str = "en") -> None:
        self._ip = ip
        self._model = model
        self._language = language
        self._family: RobotFamily = RobotFamily.from_model(model)

    @classmethod
    def connect(
        cls, ip: str, model: str, *, language: str = "en"
    ) -> "DobotRobot[object]":
        """Factory: create, connect, and return the correct subclass.

        Args:
            ip: Robot controller IP address.
            model: Robot model string (e.g. ``"CR5"``, ``"Nova"``).
            language: Default language for alarm messages.

        Returns:
            A connected ``DobotRobotV3`` or ``DobotRobotV4`` instance.
        """
        family = RobotFamily.from_model(model)
        version = family.api_version

        robot: DobotRobot[object]
        if version is ApiVersion.V3:
            from .v3 import DobotRobotV3

            robot = DobotRobotV3(ip, model, language=language)  # type: ignore[assignment]
        elif version is ApiVersion.V4:
            from .v4 import DobotRobotV4

            robot = DobotRobotV4(ip, model, language=language)  # type: ignore[assignment]
        else:
            raise ValueError(f"Unsupported API version: {version!r}")

        logger.info(
            f"DobotRobot connected: model={model!r}, family={family.display_name}, api={version.value}, ip={ip}"
        )
        return robot

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def ip(self) -> str:
        """Robot controller IP address."""
        return self._ip

    @property
    def model(self) -> str:
        """Robot model string as provided by the user."""
        return self._model

    @property
    def family(self) -> RobotFamily:
        """Resolved robot family."""
        return self._family

    @property
    def api_version(self) -> ApiVersion:
        """Resolved API version."""
        return self._api_version

    @property
    def native(self) -> _T_Native:
        """Access the underlying SDK's ``DobotRobot`` object directly.

        Useful when you need a method that isn't exposed by the wrapper.
        """
        return self._native

    # ------------------------------------------------------------------
    # Lifecycle (implemented by subclasses)
    # ------------------------------------------------------------------

    def disconnect(self) -> None:
        """Close all TCP connections (implemented by subclass)."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "DobotRobot[_T_Native]":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.disconnect()

    # ------------------------------------------------------------------
    # repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"DobotRobot(ip={self._ip!r}, model={self._model!r}, "
            f"family={self._family.display_name!r}, api={self._api_version.value!r})"
        )
