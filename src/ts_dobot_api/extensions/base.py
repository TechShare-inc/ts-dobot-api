"""Base machinery for V4-only extension namespaces."""

from __future__ import annotations

from typing import Any

from ..exceptions import NotSupportedError
from ..models import ApiVersion


class ExtensionNamespace:
    """Base class for V4-only feature extensions.

    On a V4 robot, attribute access is proxied to the underlying
    ``DobotApiDashboard``.  On a V3 robot, any attribute access raises
    :class:`NotSupportedError`.
    """

    _feature_name: str = "this feature"
    _dashboard: Any
    _api_version: ApiVersion

    def __init__(self, dashboard: Any | None, api_version: ApiVersion) -> None:
        object.__setattr__(self, "_dashboard", dashboard)
        object.__setattr__(self, "_api_version", api_version)

    def _require_v4(self) -> Any:
        if self._api_version is not ApiVersion.V4 or self._dashboard is None:
            raise NotSupportedError(
                f"{self._feature_name} requires a V4 robot (CR / Nova 2s / Nova NG). "
                f"Current API version: {self._api_version.value}"
            )
        return self._dashboard
