"""The gateway's link state, the unit's alarms and its status flags."""

from __future__ import annotations

from modbus_connection.model import NumberField, discrete_input, integer

from .enums import AlarmCode, ConnectionState
from .errors import InvalidValueError
from .model import ComfoConnectComponent, address

ALARM_SLOTS = 5


def _alarm(code: int) -> AlarmCode | int:
    """The ``AlarmCode`` for ``code``, or the bare number for a code it lacks."""
    try:
        return AlarmCode(code)
    except ValueError:
        return code


def _alarm_slot(slot: int) -> NumberField[AlarmCode | int]:
    """The field of alarm slot ``slot``, input register 0x0002 onwards."""
    return NumberField(address(0x0001 + slot), signed=False, convert=_alarm)


class ConnectionStatus(ComfoConnectComponent):
    """Input register 0x0001 alone, which the gateway serves without a unit."""

    register_space = "input"

    connection_code = integer(address(0x0001), signed=False)
    """The raw connection state, which may be a code the manual does not list."""

    @property
    def connection_state(self) -> ConnectionState | None:
        """The connection state, or ``None`` before a read or for an unlisted code."""
        try:
            code = self.connection_code
            return None if code is None else ConnectionState(code)
        except ValueError:
            return None

    @property
    def is_connected(self) -> bool:
        """Whether the gateway reaches a ventilation unit it can serve."""
        return self.connection_state is ConnectionState.OK


class Status(ConnectionStatus):
    """Input registers 0x0001 to 0x0006 and discrete inputs 0x0001 to 0x0004."""

    active_error_1 = _alarm_slot(1)
    """The first active alarm, or 0."""
    active_error_2 = _alarm_slot(2)
    active_error_3 = _alarm_slot(3)
    active_error_4 = _alarm_slot(4)
    active_error_5 = _alarm_slot(5)

    error_flag = discrete_input(address(0x0001))
    """At least one alarm is active."""
    standby = discrete_input(address(0x0002))
    comfohood = discrete_input(address(0x0003))
    """The ComfoHood cooker hood is on."""
    filter_dirty = discrete_input(address(0x0004))
    """The filters must be replaced."""

    def active_error(self, slot: int) -> AlarmCode | int | None:
        """Alarm slot ``slot``, from 1 to 5.

        Returns 0 for an empty slot and ``None`` before the first read.
        """
        if isinstance(slot, bool) or not isinstance(slot, int):
            raise InvalidValueError(f"alarm slot {slot!r} is not an int")
        if not 1 <= slot <= ALARM_SLOTS:
            raise InvalidValueError(f"no alarm slot {slot}")
        code: AlarmCode | int | None = getattr(self, f"active_error_{slot}")
        return code

    @property
    def active_alarms(self) -> tuple[AlarmCode | int, ...]:
        """The alarms in the five slots, without the empty ones."""
        codes = (self.active_error(slot) for slot in range(1, ALARM_SLOTS + 1))
        return tuple(code for code in codes if code)
