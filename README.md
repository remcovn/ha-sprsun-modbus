# SPRSUN Modbus Integration for Home Assistant

This custom integration allows you to read and control an SPRSUN heat pump from Home Assistant over Modbus TCP.

It is designed for users who want local polling, Home Assistant entities, and direct control of key setpoints and operating mode.

## Proven Hardware Setup

The tested and validated setup is based on:

- SPRSUN CGK025V3L-B
- Elfin EW11 RS485-to-IP converter

## Modbus Register Source

The Modbus register mapping in this project is based on community-shared information from this topic:

- [Pompa ciepła SprSun Select CGK40V3L - Urządzenia / Klimatyzacja i ogrzewanie - ArturHome](https://forum.arturhome.pl/t/pompa-ciepla-sprsun-select-cgk40v3l/12596)

Always validate register behavior on your own unit before relying on write operations in production.

## What This Integration Provides

- Sensor entities for temperatures, pressures, power, fan speeds, status fields, and controller parameters
- Binary sensors for hot-water demand, heating demand, legionella program, and defrost status
- Number entities for writable setpoints, temperature deltas, and the G03 start interval
- Select entity for unit mode control
- Config flow in Home Assistant UI (no YAML required)
- Polling profiles (`fast`, `balanced`, `conservative`)
- Connection resilience through retry and backoff

## Requirements

- Home Assistant (see minimum version in [hacs.json](hacs.json))
- HACS installed
- Network access from Home Assistant to your RS485-to-IP converter
- Modbus TCP bridge configured and reachable (for example, Elfin EW11)

## Installation (HACS Custom Repository)

1. Open HACS in Home Assistant.
2. Go to Custom repositories.
3. Add this repository URL as category Integration:
   - `https://github.com/remcovn/ha-sprsun-modbus`
4. Search for `SPRSUN Modbus` in HACS and install it.
5. Restart Home Assistant.
6. Go to Settings > Devices & Services > Add Integration.
7. Select `SPRSUN Modbus` and complete setup.

## Configuration Fields

During setup, you will provide:

- Host or IP address
- Port
- Slave ID
- Base polling interval (seconds)
- Polling profile (`fast`, `balanced`, `conservative`)

## G03 Start Interval

The `SPRSUN Start Interval (G03)` number entity reads and writes register 389
in whole minutes, with a range of 1-60 minutes. The existing `Start Internal (G03)`
sensor remains available for dashboards and automations. After updating, reload
the integration or restart Home Assistant to add the new control.

## Working Status Mark

The integration reads holding register `0x0003` (decimal address `3`) and exposes
the documented status bits as read-only binary sensors:

- Bit 0: Hot Water Demand
- Bit 1: Heating Demand
- Bit 4: Legionella Program
- Bit 7: Defrost Cycle

Register behavior can vary by controller model and firmware; validate these
statuses on your own unit.

## Typical Connection Notes (Elfin EW11)

- Use Modbus TCP mode on the converter.
- Ensure serial settings match the SPRSUN controller bus settings.
- Confirm TCP port and slave ID are correct.
- Make sure Home Assistant can reach the converter over the network.

## Safety Notes

- Unit mode changes are guarded in software and may be blocked while the compressor is running.
- Wrong Modbus writes can impact heat pump behavior.
- Start with read-only validation, then enable write actions carefully.

## Troubleshooting

If the integration does not load or setup fails:

1. Update to the latest release in HACS.
2. Restart Home Assistant after updating.
3. Check Home Assistant logs for `sprsun_modbus` errors.
4. Verify host, port, slave ID, and converter network connectivity.
5. Confirm your converter is actually serving Modbus TCP data.

## Useful Repository Files

- [custom_components/sprsun_modbus/manifest.json](custom_components/sprsun_modbus/manifest.json)
- [custom_components/sprsun_modbus/config_flow.py](custom_components/sprsun_modbus/config_flow.py)
- [custom_components/sprsun_modbus/register_definitions.py](custom_components/sprsun_modbus/register_definitions.py)
- [docs/register_catalog_v1.csv](docs/register_catalog_v1.csv)
- [docs/cutover_runbook.md](docs/cutover_runbook.md)

## Maintainer

- Remco van Noorloos
- GitHub: [@remcovn](https://github.com/remcovn)

## Attribution Request

If you reuse or adapt this project, please keep visible credit to the original author:

- Remco van Noorloos
- Repository: `https://github.com/remcovn/ha-sprsun-modbus`

At minimum, keep copyright and license notices intact in source distributions.

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.

## Disclaimer

This is a community project. Use it at your own risk.

Modbus implementations and register behavior can vary between firmware revisions and heat pump models.
