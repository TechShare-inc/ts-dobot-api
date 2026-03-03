"""Robot model registry - maps model names to API versions."""

from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class ApiVersion(Enum):
    """Dobot TCP-IP protocol version."""

    V3 = "v3"
    V4 = "v4"


# -- Robot family metadata -------------------------------------------------


class _FamilyMeta(NamedTuple):
    """Metadata attached to each :class:`RobotFamily` member."""

    display_name: str
    api_version: ApiVersion


_FAMILY_META: dict[str, _FamilyMeta] = {
    "CR": _FamilyMeta("CR Series", ApiVersion.V4),
    "NOVA": _FamilyMeta("Nova Series", ApiVersion.V3),
    "NOVA_2S": _FamilyMeta("Nova 2s", ApiVersion.V4),
    "NOVA_NG": _FamilyMeta("Nova NG Series", ApiVersion.V4),
}


# -- Robot family enum -----------------------------------------------------


class RobotFamily(Enum):
    """Known Dobot robot families.

    Each member maps to a specific set of Dobot products and the protocol
    version (V3 or V4) used to communicate with them.

    Product mapping:

    ============  ============================  =========
    Member        Products                      Protocol
    ============  ============================  =========
    ``CR``        CR3, CR5, CR10, CR16           V4
    ``NOVA``      Nova 2, Nova 5                 V3
    ``NOVA_2S``   Nova 2s                        V4
    ``NOVA_NG``   Nova 5 NG, Nova 2 NG           V4
    ============  ============================  =========
    """

    CR = "CR"
    NOVA = "NOVA"
    NOVA_2S = "NOVA_2S"
    NOVA_NG = "NOVA_NG"

    # -- derived properties from _FAMILY_META ----------------------------

    @property
    def display_name(self) -> str:
        """Human-readable family name."""
        return _FAMILY_META[self.value].display_name

    @property
    def api_version(self) -> ApiVersion:
        """Protocol version used by this family."""
        return _FAMILY_META[self.value].api_version

    @classmethod
    def from_model(cls, model: str) -> RobotFamily:
        """Resolve a model string to a :class:`RobotFamily`.

        Only the canonical family names are accepted (case-insensitive):
        ``"CR"``, ``"NOVA"``, ``"NOVA_2S"``, ``"NOVA_NG"``.

        Raises:
            ValueError: If *model* is not a known family name.
        """
        normalised = model.strip().upper()
        try:
            return cls(normalised)
        except ValueError:
            known = ", ".join(f'"{m.value}"' for m in cls)
            raise ValueError(
                f"Unknown robot model {model!r}. Expected one of: {known}"
            ) from None


def resolve_api_version(model: str) -> ApiVersion:
    """Convenience: resolve *model* directly to an :class:`ApiVersion`."""
    return RobotFamily.from_model(model).api_version
