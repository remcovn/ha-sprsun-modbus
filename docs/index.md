---
title: SPRSUN Modbus for Home Assistant
description: >-
  Control and monitor your SPRSUN heat pump locally from Home Assistant over
  Modbus TCP. Tested on the SPRSUN CGK025V3L-B with an Elfin EW11. Install via HACS.
---

**SPRSUN Modbus** is a Home Assistant custom integration that lets you read and
control an SPRSUN air-to-water heat pump locally over Modbus TCP: no cloud, no
YAML. Install it via HACS and configure it in the Home Assistant UI.

[Get it on GitHub](https://github.com/remcovn/ha-sprsun-modbus) ·
[Latest release](https://github.com/remcovn/ha-sprsun-modbus/releases/latest) ·
[Add to HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=remcovn&repository=ha-sprsun-modbus&category=integration)

## What you get

- **Sensors** for temperatures, pressures, compressor
  frequency, fan speeds, DC bus voltage, compressor current, status fields and
  controller parameters
- **Estimated power** sensor, calibrated against a smart meter, because the
  heat pump's own input-power register reads 0 on tested firmware
- **Binary sensors** for hot-water demand, heating demand, legionella program
  and defrost
- **Controls** for setpoints, temperature deltas, the G03 start interval and
  unit mode
- Config flow in the UI, three polling profiles, and automatic retry and backoff

## Tested hardware

| Component | Model |
|---|---|
| Heat pump | SPRSUN CGK025V3L-B |
| RS485 to Modbus TCP bridge | Elfin EW11 |

The register map comes from community work on the SPRSUN Select CGK40V3L, so
other SPRSUN models with the same controller are likely to work. Always check
readings on your own unit before you use write actions.

## Installation

1. In Home Assistant, open **HACS → Custom repositories**.
2. Add `https://github.com/remcovn/ha-sprsun-modbus` with category **Integration**.
3. Install **SPRSUN Modbus** and restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and pick
   **SPRSUN Modbus**.
5. Enter the IP address and port of your Modbus TCP bridge, plus the slave ID.

The [README on GitHub](https://github.com/remcovn/ha-sprsun-modbus#readme)
covers configuration, the register mapping and troubleshooting.

## Register map

The full register catalog is available as
[CSV](register_catalog_v1.csv). It is based on community findings from the
[ArturHome forum](https://forum.arturhome.pl/t/pompa-ciepla-sprsun-select-cgk40v3l/12596).

## Nederlands

**SPRSUN Modbus** is een Home Assistant-integratie voor SPRSUN-warmtepompen.
Je leest de warmtepomp lokaal uit via Modbus TCP, zonder cloud, bijvoorbeeld
met een Elfin EW11 RS485-naar-wifi-module. Je ziet temperaturen, drukken,
compressorfrequentie en een geschat stroomverbruik, en je kunt setpoints en de
bedrijfsmodus instellen. Installeren gaat via
HACS. Getest op een SPRSUN CGK025V3L-B.

---

MPL-2.0 licensed · Maintained by [Remco van Noorloos](https://github.com/remcovn)
· Community project, not affiliated with SPRSUN.
