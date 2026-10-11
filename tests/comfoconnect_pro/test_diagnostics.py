"""Tests for the Zehnder ComfoConnect PRO diagnostics."""

import pytest
from homeassistant.core import HomeAssistant
from modbus_connection import ModbusTimeoutError
from modbus_connection.mock import MockModbusUnit
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.components.diagnostics import (
    get_diagnostics_for_config_entry,
)
from pytest_homeassistant_custom_component.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

pytestmark = pytest.mark.parametrize("platforms", [[]])


async def test_diagnostics(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    init_integration: MockConfigEntry,
) -> None:
    """Test diagnostics hold the raw registers and redact the host."""
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )


async def test_diagnostics_read_error(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    init_integration: MockConfigEntry,
    mock_unit: MockModbusUnit,
) -> None:
    """Test diagnostics name a failed raw read instead of failing."""
    mock_unit.fail_requests(ModbusTimeoutError())

    result = await get_diagnostics_for_config_entry(hass, hass_client, init_integration)

    assert result["read_error"] == "ModbusTimeoutError"
    assert result["raw"] is None
