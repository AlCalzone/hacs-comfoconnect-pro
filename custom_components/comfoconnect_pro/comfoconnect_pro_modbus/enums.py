"""The coded values of the ComfoConnect PRO register map."""

from __future__ import annotations

from enum import IntEnum


class ConnectionState(IntEnum):
    """Input register 0x0001: whether the gateway reaches a ventilation unit."""

    OK = 0
    NOT_COMFOAIR_Q = 30
    """The ventilation unit found on ComfoNet is not a ComfoAir Q or Flex."""
    INCOMPATIBLE_VERSION = 40
    """The ventilation unit's firmware is not compatible with the gateway."""
    NO_VENTILATION_UNIT = 50


class VentilationPreset(IntEnum):
    """Holding register 0x0001: the fan speed level."""

    AWAY = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TemperatureProfile(IntEnum):
    """Holding register 0x0002: the comfort temperature profile."""

    NORMAL = 0
    COLD = 1
    WARM = 2


class TemperatureProfileMode(IntEnum):
    """Holding register 0x0003: how the comfort temperature is chosen."""

    ADAPTIVE = 0
    FIXED = 1
    EXTERNAL_SETPOINT = 2
    """The unit follows the external setpoint, holding register 0x0004."""


class AlarmCode(IntEnum):
    """Input registers 0x0002 to 0x0006: an active ComfoAir Q alarm.

    The names follow the manual's codes. The manual writes the humidity
    sensors as φ, which the names spell ``PHI``.
    """

    HRU_T_FIRE_ERR = 21
    """Two or more temperature sensors are out of range."""
    T_HRU_ERR = 22
    """The temperature is too high for the heat recovery unit."""
    T_11_ERR = 23
    """Temperature sensor T11 exceeded its limit too often."""
    T_11_LIMIT_ERR = 24
    """Temperature sensor T11 exceeds its limit."""
    T_12_ERR = 25
    """Temperature sensor T12 exceeded its limit too often."""
    T_12_LIMIT_ERR = 26
    """Temperature sensor T12 exceeds its limit."""
    T_20_ERR = 27
    """Temperature sensor T20 exceeded its limit too often."""
    T_20_LIMIT_ERR = 28
    """Temperature sensor T20 exceeds its limit."""
    T_21_ERR = 29
    """Temperature sensor T21 exceeded its limit too often."""
    T_21_LIMIT_ERR = 30
    """Temperature sensor T21 exceeds its limit."""
    T_22_ERR = 31
    """Temperature sensor T22 exceeded its limit too often."""
    T_22_LIMIT_ERR = 32
    """Temperature sensor T22 exceeds its limit."""
    HRU_INIT_ERR = 33
    """The heat recovery unit has not been initialized."""
    HRU_FRONT_OPEN_ERR = 34
    """The front door is open."""
    H_21_RELEASE_ERR = 35
    """The preheater's side does not match the unit's orientation."""
    H_21_P_ERR = 37
    """The preheater does not deliver the requested power."""
    H_21_P_RATIO_ERR = 38
    """The preheater does not deliver the requested power ratio."""
    PHI_11_ERR = 39
    """Humidity sensor φ11 exceeded its limit too often."""
    PHI_12_ERR = 41
    """Humidity sensor φ12 exceeded its limit too often."""
    PHI_20_ERR = 43
    """Humidity sensor φ20 exceeded its limit too often."""
    PHI_21_ERR = 45
    """Humidity sensor φ21 exceeded its limit too often."""
    PHI_22_ERR = 47
    """Humidity sensor φ22 exceeded its limit too often."""
    P_12_ERR = 49
    """Pressure sensor P12 exceeded its limit too often."""
    P_22_ERR = 50
    """Pressure sensor P22 exceeded its limit too often."""
    F_12_S_ERR = 51
    """The speed of fan F12 exceeded its limit too often."""
    F_22_S_ERR = 52
    """The speed of fan F22 exceeded its limit too often."""
    PTOT_12_S_ERR = 53
    """The static pressure at sensor P12 exceeded its limit too often."""
    PTOT_22_S_ERR = 54
    """The static pressure at sensor P22 exceeded its limit too often."""
    F_12_S_SET_ERR = 55
    """Fan F12 missed its requested speed too often."""
    F_22_S_SET_ERR = 56
    """Fan F22 missed its requested speed too often."""
    QM_12_SET_ERR = 57
    """Fan F12 missed its requested mass flow too often."""
    QM_22_SET_ERR = 58
    """Fan F22 missed its requested mass flow too often."""
    T_21_SET_ERR = 59
    """The outdoor air after the preheater missed its temperature too often."""
    T_22_SET_ERR = 60
    """The supply air missed its requested temperature too often."""
    T_22_FROST_ERR = 61
    """The supply air temperature at sensor T22 was too low too often."""
    UNBALANCE_ERR = 62
    """The airflow imbalance was out of tolerance too often."""
    PRESENT_RF_ERR = 66
    """The RF hardware was present and is no longer detected."""
    PRESENT_IO_ERR = 67
    """The option box was present and is no longer detected."""
    PRESENT_H_21_ERR = 68
    """The preheater was present and is no longer detected."""
    PRESENT_H_23_ERR = 69
    """The postheater was present and is no longer detected."""
    PRESENT_HOOD_ERR = 74
    """The cooker hood was present and is no longer detected."""
    PRESENT_CCOOL_ERR = 75
    """ComfoCool was present and is no longer detected."""
    PRESENT_G_ERR = 76
    """ComfoFond was present and is no longer detected."""
    FILTER_ALARM_FLAG = 77
    """The filters must be replaced now."""
    FILTER_EXT_ERR = 78
    """The external filter input is high."""
    FILTER_WARNING_FLAG = 79
    """The filters are near the end of their life and should be ordered."""
    STANDBY_ERR = 80
    """Standby is active."""
    H_21_COMM_ERR = 81
    """The preheater does not communicate reliably."""
    T_22_MANUAL_ERR = 89
    """The bypass is in manual use."""
    CC_OVERHEAT_ERR = 90
    """ComfoCool is overheated."""
    CC_COMP_ERR = 91
    """The ComfoCool compressor reports an error."""
    CC_T_10_ERR = 92
    """The ComfoCool room temperature is out of range."""
    CC_T_13_ERR = 93
    """The ComfoCool compressor temperature is out of range."""
    CC_T_23_ERR = 94
    """The ComfoCool supply temperature is out of range."""
    T_HOOD_ERR = 95
    """The cooker hood temperature is too high."""
    IO_HOOD_DUTY_ERR = 96
    """The cooker hood is on."""
    QM_CONSTRAINT_MIN_ERR = 97
    """A status flag; the manual gives no further description."""
    H_21_QM_MIN_ERR = 98
    """The airflow is too low for the preheater."""
    CONFIG_ERR = 99
    """The configuration is invalid."""
    ANALYSIS_BUSY_WARNING = 100
    """An error analysis is running."""
    COMFONET_ERR = 101
    """The ComfoNet bus reports an error."""
    CO2_SENS_COUNT_ERR = 102
    """A controller detects fewer CO₂ sensors than before."""
    CO2_SENS_TOO_MANY_ERR = 103
    """A zone has more than 8 CO₂ sensors."""
    CO2_SENS_GENERAL_ERR = 104
    """A CO₂ sensor reports a general error."""
