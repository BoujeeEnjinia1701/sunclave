---
doc_id: SCL-PRC-001
title: SunClave design precis
project: SunClave
doc_type: Design precis
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply SCL-DDR-001 decisions (option B, $450 budget and cuts, vessel, holder, dish, aiming, load limits, pass criteria, backup heat); replace first-order numbers with SCL-CAL-001; TRL 3 model, drawing and media
---

# SunClave design precis

SunClave is a 1.4 m parabolic dish of aluminum petals that focuses sunlight onto the blackened base of a 12 L household pressure cooker held level at the focus, with a cycle logger that measures temperature in the load zone and chamber pressure and flags each cycle as pass or fail. The TRL 3 calculations (SCL-CAL-001) put about 670 W into the cooker on a clear day, enough to go from cold to the end of a 30 min hold in about 80 min and to run about four cycles between 09:00 and 15:00. Three requirements are not met on paper: there is no focal-zone guard yet (R11), the dish needs retargeting about every 13 min rather than 15 min (R14), and the prototype weighs about 41 kg against 40 kg (R16). Parts cost about $430 against the $450 budget Amish set on 2026-09-25.

> **Safety:** SunClave is a research and educational prototype, not a medical device. It has not been cleared or approved by any regulator and must not be relied on to sterilize instruments used on patients. It combines concentrated sunlight that can burn skin, blind and start fires, with a pressure vessel holding steam at about 121 °C (250 °F). See the safety section before building or operating anything.

![Hero render](../media/hero.png)

*Figure 1. SunClave with the dish aimed at a sun 50 degrees above the horizon, and a 1.75 m person for scale. The cooker is held level at the focus on a holder fixed to the stand; the dish and yoke tilt about it.*

## How it works

1. **Load.** The operator puts 1.5 L of water in the cooker, sets cleaned instruments in the basket on its trivet above the water, closes the lid and sets the cooker in the level holder at the focus.
2. **Aim.** The operator turns the stand on its castors to face the sun and tilts the dish until the shadow of the sighting gnomon falls on the center of its target. Nobody needs to look at the sun or at the bright focus. Retargeting about every 12 to 15 min keeps the focal spot on the cooker base (SCL-CAL-001 section 3).
3. **Heat and purge air.** About 670 W is absorbed by the blackened base and the black band of wall above it. The water boils, and steam leaves through the open vent for at least 5 min to push air out of the chamber before the weighted regulator is fitted. The logger recognizes this purge as a plateau at the local boiling point.
4. **Pressurize and hold.** With the regulator fitted, pressure rises to 103.4 kPa gauge and the regulator vents the excess. The hold is 20 min (unwrapped) or 30 min (wrapped) at sea level, and longer above it (decided option B): the logger computes the hold that gives the same exposure as 121 °C with z = 10 °C and records the real temperature. The operator trims the dish slightly off the sun if the regulator vents hard, to save water.
5. **Record.** Throughout, the logger reads a Pt100 probe in the load zone and an absolute pressure transducer on the lid. It checks that the load-zone temperature matches the saturation temperature for the measured pressure (air left in the chamber shows up as a lower temperature), times the hold, and at the end shows PASS or FAIL with a cycle number to copy into the register.
6. **Cool and unload.** The operator turns the dish away from the sun, fits the parking cover if the session is over, lets the pressure fall to zero on the gauge (about 10 min), removes the regulator, opens the lid and lets the load dry in the residual heat.

On cloudy days the same cooker runs on a wood, charcoal or LPG stove and is logged the same way (decided, SCL-DDR-001 item 11).

![Energy flow](../media/flow.png)

*Figure 2. Power flow during heat-up at 700 W/m² DNI and a sun 60° high, central estimates from SCL-CAL-001.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`. The general arrangement is drawing SCL-DWG-001 (`cad/drawings/`), generated from `cad/src/model.py`.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Reflector | 12 petals of polished aluminum sheet 0.5 mm, 1.4 m aperture, focal length 500 mm | SK14-style petal layout (decided) |
| 2 | Dish ribs, rim and hub | Bent 20 x 3 mm steel flat-bar ribs, 20 x 4 mm rim, bolted hub | Holds the petal shape |
| 3 | Tilt yoke and quadrant lock | Two short arms from collars on the focal-axis stub axles to the dish rim; lock lever on a slotted quadrant | Dish-axis elevation 15 to 90 degrees; lock holds up to about 38 N·m of gravity torque |
| 4 | Stand with castors | Treated timber base 1.75 x 1.10 m, uprights to 1.12 m, braces; steel bearing blocks; four castors | Timber decided to save cost (SCL-DDR-001 item 2); azimuth by turning the whole stand |
| 5 | Level pot holder | Steel ring under the body handles on two arms bolted to the uprights | Fixed to the stand: the loaded cooker's centre of mass is about 98 mm above the axis, so a swinging holder would be top-heavy |
| 6 | Pressure cooker | 12 L aluminum household cooker, 280 mm inside diameter x 200 mm deep, 103.4 kPa weighted regulator, overpressure plug; base and lowest 80 mm of wall painted matte black | Decided (SCL-DDR-001 item 4) |
| 7 | Lid with regulator | Supplied with item 6; carries items 8 to 10 | How items 8 to 10 are mounted is **open for Amish** (item 5) |
| 8 | Pressure gauge | 0 to 250 kPa, 100 mm dial with siphon | Reads without power, independent of the logger |
| 9 | Independent relief valve | Spring valve, set 125 kPa gauge or less, seat 4 mm or more | Passes 5.1 times the worst steam generation |
| 10 | Lid gland, Pt100 probe and tee | 3 mm class A Pt100 through a compression gland into the load zone; tee to the transducer | Measures where the instruments are |
| 11 | Insulated jacket | 25 mm mineral wool with aluminized skin on the upper wall | Black band and base stay bare to take the focus |
| 12 | Water charge | 1.5 L per cycle | About 1.26 L left after a central sea-level cycle |
| 13 | Instrument basket and trivet | Stainless basket 250 mm diameter x 150 mm deep on a 40 mm trivet | Resized from 270 x 180 mm, which did not fit a 12 L cooker |
| 14 | Cycle logger | ESP32-class board, Pt100 interface with 0.05 % reference, 16-bit ADC, absolute pressure transducer, base-edge thermocouple, RTC, microSD, OLED display | 1 s logging, pass or fail per cycle, boil-dry alarm; OLED decided to save cost |
| 15 | Logger power bank | 10,000 mAh USB bank with a low-current mode, kept in the shaded logger box | About 8.7 days per charge; replaces the panel and cell (decided) |
| 16 | Sighting gnomon | Pin parallel to the dish axis over a target plate | Aiming by shadow (decided) |
| 19 | Eye protection | Two pairs of shade 5 goggles | Added for R11 |
| 20 | Parking cover | Opaque cover for the dish | Added for R9 and R11 |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The cooker parts are lifted out along the vertical axis. Items 17 to 20 are not modelled.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the pressure vessel: water below the trivet, the basket and instrument load in steam, the Pt100 probe reaching into the load zone, and the jacket on the upper wall above the bare black band.*

## Key numbers (TRL 3)

All values are paper estimates from SCL-CAL-001 (`python docs/04-calcs/sizing.py`) for the design case in SCL-REQ-001 v0.3: 700 W/m² DNI, sun 60° high, 25 °C, wind 2 m/s, sea level, 2.0 kg of instruments, 1.5 L of water.

*Table 1. Headline results, central case unless a range is given.*

| Quantity | Value | Requirement |
| --- | --- | --- |
| Sun on the aperture | 1,078 W (1.539 m²) | |
| Absorbed by the cooker | 669 W on target (580 to 723 W across scenarios); 559 W at 15° sun, 755 W overhead | |
| Peak flux on the base | about 270 kW/m² in the hottest 20 mm cell; mean 11 kW/m² | |
| Heat loss at 121 °C | 395 W (black base and band 245 W, lid 101 W) | |
| Cold start to end of 30 min hold | 80 min (71 to 109 min) | R4 at risk |
| Cycles, 09:00 to 15:00 | 4 | R5 met |
| Water left after a 30 min hold | 1.26 L; 0.14 L at 1,800 m in strong sun without trimming | R10 at risk |
| Steam temperature at 103.4 kPa gauge | 120.95 °C at sea level; 117.7 °C at 1,800 m (hold 63 min) | R1 not verifiable at TRL 3 |
| Temperature and pressure accuracy | 0.44 °C; 5 kPa | R7 met |
| Air-removal check uncertainty | 0.89 °C against a 2 °C threshold | R12 at risk |
| Retarget interval for 90 % of on-target power | about 13 min | R14 not met |
| Relief valve capacity | 5.1 times the worst steam generation | R8 met |
| Tipping factor at 10 m/s | 1.30 at 15° sun | R15 at risk |
| Mass, empty | 41.0 kg; largest piece 19.4 kg | R16 not met |
| Logger autonomy | 8.7 days | R13 met |
| Parts cost | $430 against $450 | R17 met |

### Altitude and sterilizing temperature

A weighted regulator holds a fixed pressure **above ambient**, so the steam temperature falls with altitude. Under the decided option B the logger extends the hold to give the same exposure as 121 °C with z = 10 °C, and records the real temperature.

*Table 2. Steam temperature and extended hold with altitude (IAPWS-IF97, standard atmosphere).*

| Altitude | Ambient pressure | Steam temperature at 103.4 kPa gauge | Gauge pressure needed for 121 °C | Hold for 20 / 30 min at 121 °C (z = 10 °C, not validated) |
| --- | --- | --- | --- | --- |
| 0 m | 101.3 kPa | 120.95 °C | 103.7 kPa | 20 / 30 min |
| 500 m | 95.5 kPa | 120.03 °C | 109.6 kPa | 25 / 37 min |
| 1,000 m | 89.9 kPa | 119.13 °C | 115.2 kPa | 31 / 46 min |
| 1,500 m | 84.6 kPa | 118.26 °C | 120.5 kPa | 38 / 56 min |
| 1,800 m | 81.5 kPa | 117.75 °C | 123.5 kPa | 42 / 63 min |
| 2,400 m | 75.6 kPa | 116.74 °C | 129.4 kPa | 53 / 80 min |

The TRL 2 version of this table gave 121.1 °C at sea level and a 300 m limit; the IAPWS-IF97 line gives 120.95 °C, so 121 °C holds only at sea level. A maker-rated vessel of about 130 kPa gauge (option A) would reach 121 °C to about 2,400 m and remains worth searching for.

## Design choices

Decided by Amish on 2026-09-25 (SCL-DDR-001): option B for altitude; the budget cuts and a $450 budget; the pitch wording; the household 12 L aluminum cooker; the level cooker at the focus with the dish tilting about it; the locally built petal dish; manual aiming by gnomon; solid, unwrapped or single-wrapped loads only; the logger pass criteria (purge plateau of 5 min or more, hold temperature and equivalent time met, and measured temperature within 2 °C of saturation throughout the hold); and backup heat on a stove.

Still **proposed, awaiting Amish** (SCL-DDR-001):

- **Item 5: mounting the lid fittings.** Drill the maker's lid (option i), or use a cooker with factory ports or an adapter plate on the regulator stem (option ii). This is a pressure-safety trade-off and has no recommendation. SCL-CAL-001 section 8 compares the options on holes, ligaments and relief and vent capacity; neither choice changes the relief sizing.
- **Item 12:** first partner and site, chosen per area later.
- **Items 13 to 18:** the TRL 3 findings on tracking (R14), mass (R16), the guard (R11), castors (R15), water at altitude (R10) and the transducer span (R12), each with options and a recommendation.

## Safety

> **Safety:** SunClave concentrates sunlight to a few hundred times normal intensity at the focus, heats a pressure vessel to about 121 °C, and is described in a medical context. Each of these is a serious hazard. It is a research and educational prototype and not a medical device.

- **Concentrated sunlight.** The focal spot reaches about 270 kW/m² in its hottest part and can burn skin within about a second, ignite paper, cloth and dry grass, and cause permanent eye damage. Never look at the focus or into the dish when it faces the sun; wear the shade 5 goggles near the focus; aim only by the gnomon shadow; turn the dish at least 15° away from the sun before reaching toward the cooker; fit the parking cover whenever the dish is idle; keep the ground below clear of anything that can burn; never leave the dish facing the sun unattended or with children nearby.
- **Timber stand.** The stand is timber (decided). It is outside the converging light cone, but a mis-aimed dish or stray reflections can scorch it; keep the steel bearing blocks and holder between the focus and the timber, and inspect for scorching.
- **Pressure and steam.** Use only a commercially made cooker rated for the working pressure, keep its overpressure plug, fit the independent relief valve, and check that the vent is clear before every cycle. Never force the lid open; wait until the gauge reads zero and the regulator has been lifted with a tool. Steam from the regulator and relief valve can scald, so point vents away from people. Do not modify the regulator weight. How the fittings are mounted on the lid (item 5) is undecided and must be settled before anything is built.
- **Boil-dry.** A dry base under concentrated sun would pass 200 °C, where aluminum loses much of its strength. Fill 1.5 L before every cycle and trim the dish during long holds; the base-edge thermocouple alarm at 140 °C prompts the operator to turn the dish away.
- **Hot surfaces.** The lid, handles, fittings, black lower wall, base and instruments reach 121 °C or more. Use heat-resistant gloves and handle the cooker only when the dish is turned away.
- **Tipping, rolling and pinch points.** Lock the castors and the tilt quadrant; in high wind park the dish face-up. The stand can roll before it tips (SCL-CAL-001 section 10). Keep hands clear of the yoke collars and quadrant when tilting.
- **Lithium cells.** The power bank contains lithium cells; keep it shaded inside the logger box and do not charge it above 45 °C.
- **Medical claims.** A PASS on the logger shows the recorded conditions, not that the load is sterile. A cycle below 121 °C is recorded at its real temperature. Biological and chemical indicators remain the reference, and no load from this prototype should be used on a patient.

## Open questions after TRL 3

- Decide item 5 (lid fittings) and items 13 to 18.
- Confirm the cooker brand, dimensions and maker's rating in the first target area, and whether a factory-ported 12 L model exists.
- Validate the equivalent-exposure method (option B) with biological indicators; this is TRL 4 work and is on hold by Amish's instruction.
- Choose a partner and site to learn real loads, altitude and records practice.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [SCL-DWG-001](../cad/drawings/SCL-DWG-001.pdf).
