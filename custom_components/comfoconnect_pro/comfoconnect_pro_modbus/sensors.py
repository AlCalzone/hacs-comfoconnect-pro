"""Airflow, temperatures, humidity, CO₂ and filter life: input 0x0007-0x001A."""

from __future__ import annotations

from modbus_connection.model import gauge, integer

from .model import ComfoConnectComponent, address

CO2_ZONES = 8


class Sensors(ComfoConnectComponent):
    """What the ventilation unit measures."""

    register_space = "input"

    airflow = integer(address(0x0007), signed=False, unit="m³/h")

    room_temperature = gauge(address(0x0008), 0.1, unit="°C")
    extract_temperature = gauge(address(0x0009), 0.1, unit="°C")
    """The air drawn from the rooms, as it enters the unit."""
    exhaust_temperature = gauge(address(0x000A), 0.1, unit="°C")
    """The air blown outside."""
    outdoor_temperature = gauge(address(0x000B), 0.1, unit="°C")
    supply_temperature = gauge(address(0x000C), 0.1, unit="°C")
    """The air blown into the rooms."""

    room_humidity = integer(address(0x000D), signed=False, unit="%")
    extract_humidity = integer(address(0x000E), signed=False, unit="%")
    exhaust_humidity = integer(address(0x000F), signed=False, unit="%")
    outdoor_humidity = integer(address(0x0010), signed=False, unit="%")
    supply_humidity = integer(address(0x0011), signed=False, unit="%")

    co2_zone_1 = integer(address(0x0012), signed=False, unit="ppm")
    co2_zone_2 = integer(address(0x0013), signed=False, unit="ppm")
    co2_zone_3 = integer(address(0x0014), signed=False, unit="ppm")
    co2_zone_4 = integer(address(0x0015), signed=False, unit="ppm")
    co2_zone_5 = integer(address(0x0016), signed=False, unit="ppm")
    co2_zone_6 = integer(address(0x0017), signed=False, unit="ppm")
    co2_zone_7 = integer(address(0x0018), signed=False, unit="ppm")
    co2_zone_8 = integer(address(0x0019), signed=False, unit="ppm")

    filter_days_remaining = integer(address(0x001A), signed=False, unit="d")

    def co2(self, zone: int) -> int | None:
        """The CO₂ level in ``zone``, from 1 to 8."""
        if not 1 <= zone <= CO2_ZONES:
            raise ValueError(f"no CO2 zone {zone}")
        value: int | None = getattr(self, f"co2_zone_{zone}")
        return value

    @property
    def co2_zones(self) -> dict[int, int]:
        """The zones that report a CO₂ level, keyed by zone number.

        A zone that reads 0 counts as having no sensor.
        """
        levels = {zone: self.co2(zone) for zone in range(1, CO2_ZONES + 1)}
        return {zone: level for zone, level in levels.items() if level}
