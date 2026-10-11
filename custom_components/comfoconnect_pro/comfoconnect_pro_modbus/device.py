"""The top-level object for a ComfoConnect PRO gateway and its ventilation unit."""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import TYPE_CHECKING, Self

from modbus_connection import GatewayPathUnavailableError, GatewayTargetError
from modbus_connection.model import Device, Raw

from .controls import Controls
from .enums import ConnectionState
from .errors import NoVentilationUnitError
from .model import UpdateReport
from .sensors import Sensors
from .status import ConnectionStatus, Status

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit

_LOGGER = logging.getLogger(__name__)

DEFAULT_UNIT_ID = 1
"""The unit ID the gateway answers on unless it is set otherwise."""

READINGS = ("status", "sensors")
SETTINGS = ("controls",)
COMPONENTS = (*READINGS, *SETTINGS)

# The gateway answers with these when it has no path to the ventilation unit.
GATEWAY_ERRORS = (GatewayPathUnavailableError, GatewayTargetError)


class ComfoConnectPro(Device):
    """A ComfoAir Q or Flex unit behind a ComfoConnect PRO, through a ``ModbusUnit``."""

    def __init__(self, unit: ModbusUnit, *, timeout: float | None = None) -> None:
        """Set up the sub-systems."""
        super().__init__(unit)
        # Pass a timeout on only when given, because None withdraws one
        # another user of the same unit asked for.
        if timeout is not None:
            unit.require_timeout(timeout)

        self.status = Status(unit)
        self.sensors = Sensors(unit)
        self.controls = Controls(unit)
        # The components whose last refresh failed, so each failure warns once.
        self._failing: set[str] = set()

    @classmethod
    async def async_detect(
        cls, unit: ModbusUnit, *, timeout: float | None = None
    ) -> Self:
        """Read the gateway's status and build the device it describes.

        Raises ``NoVentilationUnitError`` when the gateway reports a connection
        state other than OK, or refuses a read for lack of a path to the unit.
        The timeout requirement stays on ``unit`` when detection fails.
        """
        # Build the device first, so the timeout applies to the detection
        # reads. Asking a live link for a longer timeout reconnects it.
        device = cls(unit, timeout=timeout)
        link = ConnectionStatus(unit)
        try:
            await link.async_update(notify=False)
        except GATEWAY_ERRORS as err:
            _LOGGER.debug("Gateway has no path to a ventilation unit: %s", err)
            raise NoVentilationUnitError(None, unreachable=True) from err
        state = link.connection_state
        _LOGGER.debug(
            "Gateway connection state: %s",
            link.connection_code if state is None else state.name,
        )
        if state is not ConnectionState.OK:
            raise NoVentilationUnitError(state, code=link.connection_code)
        try:
            await device.status.async_update(notify=False)
        except GATEWAY_ERRORS as err:
            raise NoVentilationUnitError(state, unreachable=True) from err
        status = device.status
        if not status.is_connected:
            raise NoVentilationUnitError(
                status.connection_state, code=status.connection_code
            )
        return device

    async def async_update_readings(self) -> UpdateReport:
        """Refresh what the unit measures and reports: status and sensors.

        Raises ``ModbusTimeoutError`` when the first component times out. A
        stalled link can hold a poll for several request timeouts.
        """
        return self._log_failures(await self.async_poll(READINGS))

    async def async_update_settings(self) -> UpdateReport:
        """Refresh the settings a client can change.

        Raises ``ModbusTimeoutError`` when the first component times out.
        """
        return self._log_failures(await self.async_poll(SETTINGS))

    async def async_update(self) -> UpdateReport:
        """Refresh readings and settings together in one report.

        Raises ``ModbusTimeoutError`` when the first component times out. A
        stalled link can hold a poll for several request timeouts.
        """
        return self._log_failures(await self.async_poll(COMPONENTS))

    def _log_failures(self, report: UpdateReport) -> UpdateReport:
        """Warn on a component's first failure and note when it recovers."""
        for name, error in report.failed.items():
            if name in self._failing:
                _LOGGER.debug("Component %s still fails to refresh: %s", name, error)
            else:
                _LOGGER.warning("Component %s failed to refresh: %s", name, error)
        for name in self._failing & report.updated:
            _LOGGER.info("Component %s refreshes again", name)
        self._failing = (self._failing - report.updated) | set(report.failed)
        return report

    async def async_read_raw(self, names: Iterable[str] | None = None) -> Raw:
        """Every register and bit this device reads, undecoded, for diagnostics."""
        return await super().async_read_raw(COMPONENTS if names is None else names)
