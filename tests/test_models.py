"""Tests for the model registry."""

import pytest

from ts_dobot_api.models import ApiVersion, RobotFamily, resolve_api_version


class TestRobotFamily:
    """Tests for RobotFamily enum and from_model resolution."""

    @pytest.mark.parametrize(
        "model, expected_family, expected_version",
        [
            ("CR3", RobotFamily.CR, ApiVersion.V4),
            ("CR5", RobotFamily.CR, ApiVersion.V4),
            ("CR10", RobotFamily.CR, ApiVersion.V4),
            ("CR16", RobotFamily.CR, ApiVersion.V4),
            ("cr5", RobotFamily.CR, ApiVersion.V4),
            ("Nova", RobotFamily.NOVA, ApiVersion.V3),
            ("NOVA", RobotFamily.NOVA, ApiVersion.V3),
            ("Nova2s", RobotFamily.NOVA_2S, ApiVersion.V4),
            ("nova 2s", RobotFamily.NOVA_2S, ApiVersion.V4),
            ("Nova NG", RobotFamily.NOVA_NG, ApiVersion.V4),
            ("NovaNG", RobotFamily.NOVA_NG, ApiVersion.V4),
            ("novang5", RobotFamily.NOVA_NG, ApiVersion.V4),
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

    def test_resolve_api_version_shortcut(self) -> None:
        assert resolve_api_version("CR5") is ApiVersion.V4
        assert resolve_api_version("Nova") is ApiVersion.V3
