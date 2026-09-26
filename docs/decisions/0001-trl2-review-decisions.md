---
doc_id: SCL-DDR-001
title: SunClave TRL 2 review decisions
project: SunClave
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 4 and 6 to 11; items 13 to 18 accepted later the same day, see SCL-DDR-002); items 5 and 12 remain proposed, awaiting Amish

> **Safety:** SunClave is a research and educational prototype, not a medical device. It concentrates sunlight to a burning intensity and holds steam at about 121 °C in a pressure vessel. Item 5 (drilling the cooker lid) is a pressure-safety trade-off and is deliberately left open.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed twelve items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The same instruction approved cross-cutting SwapCell interface items, a pricing rule for shared SwapCell packs, and a rule that community designs pick co-design partners per area later.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and SCL-PRC-001 v0.2. They are not repeated here, except for the open items.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Altitude strategy | Decided by Amish, 2026-09-25: go with recommendation. Option B: keep the 103.4 kPa cooker and extend the hold by an equivalent-exposure calculation (z = 10 °C), recorded plainly as a lower-temperature cycle and never labeled 121 °C, with a parallel search for a maker-rated vessel of about 130 kPa gauge (option A) | SCL-REQ-001 v0.3 R1 (redefined), SCL-CAL-001 section 2 |
| 2 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Option (b), then (a) if the savings fall short. The cuts (timber stand, OLED instead of e-paper, a USB power bank instead of the logger panel and cell) save about $29, short of the $37 needed, so `budget_usd` is raised from $400 to **$450** | `project.yaml`, `bom/bom.csv`, SCL-REQ-001 R13 and R17 (redefined) |
| 3 | Pitch wording | Decided by Amish, 2026-09-25: go with recommendation. The pitch now reads "with a calibrated temperature, pressure and time logger that records every cycle" instead of "a validated temperature and time logger to prove each cycle" | `project.yaml`, `README.md` |
| 4 | Pressure vessel | Decided by Amish, 2026-09-25: go with recommendation. A household 12 L aluminum cooker, with a purpose-made sterilizer such as the All-American 1915X only as a reference vessel if a partner already owns one | SCL-PRC-001 v0.3, `bom/bom.csv` item 6 |
| 6 | Level cooker at the focus | Decided by Amish, 2026-09-25: go with recommendation. The cooker stays level at the focus and the dish tilts about it. SCL-CAL-001 section 10 shows the holder must be fixed to the stand (a holder swinging on the axis would be top-heavy); this implements the decision and does not change it | `cad/src/model.py` item 5 |
| 7 | Concentrator type | Decided by Amish, 2026-09-25: go with recommendation. Build the 1.4 m petal dish; use a bought SK14 if the partner already has one | SCL-PRC-001 v0.3 |
| 8 | Aiming | Decided by Amish, 2026-09-25: go with recommendation. Manual aiming with a shadow gnomon; no tracker | SCL-PRC-001 v0.3 |
| 9 | Load limits | Decided by Amish, 2026-09-25: go with recommendation. Solid instruments only, unwrapped or single-wrapped, as a firm limit | SCL-REQ-001 R3 |
| 10 | Logger pass criteria | Decided by Amish, 2026-09-25: go with recommendation. Purge plateau of 5 min or more, hold temperature and time met (the equivalent hold under item 1), and measured temperature within 2 °C of saturation throughout the hold | SCL-REQ-001 R1, R6 and R12 |
| 11 | Backup heat | Decided by Amish, 2026-09-25: go with recommendation. The same cooker on a wood, charcoal or LPG stove on cloudy days, logged the same way | SCL-PRC-001 v0.3 concept of operation |

The problem line had no recommended rewording in the TRL 2 review and is unchanged.

Cross-cutting approvals from the same instruction, recorded here:

- **SwapCell interface v0.3.** Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell interface adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles. SunClave does not use SwapCell (the logger runs from a USB power bank), so no v0.3 items apply.
- **Shared packs are priced once.** Decided by Amish, 2026-09-25 (cross-cutting). Not applicable: SunClave has no SwapCell pack.
- **Co-design partners per area later.** Decided by Amish, 2026-09-25 (cross-cutting): community designs pick co-design partners per area later. Item 12 stays open under this rule.

### Items that remain open

*Table 2. Items left open by this record. Items 13 to 18 were later decided by Amish on 2026-09-25 (SCL-DDR-002); items 5 and 12 remain proposed, awaiting Amish.*

| # | Item | Status and options |
| --- | --- | --- |
| 5 | Mounting the gauge, relief valve and probe gland: (i) drill the maker's lid with reinforcing washers, or (ii) a cooker with factory ports, or an adapter plate on the regulator stem | Proposed, awaiting Amish. No recommendation is recorded: it is a pressure-safety trade-off for Amish. The TRL 3 model shows the fittings on the lid without choosing a method, and SCL-CAL-001 section 8 compares both options on calculable points (holes, ligaments, relief and vent capacity) |
| 12 | First partner and site for co-design | Proposed, awaiting Amish. No recommendation was made; portfolio rule: partners are chosen per area later |
| 13 | R14 tracking: power stays within 10 % of on-target for about 13 min of sun motion, not 15 min | Options: (a) relax R14 to retargeting every 12 min, with a logger reminder; (b) widen the black band on the wall to catch more of the drifting spot, at the cost of more heat loss; (c) hold the petals to a tighter slope error. Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002) |
| 14 | R16 mass: about 41.0 kg against 40 kg, because of the decided timber stand | Options: (a) relax the total to 45 kg and keep the 20 kg piece limit (met at 19.4 kg); (b) lighter timber sections; (c) return to a steel stand (about $15 more). Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002) |
| 15 | R11 guard and hot surfaces: no focal-zone guard is defined, and the black base and band (above 60 °C) are within reach | Options: (a) restate R11 so the whole pressure vessel and its fittings count as a hot zone like the lid, and rely on turning the dish off the sun before reaching in (R9), the parking cover, goggles and a marked keep-out on the ground; (b) design a physical guard at a later revision. A guard cannot close the converging light cone without shading the dish. Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002) |
| 16 | R15 stability: tipping factor 1.30 at 15° elevation, and the 153 N wind force exceeds the grip of two locked castors | Options: (a) four locking castors (about $4 more, within the $20 margin); (b) wheel chocks; (c) ballast. Recommendation: (a), plus a rule to park the dish face-up in high wind. **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002) |
| 17 | R10 at altitude: option B holds in strong sun can leave less than 0.5 L (0.14 kg at 1,800 m and 1,000 W/m²) | Options: (a) an operating rule to trim the dish off the sun during holds so only a little steam vents, with a water-budget warning in the logger; (b) 2.0 L of water above 1,000 m, which leaves only about 8 mm between the water and the basket. Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002) |
| 18 | R12 air-removal check at risk (0.89 K uncertainty against the 2 K threshold) | Option: a 0 to 300 kPa absolute transducer (0.64 K) instead of 0 to 500 kPa, with an overpressure rating above the relief set point. Recommendation: adopt it. **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002) |

## Consequences

- SCL-PRB-001, SCL-PRC-001 and SCL-REQ-001 move to v0.3 with these decisions; the precis no longer lists items 1 to 4 and 6 to 11 as proposed.
- SCL-REQ-001 R1 is restated as an equivalent exposure with the real temperature recorded, R13 as a USB-recharged power bank, and R17 as $450.
- The TRL 3 model, drawing SCL-DWG-001, `bom/bom.csv` and SCL-CAL-001 follow the decided vessel, holder, dish, aiming, timber stand, OLED logger and power bank.
- Items 13 to 18 were decided later on 2026-09-25 and are implemented through SCL-DDR-002. Items 5 and 12 do not change the model or the BOM until Amish decides them.
- TRL 4 work (building, testing, purchasing) is on hold by Amish's instruction, whatever the outcome of the open items.
