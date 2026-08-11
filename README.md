# SPRSUN Modbus Custom Integration (HACS)

Deze repository is de migratie van een package-gebaseerde Home Assistant setup naar een losse custom integratie voor SPRSUN Modbus.

## Huidige status

- Bronbestand uit bestaande HA instance aanwezig:
  - configuration.yaml
  - ha_package_sprsun_readonly.yaml
- Migratiecontract en runbook toegevoegd in docs.
- Registercatalogus v1 gegenereerd uit de package-bron.
- Pymodbus runtime basis staat klaar:
  - API-wrapper
  - DataUpdateCoordinator
  - Werkende sensor, number en select platformen
- Read-parity uitgebreid: alle registers uit docs/register_catalog_v1.csv zijn opgenomen als sensor-definitie.
- Native Unit Mode tekstsensor toegevoegd, zodat template-mapping niet meer nodig is.
- Pollingprofielen toegevoegd (fast, balanced, conservative) met fijnmazige register-cadans.
- Exponentiele reconnect/backoff toegevoegd op coordinator-niveau.

## Doel v1

- Functionele parity met huidige package voor:
  - Alle read-sensoren
  - Write-functionaliteit voor setpoints en unit mode
- Safety-regel op unit mode write:
  - Alleen schrijven wanneer compressor frequentie <= 0
- Nieuwe nette entity_ids zijn toegestaan.

## Hergebruik van HA Modbus

- Ja, hergebruik kan, maar in de praktijk gebruiken we in deze integratie een eigen Modbus laag via pymodbus.
- Reden: stabiele controle over polling, entity-model, write-guards en foutafhandeling binnen 1 custom component.
- We leunen dus niet op interne (niet-publieke) Python API's van de ingebouwde HA Modbus integratie.

## Belangrijke documenten

- docs/migration_contract_v1.md
- docs/register_catalog_v1.csv
- docs/cutover_runbook.md
- docs/entity_mapping_old_to_new.csv
- docs/side_by_side_validation_template.csv
- docs/write_validation_template.csv

## Installatie via HACS (custom repository)

1. Push deze repository naar GitHub.
2. Maak een eerste release tag, bijvoorbeeld `v0.1.0`.
3. Open HACS in Home Assistant.
4. Kies `Custom repositories`.
5. Voeg de GitHub URL toe met categorie `Integration`.
6. Zoek op `SPRSUN Modbus` in HACS en installeer.
7. Herstart Home Assistant.
8. Ga naar `Instellingen` -> `Apparaten en diensten` -> `Integratie toevoegen`.
9. Voeg `SPRSUN Modbus` toe en vul host, port, slave, scan interval en profile in.

## Release checklist (praktisch)

1. Controleer dat `manifest.json` en `hacs.json` correct zijn.
2. Verhoog versie in `custom_components/sprsun_modbus/manifest.json` bij elke release.
3. Werk changelog of release notes bij in GitHub.
4. Maak en push een semver tag, bijvoorbeeld `v0.1.1`.
5. Verifieer dat HACS de nieuwe release ziet.

## Volgende implementatiestap

1. Side-by-side validatie uitvoeren volgens docs/cutover_runbook.md als je later extra zekerheid wilt.
