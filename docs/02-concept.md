---
doc_id: SCL-PRC-001
title: SunClave design precis
project: SunClave
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, altitude finding, safety, media)
---

# SunClave design precis

SunClave is a 1.4 m parabolic dish of aluminum petals that focuses sunlight onto the blackened base of a 12 L household pressure cooker hung level at the focus, with a cycle logger that measures temperature in the load zone and chamber pressure and flags each cycle as pass or fail. First-order numbers suggest about 700 W reaches the cooker on a clear day, enough to go from cold to a 121 °C hold in about 35 to 60 min and to run about three cycles a day. Two findings matter most: the prototype parts cost about $437, over the $400 budget, and a 103 kPa (15 psi) cooker reaches 121 °C only below about 300 m altitude.

> **Safety:** SunClave is a research and educational prototype, not a medical device. It has not been cleared or approved by any regulator and must not be relied on to sterilize instruments used on patients. It combines concentrated sunlight that can burn skin, blind and start fires, with a pressure vessel holding steam at about 121 °C (250 °F). See the safety section before building or operating anything.

![Hero render](../media/hero.png)

*Figure 1. SunClave with the dish aimed at a sun 50 degrees above the horizon, and a 1.75 m person for scale. The cooker hangs level at the focus on the tilt axis.*

## How it works

1. **Load.** The operator puts 1.5 L of water in the cooker, sets cleaned instruments in a basket on a trivet above the water, closes the lid and hangs the cooker in the level holder at the focus.
2. **Aim.** The operator turns the stand on its castors to face the sun and tilts the dish until the shadow of the sighting gnomon falls on the center of its target. Nobody needs to look at the sun or at the bright focus. Retargeting every 10 to 15 min keeps the focal spot on the cooker base.
3. **Heat and purge air.** About 700 W arrives on the blackened base. The water boils, and steam leaves through the open vent for at least 5 min to push air out of the chamber before the weighted regulator is fitted. The logger recognizes this purge as a plateau at the local boiling point.
4. **Pressurize and hold.** With the regulator fitted, pressure rises to 103 kPa gauge and the regulator vents the excess. The operator holds the cycle for 20 min (unwrapped) or 30 min (wrapped), trimming the dish slightly off the sun if the regulator vents hard, to save water.
5. **Record.** Throughout, the logger reads a Pt100 probe in the load zone and an absolute pressure transducer on the lid. It checks that the load-zone temperature matches the saturation temperature for the measured pressure (air left in the chamber shows up as a lower temperature), times the hold, and at the end shows PASS or FAIL with a cycle number to copy into the register.
6. **Cool and unload.** The operator turns the dish away from the sun, lets the pressure fall to zero on the gauge, removes the regulator, opens the lid and lets the load dry in the residual heat.

![Energy flow](../media/flow.png)

*Figure 2. Power flow during heat-up at 700 W/m² DNI. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Reflector | 12 petals of polished aluminum sheet, 1.4 m aperture, focal length about 500 mm | SK14-style petal layout, cut from flat sheet |
| 2 | Dish ribs, rim and hub | Bent steel flat-bar ribs, rolled rim, bolted hub | Holds the petal shape; bending jig at TRL 3 |
| 3 | Tilt yoke and quadrant lock | Two arms pivoting on the focal axis; slotted quadrant with lock knob | Dish tilts 15 to 90 degrees about the cooker |
| 4 | Stand with castors | Square-tube base about 1.84 x 1.10 m, uprights to about 1.0 m | Azimuth by turning the whole stand |
| 5 | Level pot holder | Steel ring hung from the pivot axis | Keeps the cooker upright at every tilt |
| 6 | Pressure cooker | 12 L aluminum household cooker, 103 kPa weighted regulator, overpressure plug, base painted matte black | About 300 mm diameter by 250 mm |
| 7 | Lid with regulator | Supplied with item 6, drilled for items 8 to 10 | Drilling the lid is proposed, awaiting Amish |
| 8 | Pressure gauge | 0 to 250 kPa, 100 mm dial with siphon | Reads without power, independent of the logger |
| 9 | Independent relief valve | Spring valve, set 125 kPa gauge or less | Second line of defense after the regulator |
| 10 | Lid gland, Pt100 probe and pigtail | 3 mm class A Pt100 through a compression gland into the load zone; tee to the transducer | Measures where the instruments are, not the outer wall |
| 11 | Insulated jacket | 25 mm mineral wool with aluminized skin on the upper wall | Base stays bare to take the focus |
| 12 | Water charge | 1.5 L per cycle | About 1.0 L left at the end (estimate) |
| 13 | Instrument basket and trivet | Stainless basket about 270 x 180 mm on a trivet | Keeps the load in steam, not in water |
| 14 | Cycle logger | ESP32-class board, Pt100 interface, absolute pressure transducer, base thermocouple, RTC, microSD, e-paper display | 1 s logging, pass or fail per cycle, boil-dry alarm |
| 15 | Logger solar panel and battery | 5 W panel, one protected 18650 cell | About 5 days without sun |
| 16 | Sighting gnomon | Pin parallel to the dish axis over a target plate | Aiming by shadow |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The cooker parts are lifted out along the vertical axis.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the pressure vessel: water below the trivet, the basket and instrument load in steam, the Pt100 probe reaching into the load zone, and the jacket on the upper wall.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. The design case is defined in SCL-REQ-001 (700 W/m² DNI, 25 °C, near sea level, 2.0 kg of instruments, 1.5 L of water).

### Solar input

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Aperture area | 1.54 m² | 1.4 m diameter |
| Sun on the aperture | about 1,080 W | 1.54 m² x 700 W/m² |
| Onto the cooker base | about 790 W | 73 % optical efficiency: reflectance about 0.85, intercept about 0.90, shading by the cooker and holder about 0.95 |
| Absorbed | about 710 W | Matte black base, absorptance about 0.9 |
| Check against a commercial dish | about 700 W | SK14 rating at 750 W/m² ([EG-Solar](https://eg-solar.de/en/produkt/sk14/)); SunClave's estimate is similar |
| Peak flux on the base | about 30 to 50 kW/m² (30 to 50 suns) | About 790 W over a focal spot of 150 to 180 mm, assuming slope errors typical of hand-formed petals |

### Heat-up, hold and water

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Heat to raise the load from 25 to 121 °C | about 270 Wh (980 kJ) | Water 1.5 kg x 4.18 kJ/(kg·K), aluminum cooker 3.0 kg x 0.90, instruments and basket 2.5 kg x 0.50, all x 96 K |
| Air purge, 5 min of free steaming | about 50 Wh, about 0.08 kg of steam | 600 W for 5 min |
| Mean surface loss during heat-up | about 100 W | Half of the loss at 121 °C |
| Surface loss at 121 °C | about 200 W | Jacketed wall and lid about 75 W; bare black base radiating and convecting about 125 W |
| Net heating power | about 610 W | 710 minus 100 |
| **Cold start to 121 °C** | **about 35 min, 35 to 60 min allowing for aiming losses and haze** | 320 Wh / 610 W = 32 min |
| Measured precedent | 93 to 183 min | Kaseman et al., 2 m² concentrator, 14 to 24 L vessels ([AJTMH](https://www.ajtmh.org/view/journals/tpmd/87/4/article-p602.xml)); SunClave's smaller vessel and load explain part of the gap, but R4 is at risk |
| Surplus during the hold | about 510 W | 710 W absorbed minus 200 W loss; vented as steam unless the dish is trimmed off the sun |
| Water used, 30 min hold with no trimming | about 0.4 kg | 510 W / 2,200 kJ/kg latent heat |
| **Water left at the end** | **about 1.0 L** | 1.5 minus 0.08 purge minus 0.4 hold; R10 (0.5 L) met |
| Cycle, cold start to end of hold | about 55 to 90 min | Heat-up plus 20 or 30 min hold |
| Full turnaround | about 95 to 120 min | Plus about 20 min to depressurize and 10 min to reload |
| **Cycles on a clear day** | **about 3** | DNI above 600 W/m² from about 09:00 to 15:00 solar time; second and later cycles start warm |

### Altitude and sterilizing temperature

A weighted regulator holds a fixed pressure **above ambient**. Ambient pressure falls with altitude, so the absolute pressure and the steam temperature fall too. Saturation temperatures below use the Antoine equation for water and a standard atmosphere.

| Altitude | Ambient pressure | Steam temperature at 103 kPa gauge | Gauge pressure needed for 121 °C | Equivalent hold for 20 / 30 min at 121 °C (z = 10 °C, not validated) |
| --- | --- | --- | --- | --- |
| 0 m | 101 kPa | about 121.1 °C | 103 kPa | 20 / 30 min |
| 500 m | 96 kPa | about 120.1 °C | 109 kPa | 25 / 37 min |
| 1,000 m | 90 kPa | about 119.2 °C | 114 kPa | 30 / 45 min |
| 1,500 m | 85 kPa | about 118.4 °C | 120 kPa | 36 / 55 min |
| 1,800 m | 82 kPa | about 117.8 °C | 123 kPa | 42 / 63 min |
| 2,400 m | 76 kPa | about 116.8 °C | 129 kPa | 53 / 79 min |

R1 is therefore **not met** above about 300 m with a 103 kPa cooker. The options are in "Key design choices". The logger measures absolute pressure, so it reports the true steam temperature at any altitude.

### Cycle record and measurement

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Temperature accuracy at 121 °C | about 0.4 °C (probe), about 0.5 °C (system) | Pt100 class A tolerance 0.15 + 0.002 x 121 °C; 15-bit interface; checked at each site against boiling water at the local pressure |
| Pressure accuracy | about 5 kPa | 1 % of a 500 kPa full scale |
| Saturation-check resolution | about 1 °C | About 0.2 °C per kPa near 200 kPa absolute; R12 threshold of 2 °C is achievable, with little margin |
| Record per cycle | about 25 kB | 1 s samples of three channels for up to 2 h, packed |
| Storage | over 100,000 cycles | On a 4 GB microSD card |
| Logger energy | about 2.5 Wh per operating day | About 0.3 W for 8 h |
| Autonomy without sun | about 5 days | 12 Wh cell / 2.5 Wh per day; R13 (3 days) met |

### Aiming, wind and mass

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Pointing tolerance | about 8 degrees before the spot leaves the base | Spot shift about focal length x angle; 75 mm allowed | |
| Sun motion | up to 15 degrees per hour | | R14 (15 min) met |
| Wind force on the dish at 10 m/s | about 110 N | Drag coefficient 1.2 on 1.54 m² | |
| Overturning versus restoring moment | about 110 N·m versus about 180 N·m | Force at about 1.0 m; 33 kg on a 0.55 m half-base | R15 met, thin margin |
| Mass, empty | about 32 kg | Stand 13 kg, dish and ribs 8 kg, yoke and holder 4.5 kg, cooker and fittings 4 kg, other 2.5 kg | R16 (40 kg) met |

### Cost

| Group | Indicative cost |
| --- | --- |
| Concentrator and stand (items 1 to 5, 16) | about $192 |
| Pressure vessel and fittings (items 6 to 13) | about $146 |
| Logger and its power (items 14, 15) | about $84 |
| Hardware (item 17) | about $15 |
| **Parts total** | **about $437; R17 ($400) not met, about 9 % over** |
| Validation consumables (item 18, not in parts total) | about $45 |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Altitude strategy.** A 103 kPa cooker gives 121 °C only near sea level.
  - Option A: find a vessel whose maker rates it for about 130 kPa gauge and fit a matching regulator, so 121 °C holds up to about 2,400 m. Changing the weight of a cooker rated for 103 kPa is not acceptable.
  - Option B: keep the 103 kPa cooker and extend the hold using an equivalent-exposure calculation in the logger (about 42 or 63 min at 1,800 m). Simple and cheap, but the equivalence is unvalidated and needs biological-indicator evidence.
  - Option C: limit the first sites to below about 300 m.
  - Recommendation: B for the research prototype, recorded as a lower-temperature cycle and never labeled 121 °C, with a parallel search for Option A.
- **Pressure vessel.** A household aluminum cooker (about $55) versus a purpose-made sterilizer such as the All-American 1915X (about $430 on its own, [maker's page](https://www.pressurecooker-canner.com/1915x.html), which alone exceeds the budget) or a stainless cooker (heavier, slower to heat, more robust). Recommendation: household aluminum cooker for the prototype, with the 1915X as a reference vessel if a partner already owns one.
- **Drilling the lid for the probe, transducer and relief valve.** Drilling changes a certified vessel. Alternatives are a cooker model with factory gauge and valve ports, or a probe through a purpose-made adapter plate replacing the regulator stem. Recommendation: choose a cooker with factory ports if one exists in the target market; otherwise drill with reinforcing washers and document it. Awaiting Amish because it is a safety trade-off.
- **Level cooker at the focus, dish tilting about it.** The cooker never tilts, so water stays in place and the regulator works. The alternative, a cooker fixed to the dish, is simpler but tilts the vessel. Recommendation: level holder.
- **Concentrator type.** A 1.4 m petal dish (SK14 class, buildable locally) versus a Scheffler reflector (fixed focus that can be indoors, but larger and harder to build) or buying an SK14 kit where available. Recommendation: build the petal dish, and use a bought SK14 if the partner has one.
- **Manual aiming with a gnomon.** No motor or clockwork; the operator retargets every 10 to 15 min. A tracker is left for later. Recommendation: manual.
- **Load limits.** Solid instruments only, unwrapped or single-wrapped; no lumened, hollow or textile loads. Recommendation: adopt as a firm limit.
- **Logger pass criteria.** Purge plateau of 5 min or more; hold temperature within the target band for the set time; measured temperature within 2 °C of the saturation temperature throughout the hold. Recommendation: adopt for TRL 3 analysis.
- **Backup heat on cloudy days.** The same cooker on a wood, charcoal or LPG stove, logged the same way. Recommendation: include in the concept of operation.
- **Budget.** Options are in `docs/REVIEW.md`. The `project.yaml` budget is unchanged.

## Safety

> **Safety:** SunClave concentrates sunlight to 30 to 50 times normal intensity, heats a pressure vessel to about 121 °C, and is described in a medical context. Each of these is a serious hazard. It is a research and educational prototype and not a medical device.

- **Concentrated sunlight.** The focal zone can burn skin in seconds, ignite paper, cloth and dry grass, and cause permanent eye damage. Never look at the focus or into the dish when it faces the sun; wear shade 5 welding goggles or equivalent near the focus; aim only by the gnomon shadow; turn the dish away from the sun or cover it before reaching under the cooker; keep the ground below clear of anything that can burn; never leave the dish facing the sun unattended or with children nearby.
- **Pressure and steam.** Use only a commercially made cooker rated for the working pressure, keep its overpressure plug, fit the independent relief valve, and check that the vent is clear before every cycle. Never force the lid open; wait until the gauge reads zero and the regulator has been lifted with a tool. Steam from the regulator and relief valve can scald, so point vents away from people. Do not modify the regulator weight.
- **Boil-dry.** A dry base under concentrated sun can soften aluminum within minutes. Fill 1.5 L before every cycle; the base thermocouple alarm prompts the operator to turn the dish away.
- **Hot surfaces.** The lid, handles, fittings and instruments reach 121 °C, and the base more. Use heat-resistant gloves and handle the cooker only when the dish is turned away.
- **Tipping and pinch points.** Lock the castors and the tilt quadrant, add ballast in wind, and keep hands clear of the yoke pivots when tilting.
- **Lithium cell.** The logger's 18650 cell must be protected, shaded inside its box and never charged above 45 °C.
- **Medical claims.** A PASS on the logger shows the recorded conditions, not that the load is sterile. Biological and chemical indicators remain the reference, and no load from this prototype should be used on a patient.

## Open questions for TRL 3

- Decide the altitude strategy (Options A to C) and the vessel, including whether the lid may be drilled.
- Calculate heat-up time more carefully, including transient losses and haze, and compare with Kaseman et al.; decide whether R4 needs a larger dish.
- Confirm cooker ratings and brands available in the first target country.
- Define the focal-zone guard (R11) and a parking cover.
- Define the logger pass criteria and the equivalent-exposure method in a calculation note, with a firmware sketch clearly labeled as such.
- Close the $37 cost gap or propose a budget change.
- Choose a partner and site to learn real loads, altitude and records practice.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
