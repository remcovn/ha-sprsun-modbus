# Migratiecontract v1 - SPRSUN naar Custom Integratie

## Scope in v1

- Alle huidige read-sensoren uit ha_package_sprsun_readonly.yaml.
- Writes voor de volgende registers:
  - 202 Hot Water Setpoint
  - 203 Cooling Setpoint
  - 204 Heating Setpoint
  - 198 Heat Delta Temp
  - 199 AC Constant Temp Diff
  - 200 Hot Water Delta Temp
  - 54 Unit Mode (P06)
- Vervanging van package-helpers (input_number/input_select + automations) door integratie-native entities/services.

## Safety en schrijfregels

- Unit mode (register 54) mag alleen geschreven worden wanneer compressor frequentie <= 0.
- Setpoints met 0.5 C-resolutie worden geschreven met schaalfactor x2 op register-niveau.
- Bij write-fout of timeout:
  - duidelijke logging op warning/error niveau
  - geen silent fail
  - entity state moet consistente feedback geven

## Naamgeving en identifiers

- Nieuwe nette entity_ids zijn toegestaan.
- unique_id strategie:
  - per register een stabiele unique_id
  - aanbevolen format: sprsun_{slave}_{register}_{key}
- Friendly name wijzigingen zijn toegestaan zolang mapping oud->nieuw wordt geleverd.

## Niet in scope v1

- Geavanceerde KPI/COP berekeningen als harde requirement.
- Firmware autodetect als verplichting (wel ruimte voor profielselector).
- Volledige redesign van dashboarding.

## Bron van waarheid

- Registerdefinities en writeability: docs/register_catalog_v1.csv
- Oorspronkelijke package bron: ha_package_sprsun_readonly.yaml

## Register deduplicatiebesluit

- In de package-bron wijzen zowel "SPRSUN Inverter Current" als "Compressor Current" naar register 35.
- Voor v1 houden we in de catalogus exact 1 registerentry aan voor adres 35 om dubbele waardes in de integratie te voorkomen.
- Gekozen canonieke entry in v1: "SPRSUN Inverter Current".

## Configuratie bij toevoegen device

- Bij het toevoegen van de integratie zijn minimaal instelbaar:
  - host
  - port
  - slave id
  - basis scan interval

## Acceptatiecriteria v1

1. Config flow valideert host/port/slave en maakt config entry.
2. Coordinator pollt stabiel met ingestelde intervallen.
3. Alle kernsensoren updaten realtime tijdens bedrijf.
4. Alle v1 writes werken met correcte schaling.
5. Unit mode guard blokkeert writes als compressor frequentie > 0.
6. Herstart van Home Assistant herstelt polling zonder langdurige unavailable storm.
7. Side-by-side vergelijking 24 uur slaagt voor kernwaarden.
