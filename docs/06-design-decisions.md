---
doc_id: SCL-DEC-001
title: SunClave design decisions register
project: SunClave
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the TRL 2 and TRL 3 reviews and the design-for-construction work, items to confirm, value engineering and decisions made
---

# SunClave design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** SunClave is a research and educational prototype, not a medical device. Decision 1 below is a pressure-safety decision and must be made before the cooker is ever pressurised with the fittings on its lid.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | How the gauge, relief valve and probe gland are mounted on the cooker | (i) drill the maker's lid with reinforcing washers; (ii) a cooker with factory ports, or an adapter plate on the regulator stem | None: a pressure-safety trade-off for Amish. The calculation (SCL-CAL-001 section 8) applies to both | Build plan step 19 (lid and sensors) and safety stop S6; nothing is pressurised until this is decided | SCL-DDR-001, item 5 |
| 2 | Accept the design-for-construction changes C1 to C9 | Accept; accept with changes; reject | Accept. They keep what SunClave does and make every part makeable and every joint bolted. They also settle the four appearance-model differences noted on 2026-09-26 (logger box height, transducer on the tee, cooker handles, petal seams) | The whole build plan | SCL-DDR-003, Table 1 |
| 3 | R16 mass margin of 0.6 kg (44.4 kg against 45 kg) | (a) accept, weigh the prototype at TRL 4; (b) take about 0.9 kg out now (5 mm yoke plates, 20 x 20 mm holder arms) | (a), with (b) ready | Yoke plates (section 3.14) and holder arms (section 3.15) if (b) | SCL-DDR-003, A1 |
| 4 | Tilt lock: friction only, or a back-up pin | (a) two friction locks as modelled; (b) add a drop pin through holes in the fan | (a) for the prototype; check the slip torque at TRL 4 | Yoke plates and steps 13 and 14 if (b) | SCL-DDR-003, A2 |
| 5 | First partner and site for co-design | Chosen per area later (portfolio rule) | None yet | Not part of the build; sets the altitude and the cooker model | SCL-DDR-001, item 12 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The cooker's maker's rating for 103.4 kPa, its outside diameter (about 288 mm), and handles whose undersides are about 28 mm below the rim and reach at least 214 mm from the centre | The rating is R8; the handles must rest on the 408 mm holder ring and the jacket must clear its 348 mm hole | SCL-DDR-001 item 4, SCL-DDR-003 C3 |
| 2 | The reflector sheet takes a 12 mm flange fold without cracking its bright layer | The petals are fixed by riveting through these flanges | SCL-DDR-003 C6 |
| 3 | A 20 x 3 mm bar bends on edge in the plywood jig without buckling (bend one rib first) | If it buckles, the ribs need a heavier bar or a fabricator's rolls | SCL-DDR-003 C6 |
| 4 | Castor mounting height 102 mm and a top-plate hole pattern on a 42 mm square, all four with brakes | Sets the stand height and the drilling of the cross rails | SCL-DDR-003 C5 |
| 5 | The power bank has a low-current (always-on) mode | The logger draws about 72 mA; many banks switch off below 50 to 100 mA | SCL-CAL-001 section 11 |
| 6 | The relief valve's seat is 4 mm or more and its set pressure is 125 kPa gauge or less, preferably certified | R8 relief capacity | SCL-CAL-001 section 8 |
| 7 | The pressure transducer's overpressure rating is 600 kPa or more | It must survive a relief lift | SCL-DDR-002 item 18 |

## Value engineering

Value-engineering target: USD 450 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 497 (USD 47 over the target), validation consumables (USD 45) excluded. Main cost drivers and savings worth trying:

- The largest lines are the reflector petals (USD 75), the cycle logger (USD 66), the timber stand with castors, axles and plates (USD 58), the cooker (USD 55) and the lid gland, probe and tee (USD 30).
- Making the design constructable added USD 57 (from USD 440): the yoke plates, stand-offs and locks (line 3, USD 18 to 30), the stand's axle plates, axles, collars and brackets (line 4, USD 44 to 58), the clips (line 2), the plate ring and brackets (line 5), the larger logger box and plug-in sensor leads (line 14) and more bolts (line 17).
- Savings worth trying: have one local cutting shop cut the yoke plates, axle plates, holder ring and hub plate from one sheet of steel (likely cheaper than four separate jobs); price aluminised film on plain 0.5 mm aluminium against bright reflector sheet; buy the logger modules as one combined board; buy bolts in boxes of 50 rather than by the piece.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 4 and 6 to 11: altitude option B, budget cuts with USD 450, pitch wording, 12 L household cooker, level cooker at the focus, petal dish, gnomon aiming, load limits, logger pass criteria, backup heat | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | SCL-DDR-001 |
| 2026-09-25 | Items 13 to 18: retarget every 12 min, 45 kg total, whole vessel a marked hot zone, four locking castors, trimming rule, 0 to 300 kPa transducer | Amish: "i accept all your recommendations, go with them across all repos." | SCL-DDR-002 |
| 2026-09-25 | TRL 4 is on hold for the whole portfolio | Amish: "Make sure we don't proceed to TRL 4 on any of them" | SCL-DDR-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SCL-DDR-003 (draft, open for review as decision 2) |
| 2026-09-30 | Open decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register, Value engineering |
