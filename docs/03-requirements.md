---
doc_id: SCL-REQ-001
title: SunClave requirements
project: SunClave
doc_type: Requirements
version: "0.4"
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# SunClave requirements

These requirements are checked by calculation in SCL-CAL-001 at TRL 3. Targets are still proposals, not yet validated with users, and will be revised after co-design sessions (see SCL-PRB-001). R1, R13 and R17 were restated on 2026-09-25 to apply Amish's decisions in SCL-DDR-001 (altitude option B, and the budget cuts and $450 budget). In v0.4, R10, R11, R14 and R16 are restated or relaxed and R12's design basis changed, applying Amish's acceptance of the recommendations in SCL-DDR-002. The status column gives the TRL 3 result from SCL-CAL-001 v0.2; every value is a paper estimate.

The **design case** is a clear day with 700 W/m² direct normal irradiance (DNI) and the sun 60° above the horizon, 25 °C ambient, wind 2 m/s (below 3 m/s), a site at sea level, and a load of 2.0 kg of unwrapped or single-wrapped solid stainless instruments in a 0.5 kg basket, with 1.5 L of water in a 12 L aluminum cooker.

> **Safety:** These requirements describe a pressure vessel heated by concentrated sunlight, in a research and educational prototype that is not a medical device. R8 to R11 are safety requirements and take precedence over throughput and cost. A PASS against R1 and R12 records conditions; it does not prove sterility.

| ID | Requirement | Target | Verification (TRL 3 or later) | TRL 3 status (SCL-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Sterilizing condition (redefined 2026-09-25, SCL-DDR-001 item 1) | Saturated steam in the load zone for an exposure equal to 20 min (unwrapped) or 30 min (wrapped) at 121 °C, using z = 10 °C for any lower temperature; never below 115 °C nor above 124 °C in normal operation; the real temperature and hold are recorded and a cycle below 121 °C is never labeled 121 °C | Calculation; later instrumented cycles with biological indicators | **Not verifiable at TRL 3.** Met by calculation to 2,400 m (120.95 °C and 30.3 min at sea level; 117.7 °C and 63 min at 1,800 m), but the equivalence needs biological-indicator evidence |
| R2 | Load capacity | Basket at least 250 mm diameter by 150 mm deep; 2.0 kg of solid instruments per cycle (about two delivery kits or four suture kits) | Model check | Met: 250 x 150 mm basket in a 12.3 L cooker, 16 mm above the water |
| R3 | Load type | Solid instruments only, unwrapped or single-wrapped in porous wrap; no lumened, hollow or textile loads | Instructions and design review | Met by definition (decided, SCL-DDR-001 item 9) |
| R4 | Cycle time | Cold start to end of hold in 90 min or less in the design case | Energy calculation; later timed cycles | **At risk:** about 79 min central, 70 to 107 min across scenarios |
| R5 | Daily throughput | 3 or more complete cycles on a clear day (DNI 600 W/m² or more from 09:00 to 15:00 solar time) | Energy calculation | Met: 4 cycles in each case checked; zero on overcast days |
| R6 | Cycle record | Load-zone temperature and chamber pressure logged at 1 s intervals from start to end; cycle ID, date and time, hold duration, minimum hold temperature, equivalent exposure and a pass or fail flag stored for 1,000 or more cycles and shown to the operator at cycle end | Design review; later bench test | Met by design: about 173 kB per cycle, about 23,000 cycles on 4 GB |
| R7 | Measurement accuracy | Temperature within 0.5 °C at 121 °C; pressure within 5 kPa; field check against boiling water at each site | Component datasheets; calibration method at TRL 3 | Met on datasheets: 0.44 °C with a 0.05 % reference resistor; 3 kPa with the 0 to 300 kPa transducer. The field check needs a reference barometer |
| R8 | Pressure safety | Working pressure 103.4 kPa (15 psi) gauge set by the cooker's regulator; an independent relief valve set at 125 kPa gauge or less; the cooker's own overpressure plug retained; vessel rated by its maker for the working pressure | Design review; relief capacity calculation | Met: relief 5.1 times and vent 2.6 times the worst steam generation; vessel rating to confirm for the chosen model |
| R9 | Heat input control | Operator can stop heat input within 10 s by turning the dish off the sun, and the dish is shaded when parked | Design review | Met: below 5 % of power at 15° off the sun; parking cover in the BOM |
| R10 | Boil-dry protection (restated 2026-09-25, SCL-DDR-002 item 17) | At least 0.5 L of water left at the end of a cycle in the design case, and at any altitude to 2,400 m in 1,000 W/m² sun when the operator follows the trimming rule; logger shows a trim reminder whenever the computed hold exceeds 40 min; logger alarm if base temperature exceeds 140 °C | Water budget; later test | Met: 1.25 L left in the design case; with trimming 1.31 L at 1,800 m and 1.28 L at 2,400 m (0.14 L at 1,800 m untrimmed). Depends on the operator following the reminder |
| R11 | Burn and glare protection (restated 2026-09-25, SCL-DDR-002 item 15) | The whole pressure vessel and its fittings are a hot zone, like the lid, reached only after the dish is turned at least 15° off the sun (R9); the focus is reached only through the dish, so no physical guard; parking cover and eye protection supplied; a keep-out marked on the ground around the dish and vessel | Design review | Met by design review: parking cover, two pairs of goggles and keep-out marking in the BOM (items 19 to 21) |
| R12 | Air removal check | Logger flags any hold where measured temperature is more than 2 °C below the saturation temperature for the measured pressure | Calculation; later test with deliberate air leak | Met, narrowly: check uncertainty 0.64 °C with the 0 to 300 kPa transducer (SCL-DDR-002 item 18), 32 % of the threshold; sure to flag about 8 % air |
| R13 | Off-grid logger power (redefined 2026-09-25, SCL-DDR-001 item 2) | Logger runs 3 or more days on its own USB power bank without recharging; the bank recharges from any USB source and does not switch off at the logger's low current | Power budget | Met: about 8.7 days |
| R14 | Tracking effort (relaxed 2026-09-25, SCL-DDR-002 item 13) | Retarget no more often than every 12 min, with a logger reminder at each interval; aim by a shadow gnomon without looking at the sun or the focus | Optics calculation | Met: power stays within 10 % of on-target for about 13 min |
| R15 | Stability | Does not tip in a 10 m/s wind with the dish at any tilt and the cooker loaded | Moment calculation | **At risk:** tipping factor 1.30 at 15° elevation. Four locking castors (SCL-DDR-002 item 16) grip 218 N against 153 N of wind; park the dish face-up in high wind |
| R16 | Portability and build (relaxed 2026-09-25, SCL-DDR-002 item 14) | Total mass 45 kg or less; separates into pieces of 20 kg or less; built with hand tools, a drill and bolted joints | Mass estimate; model check | Met: about 41.0 kg empty; largest piece 19.4 kg |
| R17 | Cost (redefined 2026-09-25, SCL-DDR-001 item 2) | Parts for one prototype $450 or less, validation consumables excluded | Priced BOM (`bom/bom.csv`) | Met: $440 |

## Requirements not met or at risk

No requirement is now not met. Before SCL-DDR-002, R11, R14 and R16 were not met; they are met because their targets were restated or relaxed on Amish's acceptance of the recommendations, not because the design improved. R10 and R12 moved from at risk to met through the trimming rule and the 0 to 300 kPa transducer.

- **R4 cycle time (at risk).** Met in the central case (79 min), missed in the unfavourable one (107 min).
- **R15 stability (at risk).** Thin tipping margin at low sun (factor 1.30); the four locking castors now stop the stand rolling.
- **R1 sterilizing condition (not verifiable at TRL 3).** The equivalent-exposure method needs biological indicators.

## Assumptions

- Dish aperture 1.4 m (1.539 m²), focal length 500 mm, reflectance 0.85, slope error 10 mrad, absorber absorptance 0.92; optics by ray trace in SCL-CAL-001.
- Saturated steam temperatures from IAPWS-IF97; ICAO standard atmosphere for ambient pressure with altitude.
- Hold times follow CDC Table 7 and the IARC manual cited in SCL-PRB-001. Equivalent hold at lower temperature uses a z-value of 10 °C, which is a common engineering assumption and not a validated claim.
- "Pass" in R6 means the recorded cycle met R1 and R12. It does not prove sterility; biological and chemical indicators remain the reference.
