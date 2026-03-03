"""Tests for the model registry."""

import pytest

from ts_dobot_api.models import ApiVersion, RobotFamily, resolve_api_version


class TestRobotFamily:
    """Tests for RobotFamily enum and from_model resolution."""

    @pytest.mark.parametrize(
        "model, expected_family, expected_version",
        [
            ("CR", RobotFamily.CR, ApiVersion.V4),
            ("cr", RobotFamily.CR, ApiVersion.V4),
            ("NOVA", RobotFamily.NOVA, ApiVersion.V3),
            ("nova", RobotFamily.NOVA, ApiVersion.V3),
            ("NOVA_2S", RobotFamily.NOVA_2S, ApiVersion.V4),
            ("nova_2s", RobotFamily.NOVA_2S, ApiVersion.V4),
            ("NOVA_NG", RobotFamily.NOVA_NG, ApiVersion.V4),
            ("nova_ng", RobotFamily.NOVA_NG, ApiVersion.V4),
        ],
    )
    def test_from_model(
        self, model: str, expected_family: RobotFamily, expected_version: ApiVersion
    ) -> None:
        family = RobotFamily.from_model(model)
        assert family is expected_family
        assert family.api_version is expected_version

    def test_unknown_model_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown robot model"):
            RobotFamily.from_model("UnknownBot9000")

    def test_old_aliases_no_longer_work(self) -> None:
        """Free-form aliases (e.g. 'Nova 2s', 'novang') are no longer accepted."""
        for alias in ["Nova 2s", "novang", "Nova NG", "CR5"]:
            with pytest.raises(ValueError, match="Unknown robot model"):
                RobotFamily.from_model(alias)

    def test_resolve_api_version_shortcut(self) -> None:
        assert resolve_api_version("CR") is ApiVersion.V4
        assert resolve_api_version("Nova") is ApiVersion.V3
