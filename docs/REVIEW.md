# Review note: SunClave

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out ("APPROVED CHANGES, COMPLETE THESE"). Nothing was built or tested; TRL 4 remains on hold. SunClave remains a research and educational prototype, not a medical device.

### Approved follow-ups carried out

Done 8 of 11:

1. Done. BOM line 6 is now a pressure canner of about 12 L sold with a factory gauge and relief valve (USD 55 to 100, indicative); lines 8 and 9 are the factory-fitted gauge and relief valve at no extra cost; line 10 is the vent-stem adapter plate with gland and probe, 6 mm bore round the probe, equal to a 5.2 mm hole (USD 30 to 45). `bom/bom.csv`, `bom/bom-notes.md`.
2. Done. `cad/src/model.py`: the canner with its factory gauge, relief valve and overpressure plug; the lid's vent-pipe hole (not drilled); the adapter plate with spigot and nut carrying the gland, probe, transducer and the maker's vent pipe and weight. New checks: adapter on the lid boss, gland and transducer on the adapter, probe clear in the bore (steam passes round it), adapter clear of the gauge and relief valve, probe tip clear of the load, factory fittings on the lid, equivalent bore 3 mm or more. The canner keeps the 288 mm outside diameter; its handles rest on the holder ring, the jacket clears the ring by 5 mm and its base is on the focal plane. STEP and STL regenerated; `python cad/src/model.py --check`: 81 of 81 checks pass (was 66), including the 15 to 90 degree tilt sweep.
3. Done. SCL-CAL-001 v0.4 section 8 restated for the factory relief valve (5.2 times the worst steam generation if its seat is 4 mm or more and it is set at 125 kPa gauge or less) and the adapter's vent path (8.0 times; the regulator's own 3 mm vent 2.7 times); the "open for Amish" rows for item 5 and SCL-DDR-003 replaced by the decisions of 2026-10-02; the canner checked against the holder and R16 (4.8 kg as bought, indicative; vessel 5.9 kg; empty total 44.8 kg).
4. Done. Build plan step 19 and the canner pictures (overview, steps 18 and 19, joint 12, sketches 117 and 118) show the canner, its factory gauge and relief valve and the adapter plate; new making sketch SCL-DWG-120 for the adapter plate.
5. Done. A row of eleven 8.5 mm holes on a 163 mm radius, 7.5 degrees apart, in each yoke plate fan; a 7.5 degree arc slot in each axle plate (now 285 mm long); a 10 x 32 mm slot through each upright; an 8 mm drop pin pushed in from outside on a lanyard to an eye screw on the upright. To make room the lock slot moved from a 150 mm to a 140 mm radius (clamp force needed 270 N per knob, was 252 N) and the logger box moved down 20 mm. New checks for the pins (through a fan hole, in the plate slot, through the upright slot, clear of the lock knobs and logger box, clear of the dish, a fan hole in the slot at every elevation from 15 to 90 degrees). The pins are pulled out to re-aim, so they are not in the tilt sweep.
6. Done. Yoke plate making sketch SCL-DWG-114 and the yoke layout picture show the pin hole row; new making sketch SCL-DWG-119 for the drop pin; upright (SCL-DWG-103) and axle plate (SCL-DWG-105) sketches show the slots.
7. Done. Joint 6 shows the drop pin; step 14 fits the pins; step 13 regenerated (longer axle plates and the slot in the uprights; the pins go in at step 14, once the lock studs are in); the "Tilt lock holds" check now includes the pins.
8. Done. BOM line 3 includes two drop pins with lanyards and eye screws (USD 30 to 36).
9. Not done: TRL 4 work (slip test plan), on hold.
10. Not done: TRL 4 work (weighing plan), on hold.
11. Not done here: the photoreal renders, card and social preview are made on Amish's Mac. Prepared for it: `cad/src/product_model.py` rebuilt on the constructable design and render scenes exported to `/home/claude/renders/sunclave` (hero, exploded, detail).

### Documents changed and new versions

- `docs/04-calcs/01-sizing.md` (SCL-CAL-001 v0.4), `docs/04-calcs/sizing.py`, `docs/04-calcs/results.csv`
- `docs/05-build-plan.md` (SCL-BLD-001 v0.3): new sections 3.20 (drop pins) and 3.21 (adapter plate); bought components, steps 14 and 17 to 19, first checks and safety stop S6 updated
- `docs/02-concept.md` (SCL-PRC-001 v0.7), `docs/03-requirements.md` (SCL-REQ-001 v0.7), `docs/06-design-decisions.md` (SCL-DEC-001 v0.3), `docs/decisions/0003-design-for-construction.md` (SCL-DDR-003 v0.3)
- `cad/src/model.py`, `cad/step/*.step`, `cad/stl/*.stl`; `cad/src/sheets.py` and SCL-DWG-001 Rev P4
- `cad/src/build_plan_media.py`: making sketches SCL-DWG-103, 105, 114, 117 and 118 regenerated, SCL-DWG-119 and 120 new; overview, yoke layout, all joint and step pictures regenerated
- `cad/src/concept_media.py` and the concept media in `media/`
- `cad/src/product_model.py` (appearance model)
- `bom/bom.csv`, `bom/bom-notes.md`, `README.md` (not controlled documents)
- `docs/pdf/`: every controlled document re-rendered

### Key results (SCL-CAL-001 v0.4)

- No requirement changed status: 13 met, 2 at risk (R4, R15), 1 not verifiable at TRL 3 (R1); R17 reported against the target.
- R16 mass: 44.8 kg against 45 kg (was 44.4 kg), so the margin is now 0.2 kg. Met, but thinner than the 0.6 kg Amish accepted; a canner heavier than about 5.0 kg would take it over.
- R4: 81 min central, 72 to 111 min (was 80, 71 to 109): the canner's heavier body takes longer to heat.
- R15: tipping factor 1.40 (was 1.38).
- R8: met on capacity; the factory relief valve's seat and set pressure are purchase criteria, not known values.
- Value-engineering target: USD 450. Estimated cost of the constructable design: USD 528 (USD 78 over the target; was USD 497).

### Proposed, awaiting Amish

1. **R16 margin of 0.2 kg.** Options: (a) keep the accepted plan and weigh at TRL 4; (b) adopt the 5 mm yoke plates and lighter holder arms now. Recommendation: (a), and choose a canner of 5.0 kg or less with its fittings.
2. **Appearance model.** `cad/src/product_model.py` now takes every part from the constructable model; the appearance details (petal rivets, hub cap, canner rim, handle grips, jacket seams, gauge face, logger display and labels) add no BOM lines. The 2026-09-26 differences (taller logger enclosure, transducer on the tee, handles, petal seams) no longer apply. Recommendation: accept.

### Cross-repo actions

None.

### Safety

The canner's lid is never drilled; the factory relief valve and overpressure plug are untouched; the adapter plate's joint has no rating until the hydrostatic check of safety stop S6 (TRL 4 work). The drop pins are pinch points and must be pulled out before the knobs are loosened to re-aim; both are in the build plan.

### Recommended next step

Render session on Amish's Mac from the exported scenes, then `python .kit/cards.py .`. TRL 4 remains on hold.

## Session 2026-10-01: kit 1.7.0, constructable design and prototype build plan

Following Amish's 2026-09-30 approval of the build plan format ("this is the correct build plan ... Extend this across all the other repos"), his instruction to make each design physically buildable, and his 2026-10-01 note that budgets are value-engineering targets.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced with `.kit/CLAUDE.md`.
- Constructability review with build123d of the TRL 3 model: nine problems found (overlaps, floating parts, parts with no fixing, no feasible assembly order), listed in `docs/decisions/0003-design-for-construction.md` (SCL-DDR-003 v0.1, Draft: made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review).
- `cad/src/model.py` rewritten as a part-by-part constructable model with `python cad/src/model.py --check`: 66 checks (contacts, clearances and a 15 to 90 degree tilt sweep), all passing. STEP and STL regenerated in `cad/step/` and `cad/stl/`.
- `bom/bom.csv` lines 1 to 5, 14, 16 and 17 respecified and repriced; `bom/bom-notes.md` updated.
- `docs/04-calcs/sizing.py` now takes the structure's masses and the tilting group's centre of mass from the model, adds the holder ring and handles to the ray trace, computes the lock clamp force, and reports cost against the value-engineering target. SCL-CAL-001 v0.3, SCL-REQ-001 v0.5 and SCL-PRC-001 v0.5 updated.
- `cad/src/sheets.py`: SCL-DWG-001 Rev P3.
- `cad/src/build_plan_media.py` (new): overview, 18 making sketches (SCL-DWG-101 to 118), petal flat pattern and yoke plate layout, 14 joint close-ups and 19 assembly step pictures in `docs/05-build-plan/` and `cad/drawings/`.
- `docs/05-build-plan.md` (SCL-BLD-001 v0.1) and `docs/06-design-decisions.md` (SCL-DEC-001 v0.1) written; `project.yaml` has `design_state: constructable` and both in `trl_evidence`; README links line and "Building the prototype" section added; concept media regenerated.

### Design changes made for construction

1. Pivots: steel axle plates on the uprights, fixed 20 mm axles with collars, PTFE thrust washers, and 6 mm yoke plates that turn on the axles (replacing the bearing blocks, stub axles and collars, which overlapped).
2. Tilt lock: a slotted fan on each yoke plate clamped by a star knob on a fixed M10 stud, both sides (replacing the quadrant plate and lever, which passed through the bearing block).
3. Yoke to dish: a rectangular tube stand-off each side, clamped to the rim band by two M8 countersunk screws (the tube arms stopped short of the rim, and one bolt per side would have let the dish swing).
4. Pot holder: a flat steel ring the cooker handles rest on, on tube arms carried on the upright tops and angle brackets (the ring ran through the jacket and sat 28 mm below the handles).
5. Stand: side rails on edge across the cross rails, uprights turned 90 degrees on angle brackets, braces lapped and bolted, real 102 mm castors bolted inboard of the side rails, cross rails 40 mm longer for bolt end distance.
6. Dish frame: petals with folded flanges riveted through the ribs and tabs riveted to the rim; rib clips at the hub and rim; hub plate 200 x 4 mm; rim band 25 x 4 mm; ribs offset 15 degrees from the stand-offs.
7. Gnomon on a bracket outside the rim band (it sat on the reflector face with no fixing).
8. Logger box sized to hold the power bank, below the lock stud; transducer on the tee; plug-in sensor leads; thermocouple band clamp.
9. Assembly order made possible: a 2 mm gap at each pivot, one axle plate fitted after the dish is in.

### Key results (SCL-CAL-001 v0.3)

- Absorbed power 663 W in the design case (was 669 W); cycle 80 min central, 71 to 109 min (R4 at risk).
- Mass 44.4 kg against 45 kg (R16 met, 0.6 kg margin, was 41.0 kg); largest piece 15.4 kg; the stand now comes apart.
- Tipping factor 1.38 at 15 degrees (was 1.30; R15 at risk). Lock torque up to 45 N·m, 252 N clamp per knob needed.
- Value-engineering target: USD 450. Estimated cost of the constructable design: USD 497 (USD 47 over the target; was USD 440).
- Requirement status: 13 met, 2 at risk (R4, R15), 1 not verifiable at TRL 3 (R1), 0 not met; R17 reported against the value-engineering target.

### Decisions proposed and awaiting Amish

All are in the design decisions register (`docs/06-design-decisions.md`): accept SCL-DDR-003 (recommended; it also settles the four appearance-model differences of 2026-09-26); the 0.6 kg mass margin (A1); friction locks or a back-up pin (A2); and, unchanged, the lid-fitting method (item 5) and the first partner and site (item 12).

### Safety

No change to the pressure vessel, regulator, relief valve, lid fittings or hot-zone rules. The new pivots and locks are pinch points (the fans close like scissors as the dish tilts) and the locks are friction clamps; they are covered by safety stop S2, and the choice of a back-up pin is open as A2. The build plan stops before the cooker is pressurised (S6). SunClave remains a research and educational prototype, not a medical device.

### Stale until refreshed on Amish's Mac

The design changed visibly, so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept's tube yoke, quadrant, bearing blocks, holder and stand. They were not regenerated here.

### Recommended next step

Amish reviews SCL-DDR-003 and the register. TRL 4 remains on hold.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (94 parts: 61 shell, 28 internal, 4 accessory, 1 context), `TITLE` and `RENDER_VIEWS` (hero, exploded, and a detail view of the cooker at the focus without the dish, stand or ground). It imports PARAMS, derived(), dish_local(), to_world(), point_world() and tilt_of() from `cad/src/model.py`; the dish diameter and focal length, the tilt pose, the focal height, the stand, castor and bearing positions, the cooker, lid, jacket, basket and lid fitting positions and the logger position are as model.py. It adds:

- Dish: the reflector split into 12 petals with visible seams over the ribs, paired rivet rows along each seam, a hub cap with bolts; painted steel ribs, rim and hub; the gnomon with a white target plate, teal target rings and a stainless pin. In the exploded view the petals move radially outward so the ribs show between them.
- Tilt yoke with bearing collars and grease bosses, the lock lever and a knurled black knob; the slotted quadrant plate with white tick marks.
- Timber stand with rounded arrises, carriage bolts, painted steel bearing blocks with bolt heads and axle caps, and four castors with rubber wheels, zinc forks and teal brake pedals.
- Level pot holder ring and arms.
- Cooker: aluminum body with a rolled rim, the blackened base and lower wall band, handle brackets with black phenolic grips; the aluminized jacket with stitched seams, two straps and buckles; the lid with a gasket line, boss, phenolic handle, vent pipe and weighted regulator.
- Lid fittings: the pressure gauge with stainless case, dial, scale marks, red zone, needle and clear glass; the brass relief valve with its test ring; the brass lid gland, Pt100 sheath and tee; the pressure transducer with its connector.
- Inside the cooker: water charge, perforated stainless basket on its trivet, and a wrapped instrument pack with indicator tape in place of model.py's instrument load block (same size and position).
- Logger: IP65 enclosure with side ribs, lid and screws, OLED display with a lit readout, two teal buttons, a lit green PASS light and an unlit red FAIL light, buzzer grille, rating label, teal name band, cable glands and mounting straps round the upright; inside, the logger board and modules, microSD holder and the USB power bank (exploded view only); the cable from the logger to the lid.
- Context (not in the BOM): a compact paved ground patch under the stand. No mannequin, because SunClave is used standing still at a fixed spot.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files.

### Differences from model.py (Proposed, awaiting Amish)

1. **Logger enclosure height.** BOM line 15 says the power bank is kept in the logger box, but model.py draws a 60 x 150 x 110 mm logger box with the 50 x 140 x 60 mm power bank hanging below it, outside. The appearance model extends the enclosure downward to 60 x 150 x 183 mm (bottom at 862 mm, top unchanged at 1,045 mm) so the power bank sits inside at its model.py position. Proposed, awaiting Amish. Recommendation: adopt the taller single enclosure in model.py and BOM line 14 at the next revision; option: a separate small box for the power bank.
2. **Pressure transducer on the tee.** BOM line 14 includes a stainless pressure transducer on the lid tee (BOM line 10), but model.py ends the logger cable at the tee without a transducer body. The appearance model shows a 22 mm diameter transducer standing on the tee end with its connector, and the cable ends there. Proposed, awaiting Amish. Recommendation: add the transducer envelope to model.py at the next revision.
3. **Cooker handles.** model.py's handle bar is one massing block that passes through the cooker interior. The appearance model shows two handles outboard of the wall with the same overall span (458 mm) and height. Proposed, awaiting Amish. Recommendation: accept as appearance detail.
4. **Petal seams and hub.** model.py's reflector is one revolved sheet to the axis. The appearance model cuts 2.4 mm seams at the rib angles and a central opening inside the 75 mm hub radius, covered by a hub cap. Proposed, awaiting Amish. Recommendation: accept; it matches the 12-petal build in BOM line 1.
5. **Not shown.** The base-edge K-type thermocouple lead (BOM line 14), eye protection, parking cover, keep-out marking and validation consumables (BOM lines 18 to 21) are not modelled, as in model.py. Screws, straps, glands and bolts are appearance detail under BOM line 17; no new BOM lines are implied.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-26: sources strengthened

Amish, 2026-09-26: "Fix the weaker sources." All README source links in the Concept rationale, Burning platform, Where it could be used and What sparked the idea sections were fetched and checked against the claims they support.

| Where | Old source | New source |
| --- | --- | --- |
| By country or region: Andean Peru and Bolivia | None (row uncited) | Row rewritten as Peru and Bolivia (Andes) and cited to the [WHO fact sheet on electricity in health-care facilities](https://www.who.int/news-room/fact-sheets/detail/electricity-in-health-care-facilities): in Latin America and the Caribbean about 8 % of facilities have no electricity and about 72 % have a reliable supply. No altitude figure is claimed. |
| By country or region: Sahel (Niger, Mali, Chad) | Global Solar Atlas (could not be fetched for verification); grid claim uncited | Narrowed to Niger and cited to the [African Development Bank Desert to Power roadmap for Niger (2020)](https://www.afdb.org/sites/default/files/2024/08/23/desert-to-power_dtp_roadmap_for_niger_en_oct2020.pdf): daily irradiation about 7 kWh/m², electricity access about 13 % nationally and about 1 % in rural areas in 2018. |
| By country or region: Puerto Rico | US Army Corps of Engineers fact sheet (returned HTTP 403, could not be verified) | [GAO-19-296](https://www.gao.gov/products/gao-19-296): about 11 months to restore power to all customers after Hurricanes Irma and Maria in 2017. |
| By country or region: Kenya | Uncited claim that many facilities sit at 1,000 to 2,000 m | Removed; the row keeps the cited WHO figure and the cooker physics from the calculation note. |

Links kept after verification: WHO fact sheet on electricity in health-care facilities, WHO questions and answers on surgical site infections, Bureau International des Expositions on Mouchot at Expo 1878, Smithsonian National Museum of American History (Papin 1679, Chamberland 1879). The inspiration already rests on primary and museum sources, so it and INSPIRATIONS.md are unchanged. docs/01-problem.md cites the Global Solar Atlas (World Bank and ESMAP data) for a different claim (clear-sky DNI) and is unchanged. No controlled document changed, so no version was bumped.

## Session 2026-09-25: recommendations accepted

Amish wrote, in chat on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation (items 13 to 18) is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (SCL-DDR-002 v0.1). Items 1 to 4 and 6 to 11 were already decided (SCL-DDR-001).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| 13 | R14 relaxed to retargeting every 12 min, with a logger reminder | Target 15 min; 13 min achieved; not met | Target 12 min; met. Mean absorbed power 630 W to 638 W; central cycle 79.9 min to 79.0 min; unfavourable 109.2 min to 106.6 min |
| 14 | R16 total relaxed to 45 kg, 20 kg piece limit kept | 41.0 kg against 40 kg; not met | 41.0 kg against 45 kg; met |
| 15 | R11 restated: whole vessel a marked hot zone, no physical guard | Guard undefined; not met | Met by design review; BOM item 21 keep-out marking added ($6) |
| 16 | Four locking castors; park face-up in high wind | Two locking; grip 109 N against 153 N of wind | Four locking; grip 218 N; castors $40 to $44; model adds brake pedals; SCL-DWG-001 Rev P1 to P2. Tipping factor still 1.30, R15 still at risk |
| 17 | Trimming rule with a logger trim reminder for holds over 40 min | 0.14 kg of water left at 1,800 m in strong sun; at risk | 1.31 kg at 1,800 m and 1.28 kg at 2,400 m with trimming; met (R10 restated) |
| 18 | 0 to 300 kPa absolute transducer, overpressure rating 600 kPa or more | Check uncertainty 0.89 K, pressure 5 kPa; at risk | 0.64 K (32 % of the 2 K threshold), pressure 3 kPa; met, narrowly |

Budget: unchanged at $450 in `project.yaml`. Parts rose from $430 to $440, a margin of $10.

Files changed: `docs/03-requirements.md` (SCL-REQ-001 v0.4: R10, R11, R14 and R16 restated or relaxed; status column), `docs/02-concept.md` (SCL-PRC-001 v0.4), `docs/04-calcs/sizing.py`, `results.csv` and `01-sizing.md` (SCL-CAL-001 v0.2), `docs/decisions/0001-trl2-review-decisions.md` (SCL-DDR-001 v0.2, items 13 to 18 marked decided), `bom/bom.csv` and `bom-notes.md`, `cad/src/model.py` (four castor brake pedals; STEP and STL re-exported), `cad/src/sheets.py` (SCL-DWG-001 Rev P2, notes), `cad/src/concept_media.py` (cost figure; all media regenerated and inspected), `project.yaml` (DDR-002 added to the evidence list) and `README.md`.

README: added "Concept rationale", "Burning platform" (WHO electricity and surgical site infection figures), "Where it could be used" and "What sparked the idea". The inspiration is Augustin Mouchot's parabolic solar collector heating a blackened boiler at the 1878 Paris Exposition, together with Chamberland's 1879 autoclave descended from Papin's pressure cooker. `docs/01-problem.md` did not attribute the idea to any session and was not changed. All generated files were re-rendered with the designmolecule.com footer.

### Requirement status (SCL-CAL-001 v0.2)

14 met, 2 at risk, 1 not verifiable at TRL 3, 0 not met.

- Not met: none. R11, R14 and R16 are met because their targets were restated or relaxed by decision, not because the design improved.
- At risk: R4 cycle time (79 min central, 107 min unfavourable, against 90 min); R15 stability (tipping factor 1.30 at 15° sun in a 10 m/s wind).
- Not verifiable at TRL 3: R1, because the equivalent-exposure method needs biological indicators.
- Met: R2, R3, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R16, R17.

### Still awaiting Amish

- **Item 5: mounting the lid fittings** (drilled lid, factory ports or adapter plate). No recommendation; a pressure-safety trade-off. Must be decided before anything is built.
- **Item 12: first partner and site.** No recommendation; chosen per area later.

### Cross-repo actions

None. No SunClave decision needs another repo to change.

### Safety

The restated R11 relies on procedure (turning the dish 15° off the sun, the parking cover, goggles and a marked keep-out) rather than a physical guard, and the restated R10 relies on the operator following the trim reminder. Both keep the 140 °C base alarm and the safety sections unchanged. SunClave remains a research and educational prototype, not a medical device.

### TRL

`trl: 3` and `trl_target: 3`. TRL 4 remains on hold by Amish's instruction. The retarget and trim reminders are recorded as firmware rules only; no firmware, purchasing, build or test work was done.

## Session 2026-09-25: TRL 3

TRL 4 is on hold by Amish's instruction ("Make sure we don't proceed to TRL 4 on any of them"). This session took SunClave from TRL 2 to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SCL-DDR-001 v0.1): records items 1 to 4 and 6 to 11 of the TRL 2 review as "Decided by Amish, 2026-09-25: go with recommendation", the cross-cutting approvals (SwapCell does not apply), and the open items 5, 12 and 13 to 18.
- `docs/04-calcs/01-sizing.md` (SCL-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: IAPWS-IF97 steam and altitude, a Monte Carlo ray trace of the dish onto the level cooker, heat loss, cycle and clear-day simulation, measurement uncertainty, relief and vent capacity for both lid options, boil-dry, masses, wind and castor grip, logger power, cost, and a results table for R1 to R17. The script reads `cad/src/model.py` and `bom/bom.csv`.
- `cad/src/model.py`: parametric build123d model (paraboloid reflector, ribs, rim, yoke, timber stand, fixed pot holder, 12 L cooker with lid fittings, jacket, water, basket, logger and power bank). Exports `cad/step/sunclave-{assembly,dish,stand,vessel}.step` and matching STL files in `cad/stl/`.
- `cad/src/sheets.py` and `cad/drawings/SCL-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps SCL-DWG-010, so SCL-DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: 20 lines, every line priced with a supplier type; parts total $430 against $450.
- `cad/src/concept_media.py` now builds the media from the model: `media/hero.png`, `exploded.png`, `cutaway.png`, `flow.png` (SCL-CAL-001 numbers), `concept-blueprint.png`, `.pdf`, `.svg`, `model.glb` and `viewer.html`. Each image was inspected; exploded offsets were adjusted so the stand and dish callouts no longer overlap. No `media/_views*` folders remain.
- SCL-PRB-001, SCL-PRC-001 and SCL-REQ-001 moved to v0.3 with the decisions and the TRL 3 numbers. `project.yaml`: `trl: 3`, `trl_target: 3`, evidence list, new pitch, `budget_usd: 450`. `README.md`: new pitch, TRL 3 badge and summary.

### Requirements (SCL-CAL-001 Table 10)

9 met, 4 at risk, 1 not verifiable at TRL 3, 3 not met.

- **Not met: R11 burn and glare.** No focal-zone guard is defined, and the black base and 80 mm wall band (above 60 °C) are within reach. Goggles and a parking cover were added to the BOM.
- **Not met: R14 tracking.** Absorbed power stays within 10 % of on-target for about 13 min of sun motion (3.2° of pointing error), not 15 min.
- **Not met: R16 mass.** About 41.0 kg empty against 40 kg, mostly because the decided timber stand weighs about 19.4 kg. Every handling piece is within 20 kg.
- At risk: R4 cycle time (80 min central, 109 min unfavourable, against 90 min); R10 boil-dry (option B holds at 1,800 m in strong sun leave 0.14 L without trimming); R12 air-removal check (0.89 °C uncertainty against 2 °C); R15 stability (tipping factor 1.30 at 15° sun, and the stand rolls on two locked castors).
- Not verifiable at TRL 3: R1, because the equivalent-exposure method of option B needs biological indicators.
- Met: R2, R3, R5 (4 cycles), R6, R7 (0.44 °C with a 0.05 % reference), R8 (relief 5.1 times the worst steam generation), R9, R13 (8.7 days), R17 ($430).

Corrections to TRL 2 numbers (SCL-CAL-001 section 14): the regulator gives 120.95 °C at sea level, so 121 °C holds only at sea level, not below 300 m; absorbed power is 669 W, not 710 W; heat loss at 121 °C is 395 W, not 200 W; peak flux is about 270 kW/m², not 30 to 50; the 270 x 180 mm basket did not fit a 12 L cooker and is now 250 x 150 mm.

### Decisions recorded (SCL-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: altitude option B; budget option (b) then (a), so `budget_usd` is now $450 after the cuts saved about $29; the pitch wording; the household 12 L aluminum cooker; the level cooker at the focus (the holder is fixed to the stand, because a swinging holder would be top-heavy); the petal dish; manual gnomon aiming; the load limits; the logger pass criteria; backup heat on a stove. The problem line had no recommended rewording and is unchanged.

### Still awaiting Amish

- **Item 5: drilling the cooker lid** versus a factory-ported cooker or an adapter plate. No recommendation; it is a safety trade-off. The model shows the fittings without choosing, and SCL-CAL-001 section 8 lists both options side by side.
- **Item 12:** first partner and site (per area later).
- **New items 13 to 18,** each with a recommendation: R14 (relax to 12 min), R16 (relax to 45 kg total), R11 (treat the whole vessel as a hot zone, no physical guard), R15 (four locking castors, about $4), R10 (trimming rule and logger water warning), R12 (0 to 300 kPa transducer). **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-002; see the session below).

### Safety concerns

- The focal spot is far hotter than the TRL 2 documents said: about 270 kW/m² in its hottest 20 mm. Goggles, gnomon aiming, the parking cover and turning the dish at least 15° away before reaching in are essential. R11 is not met.
- The lid-fitting method (item 5) must be decided before anything is built. Relief and vent capacity are ample for both options, but no calculation can show whether a drilled lid keeps the maker's rating.
- Option B at altitude lengthens holds; in strong sun the cooker can boil nearly dry at 1,800 m and fully dry at 2,400 m unless the dish is trimmed. A dry base would pass 200 °C.
- The base thermocouple must sit at the base edge, out of the focal spot, or the boil-dry alarm will misread. Normal boiling leaves only 6.5 K of margin to the 140 °C alarm.
- The quadrant lock carries up to about 38 N·m of gravity torque plus wind; the stand can roll in a 10 m/s wind on two locked castors.
- The timber stand can scorch from stray reflections; the power bank is a lithium pack and must stay shaded.
- Medical claims: the documents still state that SunClave is a research and educational prototype, not a medical device, and that a PASS does not prove sterility.

### Problems and notes

- The kit's exploded-view callouts still cover the smallest parts (gauge 8, relief valve 9, gland 10 and power bank 15) at this scale. A kit change (offset labels with leader lines) would fix it; not made here.
- The kit's cutaway cutter is centered on Z = 0, so `concept_media.py` still lowers the vessel before cutting (as at TRL 2).
- The reflector is modelled 3 mm thick for visibility; mass uses 0.5 mm.
- No citations were flagged as unchecked in the TRL 2 review; none were re-verified. The new CAL cites Watmuff, Charters and Proctor (1977) for wind convection and uses IAPWS-IF97, checked in the script against steam-table values.
- No TRL 4 material exists in this repo (`build-log/` holds only its README; `electronics/` and `firmware/` are empty).
- Suggestions, not changes: an insulated lid cover could recover up to about 80 W of the 101 W lid loss and shorten heat-up; a kit fix for callouts.

### Recommended next step

Decide item 5 (lid fittings) and items 13 to 18, then update SCL-REQ-001 and the BOM on paper. TRL 4 is on hold by Amish's instruction and no TRL 4 work should start. For the record only, TRL 4 would need: a built prototype with the lid-fitting decision implemented; a lab test report (TST, `environment: lab`) covering a hydrostatic check of the vessel as fitted, the relief valve lift, heat-up and hold timing, logger calibration against a reference thermometer and barometer, the air-removal check with a deliberate leak, and biological and chemical indicators for the option B equivalence; and dated build log entries.

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch)

### What was done

- `docs/01-problem.md` (SCL-PRB-001 v0.2): problem with cited sources (WHO electricity data, CDC and IARC cycle times, WHO reprocessing manual), users, operating environment, constraints, out of scope, cited prior work (Kaseman et al. solar autoclave, Rice nanoparticle autoclave, SK14 dish, pressure-cooker sterilization, EN 13060 type N), open questions, and a co-design checklist.
- `docs/03-requirements.md` (SCL-REQ-001 v0.2): 17 measurable requirements (R1 to R17) with a defined design case, verification route and concept status for each.
- `docs/02-concept.md` (SCL-PRC-001 v0.2): how it works, 16 numbered components, solar input, heat-up and water budget, altitude table, logger accuracy, aiming, wind, mass and cost, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of the petal dish, ribs, tilt yoke, castored stand, level pot holder, cooker with lid fittings, jacket, water, basket, logger, panel and gnomon, each with a BOM number; 1.75 m scale figure. The cutaway is rendered with the kit's `cutaway_parts` and `_render` on the pressure vessel only (see notes).
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts, `cutaway.png` of the vessel, `flow.png` (power during heat-up, estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 18 lines numbered to match the exploded view, indicative USD prices; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line before "## Problem"; problem, concept and key components brought in line with the precis; safety note extended to concentrated sunlight.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` unchanged.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Power absorbed by the cooker at 700 W/m² DNI | about 710 W (1.4 m dish, 1.54 m²) | |
| Cold start to 121 °C | about 35 min; 35 to 60 min with aiming losses | R4 met on estimate, at risk (precedent 93 to 183 min) |
| Cycle, cold start to end of hold | about 55 to 90 min | R4 (90 min) |
| Cycles per clear day | about 3; none when overcast | R5 met on estimate |
| Water left after a 30 min hold | about 1.0 L of 1.5 L | R10 met |
| Steam temperature at 103 kPa gauge | 121.1 °C at 0 m; about 117.8 °C at 1,800 m | **R1 not met above about 300 m** |
| Temperature accuracy | about 0.5 °C (Pt100 class A) | R7 met on datasheets |
| Logger autonomy without sun | about 5 days | R13 met |
| Wind at 10 m/s | about 110 N·m overturning versus about 180 N·m restoring | R15 met, thin margin |
| Mass, empty | about 32 kg | R16 met |
| Parts cost | about $437 (validation consumables about $45 extra) | **R17 not met, about 9 % over** |

Requirements not met or at risk:

- **R1 (sterilizing temperature) not met above about 300 m** with a 103 kPa cooker. Many target sites are at 1,000 to 2,000 m.
- **R17 (cost) not met:** about $437 against $400.
- **R4 (cycle time) at risk:** the estimate is well below the only measured precedent.
- **R11 (burn and glare protection) partly met:** a focal-zone guard is not yet defined.
- **R12 (air-removal check)** is feasible, but the 5 kPa pressure accuracy leaves little margin on the 2 °C threshold.

### Proposed, awaiting Amish

Status update: items 1 to 4 and 6 to 11 are **Decided by Amish, 2026-09-25: go with recommendation** (SCL-DDR-001). Items 5 and 12 had no recommendation and remain proposed, awaiting Amish.

1. **Altitude strategy.** Option A: a vessel rated by its maker for about 130 kPa gauge. Option B: keep the 103 kPa cooker and extend the hold by an equivalent-exposure calculation (unvalidated; needs biological indicators). Option C: sites below about 300 m only. Recommendation: B for the research prototype, recorded plainly as a lower-temperature cycle, with a search for A.
2. **Budget.** Option (a): raise `budget_usd` to $450. Option (b): cut about $40 (timber stand instead of steel, OLED instead of e-paper, a USB power bank instead of the logger panel). Option (c): accept the overrun for the prototype and state it. Recommendation: (b), then (a) if the savings fall short. `project.yaml` is unchanged.
3. **Pitch wording.** The pitch says "validated temperature and time logger". The logger can be calibrated and can record evidence, but neither it nor the system is validated in the regulatory sense, and a PASS does not prove sterility. Proposed wording: "with a calibrated temperature, pressure and time logger that records every cycle". Not changed in `project.yaml` or the README tagline, because it changes the pitch.
4. **Pressure vessel:** household 12 L aluminum cooker (about $55) rather than a purpose-made sterilizer such as the All-American 1915X (about $430 alone).
5. **Drilling the cooker lid** for the probe gland, transducer, gauge and relief valve, versus a cooker with factory ports or an adapter plate on the regulator stem. Safety trade-off.
6. Level cooker hung at the focus with the dish tilting about it.
7. Locally built 1.4 m petal dish rather than a Scheffler reflector or a bought SK14 kit.
8. Manual aiming with a shadow gnomon; no tracker.
9. Load limits: solid instruments only, unwrapped or single-wrapped.
10. Logger pass criteria: purge plateau of 5 min or more, hold temperature and time met, and measured temperature within 2 °C of saturation.
11. Backup heat on cloudy days from a wood, charcoal or LPG stove, logged the same way.
12. First partner and site for co-design.

### Safety concerns

- Concentrated sunlight (about 30 to 50 suns at the focus): eye damage, skin burns and fire. Aiming by shadow, goggles, a parking cover and a focal-zone guard are needed.
- Pressure vessel: only a maker-rated cooker, overpressure plug kept, an independent relief valve, no change to the regulator weight, and never forcing the lid. Drilling the lid needs a careful decision (item 5).
- Boil-dry of an aluminum base under concentrated sun; mitigated by the water budget and the base thermocouple alarm.
- Scalds from steam venting, hot instruments and lid; tipping in wind; pinch points at the pivots.
- Small lithium cell in a sunny location.
- Medical claims: the documents state that SunClave is a research and educational prototype, not a medical device, and that a logger PASS does not prove sterility. These statements must stay.

### Problems and notes

- The kit's cutaway cutter is centered on Z = 0, so it misses parts about 1 m up when the large stand and dish are excluded. `concept_media.py` lowers the vessel parts before cutting and calls the kit's `cutaway_parts` and `_render` directly. Suggest fixing `cutaway_parts` in the kit to center the cutter on the parts' bounding box (a kit change, not made here).
- In the exploded view the smallest parts (gauge, relief valve, gnomon) are partly covered by their callout circles at this scale.
- The dish is modeled as a spherical cap as a stand-in for the paraboloid (massing only).
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- SwapCell is not relevant to this design and is not proposed.

### Recommended next step

Review this note and the media, then decide items 1 to 3 (altitude, budget, pitch wording) and item 5 (drilling the lid). If approved, run `/advance-trl3` to check the optics, heat-up and water budget, altitude method and wind stability by calculation, and produce the parametric model and drawing sheet.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." Nothing was built or tested; TRL 4 remains on hold.

### Decisions recorded

5 decisions moved from "Open decisions" to "Decisions made" in the design decisions register, dated 2026-10-02. Lid fittings decided (no drilling; a pressure canner with a factory gauge and relief valve, the probe gland on a vent-stem adapter plate); design for construction (SCL-DDR-003) accepted with A1 and with A2 changed to add a back-up drop pin; a university biomedical or global health engineering group named as the first partner to approach. Nothing is to be pressurised until the follow-ups for decision 1 are carried into the design.

### Documents changed

- `docs/01-problem.md` (SCL-PRB-001 v0.4)
- `docs/02-concept.md` (SCL-PRC-001 v0.6)
- `docs/03-requirements.md` (SCL-REQ-001 v0.6)
- `docs/05-build-plan.md` (SCL-BLD-001 v0.2)
- `docs/06-design-decisions.md` (SCL-DEC-001 v0.2)
- `docs/decisions/0001-trl2-review-decisions.md` (SCL-DDR-001 v0.3)
- `docs/decisions/0002-recommendations-accepted.md` (SCL-DDR-002 v0.2)
- `docs/decisions/0003-design-for-construction.md` (SCL-DDR-003 v0.2)
- `README.md` (not a controlled document)
- `bom/bom-notes.md` (not a controlled document)
- `docs/pdf/`: every controlled document re-rendered.

### Follow-up actions to carry approved decisions into the design

The model, drawings, build plan pictures, BOM quantities and prices, and calculations were not changed in this session. These actions carry the approved decisions into them:

1. Decision 1 (bom): Respecify BOM line 6 as a pressure canner of about 12 L sold with a factory gauge and relief valve; lines 8 and 9 become the factory-fitted parts or are removed; line 10 gains the vent-stem adapter plate with a bore of 3 mm or more; reprice.
2. Decision 1 (model): Model the pressure canner with its factory gauge and relief valve and the vent-stem adapter plate carrying the probe gland; check the canner fits the holder ring and the focus.
3. Decision 1 (calcs): SCL-CAL-001 section 8: restate the relief and vent capacity for the factory relief valve and the 3 mm vent-stem bore, and replace the "open for Amish" wording on item 5 and SCL-DDR-003 with the decisions of 2026-10-02; check the canner's volume, mass and dimensions against R16 and the holder.
4. Decision 1 (pictures): Build plan step 19 and the cooker pictures: show the canner, its factory fittings and the adapter plate.
5. Decision 4 (model): Add a row of pin holes in each yoke plate fan and a drop pin with a lanyard on the stand; re-run the constructability checks.
6. Decision 4 (drawings): Yoke plate making sketch: add the pin hole row; making sketch for the drop pin.
7. Decision 4 (pictures): Build plan: joint 6 (tilt lock) and steps 13 and 14 pictures to show the drop pin; add the pin to the "Tilt lock holds" check.
8. Decision 4 (bom): BOM line 3: add the drop pins and lanyards and price them.
9. Decision 4 (docs): TRL 4 test plan: slip test of the friction locks against twice the 45 N·m worst torque.
10. Decision 3 (docs): TRL 4 test plan: weigh the prototype against R16 (45 kg), with the 5 mm yoke plates and lighter holder arms ready.
11. Decision 2 (pictures): At the next render session on Amish's Mac, redraw the photoreal renders, card and social preview to the constructable design (yoke plates, axle plates, holder and stand).

### Points found in the review

Raised when the recommendations were written (2026-10-01) and not yet acted on:

- Item 1 is a precondition for the whole pressure system: nothing should be pressurised until it is decided, as the register says.
- The value-engineering figure (USD 497 against USD 450) excludes USD 45 of validation consumables; that is consistent with the target, but the consumables are a recurring cost per batch of tests.
- Renders still show the concept tube yoke, quadrant, bearing blocks, holder and stand.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
