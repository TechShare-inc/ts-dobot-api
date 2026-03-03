"""Tests for custom exceptions."""

import pytest

from ts_dobot_api.exceptions import (
    ConnectionError,
    NotSupportedError,
    StartupError,
    TsDobotError,
)

# ── Hierarchy ─────────────────────────────────────────────────────────────


class TestExceptionHierarchy:
    """All custom exceptions inherit from TsDobotError → Exception."""

    def test_base_is_exception(self) -> None:
        assert issubclass(TsDobotError, Exception)

    @pytest.mark.parametrize(
        "exc_cls",
        [NotSupportedError, ConnectionError, StartupError],
    )
    def test_subclass_of_base(self, exc_cls: type) -> None:
        assert issubclass(exc_cls, TsDobotError)

    @pytest.mark.parametrize(
        "exc_cls",
        [NotSupportedError, ConnectionError, StartupError],
    )
    def test_subclass_of_exception(self, exc_cls: type) -> None:
        assert issubclass(exc_cls, Exception)


# ── Raise / Catch ─────────────────────────────────────────────────────────


class TestRaiseCatch:
    """Each exception can be raised and caught as TsDobotError."""

    @pytest.mark.parametrize(
        "exc_cls",
        [TsDobotError, NotSupportedError, ConnectionError, StartupError],
    )
    def test_raise_and_catch_as_base(self, exc_cls: type) -> None:
        with pytest.raises(TsDobotError):
            raise exc_cls("test message")

    @pytest.mark.parametrize(
        "exc_cls",
        [TsDobotError, NotSupportedError, ConnectionError, StartupError],
    )
    def test_message_preserved(self, exc_cls: type) -> None:
        err = exc_cls("something went wrong")
        assert str(err) == "something went wrong"

    def test_catch_specific_type(self) -> None:
        with pytest.raises(NotSupportedError):
            raise NotSupportedError("v3 only")

        with pytest.raises(ConnectionError):
            raise ConnectionError("timeout")

        with pytest.raises(StartupError):
            raise StartupError("enable failed")

    def test_no_args(self) -> None:
        """Exceptions can be instantiated without a message."""
        for exc_cls in (TsDobotError, NotSupportedError, ConnectionError, StartupError):
            err = exc_cls()
            assert str(err) == ""
