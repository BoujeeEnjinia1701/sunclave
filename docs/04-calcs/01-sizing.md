---
doc_id: SCL-CAL-001
title: SunClave sizing and first-principles checks
project: SunClave
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (steam and altitude, ray-traced optics, heat loss, cycle and day simulation, measurement, relief capacity for both lid options, boil-dry, masses, wind, logger power, cost) against every requirement
---

# SunClave sizing and first-principles checks

On paper SunClave works, but it is slower, heavier and less forgiving to aim than the TRL 2 estimates said. The ray trace puts about 670 W into the cooker at 700 W/m² direct sun (not 710 W), the vessel loses about 395 W at 121 °C (not 200 W), and a cold start reaches the end of a 30 min hold in about 80 min in the central case and about 109 min in the unfavourable one. Of the 17 requirements, 9 are met, 4 are at risk, 1 cannot be verified at TRL 3 and 3 are **not met**: R11 (the focal-zone guard is still undefined, and the blackened lower wall is hot and within reach), R14 (power stays within 10 % of on-target for only about 13 min of sun motion, not 15 min) and R16 (about 41.0 kg empty against 40 kg). The regulator gives 120.95 °C at sea level, so the "121 °C below about 300 m" claim of TRL 2 was optimistic; the decided altitude strategy (option B) extends the hold instead.

> **Safety:** SunClave is a research and educational prototype, not a medical device. Nothing in this note shows that a load is sterile. The design concentrates sunlight to a few hundred times normal intensity at the focus and holds steam at about 121 °C (250 °F) in a pressure vessel. The numbers here are paper estimates and do not replace the maker's rating of the cooker, a certified relief valve or biological indicators.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `PARAMS` in `cad/src/model.py` and the prices from `bom/bom.csv`, so the model, the drawing SCL-DWG-001 and this note agree. Nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Vessel, dish, aiming, load limits, altitude strategy, budget | As decided | SCL-DDR-001 items 1 to 4 and 6 to 11 |
| Lid fittings | Shown on the lid; mounting method not decided | SCL-DDR-001 open item 5; section 8 covers both options |
| Design case | 700 W/m² direct normal irradiance (DNI), sun 60° above the horizon, 25 °C, wind 2 m/s, sea level, 2.0 kg of stainless instruments in a 0.5 kg basket, 1.5 L of water | SCL-REQ-001 v0.3 |
| Dish | 1.4 m aperture (1.539 m²), focal length 500 mm, depth 245 mm, rim angle 70.0° | `cad/src/model.py` |
| Reflector | Reflectance 0.85; slope error 10 mrad (one standard deviation per axis) | Polished aluminum sheet bent into gores by hand |
| Sun | Pillbox sunshape of 4.65 mrad half-angle; apparent motion up to 15° per hour | Solar disc; worst case at low declination |
| Absorber paint | Absorptance 0.92 up to 60° incidence, falling linearly to half that at 90° | High-temperature matte black; angle fall-off assumed |
| Cooker | 280 mm inside diameter x 200 mm deep (12.3 L), 4 mm wall, 6 mm base, 5 mm lid, aluminum 2,700 kg/m³ | Typical 12 L household cooker; brand to be confirmed |
| Water and steam | IAPWS-IF97 saturation line; latent heat 2,256 kJ/kg at 100 °C and 2,188 kJ/kg at 125 °C | Steam tables |
| Ambient pressure | ICAO standard atmosphere | |
| Regulator and relief | 103.4 kPa (15 psi) gauge; relief set at 125 kPa gauge | SCL-REQ-001 R8 |
| Equivalent exposure | z-value 10 °C, reference 121 °C | Common engineering assumption, **not validated** |
| Wind convection | h = 2.8 + 3.0 v W/(m² K) | Watmuff, Charters and Proctor (1977), as used in solar collector texts |
| Jacket | 25 mm mineral wool, k = 0.040 W/(m K) at 50 °C rising 0.0002 per K; aluminized skin emissivity 0.3 | Supplier data typical |
| Surfaces | Black base and band emissivity 0.9, 5 K above the water; lid emissivity 0.2; 0.03 m² of handles and fittings at emissivity 0.5 | Assumed |
| Retargeting | Every 15 min, so the pointing error grows from 0 to 3.75° between retargets | R14 target |

Three scenarios bracket the result: **favourable** (reflectance 0.88, slope error 6 mrad, absorptance 0.95, wind 1 m/s), **central** (0.85, 10 mrad, 0.92, 2 m/s) and **unfavourable** (0.78 for a dusty dish, 15 mrad, 0.88, 3 m/s). Central values are quoted unless a range is given.

## 2. Steam temperature and altitude (R1)

A weighted regulator holds a fixed pressure above ambient. At sea level 103.4 kPa gauge gives **120.95 °C**, just under 121.0 °C, and the steam temperature falls by about 0.19 K per 100 m of altitude. The TRL 2 statement that the cooker reaches 121 °C "below about 300 m" was wrong; it reaches 121.0 °C only at sea level, and only within the tolerance of the weight.

*Table 2. Steam temperature and the decided extended hold (option B) with altitude.*

| Altitude | Ambient | Boiling point | Steam at 103.4 kPa gauge | Gauge needed for 121 °C | Hold for 20 / 30 min at 121 °C (z = 10 °C) |
| --- | --- | --- | --- | --- | --- |
| 0 m | 101.3 kPa | 100.0 °C | 120.95 °C | 103.7 kPa | 20 / 30 min |
| 250 m | 98.4 kPa | 99.1 °C | 120.49 °C | 106.7 kPa | 23 / 34 min |
| 500 m | 95.5 kPa | 98.3 °C | 120.03 °C | 109.6 kPa | 25 / 37 min |
| 1,000 m | 89.9 kPa | 96.6 °C | 119.13 °C | 115.2 kPa | 31 / 46 min |
| 1,500 m | 84.6 kPa | 95.0 °C | 118.26 °C | 120.5 kPa | 38 / 56 min |
| 1,800 m | 81.5 kPa | 94.0 °C | 117.75 °C | 123.5 kPa | 42 / 63 min |
| 2,400 m | 75.6 kPa | 92.0 °C | 116.74 °C | 129.4 kPa | 53 / 80 min |

Under the decided option B, R1 is restated as an exposure equivalent to 20 or 30 min at 121 °C, with the real temperature recorded. On the calculation the cycle delivers that at every altitude to 2,400 m (116.7 °C, never below the 115 °C floor). Whether the lower-temperature cycle kills as well as the 121 °C one is a microbiological question that only biological indicators can answer, so **R1 is not verifiable at TRL 3**. If the relief valve lifts at 125 kPa gauge, the steam reaches 124.2 °C at sea level, just above the 124 °C cap; that is a fault condition, not a normal cycle.

## 3. Optics (R4, R9, R14)

A Monte Carlo ray trace (60,000 rays) follows sunlight from the aperture to the reflector and on to the level cooker. It includes the shadow of the vessel, holder ring and holder arms, the pillbox sun, slope errors, pointing error and the true receiver shape: the black base on the focal plane, the 80 mm black band of wall above it, and the jacket, which is aluminized and counted as lost. Because the cooker stays level while the dish tilts, the light arrives at the base from one side, and at low sun a quarter of it lands on the wall band instead.

*Table 3. Share of the sun on the aperture absorbed by the cooker, central case, on target.*

| Sun elevation | Unshaded | Onto the vessel | Onto black surfaces | Absorbed | Absorbed at 700 W/m² | Share on the base |
| --- | --- | --- | --- | --- | --- | --- |
| 15° | 0.903 | 0.723 | 0.601 | 0.519 | 559 W | 0.75 |
| 30° | 0.894 | 0.738 | 0.674 | 0.590 | 636 W | 0.73 |
| 45° | 0.890 | 0.723 | 0.720 | 0.622 | 671 W | 0.79 |
| 60° | 0.895 | 0.727 | 0.727 | 0.621 | 669 W | 0.92 |
| 75° | 0.906 | 0.765 | 0.765 | 0.663 | 714 W | 1.00 |
| 90° | 0.923 | 0.785 | 0.785 | 0.700 | 755 W | 1.00 |

In the design case (60°) the power flow is: 1,078 W on the aperture, 819 W reflected and not shaded, 784 W onto the vessel, and **669 W absorbed** (optical efficiency 0.62). The favourable and unfavourable scenarios absorb 723 W and 580 W. The TRL 2 estimate of 710 W assumed 95 % unshaded; the vessel, holder ring and arms shade about 10 %.

The mean flux over the base is about 11 kW/m², but the spot is small: the hottest 20 mm cell receives about **270 kW/m²** (270 suns), far above the 30 to 50 kW/m² stated at TRL 2. The base spreads this heat and the water boils it off (section 9), but the focus is more dangerous to skin and eyes than the TRL 2 documents said.

**Pointing.** The absorbed power falls to 90 % of on-target at a pointing error of about 3.2° (average of elevation and azimuth errors). At the worst-case sun motion of 15° per hour that takes **about 13 min**, so R14 (retarget no more often than every 15 min) is **not met**. The cycle times below assume 15 min retargeting and include the resulting loss (mean 630 W instead of 669 W). Tilting the dish about 15° off the sun cuts the absorbed power below 5 % (R9).

## 4. Heat loss from the vessel

*Table 4. Heat loss at 2 m/s wind and 25 °C ambient.*

| Vessel temperature | Total | Black base and band | Lid | Handles and fittings | Jacketed wall | Jacket skin |
| --- | --- | --- | --- | --- | --- | --- |
| 60 °C | 134 W | 85 W | 35 W | 9 W | 5 W | 28 °C |
| 100 °C | 298 W | 185 W | 77 W | 25 W | 11 W | 33 °C |
| 121 °C | 395 W | 245 W | 101 W | 35 W | 15 W | 36 °C |

The base must stay bare and black to absorb the focus, and it radiates and convects about 245 W at 121 °C; the bare aluminum lid loses about 100 W. The jacket works (15 W), but it covers only a small share of the loss. The TRL 2 figure of 200 W at 121 °C was about half the value here. An insulated lid cover would recover up to about 80 W; this is a suggestion in `docs/REVIEW.md`, not a change to the design.

## 5. Heat-up, hold and water (R4, R10)

The vessel's heat capacity without water is 5.16 kJ/K (body 3.01 kg, lid 0.95 kg, fittings 0.90 kg, instruments 2.0 kg, basket 0.5 kg). The simulation steps in 5 s: heat with the vent open to the local boiling point, 5 min of free steaming to purge air, fit the regulator and heat to the regulated temperature, then hold with the surplus venting through the regulator.

*Table 5. Design cycle at sea level with a 30 min hold (wrapped instruments).*

| Scenario | Mean absorbed | To boiling | Cold start to 121 °C | Cold start to end of hold | Water left of 1.5 L | Cool-down to zero gauge |
| --- | --- | --- | --- | --- | --- | --- |
| Favourable | 677 W | 25.8 min | 40.6 min | 71.0 min | 1.14 kg | 13 min |
| Central | 630 W | 30.6 min | 49.5 min | **79.9 min** | 1.26 kg | 11 min |
| Unfavourable | 548 W | 42.0 min | 78.8 min | **109.2 min** | 1.41 kg | 9 min |

R4 (90 min or less in the design case) is met in the central case and **at risk** overall: a dusty dish with a rougher surface misses it by about 19 min, and the only measured precedent (Kaseman et al., 93 to 183 min of heat-up with 14 to 24 L vessels, cited in SCL-PRB-001) is slower still. With a 20 min hold (unwrapped) the central cycle is 69.8 min; at 600 W/m² it is 94.4 min.

**Water.** In the central case the purge uses 0.044 kg and the hold 0.195 kg, leaving 1.26 kg, well above the 0.5 L of R10. The worst sea-level case, favourable optics at 1,000 W/m² with no trimming, leaves 0.80 kg. Under option B, however, holds grow with altitude and strong sun is common at altitude:

*Table 6. Option B cycles at altitude (30 min reference hold).*

| Altitude | Steam | Hold | Cycle, central | Water left, central | Water left, 1,000 W/m² favourable, no trimming |
| --- | --- | --- | --- | --- | --- |
| 0 m | 121.0 °C | 30 min | 80 min | 1.26 kg | 0.80 kg |
| 1,000 m | 119.1 °C | 46 min | 94 min | 1.15 kg | 0.48 kg |
| 1,800 m | 117.7 °C | 63 min | 110 min | 1.02 kg | 0.14 kg |
| 2,400 m | 116.7 °C | 80 min | 126 min | 0.90 kg | boils dry before the end of the hold |

If the operator trims the dish off the sun so that only about 50 W vents during the hold, 1.31 kg is left even at 1,800 m and 1,000 W/m². R10 is therefore met in the design case but **at risk** for option B cycles in strong sun; a trimming rule is proposed in SCL-DDR-001 (open item 17). Cycle time at altitude also exceeds 90 min at 1,000 m and above; R4 is defined at sea level.

## 6. Cycles in a clear day (R5)

The day simulation starts cold at 09:00 solar time, uses the absorbed power for the sun's elevation at each moment (interpolated from Table 3 with 15 min retargeting), cools to zero gauge, allows 10 min to reload, and restarts warm: the pot and remaining water start at the boiling point, with fresh instruments and top-up water at 25 °C, which gives a restart temperature of about 89 °C. A cycle counts only if its hold ends by 15:00.

*Table 7. Complete cycles between 09:00 and 15:00.*

| Case | Cycles | Hold end times (solar hours) |
| --- | --- | --- |
| Equator, equinox, 700 W/m² | 4 | 10.34, 11.56, 12.76, 14.01 |
| 15° N, winter solstice, 700 W/m² | 4 | 10.36, 11.65, 12.93, 14.22 |
| Equator, equinox, 600 W/m² | 4 | 10.58, 11.88, 13.18, 14.58 |

R5 (3 or more) is **met** with one cycle of margin, because warm restarts take only 50 to 60 min. The TRL 2 estimate of 3 cycles assumed a 30 min turnaround; the natural cool-down is 9 to 13 min.

## 7. Measurement (R7, R12)

At 121 °C a Pt100 reads 146.44 Ω and changes by 0.3769 Ω/K. The class A tolerance is 0.39 K, a 0.1 % reference resistor on the MAX31865 board adds 0.39 K and a 0.05 % resistor 0.19 K; the 15-bit step is 0.035 K. The root sum square is **0.55 K with a 0.1 % reference** (fails R7's 0.5 K) and **0.44 K with 0.05 %**, so the BOM now specifies the 0.05 % part and R7 is **met on datasheets**. The pressure transducer, 1 % of a 500 kPa span read through a 16-bit ADS1115 converter, gives 5 kPa, equal to the R7 target.

The field check against boiling water needs care: near 100 °C the boiling point changes by 0.277 K per kPa, so checking against the logger's own transducer (±5 kPa) carries ±1.4 K of doubt. A reference barometer reading to 0.2 kPa (a phone barometer or the nearest weather station) reduces this to 0.06 K.

For the air-removal check (R12), the saturation temperature changes by 0.155 K per kPa near 205 kPa absolute, so the pressure error alone is 0.78 K and the combined check uncertainty is **0.89 K** against a 2 K threshold. A 2 K deficit means about 6.1 % air by volume; allowing for the uncertainty, the logger is sure to flag about 9 % air and may flag from about 3 %. R12 is **at risk**. A 0 to 300 kPa transducer (3 kPa) would cut the check uncertainty to 0.64 K; this is proposed in SCL-DDR-001 (open item 18).

## 8. Pressure safety and the lid options (R8)

The worst steam generation is the favourable optics at 1,000 W/m² with the sun overhead and no heat loss: 1,153 W absorbed, **0.52 g/s** of steam. Choked-flow capacities with a discharge coefficient of 0.6 are:

- the regulator vent (3 mm bore, assumed): 1.36 g/s, 2.6 times the worst generation;
- the independent relief valve (4 mm seat, assumed) at 125 kPa gauge: 2.66 g/s, 5.1 times the worst generation. Any seat of 1.8 mm or more would pass it.

The pressure on the lid is 6.4 kN at 103.4 kPa and 7.7 kN at 125 kPa, over the 280 mm bore. R8 is **met** on capacity; the vessel's own rating can only be confirmed from the maker's data for the model chosen.

How the gauge, relief valve and probe gland are mounted is **open for Amish** (SCL-DDR-001 open item 5). The calculation applies to both options and does not choose between them:

*Table 8. Lid options compared on calculable points only.*

| Point | Option (i): drill the maker's lid | Option (ii): factory ports or an adapter plate on the regulator stem |
| --- | --- | --- |
| New holes in the maker's lid | 3 (two 11.1 mm tap drills for 1/4 in NPT, one 8.7 mm for 1/8 in NPT) | 0 |
| Metal removed | 30.9 mm of drilled diameter, 0.41 % of the lid area | None from the lid |
| Spacing | Smallest ligament between holes 67 mm; smallest distance to the bore 41 mm | Set by the maker or the adapter |
| Relief and vent capacity | As above (5.1 and 2.6 times) | Same, provided the adapter keeps a vent bore of 3 mm or more (1.36 g/s) and leaves the overpressure plug untouched |
| What a calculation cannot show | Whether the maker's rating still holds after drilling; the lid is not a flat plate and its design data are not public | Whether a factory-ported 12 L cooker exists in the target market, and the rating of an adapter joint |

## 9. Boil-dry and base temperature (R10)

At 121 °C the surplus is about 235 W. If the operator forgot to turn the dish away after a central hold, the 1.26 kg left would boil dry in about 196 min. While water remains, Rohsenow's nucleate boiling correlation at the peak absorbed flux (252 kW/m²) puts the hottest spot of the base 10.3 K above the water, about 131 °C, which leaves 6.5 K below the 140 °C alarm after a 2.2 K type K tolerance. The thermocouple must sit at the base edge, out of the focal spot, or it will read the sunlight rather than the metal. A dry base in full sun would settle near 227 °C on average and hotter at the spot, where aluminum loses much of its strength; the alarm and the water rule matter.

## 10. Masses, handling and wind (R15, R16)

*Table 9. Mass estimate from the model parameters.*

| Group | Mass |
| --- | --- |
| Dish: reflector (0.5 mm aluminum, 1.71 m²), ribs, rim, hub, gnomon | 10.9 kg |
| Yoke (two 269 mm arms, collars, lock) | 1.7 kg |
| Timber stand with quadrant, bearing blocks and castors (12.0 kg of timber) | 19.4 kg |
| Pot holder | 2.6 kg |
| Vessel with fittings, jacket and basket | 5.6 kg |
| Logger and power bank | 0.9 kg |
| **Empty total** | **41.0 kg** (44.5 kg loaded) |

R16 is **not met** on total mass: about 41.0 kg against 40 kg. The decided timber stand is heavier than the TRL 2 steel estimate (13 kg). The handling pieces are all within 20 kg: the stand 19.4 kg, the dish with yoke 12.6 kg, the vessel 5.6 kg and the bolted-on holder and logger 3.5 kg.

The loaded vessel's centre of mass sits about 98 mm above its base, which lies on the tilt axis. A holder free to swing on that axis would be top-heavy, so the model fixes the holder to the uprights and lets only the dish and yoke turn on the stub axles. The dish's own centre of mass is 366 mm from the axis, so the quadrant lock must hold up to 37.9 N·m of gravity torque at 15° elevation.

**Wind at 10 m/s** (60 Pa): the dish is taken as a plate with a drag coefficient of 1.4 when the wind blows onto the reflector and 1.2 onto the back, acting at the aperture centre, with the vessel and uprights added. The worst case is a low sun (15° elevation) with the wind blowing onto the reflector, because the dish then leans over the lee castor line: 153 N, 134 N·m overturning against 174 N·m restoring, a factor of **1.30**. Every other case is 1.50 or better. R15 (does not tip) is met on this estimate, but with a thin margin it is recorded as **at risk**. The same 153 N exceeds the 109 N of grip from two locked castors (friction coefficient 0.5), so the stand would roll before it tipped; four locking castors would give 218 N (SCL-DDR-001 open item 16).

## 11. Logger power and record (R6, R13)

The logger draws about 0.31 W (ESP32, sensors, OLED and microSD), or 2.9 Wh for an 8 h operating day through an 85 % converter. A 10,000 mAh power bank, at 85 % output efficiency and 80 % usable, stores 25.2 Wh: **8.7 days** without recharging, against 3 days in R13. The logger draws only about 72 mA at 5 V, and many power banks switch off below 50 to 100 mA, so the bank must have a low-current (always-on) mode. A record of 16 bytes per 1 s sample for up to 3 h is 173 kB per cycle; a 4 GB card holds about 23,000 cycles (R6 asks for 1,000).

## 12. Cost (R17)

The priced BOM (`bom/bom.csv`) totals **$430** for parts (every line except item 18), against the $450 budget set by Amish's decision (SCL-DDR-001 item 2), a margin of $20. The decided cuts (timber stand, OLED display, power bank) save about $29 against the TRL 2 prices, which was short of the $37 needed to reach $400; the new safety items (goggles and parking cover, $22) and the 0.05 % reference and ADS1115 are included. Validation consumables (item 18, $45) are excluded, as R17 states. All prices are indicative estimates by supplier type, not quotes.

## 13. Results against every requirement

*Table 10. Requirement status at TRL 3 (also in `docs/04-calcs/results.csv`).*

| ID | Requirement | Value (central unless stated) | Target (SCL-REQ-001 v0.3) | Status |
| --- | --- | --- | --- | --- |
| R1 | Sterilizing condition (redefined) | 120.95 °C and 30.3 min at 0 m; 117.7 °C and 63 min at 1,800 m | Exposure equal to 20 or 30 min at 121 °C (z = 10 °C), 115 to 124 °C, real temperature recorded | Not verifiable at TRL 3 |
| R2 | Load capacity | Basket 250 x 150 mm in a 12.3 L cooker, 16 mm above the water | Basket 250 x 150 mm or more; 2.0 kg | Met |
| R3 | Load type | Solid instruments, unwrapped or single-wrapped | No lumened, hollow or textile loads | Met |
| R4 | Cycle time | 80 min (71 to 109 min) | 90 min or less | At risk |
| R5 | Daily throughput | 4 cycles in every case of Table 7 | 3 or more | Met |
| R6 | Cycle record | 173 kB per cycle; about 23,000 cycles on 4 GB | 1 s logging; 1,000 cycles | Met |
| R7 | Measurement accuracy | 0.44 K (0.05 % reference); 5 kPa | 0.5 K; 5 kPa | Met |
| R8 | Pressure safety | Relief 5.1 times, vent 2.6 times the worst steam generation | Relief 125 kPa gauge or less; vessel rated by its maker | Met |
| R9 | Heat input control | Below 5 % of power at 15° off the sun; parking cover | Stop within 10 s; dish shaded when parked | Met |
| R10 | Boil-dry protection | 1.26 kg left (design); 0.14 kg at 1,800 m and 1,000 W/m² without trimming | 0.5 L left; alarm at 140 °C | At risk |
| R11 | Burn and glare protection | Focal-zone guard not defined; black base and band above 60 °C within reach | No surface above 60 °C within reach except lid and handles; guard; eye protection | **Not met** |
| R12 | Air-removal check | Check uncertainty 0.89 K; sure to flag 9 % air | Flag a hold more than 2 K below saturation | At risk |
| R13 | Logger power (redefined) | 8.7 days on a 10,000 mAh bank | 3 days without charging; USB recharge | Met |
| R14 | Tracking effort | 90 % of on-target power held for about 13 min | Retarget no more often than every 15 min | **Not met** |
| R15 | Stability | Tipping factor 1.30 (15° elevation); rolls on two locked castors | Does not tip at 10 m/s | At risk |
| R16 | Portability and build | 41.0 kg empty; largest piece 19.4 kg | 40 kg or less; pieces 20 kg or less | **Not met** |
| R17 | Cost (redefined) | $430 | $450 or less for parts | Met |

Summary: 9 met, 4 at risk (R4, R10, R12, R15), 1 not verifiable at TRL 3 (R1) and 3 not met (R11, R14, R16).

## 14. Checks against earlier claims

The TRL 2 documents stated several numbers that this note corrects; SCL-PRC-001 and SCL-REQ-001 v0.3 now carry the values above.

- Steam at sea level: 121.1 °C claimed, **120.95 °C** calculated; 121 °C "below about 300 m" claimed, **sea level only**.
- Absorbed power: about 710 W claimed, **669 W** (ray trace, 60° sun); shading about 10 %, not 5 %.
- Loss at 121 °C: about 200 W claimed, **395 W**.
- Cold start to 121 °C: about 35 min claimed, **49.5 min** central.
- Peak flux on the base: 30 to 50 kW/m² claimed, **about 270 kW/m²** in the hottest 20 mm cell.
- Pointing tolerance: about 8° claimed, **3.2°** to 90 % of on-target power.
- Cycles per day: about 3 claimed, **4** (faster warm restarts).
- Wind: 110 N·m against 180 N·m claimed, **134 N·m against 174 N·m** at the worst tilt.
- Mass: about 32 to 33 kg claimed, **41.0 kg** with the decided timber stand.
- Basket: 270 x 180 mm claimed; it does not fit a 12 L cooker, so it is now **250 x 150 mm**, the R2 minimum.
- Logger autonomy: about 5 days on the panel and cell, now **8.7 days** on the decided power bank.
