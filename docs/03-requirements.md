---
doc_id: SCL-REQ-001
title: SunClave requirements
project: SunClave
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with design case and status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply SCL-DDR-001 (R1, R13 and R17 redefined, design case completed) and replace the status column with the TRL 3 results of SCL-CAL-001
---

# SunClave requirements

These requirements are checked by calculation in SCL-CAL-001 at TRL 3. Targets are still proposals, not yet validated with users, and will be revised after co-design sessions (see SCL-PRB-001). R1, R13 and R17 were restated on 2026-09-25 to apply Amish's decisions in SCL-DDR-001 (altitude option B, and the budget cuts and $450 budget). The status column gives the TRL 3 result; every value is a paper estimate.

The **design case** is a clear day with 700 W/m² direct normal irradiance (DNI) and the sun 60° above the horizon, 25 °C ambient, wind 2 m/s (below 3 m/s), a site at sea level, and a load of 2.0 kg of unwrapped or single-wrapped solid stainless instruments in a 0.5 kg basket, with 1.5 L of water in a 12 L aluminum cooker.

> **Safety:** These requirements describe a pressure vessel heated by concentrated sunlight, in a research and educational prototype that is not a medical device. R8 to R11 are safety requirements and take precedence over throughput and cost. A PASS against R1 and R12 records conditions; it does not prove sterility.

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 3 status (SCL-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Sterilizing condition (redefined 2026-09-25, SCL-DDR-001 item 1) | Saturated steam in the load zone for an exposure equal to 20 min (unwrapped) or 30 min (wrapped) at 121 °C, using z = 10 °C for any lower temperature; never below 115 °C nor above 124 °C in normal operation; the real temperature and hold are recorded and a cycle below 121 °C is never labeled 121 °C | Calculation; later instrumented cycles with biological indicators | **Not verifiable at TRL 3.** Met by calculation to 2,400 m (120.95 °C and 30.3 min at sea level; 117.7 °C and 63 min at 1,800 m), but the equivalence needs biological-indicator evidence |
| R2 | Load capacity | Basket at least 250 mm diameter by 150 mm deep; 2.0 kg of solid instruments per cycle (about two delivery kits or four suture kits) | Model check | Met: 250 x 150 mm basket in a 12.3 L cooker, 16 mm above the water |
| R3 | Load type | Solid instruments only, unwrapped or single-wrapped in porous wrap; no lumened, hollow or textile loads | Instructions and design review | Met by definition (decided, SCL-DDR-001 item 9) |
| R4 | Cycle time | Cold start to end of hold in 90 min or less in the design case | Energy calculation; later timed cycles | **At risk:** about 80 min central, 71 to 109 min across scenarios |
| R5 | Daily throughput | 3 or more complete cycles on a clear day (DNI 600 W/m² or more from 09:00 to 15:00 solar time) | Energy calculation | Met: 4 cycles in each case checked; zero on overcast days |
| R6 | Cycle record | Load-zone temperature and chamber pressure logged at 1 s intervals from start to end; cycle ID, date and time, hold duration, minimum hold temperature, equivalent exposure and a pass or fail flag stored for 1,000 or more cycles and shown to the operator at cycle end | Design review; later bench test | Met by design: about 173 kB per cycle, about 23,000 cycles on 4 GB |
| R7 | Measurement accuracy | Temperature within 0.5 °C at 121 °C; pressure within 5 kPa; field check against boiling water at each site | Component datasheets; calibration method at TRL 3 | Met on datasheets: 0.44 °C with a 0.05 % reference resistor; 5 kPa. The field check needs a reference barometer |
| R8 | Pressure safety | Working pressure 103.4 kPa (15 psi) gauge set by the cooker's regulator; an independent relief valve set at 125 kPa gauge or less; the cooker's own overpressure plug retained; vessel rated by its maker for the working pressure | Design review; relief capacity calculation | Met: relief 5.1 times and vent 2.6 times the worst steam generation; vessel rating to confirm for the chosen model |
| R9 | Heat input control | Operator can stop heat input within 10 s by turning the dish off the sun, and the dish is shaded when parked | Design review | Met: below 5 % of power at 15° off the sun; parking cover in the BOM |
| R10 | Boil-dry protection | At least 0.5 L of water left at the end of a cycle in the design case; logger alarm if base temperature exceeds 140 °C | Water budget; later test | **At risk:** 1.26 L left in the design case, but 0.14 L after a 63 min hold at 1,800 m in strong sun without trimming |
| R11 | Burn and glare protection | No exposed surface above 60 °C within reach during normal operation other than the lid and handles; focal zone guarded; eye protection supplied | Design review | **Not met:** guard not defined; black base and wall band within reach. Goggles and parking cover added. Options in SCL-DDR-001 item 15 |
| R12 | Air removal check | Logger flags any hold where measured temperature is more than 2 °C below the saturation temperature for the measured pressure | Calculation; later test with deliberate air leak | **At risk:** check uncertainty 0.89 °C; sure to flag about 9 % air |
| R13 | Off-grid logger power (redefined 2026-09-25, SCL-DDR-001 item 2) | Logger runs 3 or more days on its own USB power bank without recharging; the bank recharges from any USB source and does not switch off at the logger's low current | Power budget | Met: about 8.7 days |
| R14 | Tracking effort | Retarget no more often than every 15 min; aim by a shadow gnomon without looking at the sun or the focus | Optics calculation | **Not met:** power stays within 10 % of on-target for about 13 min. Options in SCL-DDR-001 item 13 |
| R15 | Stability | Does not tip in a 10 m/s wind with the dish at any tilt and the cooker loaded | Moment calculation | **At risk:** tipping factor 1.30 at 15° elevation; rolls on two locked castors |
| R16 | Portability and build | Total mass 40 kg or less; separates into pieces of 20 kg or less; built with hand tools, a drill and bolted joints | Mass estimate; model check | **Not met:** about 41.0 kg empty; largest piece 19.4 kg (met). Options in SCL-DDR-001 item 14 |
| R17 | Cost (redefined 2026-09-25, SCL-DDR-001 item 2) | Parts for one prototype $450 or less, validation consumables excluded | Priced BOM (`bom/bom.csv`) | Met: $430 |

## Requirements not met or at risk

- **R11 burn and glare (not met).** No focal-zone guard, and the black lower wall is hot and within reach.
- **R14 tracking (not met).** About 13 min between retargets, not 15 min.
- **R16 mass (not met).** About 41.0 kg against 40 kg with the decided timber stand.
- **R4 cycle time (at risk).** Met in the central case (80 min), missed in the unfavourable one (109 min).
- **R10 boil-dry (at risk).** Long option B holds at altitude in strong sun need the dish trimmed.
- **R12 air-removal check (at risk).** The pressure transducer's span limits the check.
- **R15 stability (at risk).** Thin tipping margin at low sun, and the stand can roll.
- **R1 sterilizing condition (not verifiable at TRL 3).** The equivalent-exposure method needs biological indicators.

## Assumptions

- Dish aperture 1.4 m (1.539 m²), focal length 500 mm, reflectance 0.85, slope error 10 mrad, absorber absorptance 0.92; optics by ray trace in SCL-CAL-001.
- Saturated steam temperatures from IAPWS-IF97; ICAO standard atmosphere for ambient pressure with altitude.
- Hold times follow CDC Table 7 and the IARC manual cited in SCL-PRB-001. Equivalent hold at lower temperature uses a z-value of 10 °C, which is a common engineering assumption and not a validated claim.
- "Pass" in R6 means the recorded cycle met R1 and R12. It does not prove sterility; biological and chemical indicators remain the reference.
