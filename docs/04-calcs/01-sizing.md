---
doc_id: SCL-CAL-001
title: SunClave sizing and first-principles checks
project: SunClave
doc_type: Calculation note
version: "0.3"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (steam and altitude, ray-traced optics, heat loss, cycle and day simulation, measurement, relief capacity for both lid options, boil-dry, masses, wind, logger power, cost) against every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (SCL-DDR-003); masses taken from the model's parts; holder ring and handles in the ray trace; tilt lock force; cost against the value-engineering target
---

# SunClave sizing and first-principles checks

On paper SunClave works, but it is slower, heavier and less forgiving to aim than the TRL 2 estimates said. The ray trace puts about 660 W into the cooker at 700 W/m² direct sun (not 710 W), the vessel loses about 395 W at 121 °C (not 200 W), and a cold start reaches the end of a 30 min hold in about 80 min in the central case and about 109 min in the unfavourable one. Version 0.2 applies Amish's acceptance of the recommendations on items 13 to 18 (SCL-DDR-002): retargeting every 12 min (R14 relaxed), a 45 kg total (R16 relaxed), the whole vessel treated as a marked hot zone (R11 restated), four locking castors (R15), a trimming rule with a logger reminder (R10) and a 0 to 300 kPa transducer (R12). In v0.2, of the 17 requirements, 14 were met, 2 were at risk (R4 cycle time and R15 stability) and 1 could not be verified at TRL 3 (R1); no requirement was left not met, although three of the changes (R11, R14, R16) are restated or relaxed targets. The regulator gives 120.95 °C at sea level, so the "121 °C below about 300 m" claim of TRL 2 was optimistic; the decided altitude strategy (option B) extends the hold instead. Version 0.3 follows the constructable design of SCL-DDR-003: the masses now come from the model's parts (44.4 kg empty), the wider holder ring and the handles are in the ray trace (663 W absorbed, 80 min cycle), and the cost (USD 497) is reported against the USD 450 value-engineering target (USD 47 over) instead of as met or not met. No other requirement changes status: 13 met, 2 at risk (R4, R15) and 1 not verifiable at TRL 3 (R1).

> **Safety:** SunClave is a research and educational prototype, not a medical device. Nothing in this note shows that a load is sterile. The design concentrates sunlight to a few hundred times normal intensity at the focus and holds steam at about 121 °C (250 °F) in a pressure vessel. The numbers here are paper estimates and do not replace the maker's rating of the cooker, a certified relief valve or biological indicators.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `PARAMS` in `cad/src/model.py` and the prices from `bom/bom.csv`, so the model, the drawing SCL-DWG-001 and this note agree. Nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Vessel, dish, aiming, load limits, altitude strategy, budget | As decided | SCL-DDR-001 items 1 to 4 and 6 to 11 |
| Retargeting, mass limit, hot zone, castors, trimming rule, transducer span | As decided | SCL-DDR-002 items 13 to 18 |
| Lid fittings | Shown on the lid; mounting method not decided | SCL-DDR-001 open item 5; section 8 covers both options |
| Construction | Stand, pivots, locks, holder, dish frame and fixings as in the constructable model | SCL-DDR-003 (draft, open for Amish's review) |
| Design case | 700 W/m² direct normal irradiance (DNI), sun 60° above the horizon, 25 °C, wind 2 m/s, sea level, 2.0 kg of stainless instruments in a 0.5 kg basket, 1.5 L of water | SCL-REQ-001 v0.5 |
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
| Retargeting | Every 12 min, so the pointing error grows from 0 to 3.0° between retargets | R14 target, relaxed from 15 min (SCL-DDR-002 item 13) |
| Pressure transducer | 0 to 300 kPa absolute, 1 % of span | SCL-DDR-002 item 18 (was 0 to 500 kPa) |

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

A Monte Carlo ray trace (60,000 rays) follows sunlight from the aperture to the reflector and on to the level cooker. It includes the shadow of the vessel, the holder ring, the cooker handles and the holder arms, the pillbox sun, slope errors, pointing error and the true receiver shape: the black base on the focal plane, the 80 mm black band of wall above it, and the jacket, which is aluminized and counted as lost. Because the cooker stays level while the dish tilts, the light arrives at the base from one side, and at low sun a quarter of it lands on the wall band instead.

*Table 3. Share of the sun on the aperture absorbed by the cooker, central case, on target.*

| Sun elevation | Unshaded | Onto the vessel | Onto black surfaces | Absorbed | Absorbed at 700 W/m² | Share on the base |
| --- | --- | --- | --- | --- | --- | --- |
| 15° | 0.902 | 0.719 | 0.597 | 0.515 | 555 W | 0.76 |
| 30° | 0.890 | 0.735 | 0.671 | 0.588 | 634 W | 0.73 |
| 45° | 0.885 | 0.719 | 0.716 | 0.619 | 667 W | 0.79 |
| 60° | 0.887 | 0.721 | 0.721 | 0.615 | 663 W | 0.92 |
| 75° | 0.895 | 0.755 | 0.755 | 0.654 | 705 W | 1.00 |
| 90° | 0.897 | 0.763 | 0.763 | 0.680 | 733 W | 1.00 |

In the design case (60°) the power flow is: 1,078 W on the aperture, 812 W reflected and not shaded, 777 W onto the vessel, and **663 W absorbed** (optical efficiency 0.615). The favourable and unfavourable scenarios absorb 716 W and 575 W. The TRL 2 estimate of 710 W assumed 95 % unshaded; the vessel, holder ring, handles and arms shade about 11 %. In v0.2 the result was 669 W; the constructable holder ring (408 mm across, sized to carry the handles) shades a little more.

The mean flux over the base is about 11 kW/m², but the spot is small: the hottest 20 mm cell receives about **270 kW/m²** (270 suns), far above the 30 to 50 kW/m² stated at TRL 2. The base spreads this heat and the water boils it off (section 9), but the focus is more dangerous to skin and eyes than the TRL 2 documents said.

**Pointing.** The absorbed power falls to 90 % of on-target at a pointing error of about 3.1° (average of elevation and azimuth errors). At the worst-case sun motion of 15° per hour that takes **about 13 min**. The original R14 target of 15 min was not met; Amish accepted the recommendation to relax it to 12 min with a logger reminder (SCL-DDR-002 item 13), so R14 is now **met** with about 1 min of margin. The cycle times below assume 12 min retargeting and include the resulting loss (mean 632 W instead of 663 W). Tilting the dish about 15° off the sun cuts the absorbed power below 5 % (R9).

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
| Favourable | 679 W | 25.8 min | 40.5 min | 70.9 min | 1.14 kg | 13 min |
| Central | 632 W | 30.4 min | 49.3 min | **79.8 min** | 1.26 kg | 11 min |
| Unfavourable | 550 W | 41.8 min | 78.2 min | **108.7 min** | 1.41 kg | 9 min |

R4 (90 min or less in the design case) is met in the central case and **at risk** overall: a dusty dish with a rougher surface misses it by about 19 min, and the only measured precedent (Kaseman et al., 93 to 183 min of heat-up with 14 to 24 L vessels, cited in SCL-PRB-001) is slower still. With a 20 min hold (unwrapped) the central cycle is 69.6 min; at 600 W/m² it is 94.1 min.

**Water.** In the central case the purge uses 0.044 kg and the hold 0.197 kg, leaving 1.26 kg, well above the 0.5 L of R10. The worst sea-level case, favourable optics at 1,000 W/m² with no trimming, leaves 0.81 kg. Under option B, however, holds grow with altitude and strong sun is common at altitude:

*Table 6. Option B cycles at altitude (30 min reference hold).*

| Altitude | Steam | Hold | Cycle, central | Water left, central | Water left, 1,000 W/m² favourable, no trimming |
| --- | --- | --- | --- | --- | --- |
| 0 m | 121.0 °C | 30 min | 80 min | 1.26 kg | 0.81 kg |
| 1,000 m | 119.1 °C | 46 min | 94 min | 1.15 kg | 0.50 kg |
| 1,800 m | 117.7 °C | 63 min | 110 min | 1.02 kg | 0.15 kg |
| 2,400 m | 116.7 °C | 80 min | 126 min | 0.89 kg | boils dry before the end of the hold |

If the operator trims the dish off the sun so that only about 50 W vents during the hold, 1.31 kg is left at 1,800 m and 1.28 kg at 2,400 m, both at 1,000 W/m². Amish accepted the recommended trimming rule (SCL-DDR-002 item 17): the logger shows a trim reminder whenever the computed hold exceeds 40 min, which covers every site at 1,000 m and above, where an untrimmed hold in strong sun leaves 0.50 kg or less. With the rule, R10 (restated to include it) is **met**; it depends on the operator acting on the reminder, and the 140 °C base alarm stays as the backstop. Cycle time at altitude also exceeds 90 min at 1,000 m and above; R4 is defined at sea level.

## 6. Cycles in a clear day (R5)

The day simulation starts cold at 09:00 solar time, uses the absorbed power for the sun's elevation at each moment (interpolated from Table 3 with 12 min retargeting), cools to zero gauge, allows 10 min to reload, and restarts warm: the pot and remaining water start at the boiling point, with fresh instruments and top-up water at 25 °C, which gives a restart temperature of about 89 °C. A cycle counts only if its hold ends by 15:00.

*Table 7. Complete cycles between 09:00 and 15:00.*

| Case | Cycles | Hold end times (solar hours) |
| --- | --- | --- |
| Equator, equinox, 700 W/m² | 4 | 10.33, 11.56, 12.77, 14.02 |
| 15° N, winter solstice, 700 W/m² | 4 | 10.35, 11.63, 12.91, 14.19 |
| Equator, equinox, 600 W/m² | 4 | 10.57, 11.88, 13.18, 14.59 |

R5 (3 or more) is **met** with one cycle of margin, because warm restarts take only 50 to 60 min. The TRL 2 estimate of 3 cycles assumed a 30 min turnaround; the natural cool-down is 9 to 13 min.

## 7. Measurement (R7, R12)

At 121 °C a Pt100 reads 146.44 Ω and changes by 0.3769 Ω/K. The class A tolerance is 0.39 K, a 0.1 % reference resistor on the MAX31865 board adds 0.39 K and a 0.05 % resistor 0.19 K; the 15-bit step is 0.035 K. The root sum square is **0.55 K with a 0.1 % reference** (fails R7's 0.5 K) and **0.44 K with 0.05 %**, so the BOM now specifies the 0.05 % part and R7 is **met on datasheets**. The pressure transducer, now 1 % of a 300 kPa span (SCL-DDR-002 item 18) read through a 16-bit ADS1115 converter, gives 3 kPa, inside the 5 kPa R7 target.

The field check against boiling water needs care: near 100 °C the boiling point changes by 0.277 K per kPa, so checking against the logger's own transducer (±3 kPa) carries ±0.8 K of doubt. A reference barometer reading to 0.2 kPa (a phone barometer or the nearest weather station) reduces this to 0.06 K.

For the air-removal check (R12), the saturation temperature changes by 0.155 K per kPa near 205 kPa absolute. With the decided 0 to 300 kPa transducer the pressure error alone is 0.47 K and the combined check uncertainty is **0.64 K** against a 2 K threshold (0.89 K on the earlier 0 to 500 kPa part). That is 32 % of the threshold, inside a 3:1 test uncertainty ratio, so R12 is **met** on calculation, narrowly. A 2 K deficit means about 6.1 % air by volume; allowing for the uncertainty, the logger is sure to flag about 8 % air and may flag from about 2 %. The highest absolute pressure is 205 kPa in normal use and 226 kPa at relief lift, inside the span; the transducer's overpressure rating must exceed the relief set point, and the BOM asks for 600 kPa or more.

## 8. Pressure safety and the lid options (R8)

The worst steam generation is the favourable optics at 1,000 W/m² with the sun overhead and no heat loss: 1,119 W absorbed, **0.51 g/s** of steam. Choked-flow capacities with a discharge coefficient of 0.6 are:

- the regulator vent (3 mm bore, assumed): 1.36 g/s, 2.7 times the worst generation;
- the independent relief valve (4 mm seat, assumed) at 125 kPa gauge: 2.66 g/s, 5.2 times the worst generation. Any seat of 1.8 mm or more would pass it.

The pressure on the lid is 6.4 kN at 103.4 kPa and 7.7 kN at 125 kPa, over the 280 mm bore. R8 is **met** on capacity; the vessel's own rating can only be confirmed from the maker's data for the model chosen.

How the gauge, relief valve and probe gland are mounted is **open for Amish** (SCL-DDR-001 open item 5). The calculation applies to both options and does not choose between them:

*Table 8. Lid options compared on calculable points only.*

| Point | Option (i): drill the maker's lid | Option (ii): factory ports or an adapter plate on the regulator stem |
| --- | --- | --- |
| New holes in the maker's lid | 3 (two 11.1 mm tap drills for 1/4 in NPT, one 8.7 mm for 1/8 in NPT) | 0 |
| Metal removed | 30.9 mm of drilled diameter, 0.41 % of the lid area | None from the lid |
| Spacing | Smallest ligament between holes 67 mm; smallest distance to the bore 41 mm | Set by the maker or the adapter |
| Relief and vent capacity | As above (5.2 and 2.7 times) | Same, provided the adapter keeps a vent bore of 3 mm or more (1.36 g/s) and leaves the overpressure plug untouched |
| What a calculation cannot show | Whether the maker's rating still holds after drilling; the lid is not a flat plate and its design data are not public | Whether a factory-ported 12 L cooker exists in the target market, and the rating of an adapter joint |

## 9. Boil-dry and base temperature (R10)

At 121 °C the surplus is about 237 W. If the operator forgot to turn the dish away after a central hold, the 1.26 kg left would boil dry in about 195 min. While water remains, Rohsenow's nucleate boiling correlation at the peak absorbed flux (250 kW/m²) puts the hottest spot of the base 10.3 K above the water, about 131 °C, which leaves 6.5 K below the 140 °C alarm after a 2.2 K type K tolerance. The thermocouple must sit at the base edge, out of the focal spot, or it will read the sunlight rather than the metal. A dry base in full sun would settle near 228 °C on average and hotter at the spot, where aluminum loses much of its strength; the alarm and the water rule matter.

## 10. Masses, handling and wind (R15, R16)

Since v0.3 the masses of the structure come from the constructable model (SCL-DDR-003): each part's volume times its density (steel 7,850, aluminium 2,700 and timber 500 kg/m³), the petals at their real 0.5 mm thickness with their flanges and tabs, and catalogue masses for the castors and lock studs.

*Table 9. Mass from the model's parts.*

| Group | Mass |
| --- | --- |
| Dish: petals (2.56 kg), ribs, rim band, hub plate, clips, gnomon and rivets | 12.0 kg |
| Yoke plates and rim stand-offs | 3.3 kg |
| Stand: timber (12.7 kg), castors, axle plates, axles, collars, brackets, lock studs and bolts | 18.9 kg |
| Pot holder: ring, arms, brackets and bolts | 3.5 kg |
| Vessel with fittings, jacket and basket | 5.6 kg |
| Logger, transducer, cable and power bank | 1.0 kg |
| **Empty total** | **44.4 kg** (47.9 kg loaded) |

The total is 44.4 kg against the 45 kg of R16 (relaxed by SCL-DDR-002 item 14), so R16 is **met** with 0.6 kg of margin; v0.2 estimated 41.0 kg before the clips, plates, brackets and bolts of the constructable design were counted. The stand now bolts together and comes apart, so the handling pieces are the dish with its yoke plates (15.4 kg), each stand side frame (6.0 kg), each cross rail with its castors (3.4 kg), the bolted-on holder and logger (4.5 kg) and the empty vessel (5.6 kg), all within 20 kg.

The loaded vessel's centre of mass sits about 98 mm above its base, which lies on the tilt axis. A holder free to swing on that axis would be top-heavy, so the holder ring is fixed to the uprights and only the dish and yoke plates turn on the axles. The tilting group (15.4 kg) has its centre of mass 321 mm from the axis, so the locks carry up to 45.4 N·m of gravity torque at 15° elevation (v0.2: 37.9 N·m for the dish alone). Each of the two star-knob locks clamps the yoke plate's fan on both faces at a 150 mm radius; with a steel-on-steel friction coefficient of 0.3 each needs a clamp force of about 252 N, against about 2,000 N from a hand-tight M10.

**Wind at 10 m/s** (60 Pa): the dish is taken as a plate with a drag coefficient of 1.4 when the wind blows onto the reflector and 1.2 onto the back, acting at the aperture centre, with the vessel and uprights added. The worst case is a low sun (15° elevation) with the wind blowing onto the reflector, because the dish then leans over the lee castor line: 153 N, 134 N·m overturning against 185 N·m restoring, a factor of **1.38** (1.30 in v0.2, before the heavier tilting group and the wider castor line of the constructable stand). Every other case is 1.61 or better. The tipping line is taken at the castor centres, 515 mm from the middle, less 25 mm for the swivel offset. R15 (does not tip) is met on this estimate, but with a thin margin it is recorded as **at risk**. The same 153 N exceeded the 109 N of grip from the two locked castors of v0.1 (friction coefficient 0.5), so the stand would have rolled before it tipped. With the decided four locking castors (SCL-DDR-002 item 16) the grip is 235 N, 1.5 times the wind force. The tipping factor is unchanged, so R15 stays **at risk**, and the decided rule is to park the dish face-up in high wind.

## 11. Logger power and record (R6, R13)

The logger draws about 0.31 W (ESP32, sensors, OLED and microSD), or 2.9 Wh for an 8 h operating day through an 85 % converter. A 10,000 mAh power bank, at 85 % output efficiency and 80 % usable, stores 25.2 Wh: **8.7 days** without recharging, against 3 days in R13. The logger draws only about 72 mA at 5 V, and many power banks switch off below 50 to 100 mA, so the bank must have a low-current (always-on) mode. A record of 16 bytes per 1 s sample for up to 3 h is 173 kB per cycle; a 4 GB card holds about 23,000 cycles (R6 asks for 1,000).

## 12. Cost (R17)

Value-engineering target: USD 450 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 497 for parts (every line of `bom/bom.csv` except item 18), USD 47 over the target. In v0.2 the parts came to USD 440; making the design constructable (SCL-DDR-003) respecified and repriced lines 1 to 5, 14, 16 and 17 and added USD 57, mostly the yoke plates and locks (line 3), the axle plates, axles and brackets (line 4), the plate ring (line 5), the larger logger box with plug-in leads (line 14) and more bolts (line 17). Validation consumables (item 18, USD 45) are excluded, as R17 states. All prices are indicative estimates by supplier type, not quotes. The main cost drivers and the savings worth trying are in the design decisions register (SCL-DEC-001, Value engineering).

## 13. Results against every requirement

*Table 10. Requirement status at TRL 3 (also in `docs/04-calcs/results.csv`).*

| ID | Requirement | Value (central unless stated) | Target (SCL-REQ-001 v0.5) | Status |
| --- | --- | --- | --- | --- |
| R1 | Sterilizing condition (redefined) | 120.95 °C and 30.3 min at 0 m; 117.7 °C and 63 min at 1,800 m | Exposure equal to 20 or 30 min at 121 °C (z = 10 °C), 115 to 124 °C, real temperature recorded | Not verifiable at TRL 3 |
| R2 | Load capacity | Basket 250 x 150 mm in a 12.3 L cooker, 16 mm above the water | Basket 250 x 150 mm or more; 2.0 kg | Met |
| R3 | Load type | Solid instruments, unwrapped or single-wrapped | No lumened, hollow or textile loads | Met |
| R4 | Cycle time | 80 min (71 to 109 min) | 90 min or less | At risk |
| R5 | Daily throughput | 4 cycles in every case of Table 7 | 3 or more | Met |
| R6 | Cycle record | 173 kB per cycle; about 23,000 cycles on 4 GB | 1 s logging; 1,000 cycles | Met |
| R7 | Measurement accuracy | 0.44 K (0.05 % reference); 3 kPa (0 to 300 kPa) | 0.5 K; 5 kPa | Met |
| R8 | Pressure safety | Relief 5.2 times, vent 2.7 times the worst steam generation | Relief 125 kPa gauge or less; vessel rated by its maker | Met |
| R9 | Heat input control | Below 5 % of power at 15° off the sun; parking cover | Stop within 10 s; dish shaded when parked | Met |
| R10 | Boil-dry protection (restated) | 1.26 kg left (design); with the trimming rule 1.31 kg at 1,800 m and 1.28 kg at 2,400 m, 1,000 W/m² (0.15 kg at 1,800 m untrimmed) | 0.5 L left in the design case and, with the trimming rule, at altitude; trim reminder; alarm at 140 °C | Met |
| R11 | Burn and glare protection (restated) | Whole vessel and fittings a marked hot zone, reached only with the dish 15° off the sun; parking cover, goggles and keep-out marking in the BOM | Vessel and fittings a marked hot zone; focus reachable only through the dish; eye protection; keep-out marked | Met (design review) |
| R12 | Air-removal check | Check uncertainty 0.64 K (0 to 300 kPa transducer); sure to flag 8 % air | Flag a hold more than 2 K below saturation | Met |
| R13 | Logger power (redefined) | 8.7 days on a 10,000 mAh bank | 3 days without charging; USB recharge | Met |
| R14 | Tracking effort (relaxed) | 90 % of on-target power held for about 13 min | Retarget no more often than every 12 min; logger reminder | Met |
| R15 | Stability | Tipping factor 1.38 (15° elevation); four locked castors grip 235 N against 153 N of wind | Does not tip at 10 m/s | At risk |
| R16 | Portability and build (relaxed) | 44.4 kg empty; largest piece 15.4 kg | 45 kg or less; pieces 20 kg or less | Met |
| R17 | Cost (redefined) | USD 497 | USD 450 value-engineering target for parts | Over the target by USD 47 |

Summary: 13 met, 2 at risk (R4, R15), 1 not verifiable at TRL 3 (R1), 0 not met, and R17 reported against the value-engineering target (USD 47 over). In v0.1 the count was 9 met, 4 at risk (R4, R10, R12, R15), 1 not verifiable and 3 not met (R11, R14, R16); the change comes from the decisions in SCL-DDR-002, of which R14, R16 and R11 are relaxed or restated targets rather than design improvements.

## 14. Checks against earlier claims

The TRL 2 documents stated several numbers that this note corrects; SCL-PRC-001 and SCL-REQ-001 v0.5 now carry the values above.

- Steam at sea level: 121.1 °C claimed, **120.95 °C** calculated; 121 °C "below about 300 m" claimed, **sea level only**.
- Absorbed power: about 710 W claimed, **663 W** (ray trace, 60° sun); shading about 11 %, not 5 %.
- Loss at 121 °C: about 200 W claimed, **395 W**.
- Cold start to 121 °C: about 35 min claimed, **49.3 min** central.
- Peak flux on the base: 30 to 50 kW/m² claimed, **about 270 kW/m²** in the hottest 20 mm cell.
- Pointing tolerance: about 8° claimed, **3.1°** to 90 % of on-target power.
- Cycles per day: about 3 claimed, **4** (faster warm restarts).
- Wind: 110 N·m against 180 N·m claimed, **134 N·m against 185 N·m** at the worst tilt.
- Mass: about 32 to 33 kg claimed, **44.4 kg** with the decided timber stand and the constructable design.
- Basket: 270 x 180 mm claimed; it does not fit a 12 L cooker, so it is now **250 x 150 mm**, the R2 minimum.
- Logger autonomy: about 5 days on the panel and cell, now **8.7 days** on the decided power bank.
