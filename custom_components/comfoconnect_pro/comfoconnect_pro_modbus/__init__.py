"""Read and control Zehnder ventilation units through a ComfoConnect PRO."""

from .controls import BOOST_TIME_24_HOURS, Controls
from .device import COMPONENTS, ComfoConnectPro, NoVentilationUnitError
from .enums import (
    AlarmCode,
    ConnectionState,
    TemperatureProfile,
    TemperatureProfileMode,
    VentilationPreset,
)
from .model import ComfoConnectComponent, UpdateReport, address
from .sensors import CO2_ZONES, Sensors
from .status import ALARM_SLOTS, Status, alarm

__all__ = [
    "ALARM_SLOTS",
    "BOOST_TIME_24_HOURS",
    "CO2_ZONES",
    "COMPONENTS",
    "AlarmCode",
    "ComfoConnectComponent",
    "ComfoConnectPro",
    "ConnectionState",
    "Controls",
    "NoVentilationUnitError",
    "Sensors",
    "Status",
    "TemperatureProfile",
    "TemperatureProfileMode",
    "UpdateReport",
    "VentilationPreset",
    "address",
    "alarm",
]
