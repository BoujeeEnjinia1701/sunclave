# BOM notes

Prices are indicative estimates by supplier type (TRL 3), not quotes; they will be confirmed with named suppliers once a partner area is chosen. Row numbers match the exploded view (`media/exploded.png`) and the model (`cad/src/model.py`). Items 7 and 12 have no separate cost; items 17 to 21 are not modelled.

Value-engineering target: USD 450 (`budget_usd` in `project.yaml`, a hypothetical control target, not a limit). Estimated cost of the constructable design (every line except 18): **USD 497**, USD 47 over the target. The total is computed from this file by `docs/04-calcs/sizing.py`.

Changes at TRL 3:

- Decided cuts (SCL-DDR-001 item 2): timber stand instead of steel tube (item 4, $55 to $40), OLED instead of e-paper (item 14), and a USB power bank instead of the 5 W panel and 18650 cell (item 15, $18 to $12). Together with the TRL 2 prices these save about $29, short of the $37 needed to reach $400, so the budget rose to $450.
- Item 13, basket: resized to 250 x 150 mm on a 40 mm trivet, because 270 x 180 mm does not fit a 12 L cooker (SCL-CAL-001 section 1).
- Item 14, logger: a 0.05 % reference resistor on the Pt100 interface (needed for R7) and a 16-bit ADS1115 converter for the pressure transducer are included in the $58.
- Items 19 and 20, eye protection and a parking cover: added for R9 and R11 ($22).
- Item 9: seat bore 4 mm or more specified from the relief capacity check (SCL-CAL-001 section 8).

Item 18 (chemical and biological indicators, about $45) is not in the parts total because it is needed only for testing at TRL 4 and later, which is on hold by Amish's instruction.

Changes from Amish's acceptance of the recommendations (SCL-DDR-002, 2026-09-25):

- Item 4: all four castors lock instead of two ($40 to $44; item 16).
- Item 14: a 0 to 300 kPa absolute transducer with an overpressure rating of 600 kPa or more instead of 0 to 500 kPa, at a similar price (item 18). The 12 min retarget reminder and the trim reminder are firmware rules for the existing buzzer and display (items 13 and 17).
- Item 21: keep-out marking for the restated R11 ($6; item 15).

These add $10, from $430 to $440. How BOM items 8 to 10 are mounted on the lid (item 5) was decided on 2026-10-02: the lid is not drilled; item 6 becomes a pressure canner sold with a factory gauge and relief valve, and the probe gland (item 10) goes on an adapter plate on the vent stem with a bore of 3 mm or more. Items 6, 8, 9 and 10 are to be respecified and repriced; the prices listed are unchanged until then.

Changes for the constructable design (SCL-DDR-003, 2026-10-01, accepted by Amish on 2026-10-02, with a back-up drop pin to be added to item 3), USD 440 to USD 497:

- Item 1: petals with folded flanges and rim tabs, riveted (price unchanged).
- Item 2: ribs at 15 degree offsets, 25 x 4 mm rim band, 200 x 4 mm hub plate and 24 rib clips (USD 30 to 36).
- Item 3: yoke plates with lock fans, rim stand-offs, lock studs and star knobs replace the tube arms, collars, lever and quadrant (USD 18 to 30).
- Item 4: bolted timber stand with side rails on edge and lapped braces, steel axle plates, axles and collars, foot brackets, real 102 mm castors (USD 44 to 58).
- Item 5: flat holder ring cut from plate, arms carried on the upright tops, arm brackets (USD 12 to 17).
- Item 14: a box large enough for the power bank, the transducer on the tee, plug-in sensor leads and the thermocouple band clamp (USD 58 to 66).
- Item 16: gnomon bracket on the rim band (USD 2 to 4).
- Item 17: more bolts for the bolted joints (USD 15 to 25).

The main cost drivers and the savings worth trying are in the design decisions register (`docs/06-design-decisions.md`, Value engineering).
