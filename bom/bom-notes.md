# BOM notes

Prices are indicative estimates by supplier type (TRL 3), not quotes; they will be confirmed with named suppliers once a partner area is chosen. Row numbers match the exploded view (`media/exploded.png`) and the model (`cad/src/model.py`). Items 7 and 12 have no separate cost; items 17 to 20 are not modelled.

Parts for one prototype (every line except 18) total **$430**, within the **$450** budget in `project.yaml` (raised from $400 by Amish on 2026-09-25, SCL-DDR-001 item 2), a margin of $20. The total is computed from this file by `docs/04-calcs/sizing.py`.

Changes at TRL 3:

- Decided cuts (SCL-DDR-001 item 2): timber stand instead of steel tube (item 4, $55 to $40), OLED instead of e-paper (item 14), and a USB power bank instead of the 5 W panel and 18650 cell (item 15, $18 to $12). Together with the TRL 2 prices these save about $29, short of the $37 needed to reach $400, so the budget rose to $450.
- Item 13, basket: resized to 250 x 150 mm on a 40 mm trivet, because 270 x 180 mm does not fit a 12 L cooker (SCL-CAL-001 section 1).
- Item 14, logger: a 0.05 % reference resistor on the Pt100 interface (needed for R7) and a 16-bit ADS1115 converter for the pressure transducer are included in the $58.
- Items 19 and 20, eye protection and a parking cover: added for R9 and R11 ($22).
- Item 9: seat bore 4 mm or more specified from the relief capacity check (SCL-CAL-001 section 8).

Item 18 (chemical and biological indicators, about $45) is not in the parts total because it is needed only for testing at TRL 4 and later, which is on hold by Amish's instruction.

Open items that would change this BOM if Amish accepts them (SCL-DDR-001): four locking castors instead of two (open item 16, about $4 more) and a 0 to 300 kPa transducer instead of 0 to 500 kPa (open item 18, similar price). How BOM items 8 to 10 are mounted on the lid (open item 5) is undecided and does not change the prices listed.
