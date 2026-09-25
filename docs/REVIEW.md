# Review note: SunClave

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
