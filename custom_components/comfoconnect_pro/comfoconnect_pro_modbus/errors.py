"""The errors the library raises itself."""

from __future__ import annotations

from .enums import ConnectionState


class ComfoConnectProError(Exception):
    """The base of every error this library raises itself."""


class InvalidValueError(ComfoConnectProError, ValueError):
    """A value or argument is outside what the library accepts.

    A write that raises it sends nothing.
    """


class NoVentilationUnitError(ComfoConnectProError):
    """The gateway answered, but it does not reach a ventilation unit it serves."""

    def __init__(
        self,
        state: ConnectionState | None,
        *,
        code: int | None = None,
        unreachable: bool = False,
    ) -> None:
        """Initialize the error.

        Pass the raw ``code`` for a state the manual does not list, and
        ``unreachable`` when the gateway refused a read for lack of a path to
        the unit.
        """
        if state is not None:
            code = state.value
        if unreachable and state is ConnectionState.OK:
            message = (
                "the gateway reported connection state OK, then lost its path "
                "to the ventilation unit"
            )
        elif unreachable:
            message = "the gateway has no path to the ventilation unit"
        elif state is not None:
            message = (
                f"the gateway's connection state is {state.value} ({state.name}), "
                "not 0 (OK)"
            )
        elif code is not None:
            message = f"the gateway's connection state is {code} (unknown), not 0 (OK)"
        else:
            message = "the gateway reported no connection state"
        super().__init__(message)
        self.state = state
        self.code = code
