"""The top-level object for a ComfoConnect PRO gateway and its ventilation unit."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Self

from modbus_connection.model import Device, Raw

from .controls import Controls
from .enums import ConnectionState
from .model import UpdateReport
from .sensors import Sensors
from .status import Status

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit

COMPONENTS = ("status", "sensors", "controls")


class NoVentilationUnitError(Exception):
    """The gateway answered, but it does not reach a ventilation unit it serves."""

    def __init__(self, state: ConnectionState | None) -> None:
        """Initialize the error."""
        shown = "nothing" if state is None else f"{state.value} ({state.name})"
        super().__init__(f"the gateway's connection state is {shown}, not 0 (OK)")
        self.state = state


class ComfoConnectPro(Device):
    """A ComfoAir Q or Flex unit behind a ComfoConnect PRO, through a ``ModbusUnit``."""

    def __init__(self, unit: ModbusUnit, *, timeout: float | None = None) -> None:
        """Set up the sub-systems."""
        super().__init__(unit)
        unit.require_timeout(timeout)

        self.status = Status(unit)
        self.sensors = Sensors(unit)
        self.controls = Controls(unit)

    @classmethod
    async def async_detect(
        cls, unit: ModbusUnit, *, timeout: float | None = None
    ) -> Self:
        """Read the gateway's status and build the device it describes.

        Raises ``NoVentilationUnitError`` when the gateway reports a connection
        state other than OK.
        """
        device = cls(unit, timeout=timeout)
        await device.status.async_update(notify=False)
        if not device.status.is_connected:
            raise NoVentilationUnitError(device.status.connection_state)
        return device

    async def async_update(self) -> UpdateReport:
        """Refresh the status, the measurements and the settings in one report."""
        return await self.async_poll(COMPONENTS)

    async def async_read_raw(self, names: Iterable[str] | None = None) -> Raw:
        """Every register and bit this device reads, undecoded, for diagnostics."""
        return await super().async_read_raw(COMPONENTS if names is None else names)
