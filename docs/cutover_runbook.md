# Cutover Runbook - SPRSUN Package naar Custom Integratie

## Testmetadata

- Tester:
- Datum start:
- Datum einde:
- HA versie:
- Integratie versie:
- Poll profile:
- Host:
- Port:
- Slave:

## Fase A - Parallel draaien

Doel: valideren zonder productie-impact.

1. Installeer custom integratie naast bestaande package setup.
2. Gebruik tijdelijke of prefixed namen voor nieuwe entities.
3. Controleer dat polling en writes technisch werken.
4. Vergelijk kernwaarden gedurende minimaal 24 uur.

### Side-by-side meetset (24 uur)

- Meetpunt: Inlet Temperature
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 0.5 C
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: Outlet Temperature
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 0.5 C
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: Ambient Temperature
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 0.5 C
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: Compressor Frequency
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 1 Hz
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: Compressor Current of Inverter Current
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 1 A
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: Pump PWM
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 2 %
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: SPRSUN Input Power
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: +/- 150 W
  - Meetinterval: 1 min
  - Resultaat: pass/fail
  - Opmerking:
- Meetpunt: Unit Mode (P06)
  - Oude entity:
  - Nieuwe entity:
  - Tolerantie: exact
  - Meetinterval: event based
  - Resultaat: pass/fail
  - Opmerking:

### Runtime stabiliteit

- Controle: Polling loopt door
  - Methode: 60 min observeren
  - Verwachting: geen gat groter dan 2x poll-interval
  - Resultaat: pass/fail
  - Opmerking:
- Controle: Reconnect gedrag
  - Methode: netwerkonderbreking simuleren
  - Verwachting: herstel zonder handmatige actie
  - Resultaat: pass/fail
  - Opmerking:
- Controle: Unavailable storm
  - Methode: restart plus reconnect scenario
  - Verwachting: geen langdurige unavailable golf
  - Resultaat: pass/fail
  - Opmerking:

## Fase B - Gecontroleerde omschakeling

1. Zet dashboards om naar nieuwe entity_ids.
2. Zet automations om naar nieuwe entities en services.
3. Schakel oude package write-automations uit.
4. Verwijder package-sensoren pas na succesvolle verificatie.

### Omschakelchecklist

- [ ] Dashboards verwijzen naar nieuwe entities.
- [ ] Automations verwijzen naar nieuwe entities of services.
- [ ] Oude package write-automations zijn uitgeschakeld.
- [ ] Side-by-side vergelijking over 24 uur is succesvol afgerond.

## Rollback

1. Schakel custom integratie uit.
2. Schakel package weer volledig in.
3. Controleer of oude write-pad direct weer functioneert.

### Rollback-triggers

- Unit mode write guard werkt niet betrouwbaar.
- Herhaalde write timeouts zonder herstel.
- Kernsensoren wijken structureel buiten tolerantie af.
- Persistente unavailable toestand na restart of reconnect.

## Go/No-Go checklist

- [ ] Config entry is stabiel en reconnects zijn gezond.
- [ ] Geen write timeouts in normale operatie.
- [ ] Unit mode write guard werkt aantoonbaar.
- [ ] Kernsensoren blijven binnen afgesproken tolerantie versus oude setup.
- [ ] Herstartscenario is getest en geslaagd.
- [ ] HACS install of update pad is getest op schone testomgeving.

### Go/No-Go aftekening

- Config entry stabiel: pass/fail
- Writes stabiel: pass/fail
- Unit mode guard OK: pass/fail
- 24h side-by-side OK: pass/fail
- Restart en reconnect OK: pass/fail
- HACS install en update OK: pass/fail

Eindbesluit:

- Go of No-Go:
- Beslisser:
- Datum:

## Verificatie van writes

1. Hot Water Setpoint write naar register 202 met x2 schaal.
2. Cooling Setpoint write naar register 203 met x2 schaal.
3. Heating Setpoint write naar register 204 met x2 schaal.
4. Heat Delta Temp write naar register 198 met x1 schaal.
5. AC Constant Temp Diff write naar register 199 met x1 schaal.
6. Hot Water Delta Temp write naar register 200 met x1 schaal.
7. Unit Mode write naar register 54 alleen bij compressor frequentie <= 0.

### Write testformulier

Gebruik voor logging per write test:

- docs/write_validation_template.csv

- Test: Hot Water Setpoint
  - Input: 45.5 C
  - Verwachte write: 202 = 91
  - Guard: n.v.t.
  - Resultaat: pass/fail
  - Opmerking:
- Test: Cooling Setpoint
  - Input: 18.0 C
  - Verwachte write: 203 = 36
  - Guard: n.v.t.
  - Resultaat: pass/fail
  - Opmerking:
- Test: Heating Setpoint
  - Input: 35.0 C
  - Verwachte write: 204 = 70
  - Guard: n.v.t.
  - Resultaat: pass/fail
  - Opmerking:
- Test: Heat Delta Temp
  - Input: 6
  - Verwachte write: 198 = 6
  - Guard: n.v.t.
  - Resultaat: pass/fail
  - Opmerking:
- Test: AC Constant Temp Diff
  - Input: 4
  - Verwachte write: 199 = 4
  - Guard: n.v.t.
  - Resultaat: pass/fail
  - Opmerking:
- Test: Hot Water Delta Temp
  - Input: 5
  - Verwachte write: 200 = 5
  - Guard: n.v.t.
  - Resultaat: pass/fail
  - Opmerking:
- Test: Unit Mode to Heating
  - Input: Heating
  - Verwachte write: 54 = 1
  - Guard: alleen bij compressor frequentie <= 0
  - Resultaat: pass/fail
  - Opmerking:
- Test: Unit Mode blocked
  - Input: Cooling
  - Verwachte write: geen write
  - Guard: blokkeren bij compressor frequentie > 0
  - Resultaat: pass/fail
  - Opmerking:
