"""Adapters package — version-specific implementations of :class:`DobotProtocol`."""

from __future__ import annotations

from ..models import ApiVersion
from ..protocol import DobotProtocol


def create_adapter(
    api_version: ApiVersion, ip: str, *, language: str = "en"
) -> DobotProtocol:
    """Factory: instantiate the correct adapter for *api_version*.

    The adapter is returned in a **disconnected** state — call
    :meth:`~DobotProtocol.connect` to open TCP sockets.
    """
    if api_version is ApiVersion.V3:
        from .v3_adapter import V3Adapter

        return V3Adapter(ip, language=language)

    if api_version is ApiVersion.V4:
        from .v4_adapter import V4Adapter

        return V4Adapter(ip, language=language)

    raise ValueError(f"Unsupported API version: {api_version!r}")
