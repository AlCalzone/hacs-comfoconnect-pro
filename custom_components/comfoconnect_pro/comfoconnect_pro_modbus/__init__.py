"""Read and control Zehnder ventilation units through a ComfoConnect PRO."""

from .controls import (
    BOOST_TIME_MAX,
    EXTERNAL_SETPOINT_MAX,
    EXTERNAL_SETPOINT_MIN,
    Controls,
)
from .device import DEFAULT_UNIT_ID, ComfoConnectPro
from .enums import (
    AlarmCode,
    ConnectionState,
    TemperatureProfile,
    TemperatureProfileMode,
    VentilationPreset,
)
from .errors import ComfoConnectProError, InvalidValueError, NoVentilationUnitError
from .model import UpdateReport
from .sensors import CO2_ZONES, Sensors
from .status import ALARM_SLOTS, Status

__all__ = [
    "ALARM_SLOTS",
    "BOOST_TIME_MAX",
    "CO2_ZONES",
    "DEFAULT_UNIT_ID",
    "EXTERNAL_SETPOINT_MAX",
    "EXTERNAL_SETPOINT_MIN",
    "AlarmCode",
    "ComfoConnectPro",
    "ComfoConnectProError",
    "ConnectionState",
    "Controls",
    "InvalidValueError",
    "NoVentilationUnitError",
    "Sensors",
    "Status",
    "TemperatureProfile",
    "TemperatureProfileMode",
    "UpdateReport",
    "VentilationPreset",
]
