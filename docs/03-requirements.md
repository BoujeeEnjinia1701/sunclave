---
doc_id: SCL-REQ-001
title: SunClave requirements
project: SunClave
doc_type: Requirements
version: "0.2"
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
---

# SunClave requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see SCL-PRB-001). The status column gives the first-order estimate from SCL-PRC-001; every status is an estimate.

The **design case** is a clear day with 700 W/m² DNI, 25 °C ambient, wind below 3 m/s, a site near sea level, and a load of 2.0 kg of unwrapped or single-wrapped solid stainless instruments in a 0.5 kg basket, with 1.5 L of water in a 12 L aluminum cooker.

> **Safety:** These requirements describe a pressure vessel heated by concentrated sunlight. R8 to R11 are safety requirements and take precedence over throughput and cost.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Sterilizing condition | Saturated steam at 121 °C or more, and not above 124 °C, held for 20 min (unwrapped) or 30 min (wrapped), measured in the load zone | Calculation; later instrumented cycles with biological indicators | Met near sea level; **not met above about 300 m** with a 103 kPa cooker (about 118 °C at 1,800 m) |
| R2 | Load capacity | Basket at least 250 mm diameter by 150 mm deep; 2.0 kg of solid instruments per cycle (about two delivery kits or four suture kits) | Model check | Met by design (270 x 180 mm basket) |
| R3 | Load type | Solid instruments only, unwrapped or single-wrapped in porous wrap; no lumened, hollow or textile loads | Instructions and design review | Met by definition; a limit of the concept |
| R4 | Cycle time | Cold start to end of hold in 90 min or less in the design case | Energy calculation; later timed cycles | Met on estimate (about 55 to 90 min); **at risk**, since Kaseman et al. measured 93 to 183 min heat-up with a larger vessel |
| R5 | Daily throughput | 3 or more complete cycles on a clear day (DNI 600 W/m² or more from 09:00 to 15:00 solar time) | Energy calculation | Met on estimate (about 3); zero on overcast days |
| R6 | Cycle record | Load-zone temperature and chamber pressure logged at 1 s intervals from start to end; cycle ID, date and time, hold duration, minimum hold temperature and a pass or fail flag stored for 1,000 or more cycles and shown to the operator at cycle end | Design review; later bench test | Met by design |
| R7 | Measurement accuracy | Temperature within 0.5 °C at 121 °C; pressure within 5 kPa; field check against boiling water at each site | Component datasheets; calibration procedure at TRL 3 | Met on datasheets (Pt100 class A about 0.4 °C); pressure about 5 kPa, marginal for R12 |
| R8 | Pressure safety | Working pressure 103 kPa (15 psi) gauge set by the cooker's regulator; an independent relief valve set at 125 kPa gauge or less; the cooker's own overpressure plug retained; vessel rated by its maker for the working pressure | Design review | Met by design |
| R9 | Heat input control | Operator can stop heat input within 10 s by turning the dish off the sun, and the dish is shaded when parked | Design review | Met by design |
| R10 | Boil-dry protection | At least 0.5 L of water left at the end of a cycle in the design case; logger alarm if base temperature exceeds 140 °C | Water budget; later test | Met on estimate (about 1.0 L left) and by design (base thermocouple in the logger) |
| R11 | Burn and glare protection | No exposed surface above 60 °C within reach during normal operation other than the lid and handles; focal zone guarded; eye protection supplied | Design review | Partly met; guard not yet defined |
| R12 | Air removal check | Logger flags any hold where measured temperature is more than 2 °C below the saturation temperature for the measured pressure | Calculation; later test with deliberate air leak | Met by design; resolution limited by R7 pressure accuracy |
| R13 | Off-grid logger power | Logger runs 3 or more days with no sun on its own battery and recharges from its own panel | Power budget | Met on estimate (about 5 days) |
| R14 | Tracking effort | Retarget no more often than every 15 min; aim by a shadow gnomon without looking at the sun or the focus | Optics estimate | Met on estimate |
| R15 | Stability | Does not tip in a 10 m/s wind with the dish at any tilt and the cooker loaded | Moment calculation | Met on estimate, thin margin (ballast may be needed) |
| R16 | Portability and build | Total mass 40 kg or less; separates into pieces of 20 kg or less; built with hand tools, a drill and bolted joints | Mass estimate; model check | Met on estimate (about 33 kg) |
| R17 | Cost | Parts for one prototype $400 or less, validation consumables excluded | Priced BOM (`bom/bom.csv`) | **Not met:** about $437 (about 9 % over) |

## Requirements not met or at risk

- **R1 at altitude (not met).** A cooker regulated at 103 kPa above ambient reaches 121 °C only below about 300 m. See the options in SCL-PRC-001.
- **R17 cost (not met).** About $437 against $400.
- **R4 cycle time (at risk).** The estimate is well below the only measured precedent.
- **R11 guard (not yet in the concept).** A focal-zone guard needs to be defined at TRL 3.

## Assumptions

- Dish aperture 1.4 m (1.54 m²), overall optical efficiency about 73 % (reflectance, spillage and shading), pot base absorptance about 0.9.
- Saturated steam temperatures from the Antoine equation for water; standard atmosphere for ambient pressure with altitude.
- Hold times follow CDC Table 7 and the IARC manual cited in SCL-PRB-001. Equivalent hold at lower temperature uses a z-value of 10 °C, which is a common engineering assumption and not a validated claim.
- "Pass" in R6 means the recorded cycle met R1 and R12. It does not prove sterility; biological and chemical indicators remain the reference.
