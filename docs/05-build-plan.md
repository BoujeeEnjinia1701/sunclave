---
doc_id: SCL-BLD-001
title: SunClave prototype build plan
project: SunClave
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (SCL-DDR-003)
---

# SunClave prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

SunClave is a research and educational prototype, not a medical device. This plan builds the dish, stand, holder, cooker set-up and logger; it stops before the cooker is ever put under pressure (safety stop S6).

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; the dish is shown face up, as it is built.*

The prototype is a 1.4 m dish of twelve polished aluminium petals that turns on two axles between the uprights of a bolted timber stand on four locking castors, with a 12 L household pressure cooker hanging level at the focus by its handles from a steel ring, and a small logger in a box on one upright. Figure 1 shows the 20 component groups in the order you make or fit them. The made parts are the timber rails, uprights and braces; the steel axle plates, axles, ribs, hub plate, clips, rim band, stand-offs, yoke plates, holder arms, brackets and ring; the aluminium petals; the gnomon; and the insulated jacket. The castors, cooker and its lid fittings, basket, logger modules, power bank and fixings are bought. The work is sawing and drilling timber; cutting, drilling, bending and filing steel bar and plate; cutting, folding and riveting thin aluminium sheet; and plugging bought electronic modules together. Nothing is welded. The parts cost about USD 497 from the bill of materials.

> **Safety:** The finished dish concentrates sunlight to about 270 times normal at the focus: it burns skin in about a second, sets fire to paper, cloth and dry grass, and can blind. Keep the dish face down or covered whenever it is outdoors until section 6 says otherwise. The dish and yoke weigh about 16 kg and swing about the axles: two people lift it, and the tilt locks are pinch points. Cut aluminium sheet and steel edges are sharp; deburr everything and wear cut-resistant gloves. Mineral wool sheds fibres; wear a dust mask and glasses when cutting the jacket. The cooker is a pressure vessel; this plan never pressurises it.

## 2. What changed to make it buildable

The concept showed what SunClave does; some of its parts could not be made, fixed or assembled as drawn. Each change below keeps what SunClave does, and all of them are recorded in decision record SCL-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Pivots and tilt lock | Steel bearing blocks with stub axles, a quadrant plate and a lock lever, all drawn through each other | A steel axle plate on each upright, a fixed 20 mm axle, a PTFE washer and a 6 mm yoke plate that turns on the axle; a fan on each yoke plate with a slot that a star knob clamps (Figures 26, 27 and 28) | A plain greased pivot is enough for a few degrees every 12 minutes; every part is cut, drilled and bolted |
| Yoke to dish | Tube arms that stopped short of the rim | A short rectangular tube between the rim band and each yoke plate, clamped by two countersunk screws (Figure 24) | Two screws per side make the dish and yoke one rigid unit |
| Pot holder | A ring that ran through the jacket and sat below the handles | A flat steel ring the handles rest on, on two tube arms that sit on the upright tops and on brackets (Figures 31 and 33) | The cooker hangs by its handles and lifts out without tools |
| Stand | Rails, uprights and braces butted together with no fixings; castors drawn shorter than real ones | Side rails on edge across the cross rails, uprights on angle brackets, braces lapped flat and bolted, real 102 mm castors (Figures 3, 6, 8 and 9) | Every timber joint is face to face and bolted; the stand comes apart in pieces of 6 kg or less |
| Dish frame | Ribs drawn into the sheet and not reaching the hub or rim; nothing for the petals to be riveted to | Petals with flanges folded down either side of each rib and riveted through it; clips at the hub and the rim; tabs riveted inside the rim band (Figures 14, 17, 18 and 20) | Rivets need a face to grip; clips are the simplest bolted joint for a bar standing on edge |
| Gnomon | On the reflector face, with no fixing | On a bracket bolted outside the rim band (Figure 22) | Shades no reflector and bolts to steel |
| Logger | Power bank hanging outside the box; no transducer on the tee | A box big enough for the bank, below the lock stud; the transducer on the tee; plug-in sensor leads (Figure 35) | Matches the bill of materials; the lid comes off without cutting wires |
| Build order | No order let the dish go between the uprights | A 2 mm gap at each pivot; one axle plate fitted after the dish is in (steps 11 to 13) | Two people can assemble it without lifting gear |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in front of the stand, facing the reflector with the dish tipped toward you; the logger box is on the right. Workshop tolerance is 1 mm on timber and 0.5 mm on steel unless a step says otherwise; drawings do not carry tolerances before TRL 4. Treat every cut end and hole in timber with end-grain preservative.

### 3.1 Cross rails (make 2)

![Figure 2. Making sketch of the cross rail](../cad/drawings/SCL-DWG-101.png)

*Figure 2. Cross rail making sketch (SCL-DWG-101).*

**What it is and what it is made from.** The front and back members of the base, laid flat; each carries two castors underneath and the ends of both side rails on top. Treated timber 70 x 35 mm.

**How to make it.**

1. Cut 1,805 mm and square both ends.
2. At each end, drill the four castor holes, 8.5 mm, on a 42 mm square centred 112.5 mm from the end and on the centre line. Check against your castors' top plates first and move the holes to suit.
3. Leave the two crossing-bolt holes at each end until step 2 of the assembly, where you drill them through the side rail and cross rail together.

**How it fits the parts next to it.**

![Figure 3. Joint 1: corner of the base](05-build-plan/joint-01.png)

*Figure 3. The side rail, on edge, crosses on top of the cross rail; the castor bolts under the cross rail just inside the side rail.*

The castor's top plate sits flat on the underside, held by four M8 bolts with the nuts on top. Each side rail sits across the top, its outer face 40 mm in from the rail end, held by two M8 bolts through both.

**Check before moving on.** The two rails are the same length within 2 mm and lie flat on the floor without rocking.

### 3.2 Side rails (make 2)

![Figure 4. Making sketch of the side rail](../cad/drawings/SCL-DWG-102.png)

*Figure 4. Side rail making sketch (SCL-DWG-102).*

**What it is and what it is made from.** The left and right members of the base, standing on edge; each carries an upright at its middle and the feet of two braces. Treated timber 45 x 70 mm.

**How to make it.**

1. Cut 1,100 mm, square both ends, and mark the middle on the top edge.
2. Brace foot holes: 10.5 mm across the 45 mm way, 470 mm each side of the middle, 35 mm up from the bottom edge.
3. Foot bracket holes: 8.5 mm down through, 65 mm each side of the middle, on the centre line.
4. Crossing holes: 8.5 mm down through at each end, at 35 and 55 mm from the end, 12 mm either side of the centre line. Drill these with the cross rail clamped square underneath (assembly step 2).

**How it fits the parts next to it.** It stands on edge across the ends of both cross rails. The upright stands on its middle; the braces lie flat on its outer and inner faces (Figures 8 and 9).

**Check before moving on.** Straight within 3 mm along its length.

### 3.3 Uprights (make 2)

![Figure 5. Making sketch of the upright](../cad/drawings/SCL-DWG-103.png)

*Figure 5. Upright making sketch (SCL-DWG-103).*

**What it is and what it is made from.** The two posts that carry the axles, the tilt locks, the holder arms and, on the right, the logger box. Treated timber 45 x 70 mm, standing with the 45 mm face toward the dish.

**How to make it.**

1. Cut 892 mm and square both ends. Choose straight timber with no knots near the holes.
2. Mark a centre line on one 70 mm face. Measure every height from the bottom end.
3. Drill across the 45 mm way, square to the face, on the centre line: brace bolt 10.5 mm at 313; lock stud 10.5 mm at 593; axle 20.5 mm at 743; axle plate bolt 10.5 mm at 823; arm bracket bolt 8.5 mm at 872.
4. Drill the axle hole with a 6 mm pilot first, from both faces, then open it to 20.5 mm from both faces so it stays square.
5. Foot bracket bolt: 8.5 mm through the 70 mm way, 28 mm up from the bottom.

**How it fits the parts next to it.**

![Figure 6. Joint 2: upright on the side rail](05-build-plan/joint-02.png)

*Figure 6. Two angle brackets, front and back, hold the upright on the side rail; one bolt through the upright holds both, one bolt each goes down through the side rail.*

The bottom end stands on the middle of the side rail. The axle plate goes on its inner face, the holder arm on its top, and on the right upright the logger box on its outer face.

**Check before moving on.** Laid side by side, the axle holes of both uprights are at the same height within 1 mm.

### 3.4 Braces (make 4)

![Figure 7. Making sketch of the brace](../cad/drawings/SCL-DWG-104.png)

*Figure 7. Brace making sketch (SCL-DWG-104), drawn laid flat.*

**What it is and what it is made from.** The diagonals that keep each upright plumb, front and back. Treated timber 45 x 35 mm.

**How to make it.**

1. Cut four 630 mm lengths with square ends.
2. Drill two 10.5 mm holes through the 35 mm way on the centre line, 585 mm apart: one 20 mm from one end (the foot), one 25 mm from the other (the top). Drill the four clamped in a stack.

**How it fits the parts next to it.**

![Figure 8. Joint 3: brace tops on the upright](05-build-plan/joint-03.png)

*Figure 8. The front brace lies on the upright's outer face and the back brace on its inner face; one M10 bolt goes through both braces and the upright.*

![Figure 9. Joint 4: brace foot on the side rail](05-build-plan/joint-04.png)

*Figure 9. Each brace foot lies flat on the side rail, 470 mm from the middle, held by one M10 bolt.*

The 45 mm face of each brace lies flat on the upright and on the side rail. The top bolt is 520 mm above the ground.

**Check before moving on.** With all bolts in, each upright stands plumb within 2 mm, checked with a spirit level on two faces.

### 3.5 Axle plates (make 2)

![Figure 10. Making sketch of the axle plate](../cad/drawings/SCL-DWG-105.png)

*Figure 10. Axle plate making sketch (SCL-DWG-105).*

**What it is and what it is made from.** A steel plate on the inner face of each upright that the yoke plate runs against and the lock clamps onto. Steel flat bar 70 x 6 mm.

**How to make it.**

1. Cut 270 mm and deburr.
2. On the centre line, measured from the top end: 11 mm hole at 25 (plate bolt), 20.5 mm hole at 105 (axle), 11 mm hole at 255 (lock stud). Drill the axle hole in steps (6, 12, 18, 20.5 mm) with the plate clamped flat.
3. Paint the plate, but leave the inner face bare where the yoke plate and the lock spacer run, and grease it there.

**How it fits the parts next to it.** It lies flat on the upright's inner face with its holes on the upright's holes, the top of the plate 44 mm below the top of the upright. An M10 bolt at the top holds it, with the nut on the inside; the axle and the lock stud pass through the other two holes (Figures 27 and 28).

**Check before moving on.** A 20 mm bar passes through the plate and the upright together.

### 3.6 Axles (make 2)

![Figure 11. Making sketch of the axle](../cad/drawings/SCL-DWG-106.png)

*Figure 11. Axle making sketch (SCL-DWG-106).*

**What it is and what it is made from.** The fixed pin each yoke plate turns on. Bright steel round bar 20 mm.

**How to make it.**

1. Cut 85 mm and file a 1 mm chamfer on both ends.
2. File a small flat 10 mm long at each collar position, 8 mm and 79 mm from the outer end, for the collar set screws.

**How it fits the parts next to it.** From outside to inside: outer collar, upright, axle plate, PTFE thrust washer, yoke plate, inner collar. The axle does not turn; the yoke plate turns on it.

**Check before moving on.** It slides through the drilled upright and axle plate by hand, and the yoke plate turns on it freely.

### 3.7 Ribs (make 12)

![Figure 12. Making sketch of the rib](../cad/drawings/SCL-DWG-107.png)

*Figure 12. Rib making sketch (SCL-DWG-107), drawn in the plane it lies in.*

**What it is and what it is made from.** The twelve curved bars behind the petals that give the dish its shape. Steel flat bar 20 x 3 mm, bent on edge.

**How to make it.**

1. Make a bending jig: a sheet of 18 mm plywood with the dish curve drawn on it from the axis line outward. The curve's height above the vertex is the radius squared divided by 2,000: at 100, 200, 300, 400, 500, 600 and 700 mm out it is 5, 20, 45, 80, 125, 180 and 245 mm. Screw hardwood blocks along the curve every 50 mm.
2. Cut twelve 720 mm lengths. Bend each on edge against the blocks a little at a time, with clamps following the bend; check against the curve. Bend one first and confirm it does not buckle.
3. With the rib on the jig, trim both ends square to the jig base: the outer end 699.5 mm and the inner end 55 mm from the axis line.
4. Clip bolt holes and rivet holes are drilled at assembly, through the clips and the flanges.

**How it fits the parts next to it.**

The rib stands on edge, 20 mm deep, just behind the petals, with its top edge along the dish curve. Its inner end stands on the hub plate (Figure 14), its outer end meets the inside of the rim band (Figure 18), and the petal flanges lie either side of it (Figure 17).

**Check before moving on.** On the jig, the rib touches the curve within 1 mm along its length, and all twelve match.

### 3.8 Hub plate

![Figure 13. Making sketch of the hub plate](../cad/drawings/SCL-DWG-108.png)

*Figure 13. Hub plate making sketch (SCL-DWG-108).*

**What it is and what it is made from.** The disc behind the centre of the dish that ties the inner ends of the ribs together. Steel plate 4 mm.

**How to make it.**

1. Cut a 200 mm disc and deburr the edge.
2. Mark twelve lines from the centre, 30 degrees apart; these are the rib lines.
3. On each line, offset 11.5 mm to the same side, drill 5.5 mm at 72.5 mm from the centre for a clip bolt.

**How it fits the parts next to it.**

![Figure 14. Joint 7: rib on the hub plate](05-build-plan/joint-07.png)

*Figure 14. Each rib's inner end stands on the hub plate; a rib clip bolts to both.*

The ribs' inner ends stand on its front face, each beside one of the twelve lines, and a clip bolts each rib to it. It sits about 22 mm behind the petals.

**Check before moving on.** The twelve holes are on a 72.5 mm radius within 1 mm.

### 3.9 Rib clips (make 24)

![Figure 15. Making sketch of the rib clip](../cad/drawings/SCL-DWG-109.png)

*Figure 15. Rib clip making sketch (SCL-DWG-109).*

**What it is and what it is made from.** Small angles that join each end of each rib to the hub plate or the rim band. Steel equal angle 20 x 20 x 3 mm.

**How to make it.**

1. Cut 24 slices 13 mm long and deburr.
2. Drill one 5.5 mm hole in the middle of each leg.

**How it fits the parts next to it.** At the hub, one leg lies on the hub plate and the other against the side of the rib (Figure 14). At the rim, one leg lies on the inside of the rim band and the other over the petal flange on the side of the rib, and one M5 bolt goes through the clip, both petal flanges and the rib (Figure 18).

**Check before moving on.** Each clip sits flat on both faces at once.

### 3.10 Rim band

![Figure 16. Making sketch of the rim band](../cad/drawings/SCL-DWG-110.png)

*Figure 16. Rim band making sketch (SCL-DWG-110).*

**What it is and what it is made from.** The steel hoop round the edge of the dish that ties the rib ends together and carries the gnomon and the two stand-offs. Steel flat bar 25 x 4 mm, rolled.

**How to make it.**

1. Roll 4,440 mm of bar the easy way into a hoop of 1,400 mm inside diameter, by hand round a circle of stakes in the ground, or have a local fabricator roll it.
2. Join the ends with a 100 mm strap of the same bar on the inside, four M5 bolts, placed where a rib will be.
3. Mark the two stand-off positions opposite each other, then the twelve rib positions 30 degrees apart starting 15 degrees from a stand-off position, then the gnomon position midway between two ribs, 90 degrees from both stand-offs.
4. Drill: two 9 mm holes 30 mm apart at each stand-off position; two 6.5 mm holes 24 mm apart at the gnomon; one 5.5 mm hole 6.5 mm up from the bottom edge, 12.5 mm beside each rib position, for its clip. Tab rivet holes are drilled at assembly.

**How it fits the parts next to it.**

![Figure 17. Joint 9: petals on a rib, cut across](05-build-plan/joint-09.png)

*Figure 17. Each petal's flange folds down beside the rib, and one rivet goes through both flanges and the rib.*

![Figure 18. Joint 8: rib end at the rim band](05-build-plan/joint-08.png)

*Figure 18. Seen from behind the dish: the rim clip bolts to the band and, over the petal flange, to the rib.*

The band stands round the rib ends with its top edge level with the edge of the petals. The rib ends stop 0.5 mm inside it and are held by the rim clips; the petal tabs are riveted to its inside face.

**Check before moving on.** Round within 3 mm across any two diameters, and flat (not twisted) when laid on the floor.

### 3.11 Petals (make 12)

![Figure 19. Making sketch of the petal](../cad/drawings/SCL-DWG-111.png)

*Figure 19. Petal making sketch (SCL-DWG-111).*

![Figure 20. Flat pattern of the petal](05-build-plan/petal-pattern.png)

*Figure 20. Flat pattern of one petal, with the fold lines, flanges, tabs and rivet positions.*

**What it is and what it is made from.** The twelve mirror segments that make up the dish. Polished or anodised aluminium reflector sheet 0.5 mm, reflectance 85 % or more, with its protective film on.

**How to make it.**

1. Make a template of the flat pattern (Figure 20) from thin card or hardboard: 34 mm wide at the inner edge, 362 mm wide at the outer edge, 678 mm long along the centre line, with a 12 mm flange beyond each long edge and two 30 x 12 mm tabs beyond the outer edge.
2. Mark twelve petals on the film side and cut them with aviation snips. Drill 3 mm relief holes where the flange and tab folds meet.
3. Fold the flanges down 90 degrees along both long edges with a hand seamer, a little at a time along the length, so the petal takes up a gentle curve. Fold the two tabs down.
4. Keep the bright face covered and handle the petals with clean cotton gloves.

**How it fits the parts next to it.** Each petal lies across two neighbouring ribs, its flanges outside the ribs. Rivets go every 50 mm through a flange, the rib and the next petal's flange (Figure 17). The tabs are riveted inside the rim band. Neighbouring petals meet over each rib with a 3 to 5 mm gap.

**Check before moving on.** The flanges are square to the face along their length, and the bright face has no creases or scratches.

### 3.12 Gnomon on its bracket

![Figure 21. Making sketch of the gnomon](../cad/drawings/SCL-DWG-112.png)

*Figure 21. Gnomon making sketch (SCL-DWG-112).*

**What it is and what it is made from.** The aiming sight: a pin whose shadow falls on a target when the dish faces the sun. A 40 mm length of 40 x 40 x 4 mm steel angle, a 120 x 120 mm plate of 3 mm aluminium, and 8 mm steel rod.

**How to make it.**

1. Bracket: drill two 6.5 mm holes 24 mm apart, 20 mm down, in the upright leg; two 5.5 mm holes in the flat leg.
2. Target plate: paint it matt white; scribe two rings, 10 and 25 mm radius, round its centre; drill an 8.5 mm centre hole and two 5.5 mm holes to match the bracket.
3. Pin: 183 mm of 8 mm rod, threaded M8 for 15 mm at one end; fit it through the centre hole with a nut each side, square to the plate.

**How it fits the parts next to it.**

![Figure 22. Joint 13: gnomon on the rim band](05-build-plan/joint-13.png)

*Figure 22. The bracket bolts to the outside of the rim band; the plate sits on its flat leg, level with the rim edge; the pin is parallel to the dish axis.*

The bracket's upright leg bolts to the outside of the rim band at the gnomon position with two M6 bolts; the plate bolts to the flat leg with two M5 bolts, its inner edge on the top edge of the band.

**Check before moving on.** An engineer's square on the plate touches the pin along its length.

### 3.13 Rim stand-offs (make 2)

![Figure 23. Making sketch of the rim stand-off](../cad/drawings/SCL-DWG-113.png)

*Figure 23. Rim stand-off making sketch (SCL-DWG-113).*

**What it is and what it is made from.** A short tube on each side of the dish that spaces the rim band off the yoke plate. Steel rectangular tube 50 x 25 x 2.5 mm.

**How to make it.**

1. Cut 99.5 mm with both ends square, and file the ends flat.
2. Drill nothing: the two screws run along its inside.

**How it fits the parts next to it.**

![Figure 24. Joint 10: rim stand-off](05-build-plan/joint-10.png)

*Figure 24. The tube is clamped end to end between the rim band and the yoke plate by two M8 countersunk screws, with nyloc nuts inside the band.*

The 25 mm sides run with the height of the rim band. One end bears on the outside of the band, the other on the inner face of the yoke plate's arm.

**Check before moving on.** The two stand-offs are the same length within 0.5 mm.

### 3.14 Yoke plates (make 2, a left and a right)

![Figure 25. Making sketch of the yoke plate](../cad/drawings/SCL-DWG-114.png)

*Figure 25. Yoke plate making sketch (SCL-DWG-114).*

![Figure 26. Yoke plate layout](05-build-plan/yoke-layout.png)

*Figure 26. Yoke plate layout, with the lock slot.*

**What it is and what it is made from.** The plate each side that carries the dish on its axle: a hub round the axle, an arm down to the stand-off, and a fan with the lock slot. Steel plate 6 mm.

**How to make it.**

1. Cut the outline of Figure 26 from 6 mm plate with a jigsaw and metal blade, or have a local cutting shop cut both: a 40 mm radius hub, a 60 mm wide arm with a round end, and a fan from 125 to 175 mm radius.
2. Drill the axle hole 20.5 mm at the hub centre and smooth it with a round file or reamer.
3. Cut the lock slot, 11 mm wide on a 150 mm radius, from the arm's centre line 75 degrees round toward the fan's far edge: drill 11 mm at each end and chain-drill between, then file smooth.
4. Drill the two stand-off holes, 9 mm, 30 mm apart across the arm, 267.5 mm from the axle centre. Countersink them 90 degrees on the outer face (the face toward the upright). The two plates are mirror images: the outer face of one is the face that is down when the other's is up.
5. Deburr and paint, leaving the outer face bare round the hub and over the fan.

**How it fits the parts next to it.**

![Figure 27. Joint 5: pivot, cut open](05-build-plan/joint-05.png)

*Figure 27. The pivot, cut open through the axle: the yoke plate turns on the fixed axle; the PTFE washer and the collars hold the stack.*

![Figure 28. Joint 6: tilt lock, cut open](05-build-plan/joint-06.png)

*Figure 28. The tilt lock: the fixed stud passes through the slot in the yoke plate's fan; tightening the star knob clamps the fan.*

The outer face runs against the PTFE washer on the axle plate, 2 mm from it; the axle passes through the hub; the lock stud passes through the slot (Figures 27 and 28). The arm's end carries the rim stand-off (Figure 24).

**Check before moving on.** Laid back to back, the two plates match all round, and each turns freely on a 20 mm bar.

### 3.15 Holder arms (make 2)

![Figure 29. Making sketch of the holder arm](../cad/drawings/SCL-DWG-115.png)

*Figure 29. Holder arm making sketch (SCL-DWG-115).*

**What it is and what it is made from.** The two bars that carry the holder ring between the tops of the uprights. Steel square tube 25 x 25 x 2 mm.

**How to make it.**

1. Cut 687 mm and fit plastic end caps.
2. Drill 8.5 mm vertically through both walls: one hole 13 mm from the inner end (ring bolt), one 65 mm from the outer end (bracket bolt).

**How it fits the parts next to it.** The outer 45 mm rests on the top of the upright, flush with its outer face, and on the flat leg of the arm bracket (Figure 31). The ring sits on the inner ends of both arms.

**Check before moving on.** Laid across both uprights, the two arms are level with each other within 1 mm.

### 3.16 Arm brackets (make 2)

![Figure 30. Making sketch of the arm bracket](../cad/drawings/SCL-DWG-116.png)

*Figure 30. Arm bracket making sketch (SCL-DWG-116).*

**What it is and what it is made from.** A short angle on the inner face of each upright that the holder arm rests on. Steel equal angle 40 x 40 x 4 mm.

**How to make it.**

1. Cut 40 mm slices and deburr.
2. Drill one 8.5 mm hole in the middle of each leg, 20 mm from the corner.

**How it fits the parts next to it.**

![Figure 31. Joint 11: holder arm on the upright](05-build-plan/joint-11.png)

*Figure 31. The arm rests on the top of the upright and on the bracket's flat leg; the bracket bolts through the upright, the arm bolts down through the bracket.*

The upright leg lies on the upright's inner face with its top level with the upright's top, held by one M8 bolt through the upright; the flat leg is under the arm, held by one M8 bolt up through both. It sits 4 mm above the top of the axle plate.

**Check before moving on.** The flat leg is level with the top of the upright.

### 3.17 Holder ring

![Figure 32. Making sketch of the holder ring](../cad/drawings/SCL-DWG-117.png)

*Figure 32. Holder ring making sketch (SCL-DWG-117).*

**What it is and what it is made from.** The flat ring the cooker hangs from by its two handles. Steel plate 4 mm.

**How to make it.**

1. Cut a flat ring 348 mm inside and 408 mm outside diameter, with a jigsaw and metal blade or at a local cutting shop.
2. Drill two 9 mm holes opposite each other on a 378 mm diameter.
3. File the inner edge smooth and paint with heat-resistant paint.

**How it fits the parts next to it.**

![Figure 33. Joint 12: cooker handle on the holder ring](05-build-plan/joint-12.png)

*Figure 33. The cooker's handle rests on the ring; the ring is bolted to the arm; the jacket clears the ring's inner edge by 5 mm.*

It lies on the inner ends of the two arms, one M8 bolt into each. The cooker drops through it and hangs by its handles, so the cooker's base sits on the focal plane.

**Check before moving on.** The cooker body and jacket pass through without touching, and both handles rest on the ring.

### 3.18 Cooker, jacket and base thermocouple

![Figure 34. Making sketch of the jacket](../cad/drawings/SCL-DWG-118.png)

*Figure 34. Jacket making sketch (SCL-DWG-118).*

**What it is and what it is made from.** The bought 12 L aluminium household pressure cooker, painted black where the sunlight lands, with an insulating jacket on its upper wall and a thermocouple at the edge of its base. The jacket is 25 mm mineral wool blanket with an aluminised glass-cloth skin.

**How to make it.**

1. Cooker: clean the outside with detergent. Mask the rest and paint the base and the lowest 80 mm of the wall with high-temperature matt black paint; cure it as the paint maker says. Do not drill, weld or change the cooker body, its regulator weight or its overpressure plug.
2. Jacket: cut a strip 96 mm wide and 1,010 mm long, foil outward, wearing gloves, a dust mask and glasses. Bind both long edges with aluminised tape.
3. Wrap the jacket round the wall from 80 mm above the base to 30 mm below the rim, butt and tape the joint, and hold it with two stainless strap clamps, 12 mm from each edge.
4. Thermocouple: hold its tip against the bare black wall 10 mm above the base with a stainless band clamp, on the side away from the logger, and lead the wire up beside the jacket.

**How it fits the parts next to it.** The handles rest on the holder ring (Figure 33); the jacket stops below the handles and clears the ring by 5 mm. The basket stands on its trivet inside, above the water.

**Check before moving on.** The paint is cured and unbroken, the jacket does not cover any of the black band, and the thermocouple reads room temperature on the logger.

### 3.19 Logger box

![Figure 35. Joint 14: logger box on the right upright](05-build-plan/joint-14.png)

*Figure 35. The logger box on the outer face of the right upright, cut open: the power bank at the back, the board in front, the sensor cable out of the top.*

**What it is and what it is made from.** A bought IP65 plastic box about 180 x 80 x 65 mm holding the logger board, its modules and display, and the power bank.

**How to make it.**

1. Drill the lid for the display window and the two buttons, and the top for one cable gland, following the box maker's advice for drilling.
2. Fit the board and modules on standoffs in front, and the power bank in a strap at the back.
3. Make up the sensor cable: Pt100 leads, transducer leads and thermocouple lead in one sheath, with a plug at the lid end so the lid comes off, and a plug at the box.

**How it fits the parts next to it.** Two stainless wood screws through the moulded holes in the back of the box go into the outer face of the right upright, the box's top about 10 mm below the lock stud's head and its bottom 600 mm above the ground. The cable runs up beside the upright, along the top of the right holder arm with cable ties, and up to the lid.

**Check before moving on.** The box closes on its gasket with the cable through the gland, and the display shows readings with the sensors plugged in.

### 3.20 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Castors (line 4).** Four 75 mm swivel castors with brakes, 102 mm mounting height, top plate with holes on a 42 mm square.
- **Pivot parts (line 4).** Four 20 mm shaft collars with set screws; two PTFE thrust washers 2 mm thick, 20.5 mm bore, about 50 mm outside diameter; four galvanised 50 x 50 mm angle brackets, 40 mm wide.
- **Lock parts (line 3).** Two M10 x 80 hex bolts, two 2 mm steel spacer washers (24 mm outside diameter), two M10 washers and two M10 star knobs.
- **Pressure cooker (line 6, with its lid, line 7).** 12 L aluminium household cooker, inside about 280 mm across and 200 mm deep, 103.4 kPa (15 psi) weighted regulator, overpressure plug, two handles on the body whose undersides are about 28 mm below the rim and reach at least 214 mm from the centre; maker's rating published.
- **Lid fittings (lines 8 to 10, and the transducer of line 14).** Pressure gauge 0 to 250 kPa with siphon; spring relief valve set at 125 kPa gauge or less, seat 4 mm or more; 1/8 in compression gland, 3 mm class A Pt100 probe and brass tee; 0 to 300 kPa absolute transducer rated to 600 kPa or more. How they pass through the lid is set in the design decisions register; fit them only that way.
- **Basket (line 13).** Stainless wire basket 250 mm across and 150 mm deep on a 40 mm trivet.
- **Logger (line 14) and power bank (line 15).** As the bill of materials: ESP32-class board, Pt100 interface with a 0.05 % reference, 16-bit converter, real-time clock, microSD, 1.3 in OLED display, buzzer, K-type thermocouple with its interface; a 10,000 mAh power bank with a low-current mode.
- **Safety items (lines 19 to 21).** Two pairs of shade 5 goggles, an opaque parking cover for the dish, barrier tape and four pegs.
- **Fixings (line 17).** Stainless or galvanised: 16 M8 x 50 (castors); 8 M8 x 120 (crossings); 2 M8 x 90 horizontal and 4 M8 x 90 vertical (foot brackets); 2 M10 x 140 and 4 M10 x 100 (braces); 2 M10 x 70 (axle plates); 2 M8 x 70 and 4 M8 x 40 (arms and ring); 4 M8 x 120 countersunk (stand-offs); about 52 M5 x 16 (clips and rim joint); 2 M6 x 16 and 2 M5 x 12 (gnomon); nyloc nuts and washers for all; about 300 aluminium rivets 3.2 mm; two 5 x 40 stainless wood screws; cable ties; high-temperature paint; grease.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 5 and 11 to 19 are on the stand; steps 6 to 10 build the dish face up on a level floor beside it.

### Step 1: castors onto the cross rails

![Step 1](05-build-plan/step-01.png)

Rails upside down on the floor. Each castor on four M8 x 50 bolts, nuts and washers on the rail, brake pedals facing outward.

### Step 2: side rails across the cross rails

![Step 2](05-build-plan/step-02.png)

Rails right way up, castors on the floor, brakes on. Lay each side rail on edge across both cross rails, its outer face 40 mm in from the rail ends; check the frame is square (equal diagonals within 3 mm), clamp, drill the crossing holes through both and fit two M8 x 120 bolts at each crossing.

### Step 3: uprights onto the side rails

![Step 3](05-build-plan/step-03.png)

Stand each upright on the middle of its side rail, the 45 mm face toward the other upright and its axle hole level with the other's. Fit the two angle brackets on its front and back faces, one M8 x 90 through the upright and both brackets, one M8 x 90 down through each bracket and the side rail. A helper holds it plumb.

### Step 4: braces

![Step 4](05-build-plan/step-04.png)

Front braces on the outer faces, back braces on the inner faces. One M10 x 140 through both braces and the upright at the top; one M10 x 100 at each foot. Check plumb on both faces, then tighten.

### Step 5: left axle plate

![Step 5](05-build-plan/step-05.png)

On the inner face of the left upright, holes on the upright's holes, M10 x 70 at the top with the nut inside. Leave the right axle plate off for now.

### Step 6: ribs onto the hub plate

![Step 6](05-build-plan/step-06.png)

Dish face up on a level floor: hub plate on a block so its front is about 267 mm below the top of the rim, each rib propped on its jig or a stand. Each rib's inner end on the hub plate beside its line; one clip and two M5 bolts each, finger tight.

### Step 7: rim band onto the rib ends

![Step 7](05-build-plan/step-07.png)

Rim band round the rib ends, its joint strap at a rib and its top edge level with the rib tops. One rim clip and two M5 bolts at each rib, finger tight. Check the band is round and level, then tighten the hub and rim bolts.

### Step 8: petals onto the ribs

![Step 8](05-build-plan/step-08.png)

Fit two opposite petals first, then their neighbours, working round. Each petal's flanges outside its two ribs; drill 3.3 mm through flange, rib and the next flange every 50 mm and rivet. Rivet the tabs inside the rim band. At each rim clip, the clip's bolt goes through clip, flange, rib and flange. Peel the film last.

### Step 9: gnomon onto the rim band

![Step 9](05-build-plan/step-09.png)

At the gnomon position, two M6 bolts through the band; plate on the flat leg with two M5 bolts; check the pin is square to the rim plane.

### Step 10: stand-offs and yoke plates onto the rim band

![Step 10](05-build-plan/step-10.png)

At each stand-off position, opposite each other: yoke plate, stand-off and band clamped by two M8 x 120 countersunk screws, heads flush on the yoke plate's outer face, nyloc nuts inside the band. The arms point down toward the dish's back, the fans toward the gnomon side. **Hold point:** safety stop S1.

### Step 11: dish into the stand

![Step 11](05-build-plan/step-11.png)

Two people lift the dish by the rim, face up, and lower it from above between the uprights until the yoke plates' axle holes line up with the uprights' holes; prop it on blocks there. The left yoke plate sits 2 mm from the left axle plate.

### Step 12: right axle plate

![Step 12](05-build-plan/step-12.png)

Slide the right axle plate down between the right yoke plate and the right upright, holes on the upright's holes, and fit its M10 x 70 at the top.

### Step 13: axles, thrust washers and collars

![Step 13](05-build-plan/step-13.png)

Grease each axle. Hold a PTFE washer between the axle plate and the yoke plate and push the axle in from outside, through the upright, plate, washer and yoke plate, into the inner collar; set the outer collar against the upright and both set screws on their flats, leaving the yoke plate free to turn. **Hold point:** safety stop S2.

### Step 14: lock studs and star knobs

![Step 14](05-build-plan/step-14.png)

Each M10 x 80 stud in from outside through the upright and the axle plate, the 2 mm spacer behind the yoke plate's slot, then through the slot; washer and star knob in front. Tilt the dish through its whole range by hand with the knobs loose, then lock it face up.

### Step 15: holder arms

![Step 15](05-build-plan/step-15.png)

Arm brackets on the inner faces of the uprights, M8 x 70 through each upright. Each arm on its upright's top and bracket, flush with the outer face; M8 x 40 up through the bracket and arm.

### Step 16: holder ring

![Step 16](05-build-plan/step-16.png)

On the inner ends of both arms, one M8 x 40 into each.

### Step 17: logger box

![Step 17](05-build-plan/step-17.png)

On the outer face of the right upright, below the lock stud, two stainless wood screws. Cable along the right arm with cable ties.

### Step 18: cooker into the holder ring

![Step 18](05-build-plan/step-18.png)

With the dish turned away from the sun or covered: water and basket in, then lower the cooker straight down through the ring until both handles rest on it. **Hold point:** safety stops S3 and S4.

### Step 19: lid and sensor cable

![Step 19](05-build-plan/step-19.png)

Close the lid as the cooker maker says, with its fittings as the design decisions register sets, and plug the sensor cable into the lid and the logger box. **Hold point:** safety stop S6: the cooker is not pressurised under this plan.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of SCL-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Tilt range and clearances | R9, R14 | Knobs loose, tilt the dish by hand from face up to 15 degrees above horizontal | It moves smoothly; nothing rubs or comes within 5 mm of anything except the yoke plate passing its axle plate |
| Tilt lock holds | R9, R15 | Lock at 15 degrees; hang a 5 kg bag from the rim at the gnomon | The dish does not move; it moves freely again when the knobs are loosened |
| Focus height | R4 | Dish face up, string across the rim; measure from the string to the cooker base along the axis | 255 mm, give or take 3 mm |
| Gnomon alignment | R14 | Shine a torch along the dish axis from 3 m away, or check the pin square to the rim plane | The pin's shadow falls inside the 10 mm ring |
| Cooker seating | R2 | Lower the cooker with its basket and jacket through the ring | Both handles rest on the ring; the jacket clears the ring all round |
| Castor brakes | R15 | All four brakes on; push the stand at the top of an upright | It does not roll |
| Mass and pieces | R16 | Weigh the parts on a bathroom scale before assembly | 45 kg or less in all (44.4 kg estimated); no piece over 20 kg |
| Logger on its power bank | R6, R7, R13 | Power on in the shade; read the probe in iced water and in boiling water, and the transducer against a barometer | Readings within 0.5 °C of the reference after the boiling-point correction, and within 5 kPa; a record is written to the card |
| Parking cover and keep-out | R9, R11 | Fit the cover; peg out the 2 m keep-out | The cover closes the whole aperture; the tape marks 2 m round the dish and cooker |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the dish is lifted into the stand.** Two people available; castor brakes on; the stand on level ground; cut-resistant gloves on; the dish indoors or face down, or covered, so it cannot catch the sun.
- **S2. Before the dish is let go on its axles.** Both axles in with both collars set; both lock studs and knobs fitted; hands kept clear of the fans and slots, which close like scissors as the dish tilts.
- **S3. Before the dish ever faces the sun.** The parking cover is at hand; everyone near wears the shade 5 goggles; the 2 m keep-out is pegged; nothing that can burn is under or near the dish; aiming is by the gnomon's shadow only, never by looking at the sun or the focus; the timber is checked for scorch marks after every session.
- **S4. Before the cooker is at the focus in sun.** At least 1.5 L of water is in it; the thermocouple and logger are working and the 140 °C alarm sounds when tested; the dish is turned at least 15 degrees off the sun before anyone reaches toward the cooker; heat-resistant gloves on.
- **S5. Before the power bank goes outside.** It sits in the shaded logger box, closed on its gasket; it is never charged above 45 °C.
- **S6. Before the cooker is ever pressurised (outside this plan).** The way the fittings pass through the lid has been decided in the design decisions register; the cooker maker's rating for 103.4 kPa is confirmed; the relief valve is fitted, set at 125 kPa gauge or less and preferably certified; the overpressure plug is in place; and a hydrostatic check of the vessel as fitted has passed (TRL 4 work).

## 7. Tools, skills and workspace

**Tools.** Handsaw or circular saw for timber; hacksaw with a 24 teeth per inch blade; jigsaw with metal blades; bench drill or a drill in a stand; drills 3 to 12 mm and 20.5 mm (or a step drill), a 6 mm long pilot drill; 90 degree countersink; flat, half-round and round files; deburring tool; aviation snips; hand seamer for folding thin sheet; hand rivet tool for 3.2 mm rivets; spanners and sockets 8, 10, 13 and 17 mm, hex keys for the collar set screws; clamps; tape measure, steel rule, engineer's square, spirit level and calipers; 18 mm plywood, hardwood blocks and screws for the rib jig; bathroom scale; multimeter.

**Skills.** No certified trade is needed. Basic woodwork and metalwork (marking out, sawing, drilling, filing), folding and riveting thin sheet, and plugging together bought electronic modules. Nothing is welded and no mains wiring is involved. Pressure work is not part of this plan.

**Workspace.** A level floor about 3 x 3 m to build the dish and stand; a bench about 1.5 x 0.6 m; a ventilated, shaded place to paint; a clean area for the petals away from metal chips; a shaded place for the logger and power bank.

**Personal protective equipment.** Safety glasses for sawing, drilling and riveting; cut-resistant gloves for sheet and bar; hearing protection when sawing; dust mask, gloves and glasses for the mineral wool; shade 5 goggles near the focus; heat-resistant gloves for the cooker; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 66 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/SCL-DWG-101` to `SCL-DWG-118`.
- General arrangement: `cad/drawings/SCL-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (SCL-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; masses, tilt torque and lock force in section 10.
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (SCL-DDR-003), with SCL-DDR-001 and SCL-DDR-002; open decisions in `docs/06-design-decisions.md` (SCL-DEC-001).
- Requirements: `docs/03-requirements.md` (SCL-REQ-001 v0.5).
