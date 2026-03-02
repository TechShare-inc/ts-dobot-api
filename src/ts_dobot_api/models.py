"""Robot model registry – maps model names to API versions."""

from __future__ import annotations

from enum import Enum


class ApiVersion(Enum):
    """Dobot TCP-IP protocol version."""

    V3 = "v3"
    V4 = "v4"


# -- Robot family metadata (kept outside the Enum to avoid metaclass issues) --
_FAMILY_META: dict[str, tuple[str, ApiVersion, tuple[str, ...]]] = {
    "CR": ("CR Series", ApiVersion.V4, ("cr",)),
    "NOVA": ("Nova Series", ApiVersion.V3, ("nova",)),
    "NOVA_2S": ("Nova 2s", ApiVersion.V4, ("nova 2s", "nova2s")),
    "NOVA_NG": ("Nova NG Series", ApiVersion.V4, ("nova ng", "novang")),
}

# Module-level registry cache (ClassVar inside Enum is broken in Python <3.11).
_family_registry: list[tuple[str, RobotFamily]] | None = None


class RobotFamily(Enum):
    """Known Dobot robot families."""

    CR = "CR"
    NOVA = "NOVA"
    NOVA_2S = "NOVA_2S"
    NOVA_NG = "NOVA_NG"

    # -- derived properties from _FAMILY_META ----------------------------

    @property
    def display_name(self) -> str:
        return _FAMILY_META[self.value][0]

    @property
    def api_version(self) -> ApiVersion:
        return _FAMILY_META[self.value][1]

    @property
    def _match_prefixes(self) -> tuple[str, ...]:
        return _FAMILY_META[self.value][2]

    @classmethod
    def _build_registry(cls) -> list[tuple[str, RobotFamily]]:
        """Return a list of ``(prefix, family)`` pairs sorted longest-first."""
        pairs: list[tuple[str, RobotFamily]] = []
        for member in cls:
            for prefix in member._match_prefixes:
                pairs.append((prefix.lower(), member))
        # Longest prefix first so "nova 2s" matches before "nova".
        pairs.sort(key=lambda p: len(p[0]), reverse=True)
        return pairs

    @classmethod
    def from_model(cls, model: str) -> RobotFamily:
        """Resolve a free-form model string to a :class:`RobotFamily`.

        Matching is case-insensitive and prefix-based.  For example
        ``"CR5"`` matches :attr:`CR`, ``"Nova2s"`` matches :attr:`NOVA_2S`.

        Raises:
            ValueError: If no family matches *model*.
        """
        global _family_registry  # noqa: PLW0603
        if _family_registry is None:
            _family_registry = cls._build_registry()
        normalised = model.strip().lower()
        for prefix, family in _family_registry:
            if normalised.startswith(prefix):
                return family
        known = ", ".join(f'"{m.display_name}"' for m in cls)
        raise ValueError(f"Unknown robot model {model!r}. Known families: {known}")


def resolve_api_version(model: str) -> ApiVersion:
    """Convenience: resolve *model* directly to an :class:`ApiVersion`."""
    return RobotFamily.from_model(model).api_version
