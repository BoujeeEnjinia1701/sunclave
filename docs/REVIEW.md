# Review note: SunClave

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
