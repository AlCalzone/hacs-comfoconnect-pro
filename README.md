# Zehnder ComfoConnect PRO for Home Assistant (HACS)

Connect a Zehnder ComfoAir Q or Flex ventilation unit to Home Assistant through the ComfoConnect PRO gateway, over Modbus TCP or Modbus RTU. This is the custom integration build of the `comfoconnect_pro` integration, for testing through [HACS](https://hacs.xyz) before the integration lands in Home Assistant itself.

It reads the airflow, the temperature and humidity of each air stream, the CO₂ levels, the filter status and the unit's alarms. It sets the fan speed, auto mode, boost, away mode, ComfoCool and the temperature profile.

## Requirements

- Home Assistant 2026.10 or later. The integration shares its Modbus connection through Home Assistant's `modbus` integration, and needs the modbus-connection release that 2026.10 ships.
- A ComfoConnect PRO gateway (product number 30006323) on ComfoNet with a ComfoAir Q or ComfoAir Flex. The older ComfoConnect LAN C is covered by Home Assistant's own [Zehnder ComfoAir Q](https://www.home-assistant.io/integrations/comfoconnect/) integration instead.
- On the gateway's web interface (for example `http://comfoconnectpro.local`), on the **Protocols and services** page: **Modbus TCP** or **Modbus RTU** selected. Note the unit ID, `1` by default.

## Installation

1. In HACS, open the menu in the top right corner and choose **Custom repositories**.
2. Add `https://github.com/AlCalzone/hacs-comfoconnect-pro` with the type **Integration**.
3. Find **Zehnder ComfoConnect PRO** in HACS, download it, and restart Home Assistant.
4. Go to **Settings** > **Devices & services**, select **Add integration**, and choose **Zehnder ComfoConnect PRO**.
5. Choose **Network (Modbus TCP)** and enter the gateway's IP address, or **Serial port (Modbus RTU)** and pick the RS-485 port, baud rate and parity set on the gateway.

The integration checks that the gateway reaches a supported ventilation unit before it creates the entry.

## What you get

All entities belong to one device.

- A fan. Its four speeds are the unit's presets: away (25 %), low (50 %), medium (75 %) and high (100 %). The **Auto** preset hands the speed to the unit. Choosing a speed turns auto mode off. The unit cannot be turned off over Modbus.
- **Airflow**, and the temperature and humidity of the room, extract, exhaust, outdoor and supply air.
- **CO₂ zone 1** to **CO₂ zone 8**, each added once its zone reports a level.
- **Filter days remaining**, and a **Filter** binary sensor that turns on when the filters are due.
- **Error**, **Standby** and **ComfoHood** binary sensors, and **Active error 1** to **5** with the alarm names. Only the first alarm slot is enabled by default.
- **Boost**, **Away** and **ComfoCool** switches.
- **Temperature profile** and **Temperature profile mode** selects, **External setpoint** and **Boost duration** numbers, and a **Reset errors** button.

The integration polls the gateway every 30 seconds.

## Reporting problems

Open an [issue](https://github.com/AlCalzone/hacs-comfoconnect-pro/issues) and attach the diagnostics download from the integration's device page. It contains the raw registers the integration read, minus the host and serial port. The register map comes from the gateway's installation manual, document revision 140, and has not been checked against a real gateway yet, so a raw dump is what a wrong value is tracked down with.

To see what the integration does, turn on debug logging:

```yaml
logger:
  logs:
    custom_components.comfoconnect_pro: debug
```

## Development

This repository follows [integration_blueprint](https://github.com/ludeeus/integration_blueprint). The code in `custom_components/comfoconnect_pro` and the tests in `tests/comfoconnect_pro` are generated, so fix bugs at their source:

- [comfoconnect-pro-modbus](https://github.com/AlCalzone/comfoconnect-pro-modbus) is the device library. It is vendored as `custom_components/comfoconnect_pro/comfoconnect_pro_modbus`, so the integration needs no package from PyPI.
- [ha-core-comfoconnect-pro](https://github.com/AlCalzone/ha-core-comfoconnect-pro) is the integration as it is meant for Home Assistant core.

With both checked out next to this repository, rebuild and test:

```bash
scripts/setup
scripts/vendor.py
python3 -m pytest
```

`scripts/vendor.py` rewrites the library imports to relative ones, turns the manifest into a custom integration's, and resolves `strings.json` into `translations/en.json`. It keeps the version in the current manifest. `scripts/develop` starts a Home Assistant instance with the integration loaded, configured by `config/configuration.yaml`.

## License

Apache License 2.0
