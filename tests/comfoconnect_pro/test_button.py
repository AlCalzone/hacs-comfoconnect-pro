"""Tests for the Zehnder ComfoConnect PRO button platform."""

import pytest
from homeassistant.components.button import DOMAIN as BUTTON_DOMAIN
from homeassistant.components.button import SERVICE_PRESS
from homeassistant.const import ATTR_ENTITY_ID, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from modbus_connection.mock import MockModbusUnit, WriteEvent
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from custom_components.comfoconnect_pro.comfoconnect_pro_modbus.model import address

pytestmark = pytest.mark.parametrize("platforms", [[Platform.BUTTON]])


async def test_buttons(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    init_integration: MockConfigEntry,
) -> None:
    """Test every button."""
    await snapshot_platform(hass, entity_registry, snapshot, init_integration.entry_id)


@pytest.mark.usefixtures("init_integration")
async def test_reset_errors(hass: HomeAssistant, mock_unit: MockModbusUnit) -> None:
    """Test pressing reset writes the self-resetting coil."""
    writes: list[WriteEvent] = []
    mock_unit.on_write(writes.append)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {ATTR_ENTITY_ID: "button.comfoair_reset_errors"},
        blocking=True,
    )

    assert writes == [WriteEvent("coil", address(0x0001), [True], 0x05)]
