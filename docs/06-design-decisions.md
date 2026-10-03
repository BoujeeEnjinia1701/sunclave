---
doc_id: SCL-DEC-001
title: SunClave design decisions register
project: SunClave
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the TRL 2 and TRL 3 reviews and the design-for-construction work, items to confirm, value engineering and decisions made
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Amish approved the recommendations for open decisions 1 to 5 (lid fittings decided; SCL-DDR-003 accepted with a back-up drop pin); moved to decisions made
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Canner, adapter plate and drop pins priced and carried into the design; value engineering and items to confirm updated"
---

# SunClave design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** SunClave is a research and educational prototype, not a medical device. Decision 1 below is a pressure-safety decision and must be made before the cooker is ever pressurised with the fittings on its lid.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The canner's maker's rating for 103.4 kPa, its outside diameter (about 288 mm), its mass with fittings (about 4.8 kg, 5.0 kg at most), and handles whose undersides are about 28 mm below the rim and reach at least 214 mm from the centre | The rating is R8; the handles must rest on the 408 mm holder ring and the jacket must clear its 348 mm hole; the mass margin of R16 is 0.2 kg | SCL-DDR-001 items 4 and 5, SCL-DDR-003 C3 |
| 2 | The reflector sheet takes a 12 mm flange fold without cracking its bright layer | The petals are fixed by riveting through these flanges | SCL-DDR-003 C6 |
| 3 | A 20 x 3 mm bar bends on edge in the plywood jig without buckling (bend one rib first) | If it buckles, the ribs need a heavier bar or a fabricator's rolls | SCL-DDR-003 C6 |
| 4 | Castor mounting height 102 mm and a top-plate hole pattern on a 42 mm square, all four with brakes | Sets the stand height and the drilling of the cross rails | SCL-DDR-003 C5 |
| 5 | The power bank has a low-current (always-on) mode | The logger draws about 72 mA; many banks switch off below 50 to 100 mA | SCL-CAL-001 section 11 |
| 6 | The canner's factory relief valve has a seat of 4 mm or more and a set pressure of 125 kPa gauge or less; the lid's vent-pipe hole and thread, for the adapter plate | R8 relief capacity; the adapter plate is made to fit the canner | SCL-CAL-001 section 8 |
| 7 | The pressure transducer's overpressure rating is 600 kPa or more | It must survive a relief lift | SCL-DDR-002 item 18 |

## Value engineering

Value-engineering target: USD 450 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 528 (USD 78 over the target), validation consumables (USD 45) excluded. Main cost drivers and savings worth trying:

- The largest lines are the pressure canner with its gauge and relief valve (USD 100), the reflector petals (USD 75), the cycle logger (USD 66), the timber stand with castors, axles and plates (USD 58) and the adapter plate, gland and probe (USD 45).
- Making the design constructable added USD 57 (from USD 440): the yoke plates, stand-offs and locks (line 3, USD 18 to 30), the stand's axle plates, axles, collars and brackets (line 4, USD 44 to 58), the clips (line 2), the plate ring and brackets (line 5), the larger logger box and plug-in sensor leads (line 14) and more bolts (line 17).
- The decisions of 2026-10-02 added USD 31 (from USD 497): the pressure canner sold with its gauge and relief valve (line 6, USD 55 to 100) in place of the household cooker and the separate gauge and relief valve (lines 8 and 9, USD 35, now supplied with the canner), the vent-stem adapter plate (line 10, USD 30 to 45) and the drop pins and lanyards (line 3, USD 30 to 36).
- Savings worth trying: compare canners sold with a gauge in the target area, since line 6 is now the largest line; have one local cutting shop cut the yoke plates, axle plates, holder ring and hub plate from one sheet of steel (likely cheaper than four separate jobs); price aluminised film on plain 0.5 mm aluminium against bright reflector sheet; buy the logger modules as one combined board; buy bolts in boxes of 50 rather than by the piece.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 4 and 6 to 11: altitude option B, budget cuts with USD 450, pitch wording, 12 L household cooker, level cooker at the focus, petal dish, gnomon aiming, load limits, logger pass criteria, backup heat | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SCL-DDR-001 |
| 2026-09-25 | Items 13 to 18: retarget every 12 min, 45 kg total, whole vessel a marked hot zone, four locking castors, trimming rule, 0 to 300 kPa transducer | Amish: "i accept all your recommendations, go with them across all repos." | SCL-DDR-002 |
| 2026-09-25 | TRL 4 is on hold for the whole portfolio | Amish: "Make sure we don't proceed to TRL 4 on any of them" | SCL-DDR-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SCL-DDR-003 (accepted on 2026-10-02, below; was open for review as decision 2) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register, Value engineering |
| 2026-10-02 | Lid fittings: the maker's lid is not drilled; a pressure canner sold with a factory gauge and relief valve is used, and the probe gland goes on an adapter plate on the vent stem that keeps a bore of 3 mm or more and leaves the overpressure plug untouched; a lid is drilled only with the maker's written approval | Amish: "i approve your recommendations for all 555 open decisions." | SCL-DDR-001, item 5 |
| 2026-10-02 | Design for construction accepted: the changes C1 to C9, as made, with the tilt lock settled under decision 4 | Amish: "i approve your recommendations for all 555 open decisions." | SCL-DDR-003, Table 1 |
| 2026-10-02 | R16 mass margin of 0.6 kg accepted; the prototype is weighed at TRL 4, with the 5 mm yoke plates and lighter holder arms ready | Amish: "i approve your recommendations for all 555 open decisions." | SCL-DDR-003, A1 |
| 2026-10-02 | Tilt lock: the two friction locks are kept for aiming and a drop pin through a row of holes in the fan is added as a back-up stop; the pin is removed only if the TRL 4 slip test shows the locks holding at least twice the 45 N·m worst torque | Amish: "i approve your recommendations for all 555 open decisions." | SCL-DDR-003, A2 |
| 2026-10-02 | First partner to approach: a university biomedical or global health engineering group with an established rural clinic partner in a sunny region below 2,400 m, for example through an Engineering World Health university chapter | Amish: "i approve your recommendations for all 555 open decisions." | SCL-DDR-001, item 12 |
