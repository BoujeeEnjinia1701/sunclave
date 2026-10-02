---
doc_id: SCL-DDR-003
title: SunClave design for construction
project: SunClave
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish; A1 accepted and A2 decided with a back-up drop pin (changed recommendation)
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 and A2 in Table 3 as written for the register on 2026-10-01 (SCL-DEC-001); A2 was changed to add a back-up drop pin. The changes were made under Amish's 2026-09-30 instruction to make the design physically buildable.

> **Safety:** SunClave is a research and educational prototype, not a medical device. Nothing in this record changes the pressure vessel, its regulator, the relief valve, the lid fittings or the hot-zone rules. The tilt lock and the pivots carry the dish's weight; they are pinch points and are covered by the safety stops in the build plan (SCL-BLD-001).

## Context

On 2026-09-30 Amish asked for every repo to get a prototype build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of SCL-DDR-002 showed what SunClave does but was a massing model: checking it with build123d found parts that overlap, parts that float with no fixing, and parts that cannot be made or assembled as drawn (C1 to C9 below).

The changes keep what SunClave does: the same 1.4 m dish with a 500 mm focal length, the same focal height (950 mm) and tilt axis, the same 15 to 90 degree tilt range, the same 12 L cooker held level at the focus with its base on the focal plane, the same lid fittings, logger, power bank, gnomon aiming and four locking castors. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 66 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must stay apart are apart by the stated clearance, and every moving part stays at least 5 mm clear of every fixed part at 15, 30, 45, 60, 75 and 90 degrees of tilt (2 mm for the yoke plate running past its axle plate, by design). All 66 pass.

## Decision

*Table 1. Problems found in the concept model and the changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| C1 | Pivot and lock: the slotted quadrant plate, the lock lever and the yoke collars all passed through the steel bearing blocks (133 cm³ of overlap); the quadrant floated 11 mm off the upright, and a stub axle in a block had no stated way to carry the yoke. | Each side now has a 6 mm steel axle plate (70 x 270 mm) on the inner face of the upright, a fixed 20 mm steel axle through the upright and plate held by two shaft collars, a 2 mm PTFE thrust washer, and a 6 mm steel yoke plate that turns on the greased axle (a plain pivot, like a gate hinge). The quadrant becomes a fan on each yoke plate with an 11 mm slot on a 150 mm radius; an M10 stud through the upright, the plate and the slot, with a spacer and a star knob, clamps the fan. Both sides lock. | The dish moves a few degrees every 12 min, so a greased plain pivot is enough and needs no bought bearing. Putting the slot on the moving plate lets the fixed stud pass through the timber with its head outside, where there is room. Two locks clamp the dish evenly; at 252 N each they hold the 45 N·m worst gravity torque, and a hand-tight M10 gives about 2,000 N. |
| C2 | The yoke arms (20 mm tubes) stopped 2.2 mm short of the rim; the arms and rim had no joint. A single bolt at each rim point would have let the dish swing about the line through both bolts. | A rim stand-off (50 x 25 x 2.5 mm rectangular tube, 99.5 mm long) each side between the rim band and the end of the yoke plate's arm, clamped by two M8 countersunk screws 30 mm apart with nyloc nuts inside the band. | Two screws per side, spaced across the arm, make the dish and yoke one rigid unit. Countersunk heads keep the yoke plate's outer face flush, so it can pass the upright 6 mm away. |
| C3 | Pot holder: the ring overlapped the jacket (569 cm³) and sat 28 mm below the cooker handles, so the cooker was not held. The handle was drawn as one block through the cooker. | A flat ring cut from 4 mm steel plate (348 mm inside, 408 mm outside diameter) at the level of the handle undersides; each handle rests on it; the jacket clears the inner edge by 5 mm. The ring sits on the two holder arms (25 x 25 x 2 mm tube), one M8 bolt each. The handles are drawn outside the wall. | A flat ring is simpler to make than a rolled band and gives the handles a flat seat. The cooker drops in and lifts out without tools, as the concept intended. |
| C4 | The holder arms ended against the timber with no fixing. | Each arm rests on the top of its upright, flush with the outer face, and on the flat leg of a 40 x 40 x 4 mm angle bracket bolted to the upright's inner face; two M8 bolts. The uprights end at the arms (1,099 mm). | The arm bears on the timber and the bracket; nothing depends on screws in end grain. |
| C5 | Stand: braces butted into the rails and uprights with overlaps and no fixings; uprights stood on the rails with no fixing; the frame rails met at one level with no joint; a 75 mm castor was drawn 80 mm tall. | Side rails turned on edge (45 x 70 mm) and laid across the ends of the cross rails, two M8 bolts at each crossing. Uprights turned so they are 45 mm along the tilt axis and 70 mm across it, standing on the side rails with two galvanised angle brackets each. Braces lapped flat on the upright and side rail faces (the front brace outside, the back brace inside), one M10 bolt at each foot and one through both braces and the upright at the top. Castors at their real 102 mm mounting height, inboard of the side rails, each on four M8 bolts into the cross rail; the cross rails run 40 mm past the side rails so the crossing bolts are clear of the rail ends. | Every timber joint is face to face and bolted, so the stand comes apart into two side frames (6.0 kg each) and two cross rails with castors (3.4 kg each). With the upright and side rail both 45 mm wide, their outer faces line up and a brace can lie flat on both. |
| C6 | Dish frame: the ribs were drawn into the reflector sheet (36 cm³), their inner ends only touched the hub plate's edge and their outer ends stopped 10 mm short of the rim, with no fixings; a petal had nothing to rivet to on a rib standing on edge. | Ribs (20 x 3 mm, on edge) sit just behind the sheet. Each petal has a 12 mm flange folded down along both long edges; neighbouring flanges lie either side of a rib and one rivet goes through both flanges and the rib. Each rib's inner end stands on a 200 mm hub plate, 4 mm thick (was 150 x 6 mm) and its outer end meets the rim band, each joint held by a clip cut from 20 x 20 x 3 mm angle (24 clips, M5 bolts). The rim band is 25 x 4 mm (was 20 x 4 mm); each petal has two tabs riveted inside it. Ribs are at 15 degrees plus 30 degree steps, so none is under a rim stand-off. | Rivets need a face to grip; the flanges give one without changing the rib or the petal layout. The clips are the simplest bolted joint between a bar on edge and a flat plate or band. The 3 to 5 mm seam over each rib is what the photoreal model already shows. |
| C7 | The gnomon's target plate was drawn on the reflector face, overlapping the petals and ribs, with no fixing. | The target plate (120 mm, 3 mm aluminium) and its pin sit on a 40 x 40 x 4 mm angle bracket bolted to the outside of the rim band at the dish's lowest point, between two ribs. | Outside the rim it shades no reflector, it is reachable from the ground, and it bolts to steel. The pin stays parallel to the dish axis, so aiming is unchanged. |
| C8 | The power bank hung below the logger box, outside it (the BOM says it is inside), and the cable to the lid ran through the lid gland. No pressure transducer was drawn on the tee. | A bought IP65 box about 180 x 80 x 65 mm holds the board, display and power bank, screwed to the outer face of the right-hand upright below the lock stud. The cable leaves through a gland, runs along the top of the right holder arm and up to the transducer, now drawn on the tee, with plugs at the lid and the box so the lid comes off. The base thermocouple is held on the bare band by a stainless band clamp. | Completes BOM line 14 as described; the box sits below the lock stud and above the braces, and the plugs let the operator open the lid without cutting wires. |
| C9 | Assembly: with the yoke plates fixed to the dish, no order of assembly let the dish go between the uprights, because the yoke plates would have needed to slide down a 6 mm gap with no clearance. | The 2 mm PTFE thrust washer sets a 2 mm gap between each yoke plate and its axle plate. The build order fits one axle plate, lowers the dish (with its yoke plates) in from above, then slides the second axle plate down into the 8 mm space left, and pushes the axles in from outside. | A build order that works with two people and no lifting gear; the washer also makes the tilt smoother. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Empty total 44.4 kg (was 41.0 kg) against the 45 kg of R16, 0.6 kg of margin, now taken from the model's parts rather than estimated. Largest piece 15.4 kg (the dish with its yoke plates), against 20 kg; the stand now comes apart, so the 19.4 kg one-piece stand of v0.2 is gone. | Steel clips, plates, brackets and bolts added; rim and hub slightly larger. |
| Optics | Absorbed power 663 W in the design case (was 669 W): the holder ring is wider than before and now counted in the ray trace with the handles. Cycle 80 min central (was 79), 109 min unfavourable (was 107). | Ring sized to carry the handles. |
| Stability | Tipping factor 1.38 at 15 degrees (was 1.30): the heavier tilting group and the slightly wider castor line help. R15 stays at risk. | Follows the model. |
| Lock | The tilting group (15.4 kg, centre of mass 321 mm from the axis) puts up to 45 N·m on the locks at 15 degrees (was 38 N·m for the dish alone). | The yoke plates now tilt with the dish and are counted. |
| Cost | Estimated cost of the constructable design USD 497 against the USD 450 value-engineering target (USD 47 over). BOM lines 1 to 5, 14, 16 and 17 respecified and repriced; no new lines. | Parts added for construction. |
| Drawings and documents | SCL-DWG-001 Rev P3; making sketches SCL-DWG-101 to 118 added; SCL-CAL-001 v0.3, SCL-REQ-001 v0.5 and SCL-PRC-001 v0.5 updated; build plan SCL-BLD-001 and register SCL-DEC-001 added. | Follows the model. |

*Table 3. Proposed for Amish; decided on 2026-10-02 as shown under each recommendation.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The R16 mass margin is now 0.6 kg (44.4 kg against 45 kg), on modelled parts and catalogue masses. | (a) accept and weigh the prototype at TRL 4; (b) take mass out now, for example 5 mm yoke plates and 20 x 20 mm holder arms (about 0.9 kg). | (a), with (b) ready if the weighed prototype is over. Accepted by Amish, 2026-10-02. |
| A2 | The tilt lock is a friction clamp (two star knobs), like the concept's lever on a slotted quadrant. A positive lock (a pin through holes at fixed elevations) would not slip, but sets the aim in steps. | (a) friction locks as modelled; (b) add a drop pin through a row of holes in the fan as a back-up. | (a) for the prototype, and check the slip torque at TRL 4; this is a pinch-point safety trade-off, so it is Amish's call. Changed in the recommendation to Amish and decided on 2026-10-02: (a) for aiming plus (b), a drop pin through a row of holes in the fan as a back-up stop, so a slip is limited to one hole; the pin is removed only if the TRL 4 slip test shows the locks holding at least twice the 45 N·m worst torque. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SCL-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 14 met, 2 at risk (R4, R15), 1 not verifiable at TRL 3 (R1); R17 is reported against the value-engineering target (USD 47 over), not as met or not met (SCL-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept's tube yoke, quadrant, bearing blocks, holder and stand; they need updating on Amish's Mac.
- The lid-fitting method (SCL-DDR-001 item 5) was decided on 2026-10-02: the maker's lid is not drilled; a pressure canner sold with a factory gauge and relief valve is used, and the probe gland goes on an adapter plate on the vent stem that keeps a bore of 3 mm or more and leaves the overpressure plug untouched; a lid is drilled only with the maker's written approval. The model still shows the fittings on the lid and must be updated (`docs/REVIEW.md`, 2026-10-02).
- With A2 decided, a back-up drop pin is to be added to the yoke plates and stand; with A1 accepted, the prototype is weighed at TRL 4.
