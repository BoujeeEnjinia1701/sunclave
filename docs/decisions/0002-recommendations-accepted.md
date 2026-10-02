---
doc_id: SCL-DDR-002
title: SunClave recommendations accepted
project: SunClave
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all open recommendations (items 13 to 18) and the items that remain open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Items 5 and 12 decided by Amish on 2026-10-02 (recommendations approved, SCL-DEC-001)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 13 to 18); items 5 and 12 were decided on 2026-10-02 (SCL-DEC-001)

> **Safety:** SunClave is a research and educational prototype, not a medical device. It concentrates sunlight to a burning intensity and holds steam at about 121 °C (250 °F) in a pressure vessel. Item 5 (mounting the lid fittings) is a pressure-safety trade-off with no recommendation and stays open.

## Context

After the TRL 3 session, SCL-DDR-001 and `docs/REVIEW.md` listed items 5 and 12 to 18 as "Proposed, awaiting Amish". Items 13 to 18 each carried a recommendation; items 5 and 12 did not. On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos."

This record lists what that instruction decides, what changed in the repo because of it, and what stays open. TRL 4 remains on hold by Amish's instruction.

## Options considered

The options for each item are in SCL-DDR-001 Table 2 and `docs/REVIEW.md` (TRL 3 section). Where an item offered several options, the recommended option is the decision.

## Decision

*Table 1. Newly decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 13 | R14 tracking | Option (a): relax R14 to retargeting no more often than every 12 min, with a logger reminder at each interval | SCL-REQ-001 v0.4 R14 relaxed (15 min to 12 min); SCL-CAL-001 v0.2 retargets every 12 min, so the mean absorbed power rises from 630 W to 638 W and the central cycle falls from 79.9 min to 79.0 min; R14 moves from not met to met (about 13 min held against 12 min). The reminder is a firmware rule for the existing buzzer (BOM item 14); no firmware is written |
| 14 | R16 mass | Option (a): relax the total to 45 kg and keep the 20 kg piece limit | SCL-REQ-001 v0.4 R16 relaxed (40 kg to 45 kg); R16 moves from not met to met (41.0 kg; largest piece 19.4 kg); drawing SCL-DWG-001 note updated |
| 15 | R11 guard and hot surfaces | Option (a): restate R11 so the whole pressure vessel and its fittings are a hot zone, reached only with the dish turned off the sun, relying on the parking cover, goggles and a marked keep-out on the ground; no physical guard | SCL-REQ-001 v0.4 R11 restated; new BOM item 21, keep-out marking ($6); SCL-PRC-001 v0.4 safety section; drawing note; R11 moves from not met to met by design review |
| 16 | R15 stability | Option (a): four locking castors instead of two, plus a rule to park the dish face-up in high wind | BOM item 4 ($40 to $44); `cad/src/model.py` adds a brake pedal on each castor (`CASTOR_LOCKS` = 4), STEP and STL re-exported; drawing SCL-DWG-001 Rev P1 to P2; grip rises from 109 N to 218 N against 153 N of wind. The tipping factor stays 1.30, so R15 stays at risk |
| 17 | R10 water at altitude | Option (a): an operating rule to trim the dish off the sun during holds so only a little steam vents, with a water-budget (trim) reminder from the logger | SCL-REQ-001 v0.4 R10 restated to include the rule; the logger shows a trim reminder whenever the computed hold exceeds 40 min; SCL-CAL-001 v0.2 shows 1.31 kg left at 1,800 m and 1.28 kg at 2,400 m in 1,000 W/m² sun with trimming (0.14 kg at 1,800 m untrimmed); R10 moves from at risk to met |
| 18 | R12 transducer span | Adopt a 0 to 300 kPa absolute transducer instead of 0 to 500 kPa, with an overpressure rating above the relief set point | BOM item 14 spec (overpressure 600 kPa or more, same $58); SCL-CAL-001 v0.2 check uncertainty 0.89 K to 0.64 K and pressure accuracy 5 kPa to 3 kPa; R12 moves from at risk to met, narrowly (32 % of the 2 K threshold) |

The budget is unchanged at $450 (`project.yaml`). Parts rise from $430 to $440 (castors $4, keep-out marking $6), a margin of $10.

### Items that remain open

*Table 2. Items with no recommendation here, decided on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| 5 | Mounting the gauge, relief valve and probe gland: drill the maker's lid, or a cooker with factory ports or an adapter plate on the regulator stem | Decided by Amish, 2026-10-02 (recommendation approved, SCL-DEC-001): the maker's lid is not drilled; a pressure canner sold with a factory gauge and relief valve is used, and the probe gland goes on an adapter plate on the vent stem that keeps a bore of 3 mm or more and leaves the overpressure plug untouched; a lid is drilled only with the maker's written approval. |
| 12 | First partner and site for co-design | Decided by Amish, 2026-10-02 (recommendation approved, SCL-DEC-001): first partner to approach is a university biomedical or global health engineering group with an established rural clinic partner in a sunny region below 2,400 m, for example through an Engineering World Health university chapter. |

### Cross-repo actions

None. No decision in this record needs another repo to change.

## Consequences

- SCL-PRC-001 and SCL-REQ-001 move to v0.4, SCL-CAL-001 to v0.2, SCL-DDR-001 to v0.2 and drawing SCL-DWG-001 to Rev P2.
- Requirement status (SCL-CAL-001 v0.2): 14 met, 2 at risk (R4 cycle time, R15 stability), 1 not verifiable at TRL 3 (R1), 0 not met. Before this record: 9 met, 4 at risk, 1 not verifiable, 3 not met. R11, R14 and R16 are met because their targets were restated or relaxed, not because the design improved.
- The retarget and trim reminders are recorded as firmware rules only. Writing and testing firmware, buying parts and building anything are TRL 4 work, which is on hold by Amish's instruction.
- `trl` and `trl_target` stay at 3.
