"""SunClave prototype build plan pictures (SCL-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps ...]
With no argument it draws everything; `sheets 107` draws one making sketch. Every picture is drawn
from cad/src/model.py, so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SCL-DWG-101 to 120        making sketches for the made components
    docs/05-build-plan/petal-pattern.png   flat pattern of one petal
    docs/05-build-plan/yoke-layout.png     hole and slot positions on the yoke plate
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402
from model import PARAMS as P  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
DATE2 = "2026-10-02"          # sheets changed for the decisions of 2026-10-02 (drop pin, adapter plate)
D = M.derived(P)
ELEV = 50.0
C = M.build_components(P, elev=ELEV)
L = {**M.dish_components(P), **M.yoke_components(P)}          # dish-frame shapes (dish face up)
FZ = P["F_Z"]

COL = {"cross_rails": "#92400E", "side_rails": "#A16207", "uprights": "#B45309", "braces": "#CA8A04",
       "castors": "#374151", "foot_brackets": "#6B7280", "axle_plates": "#1D4ED8", "axles": "#111827",
       "collars": "#334155", "thrust_washers": "#F5F5F4", "lock_studs": "#0F766E", "plate_bolts": "#111827",
       "stand_bolts": "#111827", "ribs": "#475569", "hub": "#334155", "hub_clips": "#7C3AED", "rim_clips": "#7C3AED",
       "rim": "#1E293B", "petals": "#BAC8D3", "flanges": "#94A3B8", "tabs": "#94A3B8", "gnomon": "#EA580C",
       "standoffs": "#BE123C", "standoff_screws": "#111827", "yoke_plates": "#D4A017", "ring": "#0E7490",
       "arms": "#155E75", "arm_brackets": "#0369A1", "holder_bolts": "#111827", "body": "#4B5563", "lid": "#9CA3AF",
       "gauge": "#64748B", "relief": "#DC2626", "gland": "#7C3AED", "transducer": "#7C3AED", "jacket": "#FDE68A",
       "water": "#38BDF8", "basket": "#0F766E", "load": "#E5E7EB", "thermocouple": "#B91C1C",
       "logger_box": "#115E59", "power_bank": "#1E3A8A", "logger_board": "#16A34A", "cable": "#111827",
       "drop_pins": "#DB2777", "adapter": "#0891B2"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def cp(key, name=None, explode=(0, 0, 0), color=None, shape=None):
    c = C[key]
    return part(name or c.name, shape if shape is not None else c.shape, color or COL.get(key, "#6B7280"), explode)


def CF(shapes):
    """Group shapes for drawing without a boolean union (much faster than fusing)."""
    import build123d as b
    out = []
    for sh in shapes:
        out += list(sh.solids())
    return b.Compound(out)


def S(*keys):
    return CF([C[k].shape for k in keys])


def kids(key):
    sh = C[key].shape
    try:
        return list(sh)
    except TypeError:
        return [sh]


def loc(key):
    return L[key][1]


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & M.bx(x0, x1, y0, y1, z0, z1)


def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def rot_z(shape, deg):
    import build123d as b
    return b.Rot(0, 0, deg) * shape


# ----------------------------------------------------------------- overview
def overview():
    C90 = M.build_components(P, elev=90)
    SS = lambda *ks: CF([C90[k].shape for k in ks])  # noqa: E731
    dx = -2150
    items = [
        ("cross_rails", "Cross rails and castors", ("cross_rails", "castors"), (0, 0, -260)),
        ("side_rails", "Side rails", ("side_rails",), (0, 0, -120)),
        ("uprights", "Uprights and foot brackets", ("uprights", "foot_brackets"), (0, 0, 0)),
        ("braces", "Braces", ("braces",), (0, -520, -80)),
        ("axle_plates", "Axle plates", ("axle_plates",), (0, 0, 420)),
        ("axles", "Axles, collars, PTFE thrust washers", ("axles", "collars", "thrust_washers"), (0, 0, 560)),
        ("ribs", "Ribs, hub plate and rib clips", ("ribs", "hub", "hub_clips", "rim_clips"), (dx, 0, -420)),
        ("rim", "Rim band", ("rim",), (dx, 0, 80)),
        ("petals", "Petals", ("petals", "flanges", "tabs"), (dx, 0, 520)),
        ("gnomon", "Gnomon on its bracket", ("gnomon",), (dx, -150, 1050)),
        ("standoffs", "Rim stand-offs", ("standoffs", "standoff_screws"), (dx, 0, 820)),
        ("yoke_plates", "Yoke plates", ("yoke_plates",), (dx, 0, 1050)),
        ("lock_studs", "Lock studs, star knobs and drop pins", ("lock_studs", "drop_pins"), (0, 0, 920)),
        ("arms", "Holder arms and brackets", ("arms", "arm_brackets"), (0, 0, 1000)),
        ("ring", "Holder ring", ("ring",), (0, 0, 1250)),
        ("body", "Canner, painted, with thermocouple", ("body", "thermocouple"), (1500, 0, 0)),
        ("jacket", "Insulated jacket", ("jacket",), (1500, 0, 380)),
        ("basket", "Basket and trivet", ("basket",), (1500, 0, -560)),
        ("lid", "Lid, factory gauge and relief valve, adapter plate, sensors", ("lid", "gauge", "relief", "adapter", "gland", "transducer"), (1500, 0, 640)),
        ("logger_box", "Logger box, power bank, cable", ("logger_box", "power_bank", "logger_board"), (450, -450, -250)),
    ]
    parts = [part(n, SS(*ks), COL[k], off) for k, n, ks, off in items]
    return bv.overview(parts, OUT / "overview.png", "SunClave prototype: every component, pulled apart",
                       subtitle="Numbered in build order: stand 1 to 6, dish 7 to 13, holder 14 and 15, vessel 16 to 19, logger 20",
                       elev=20, azim=-62, size=(12, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
SHEETS = {}


def sheet(no):
    def deco(fn):
        SHEETS[no] = fn
        return fn
    return deco


def _cs(key_part, neighbours, no, title, material, notes, view_shape=None, inset=(24, -58), date=DATE):
    return bv.component_sheet(key_part, neighbours, project="SunClave", dwg_no=f"SCL-DWG-{no}", title=title,
                              material=material, notes=notes, date=date, view_shape=view_shape, inset_view=inset)


def _g(key):
    return part(C[key].name, C[key].shape, "#9CA3AF")


@sheet(101)
def s101():
    r = kids("cross_rails")[0]
    return _cs(part("Cross rail", r, COL["cross_rails"]), [_g("side_rails"), _g("castors"), _g("uprights")], 101,
               "SunClave cross rail (make 2): making sketch", "Treated timber 70 x 35 mm, laid flat",
               ["Make two. Cut 1,805 mm of 70 x 35 mm treated timber; square the ends.",
                "Lay it flat (70 mm wide, 35 mm thick). It runs across the stand,",
                "  front and back, under the ends of the side rails.",
                "Crossing bolts: two 8.5 mm holes at each end: 50.5 mm from the end",
                "  on the centre line, and 74.5 mm from the end, 20 mm toward the",
                "  inside of the stand. Drill with the side rail clamped in place.",
                "Castor holes: four 8.5 mm holes at each end on a 42 mm square,",
                "  centred 112.5 mm in from the end and on the centre line.",
                "Seal every cut end and hole with end-grain sealer.",
                "Fit: a side rail sits across each end; a castor bolts underneath.",
                "Check: the two rails are the same length within 2 mm."], inset=(25, -60))


@sheet(102)
def s102():
    r = kids("side_rails")[0]
    return _cs(part("Side rail", r, COL["side_rails"]), [_g("cross_rails"), _g("uprights"), _g("braces")], 102,
               "SunClave side rail (make 2): making sketch", "Treated timber 45 x 70 mm, on edge",
               ["Make two. Cut 1,100 mm of 45 x 70 mm treated timber; square ends.",
                "It stands on edge (70 mm tall, 45 mm wide) on the cross rails.",
                "Crossing bolts: drill 8.5 mm down through at each end, 35 mm and",
                "  55 mm from the end, 12 mm either side of the centre line (drill",
                "  with the cross rail clamped square underneath).",
                "Brace foot bolt: 10.5 mm across, 470 mm each side of the middle,",
                "  35 mm up from the bottom edge.",
                "Foot bracket bolts: 8.5 mm down through, 65 mm each side of the",
                "  middle, on the centre line.",
                "Mark the middle: the upright stands there.",
                "Check: straight within 3 mm along its length."], inset=(25, -60))


@sheet(103)
def s103():
    r = kids("uprights")[0]
    return _cs(part("Upright", r, COL["uprights"]), [_g("side_rails"), _g("braces"), _g("axle_plates"), _g("arms")], 103,
               "SunClave upright (make 2): making sketch", "Treated timber 45 x 70 mm",
               [f"Make two. Cut {D['upr_top'] - D['z_sr'][1]:.0f} mm of 45 x 70 mm timber; square the ends.",
                "Heights below are from the bottom end. Drill across the 45 mm way,",
                "  square to the face, on the centre line of the 70 mm face:",
                f"  brace bolt 10.5 mm at {P['BRACE_Z'] - D['z_sr'][1]:.0f}; lock stud 10.5 mm at {FZ + P['LOCK_Z'] - D['z_sr'][1]:.0f};",
                f"  axle 20.5 mm at {FZ - D['z_sr'][1]:.0f}; plate bolt 10.5 mm at {FZ + P['PLATE_BOLT_Z'] - D['z_sr'][1]:.0f};",
                f"  arm bracket bolt 8.5 mm at {D['upr_top'] - 20 - D['z_sr'][1]:.0f}; drop pin slot 10 x 32 mm at",
                f"  {FZ - P['PIN_R'] - D['z_sr'][1]:.0f} (two 10 mm holes 22 mm apart, chisel between).",
                "Foot bracket bolt: 8.5 mm through the 70 mm way, 28 mm up.",
                f"Lanyard eye screw: outer face, {P['PIN_EYE'][0]:.0f} mm off centre, at {FZ + P['PIN_EYE'][1] - D['z_sr'][1]:.0f}.",
                "The axle hole sets the focus height: drill it from both faces",
                "  with a long bit after a 6 mm pilot, so it stays square.",
                "Fit: stands on the middle of a side rail; the axle plate goes on",
                "  the inner face, the logger box on the outer face of one upright.",
                "Check: the axle holes of both uprights are at the same height."], inset=(22, -55), date=DATE2)


@sheet(104)
def s104():
    br = kids("braces")[0]
    a = (D["xo"] + P["BRACE_T"] / 2, -P["BRACE_Y"], (D["z_sr"][0] + D["z_sr"][1]) / 2)
    b = (a[0], 0.0, P["BRACE_Z"])
    ln = math.hypot(b[1] - a[1], b[2] - a[2])
    u = (0, (b[1] - a[1]) / ln, (b[2] - a[2]) / ln)
    fl = flat(br, a, u, (1, 0, 0))
    return _cs(part("Brace", br, COL["braces"]), [_g("uprights"), _g("side_rails"), _g("cross_rails")], 104,
               "SunClave brace (make 4): making sketch", "Treated timber 45 x 35 mm", view_shape=fl, inset=(20, -30),
               notes=[f"Make four. Cut {ln + 45:.0f} mm of 45 x 35 mm timber, ends square.",
                      f"Two 10.5 mm holes through the 35 mm way, {ln:.0f} mm apart, 20 mm",
                      "  and 25 mm in from the ends, on the centre line.",
                      "Drill the four together clamped in a stack so they match.",
                      "Fit: the 45 mm face lies flat on the upright and the side rail.",
                      "  On each upright the front brace is on the outer face and the",
                      "  back brace on the inner face; one M10 bolt goes through both",
                      f"  braces and the upright at {P['BRACE_Z']:.0f} mm above the ground.",
                      "  The foot bolt goes through the brace and the side rail.",
                      "Check: with both bolts in, the upright stands plumb within 2 mm."])


@sheet(105)
def s105():
    ap = kids("axle_plates")[0]
    return _cs(part("Axle plate", ap, COL["axle_plates"]), [_g("uprights"), _g("axles"), _g("yoke_plates")], 105,
               "SunClave axle plate (make 2): making sketch", "Steel flat bar 70 x 6 mm", inset=(20, -40),
               date=DATE2,
               notes=[f"Make two. Cut {P['AXLE_PLATE'][2]:.0f} mm of 70 x 6 mm steel flat bar; deburr.",
                      "Three holes on the centre line, measured from the top end:",
                      f"  bolt 11 mm at 25; axle 20.5 mm at 105; lock stud 11 mm at {105 - P['LOCK_Z']:.0f}.",
                      f"Drop pin slot: 8.5 mm wide on a {P['PIN_R']:.0f} mm radius from the axle",
                      f"  hole, centred {105 + P['PIN_R']:.0f} from the top, {P['PIN_PITCH']:.1f} degrees long (21 mm",
                      "  between the end centres): drill both ends, saw and file between.",
                      "Drill the axle hole in steps (6, 12, 18, 20.5 mm) on a drill",
                      "  press, the plate clamped flat.",
                      "Paint or galvanise; leave the face around the axle bare and",
                      "  greased, and the face around the stud bare for the lock.",
                      "Fit: flat on the inner face of the upright, holes on the upright",
                      "  holes; the M10 plate bolt at the top, the stud at the bottom.",
                      "Check: a 20 mm bar passes through plate and upright together."])


@sheet(106)
def s106():
    ax = kids("axles")[0]
    return _cs(part("Axle", ax, COL["axles"]), [_g("uprights"), _g("axle_plates"), _g("yoke_plates"), _g("collars")], 106,
               "SunClave axle (make 2): making sketch", "Bright steel round bar 20 mm", inset=(20, -40),
               notes=[f"Make two. Cut {ax.bounding_box().size.X:.0f} mm of 20 mm bright steel round bar.",
                      "File a 1 mm chamfer on both ends so it starts into the holes.",
                      "File a small flat 10 mm long at each collar position (12 mm",
                      "  and 79 mm from the outer end) for the collar set screws.",
                      "Fit, from outside to inside: outer collar, upright, axle plate,",
                      "  PTFE thrust washer, yoke plate, inner collar.",
                      "The axle does not turn: the yoke plate turns on it, greased.",
                      "Check: it slides through the drilled upright and plate by hand."])


def _rib_local():
    a = M.rib_angles(P)[0]
    rib = list(loc("ribs"))[0]
    return rot_z(rib, -a), a


@sheet(107)
def s107():
    rl, a = _rib_local()
    ribw = M.to_world(list(loc("ribs"))[0], P, ELEV)
    return _cs(part("Rib", ribw, COL["ribs"]), [_g("petals"), _g("rim"), _g("hub")], 107,
               "SunClave rib (make 12): making sketch", "Steel flat bar 20 x 3 mm, bent on edge", view_shape=rl,
               inset=(30, -70),
               notes=["Make twelve. Cut 720 mm of 20 x 3 mm flat bar each.",
                      "Bend on edge (the hard way) in a plywood jig cut to the curve",
                      "  of the dish: height above the vertex = radius squared / 2,000.",
                      "  At 100, 200, 300, 400, 500, 600, 700 mm out: 5, 20, 45, 80,",
                      "  125, 180, 245 mm. Clamp the bar to the jig as you go.",
                      "The top edge of the bent rib follows the curve; the rib stands",
                      "  20 mm deep behind the petals.",
                      "Trim both ends square to the jig base (upright): the outer end",
                      "  699.5 mm and the inner end 55 mm from the axis line.",
                      "Clip bolt holes and rivet holes are drilled at assembly,",
                      "  through the clips and the petal flanges.",
                      "Check: on the jig the rib touches the curve within 1 mm."])


@sheet(108)
def s108():
    return _cs(part("Hub plate", M.to_world(loc("hub"), P, ELEV), COL["hub"]), [_g("ribs"), _g("hub_clips")], 108,
               "SunClave hub plate: making sketch", "Steel plate 4 mm", view_shape=loc("hub"), inset=(40, -70),
               notes=["Cut a 200 mm disc from 4 mm steel plate; deburr the edge.",
                      "Mark twelve lines from the centre, 30 degrees apart. These are",
                      "  the rib lines; the clips sit 1.5 mm to one side of each line.",
                      "On each line, offset 11.5 mm to the clip side, drill 5.5 mm at",
                      "  72.5 mm from the centre for the clip bolt.",
                      "Paint the back; the front is hidden behind the petals.",
                      "Fit: the ribs' inner ends stand on its front face, each held by",
                      "  a rib clip; it hangs about 22 mm behind the petals.",
                      "Check: the twelve holes are on a 72.5 mm radius within 1 mm."])


@sheet(109)
def s109():
    a = M.rib_angles(P)[0]
    clip = list(loc("hub_clips"))[0]
    return _cs(part("Rib clip", M.to_world(clip, P, ELEV), COL["hub_clips"]), [_g("ribs"), _g("hub")], 109,
               "SunClave rib clip (make 24): making sketch", "Steel equal angle 20 x 20 x 3 mm",
               view_shape=rot_z(clip, -a), inset=(40, -70),
               notes=["Make 24 (12 at the hub, 12 at the rim): all the same.",
                      "Cut 13 mm slices from 20 x 20 x 3 mm steel angle; deburr.",
                      "Drill one 5.5 mm hole in the middle of each leg.",
                      "At the hub: one leg on the hub plate, the other against the side",
                      "  of the rib, M5 bolt through each leg.",
                      "At the rim: one leg on the inside of the rim band, the other",
                      "  over the petal flange on the side of the rib; one M5 bolt",
                      "  through clip, flange, rib and the next petal's flange.",
                      "Check: a clip sits flat on both faces at once."])


@sheet(110)
def s110():
    return _cs(part("Rim band", M.to_world(loc("rim"), P, ELEV), COL["rim"]), [_g("ribs"), _g("petals"), _g("standoffs")], 110,
               "SunClave rim band: making sketch", "Steel flat bar 25 x 4 mm, rolled", view_shape=loc("rim"), inset=(40, -70),
               notes=["Roll 4,440 mm of 25 x 4 mm flat bar the easy way into a ring",
                      "  1,400 mm inside diameter (by hand round a ring of stakes, or",
                      "  by a local fabricator with rolls). Join the ends with a 100 mm",
                      "  strap of the same bar inside, four M5 bolts, at a rib position.",
                      "Mark twelve rib positions 30 degrees apart, starting 15 degrees",
                      "  from the two stand-off positions, which are opposite each other.",
                      "Drill: 9 mm pairs (30 mm apart) at the two stand-off positions;",
                      "  6.5 mm pair (24 mm apart) at the gnomon, midway between two",
                      "  ribs; 5.5 mm for each rim clip; tab rivets at assembly.",
                      "Check: round within 3 mm across any two diameters."])


@sheet(111)
def s111():
    sheet_ = loc("petals")
    one = sorted(sheet_.solids(), key=lambda s_: -s_.volume)[0]
    c = one.center()
    ang = math.degrees(math.atan2(c.Y, c.X))
    return _cs(part("Petal", M.to_world(one, P, ELEV), COL["petals"]), [_g("ribs"), _g("rim")], 111,
               "SunClave petal (make 12): making sketch", "Aluminium reflector sheet 0.5 mm, 85 % reflectance",
               view_shape=rot_z(one, -ang), inset=(40, -70),
               notes=["Make twelve from the flat pattern (petal pattern picture).",
                      "Leave the protective film on until the dish is finished.",
                      "Cut with aviation snips; drill 3 mm relief holes where folds meet.",
                      "Fold a 12 mm flange down along both long edges, a little at a",
                      "  time along the length, so the petal takes up a gentle curve.",
                      "Fold the two 30 mm tabs down at the outer edge.",
                      "Lay the petal on two neighbouring ribs, flanges outside the ribs;",
                      "  drill 3.3 mm through flange and rib every 50 mm and rivet with",
                      "  3.2 mm aluminium rivets; rivet each tab to the rim band.",
                      "Never scratch the bright face; handle with clean cotton gloves.",
                      "Check: the petal edges meet over each rib with a gap of 3 to 5 mm."])


@sheet(112)
def s112():
    g = loc("gnomon")
    return _cs(part("Gnomon", M.to_world(g, P, ELEV), COL["gnomon"]), [_g("rim"), _g("petals")], 112,
               "SunClave gnomon on its bracket: making sketch", "Steel angle 40 x 40 x 4, aluminium plate 3 mm, steel pin 8 mm",
               view_shape=rot_z(g, -270), inset=(40, -100),
               notes=["Bracket: 40 mm of 40 x 40 x 4 mm angle. Upright leg: two 6.5 mm",
                      "  holes 24 mm apart, 20 mm down. Flat leg: two 5.5 mm holes.",
                      "Target plate: 120 x 120 mm of 3 mm aluminium, painted matt white;",
                      "  scribe two rings, 10 and 25 mm radius, at its centre.",
                      "Pin: 8 mm steel rod 183 mm long, threaded M8 for 15 mm at one end,",
                      "  through a centre hole with a nut each side, square to the plate.",
                      "Fit: the bracket's upright leg on the outside of the rim band at",
                      "  the lowest point of the dish, the plate on the flat leg flush",
                      "  with the rim edge; the pin is parallel to the dish axis.",
                      "Check: an engineer's square on the plate touches the pin."])


@sheet(113)
def s113():
    so = list(loc("standoffs"))[0]
    return _cs(part("Rim stand-off", M.to_world(so, P, ELEV), COL["standoffs"]), [_g("rim"), _g("yoke_plates"), _g("petals")], 113,
               "SunClave rim stand-off (make 2): making sketch", "Steel rectangular tube 50 x 25 x 2.5 mm",
               view_shape=so, inset=(30, -60),
               notes=[f"Make two. Cut {so.bounding_box().size.X:.1f} mm of 50 x 25 x 2.5 mm tube, ends square.",
                      "Nothing is drilled in the tube: the two M8 screws run along its",
                      "  inside, so it is a spacer clamped end to end.",
                      "File both ends flat and square so they bear on the rim band",
                      "  and on the yoke plate across their full face.",
                      "Fit: the 25 mm sides run with the rim band's height; two M8",
                      "  countersunk screws 30 mm apart pass through the yoke plate, the",
                      "  tube and the rim band, nyloc nuts inside the band.",
                      "Check: the length of the two stand-offs matches within 0.5 mm."])


@sheet(114)
def s114():
    import build123d as b
    yp_flat = b.extrude(M.yoke_plate_2d(P), amount=P["YOKE_T"])
    return _cs(part("Yoke plate", kids("yoke_plates")[0], COL["yoke_plates"]),
               [_g("axle_plates"), _g("uprights"), _g("standoffs"), _g("rim")], 114,
               "SunClave yoke plate (make 2): making sketch", "Steel plate 6 mm", view_shape=yp_flat, inset=(15, -30), date=DATE2,
               notes=["Make two, a left and a right: the same outline, countersunk on",
                      "  opposite faces. Cut from 6 mm steel plate by jigsaw or a",
                      "  local cutting shop to the yoke layout picture: a 40 mm radius",
                      f"  hub, a 60 mm wide arm {D['standoff_r']:.1f} mm to the stand-off holes,",
                      "  and a fan from 125 to 175 mm radius.",
                      "Axle hole 20.5 mm at the hub centre, reamed smooth.",
                      f"Lock slot 11 mm wide on a {P['SLOT_R']:.0f} mm radius, from the arm's line",
                      "  round 75 degrees toward the fan's far edge.",
                      f"Drop pin holes: eleven 8.5 mm on a {P['PIN_R']:.0f} mm radius, the first",
                      f"  on the arm's line, then every {P['PIN_PITCH']:.1f} degrees along the slot.",
                      "Stand-off holes: two 9 mm, 30 mm apart, countersunk 90 degrees",
                      "  on the outer face so the M8 heads sit flush.",
                      "Fit: the outer face runs on the PTFE washer by the axle plate.",
                      "Check: laid back to back, the two plates match all round."])


@sheet(115)
def s115():
    arm = kids("arms")[0]
    return _cs(part("Holder arm", arm, COL["arms"]), [_g("uprights"), _g("ring"), _g("arm_brackets"), _g("body")], 115,
               "SunClave holder arm (make 2): making sketch", "Steel square tube 25 x 25 x 2 mm", inset=(25, -50),
               notes=[f"Make two. Cut {arm.bounding_box().size.X:.0f} mm of 25 x 25 x 2 mm tube; cap the ends.",
                      "Drill 8.5 mm vertically through both walls:",
                      f"  ring bolt {(P['RING_R'][0] + P['RING_R'][1]) / 2 - P['RING_R'][0] - 2:.0f} mm from the inner end;",
                      f"  bracket bolt {D['xo'] - D['xi'] + 20:.0f} mm from the outer end.",
                      "Fit: the outer 45 mm rests on the top of the upright, flush with",
                      "  its outer face; the bracket under it on the upright's inner face.",
                      "  The holder ring sits on the inner ends of both arms.",
                      "Check: laid across both uprights, the arms are level within 1 mm."])


@sheet(116)
def s116():
    br = kids("arm_brackets")[0]
    return _cs(part("Arm bracket", br, COL["arm_brackets"]), [_g("uprights"), _g("arms"), _g("axle_plates")], 116,
               "SunClave arm bracket (make 2): making sketch", "Steel equal angle 40 x 40 x 4 mm", inset=(25, -50),
               notes=["Make two. Cut 40 mm slices of 40 x 40 x 4 mm angle; deburr.",
                      "One 8.5 mm hole in the middle of each leg, 20 mm from the corner.",
                      "Fit: the upright leg flat on the inner face of the upright, its",
                      "  top level with the upright's top, M8 bolt through the upright;",
                      "  the flat leg under the holder arm, M8 bolt up through both.",
                      "It sits 4 mm above the top of the axle plate.",
                      "Check: the flat leg is level with the upright's top end."])


@sheet(117)
def s117():
    return _cs(part("Holder ring", C["ring"].shape, COL["ring"]), [_g("arms"), _g("body"), _g("jacket")], 117,
               "SunClave holder ring: making sketch", "Steel plate 4 mm", inset=(30, -60),
               notes=["Cut a flat ring from 4 mm steel plate: 348 mm inside and 408 mm",
                      "  outside diameter (jigsaw with a metal blade, or a cutting shop).",
                      "Two 9 mm holes on a 378 mm diameter, opposite each other.",
                      "File the inner edge smooth; paint with heat-resistant paint.",
                      "Fit: it lies on the two holder arms, one M8 bolt into each;",
                      "  the canner drops through it and hangs by its two handles.",
                      "  The jacket clears the inner edge by 5 mm all round.",
                      "Check: the canner body and jacket pass through without touching."], date=DATE2)


@sheet(118)
def s118():
    jk = list(C["jacket"].shape)[0]
    return _cs(part("Jacket", C["jacket"].shape, COL["jacket"]), [_g("body"), _g("ring")], 118,
               "SunClave insulated jacket: making sketch", "Mineral wool blanket 25 mm, aluminised glass cloth skin",
               view_shape=jk, inset=(30, -60),
               notes=["Cut a strip of 25 mm aluminised blanket 96 mm wide and 1,010 mm",
                      "  long, foil outward; wear gloves, a dust mask and glasses.",
                      "Bind both long edges with aluminised tape.",
                      "Fit: wrap it round the canner wall from 80 mm above the base to",
                      "  30 mm below the rim, butt the ends and tape the joint.",
                      "  Hold it with two stainless strap clamps, 12 mm from each edge.",
                      "The lowest 80 mm of wall and the base stay bare and black.",
                      "Check: it stops below the handles and clears the ring by 5 mm."], date=DATE2)


@sheet(119)
def s119():
    import build123d as b
    pr = [k for k in kids("drop_pins") if k.bounding_box().center().X > 0][0]
    L_ = D["xo"] + 8 - D["x_yoke"]
    return _cs(part("Drop pin", pr, COL["drop_pins"]), [_g("uprights"), _g("axle_plates"), _g("yoke_plates")], 119,
               "SunClave drop pin and lanyard (make 2): making sketch", "Bright steel round bar 8 mm, steel ring, stainless wire",
               inset=(20, -40), date=DATE2,
               notes=[f"Make two. Cut {L_ - 8:.0f} mm of 8 mm bright steel bar; chamfer",
                      "  one end 1 mm so it finds the hole.",
                      "Head: a steel washer 18 mm across, 8 mm thick (or two",
                      "  washers), pinned or glued on the other end; or buy a",
                      f"  ready-made 8 mm locking pin about {L_:.0f} mm long.",
                      "Lanyard: 300 mm of stainless wire rope with crimped loops,",
                      "  from the head to an eye screw on the upright's outer face.",
                      "Fit: push it in from outside the stand, through the slot",
                      "  in the upright, the slot in the axle plate and the",
                      "  fan hole that shows in the slot; its tip ends flush with",
                      "  the fan's inner face. Pull it out to re-aim the dish.",
                      "Check: it slides in and out by hand at every aim."])


@sheet(120)
def s120():
    al, aw_, ah = P["ADAPTER"]
    return _cs(part("Adapter plate", C["adapter"].shape, COL["adapter"]), [_g("lid"), _g("gland"), _g("transducer")], 120,
               "SunClave vent-stem adapter plate: making sketch", "Stainless steel bar 40 x 20 mm, threaded spigot and nut",
               inset=(30, -60), date=DATE2,
               notes=[f"Have a machine shop make it: {al:.0f} x {aw_:.0f} x {ah:.0f} mm stainless block",
                      "  with a threaded spigot underneath that fits the canner's",
                      f"  own vent-pipe hole ({P['LID_PORT_D']:.0f} mm here: measure the canner) and a",
                      "  nut and high-temperature gasket to clamp it to the lid.",
                      f"Bore {P['PORT_D']:.0f} mm up through the spigot to the gland port on top.",
                      f"Two side ports on top, {P['VENT_X']:.0f} mm each side of the centre: the",
                      "  canner's own vent pipe (its thread) and 1/4 in NPT for the",
                      "  transducer; drill a 4 mm passage from the bore to each.",
                      "Gland port 1/8 in NPT on the centre for the probe gland.",
                      "The lid itself is not drilled; the overpressure plug stays.",
                      "Check: with the probe in, a 3 mm drill passes the vent",
                      "  passage, and a 2.5 mm wire passes beside the probe."])


def sheets(which=None):
    out = []
    for no, fn in sorted(SHEETS.items()):
        if which and str(no) not in which:
            continue
        out.append(fn())
        print("sheet", no, flush=True)
    return out


# ----------------------------------------------------------------- flat layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MPoly, Circle as MCirc
    INK, MUT, AC, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"
    res = []
    repo = "github.com/BoujeeEnjinia1701/sunclave"

    # petal flat pattern: developed along the meridian, width from the arc between the rib planes
    f, R, r0 = P["FOCAL"], P["D_DISH"] / 2, P["HUB_R0"]
    gap = P["RIB_T"] / 2 + 1.0
    n = 120
    rs = [r0 + (R - r0) * i / n for i in range(n + 1)]
    s, acc = [0.0], 0.0
    for a, b in zip(rs[:-1], rs[1:]):
        acc += math.hypot(b - a, M._para(b, f) - M._para(a, f)); s.append(acc)
    half = [r * (math.pi / P["N_PETALS"] - math.asin(gap / r)) for r in rs]
    fl = P["FLANGE"]
    fig = plt.figure(figsize=(12, 7.5), dpi=150)
    ax = fig.add_axes([0.05, 0.12, 0.62, 0.74]); ax.set_aspect("equal"); ax.set_axis_off()
    top = [(si, h) for si, h in zip(s, half)]
    body = top + [(si, -h) for si, h in reversed(list(zip(s, half)))]
    ax.add_patch(MPoly(body, closed=True, fc="#E2E8F0", ec=INK, lw=1.1))
    k0 = next(i for i, r in enumerate(rs) if r >= P["FLANGE_R0"])
    for sg in (1, -1):
        fpts = [(si, sg * h) for si, h in zip(s[k0:], half[k0:])] + [(si, sg * (h + fl)) for si, h in reversed(list(zip(s[k0:], half[k0:])))]
        ax.add_patch(MPoly(fpts, closed=True, fc="#F8FAFC", ec=MUT, lw=0.8, ls="--"))
    tw, td = P["TAB"]
    for sg in (1, -1):
        yc = sg * R * math.radians(5)
        ax.add_patch(MPoly([(s[-1], yc - tw / 2), (s[-1] + td, yc - tw / 2), (s[-1] + td, yc + tw / 2), (s[-1], yc + tw / 2)],
                           closed=True, fc="#F8FAFC", ec=MUT, lw=0.8, ls="--"))
    # rivet lines and stations
    for st in range(0, int(s[-1]), 50):
        if st < s[k0] + 10:
            continue
        hh = half[min(range(len(s)), key=lambda j: abs(s[j] - st))]
        for sg in (1, -1):
            ax.add_patch(MCirc((st, sg * (hh + fl / 2)), 1.6, fc="white", ec=INK, lw=0.5))
    for r_mark in (100, 200, 300, 400, 500, 600, 700):
        j = min(range(len(rs)), key=lambda q: abs(rs[q] - r_mark))
        ax.plot([s[j], s[j]], [-half[j] - fl - 6, half[j] + fl + 6], color=AC, lw=0.4, ls=":")
        ax.plot([s[j], s[j]], [half[j] + fl + 6, half[j] + fl + 14], color=AC, lw=0.4, ls=":")
        ax.text(s[j], half[j] + fl + 16, f"{s[j]:.0f}", ha="center", va="bottom", fontsize=7, color=AC)
        ax.text(s[j], -half[j] - fl - 16, f"{2 * half[j]:.0f} wide", ha="center", va="top", fontsize=7, color=INK)
    ax.text(-8, 0, "inner edge\n(hub end)", ha="right", va="center", fontsize=7.5, color=MUT)
    ax.text(s[-1] + td + 6, 0, "outer edge\n(rim)", ha="left", va="center", fontsize=7.5, color=MUT)
    ax.set_xlim(-60, s[-1] + 70); ax.set_ylim(-half[-1] - fl - 45, half[-1] + fl + 45)
    fig.text(0.03, 0.965, "Petal: flat pattern (make 12)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Developed along the curve of the dish. Teal figures: distance along the centre line from the inner edge, mm.\n"
             "Black figures: width of the bright face between the fold lines at that station. Dashed: 12 mm flanges and 30 x 12 mm tabs, folded down.",
             fontsize=8.2, color=MUT, va="top")
    key = ["Fold lines: the outline of the bright face.", "Flanges fold down 90 degrees along both", "  long edges; tabs fold down at the rim.",
           "Circles: rivet holes, 3.3 mm, every 50 mm", "  along each flange, drilled at assembly", "  through flange and rib together.",
           "", f"Inner edge {2 * half[0]:.0f} mm wide, {r0:.0f} mm from the axis.", f"Outer edge {2 * half[-1]:.0f} mm wide, {R:.0f} mm from the axis.",
           f"Length along the centre line {s[-1]:.0f} mm.", "", "Mark on the protective film; cut with", "  aviation snips; drill 3 mm relief holes",
           "  where the flange and tab folds meet."]
    for i, t in enumerate(key):
        fig.text(0.70, 0.84 - i * 0.033, t, fontsize=8.2, color=INK, va="top")
    fig.text(0.03, 0.02, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color=WARN)
    fig.text(0.97, 0.02, repo, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "petal-pattern.png", facecolor="white"); plt.close(fig); res.append(OUT / "petal-pattern.png")

    # yoke plate layout, seen from the inner face, arm pointing down
    Ls = D["standoff_r"]
    fig = plt.figure(figsize=(10, 10.5), dpi=150)
    ax = fig.add_axes([0.06, 0.06, 0.6, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    face = M.yoke_plate_2d(P).faces()[0]
    ax.add_patch(MPoly([(v.X, v.Y) for v in face.outer_wire().positions([i / 400 for i in range(401)])], closed=True,
                       fc="#FEF3C7", ec=INK, lw=1.1))
    for wv in face.inner_wires():
        ax.add_patch(MPoly([(v.X, v.Y) for v in wv.positions([i / 300 for i in range(301)])], closed=True, fc="white", ec=INK, lw=0.9))
    ax.plot([0, 0], [60, -Ls - 45], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.plot([-200, 60], [0, 0], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.annotate("axle 20.5 mm\nat the centre", (0, 0), (48, 40), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    a_mid = math.radians(-128)
    sr, pr_ = P["SLOT_R"], P["PIN_R"]
    ax.annotate(f"lock slot 11 mm wide,\n{sr:.0f} mm radius,\nfrom the arm line\n75 degrees round", (sr * math.cos(a_mid), sr * math.sin(a_mid)),
                (-300, -250), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    a_p = math.radians(-157.5)
    ax.annotate(f"drop pin holes: eleven 8.5 mm\non a {pr_:.0f} mm radius,\nevery {P['PIN_PITCH']:.1f} degrees", (pr_ * math.cos(a_p), pr_ * math.sin(a_p)),
                (-345, -125), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    ax.annotate(f"two 9 mm holes, 30 mm apart,\n{Ls:.1f} mm from the axle centre,\ncountersunk on the outer face", (15, -Ls), (40, -Ls + 40),
                fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    ax.annotate("fan: 125 to 175 mm radius", (-175 * math.cos(math.radians(10)), -175 * math.sin(math.radians(10))), (-300, 55),
                fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    ax.annotate("hub 40 mm radius", (28, 28), (60, 90), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    ax.annotate("arm 60 mm wide", (30, -150), (70, -170), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5))
    ax.set_xlim(-350, 160); ax.set_ylim(-Ls - 60, 120)
    fig.text(0.04, 0.975, "Yoke plate: layout (make 2, a left and a right)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.945, "6 mm steel plate, the right-hand plate seen from its outer face (the face that runs on the axle plate), arm pointing down.\nThe left-hand plate is the same outline turned over. Sizes in mm, from the model.",
             fontsize=8.2, color=MUT, va="top")
    keyt = ["How the lock works", "", "The lock stud stays still in the", "upright. As the dish tilts from", "90 degrees (pointing straight up)",
            "to 15 degrees (low sun), the slot", "slides past the stud.", "", "At 90 degrees the stud sits at the", "end of the slot on the arm line;",
            "at 15 degrees, at the far end.", "", "Tighten the star knob to clamp the", "fan; loosen it to tilt.", "",
            "Back-up stop: a drop pin goes", "through the upright, the short slot", "in the axle plate and whichever",
            "hole shows in the slot. If a lock", "slips, the dish turns at most", f"{P['PIN_PITCH']:.1f} degrees before the pin stops it."]
    for i, t in enumerate(keyt):
        fig.text(0.70, 0.86 - i * 0.03, t, fontsize=8.4, color=INK, va="top", fontweight="bold" if i == 0 else "normal")
    fig.text(0.04, 0.02, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color=WARN)
    fig.text(0.96, 0.02, repo, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "yoke-layout.png", facecolor="white"); plt.close(fig); res.append(OUT / "yoke-layout.png")
    return res


# ----------------------------------------------------------------- joints
def joints(which=None):
    out = []
    xo, xi = D["xo"], D["xi"]
    yr = P["BASE_Y"] / 2 - P["RAIL_W"] / 2
    zs0, zs1 = D["z_sr"]
    zl0 = D["z_lr"][0]

    def J(n, parts_, title, sub, **kw):
        if which and str(n) not in which:
            return
        out.append(bv.joint([p for p in parts_ if p is not None], OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))
        print("joint", n, flush=True)

    # 1 corner: side rail across the cross rail, castor underneath
    b = (700, 900, -600, -440, -5, zs1 + 15)
    J(1, [part("Cross rail", win(C["cross_rails"].shape, *b), COL["cross_rails"]),
          part("Side rail, on edge", win(C["side_rails"].shape, *b), COL["side_rails"]),
          part("Castor, four M8 bolts into the cross rail", win(C["castors"].shape, *b), COL["castors"]),
          part("M8 crossing bolts; M10 brace foot bolt", win(C["stand_bolts"].shape, *b), "#111827")],
      "corner of the base (front right)", "The side rail crosses on top of the cross rail; the castor sits inboard of the side rail",
      elev=22, azim=-55, size=(8, 6))
    # 2 upright foot
    b = (790, 900, -100, 100, zs0 - 10, zs1 + 70)
    J(2, [part("Side rail", win(C["side_rails"].shape, *b), COL["side_rails"]),
          part("Upright", win(C["uprights"].shape, *b), COL["uprights"]),
          part("Foot brackets, front and back", win(C["foot_brackets"].shape, *b), COL["foot_brackets"]),
          part("M8 bolts", win(C["stand_bolts"].shape, *b), "#111827")],
      "upright on the side rail", "One bolt through the upright holds both brackets; one bolt each down through the side rail",
      elev=25, azim=-60, size=(8, 6))
    # 3 brace top: both braces and the upright, one bolt
    b = (770, 920, -90, 90, P["BRACE_Z"] - 70, P["BRACE_Z"] + 50)
    J(3, [part("Upright", win(C["uprights"].shape, *b), COL["uprights"]),
          part("Front brace (outer face)", win(C["braces"].shape & M.bx(xo, xo + 40, -600, 600, 0, 2000), *b), COL["braces"]),
          part("Back brace (inner face)", win(C["braces"].shape & M.bx(xi - 40, xi, -600, 600, 0, 2000), *b), "#EAB308"),
          part("One M10 bolt through all three", win(C["stand_bolts"].shape, *b), "#111827")],
      "brace tops on the upright (right side)", "The braces lap the upright on opposite faces, so one bolt holds both",
      elev=20, azim=-35, size=(8, 6))
    # 4 brace foot
    b = (840, 920, -560, -380, zs0 - 5, zs1 + 60)
    J(4, [part("Side rail", win(C["side_rails"].shape, *b), COL["side_rails"]),
          part("Front brace", win(C["braces"].shape, *b), COL["braces"]),
          part("M10 bolt through brace and side rail", win(C["stand_bolts"].shape, *b), "#111827"),
          part("Cross rail", win(C["cross_rails"].shape, *b), COL["cross_rails"])],
      "brace foot on the side rail (front right)", "The brace lies flat on the side rail's outer face",
      elev=15, azim=-20, size=(8, 6))
    # 5 pivot, cut open through the axis
    b = (770, 890, -40, 40, FZ - 70, FZ + 70)
    J(5, [part("Upright (timber)", win(C["uprights"].shape, *b), COL["uprights"]),
          part("Axle plate", win(C["axle_plates"].shape, *b), COL["axle_plates"]),
          part("PTFE thrust washer", win(C["thrust_washers"].shape, *b), "#E7E5E4"),
          part("Yoke plate (turns)", win(C["yoke_plates"].shape, *b), COL["yoke_plates"]),
          part("Axle, 20 mm (fixed)", win(C["axles"].shape, *b), COL["axles"]),
          part("Collars", win(C["collars"].shape, *b), COL["collars"])],
      "pivot (right side), cut open through the axle", "The yoke plate turns on the greased axle; the collars hold the stack together",
      cut="+Y", elev=12, azim=-80, size=(8, 6))
    # 6 lock, cut open
    zl = FZ + P["LOCK_Z"]
    b = (760, 890, -40, 40, zl - 50, zl + 50)
    J(6, [part("Upright (timber)", win(C["uprights"].shape, *b), COL["uprights"]),
          part("Axle plate", win(C["axle_plates"].shape, *b), COL["axle_plates"]),
          part("Yoke plate fan (slot)", win(C["yoke_plates"].shape, *b), COL["yoke_plates"]),
          part("Lock stud, spacer, washer, star knob", win(C["lock_studs"].shape, *b), COL["lock_studs"]),
          part("Drop pin, lanyard and eye screw (back-up stop)", win(C["drop_pins"].shape, *b), COL["drop_pins"])],
      "tilt lock and drop pin (right side), cut open", "Knob tight: the fan is clamped. The drop pin, pushed in from outside, stops the dish if the lock slips",
      cut="+Y", elev=12, azim=-80, size=(8, 6))
    # dish joints in the dish frame (dish face up)
    a = M.rib_angles(P)[0]
    R = P["D_DISH"] / 2

    def lw(key, x0, x1, y0, y1, z0, z1):
        return rot_z(loc(key), -a) & M.bx(x0, x1, y0, y1, z0, z1)
    hz = M.dish_profile(P)["hub_front"]
    b = (25, 120, -35, 40, hz - 8, 12)
    J(7, [part("Hub plate", lw("hub", *b), COL["hub"]), part("Rib", lw("ribs", *b), COL["ribs"]),
          part("Rib clip, M5 bolt in each leg", lw("hub_clips", *b), COL["hub_clips"]),
          part("Petal (inner edge)", lw("petals", *b), COL["petals"])],
      "rib on the hub plate", "The rib stands on edge on the hub plate; a clip bolts to both", elev=25, azim=-120, size=(8, 6))
    zr0 = R ** 2 / 2000 - P["RIM_W"]
    b = (660, 712, -15, 45, zr0 - 5, zr0 + 32)
    J(8, [part("Rim band", lw("rim", *b), COL["rim"]), part("Rib", lw("ribs", *b), COL["ribs"]),
          part("Rim clip over the petal flange", lw("rim_clips", *b), COL["rim_clips"]),
          part("Petal flange", lw("flanges", *b), COL["flanges"]),
          part("Petal (outer edge)", lw("petals", *b), COL["petals"])],
      "rib end at the rim band, seen from behind the dish", "The clip bolts through the band, and through clip, flange, rib and flange",
      elev=-35, azim=200, size=(8, 6))
    r9 = 400.0
    b = (r9 - 10, r9 + 10, -22, 22, M._para(r9, 500) - 24, M._para(r9, 500) + 2)
    J(9, [part("Rib, 20 x 3 mm on edge", lw("ribs", *b), COL["ribs"]),
          part("Petal flanges, riveted through the rib", lw("flanges", *b), COL["flanges"]),
          part("Petals, bright face up", lw("petals", *b), COL["petals"])],
      "petals on a rib, cut across, seen from the hub end", "Each petal's flange folds down beside the rib; one rivet goes through both flanges and the rib",
      elev=8, azim=192, size=(8, 6))
    # 10 stand-off between the rim band and the yoke plate (dish frame, not rotated)
    zc = (D["rim_z"][0] + D["rim_z"][1]) / 2
    b = (660, 820, -60, 60, zc - 60, zc + 60)
    lo = lambda k: loc(k) & M.bx(*b)  # noqa: E731
    J(10, [part("Rim band", lo("rim"), COL["rim"]), part("Rim stand-off (tube)", lo("standoffs"), COL["standoffs"]),
           part("Yoke plate (arm end)", lo("yoke_plates"), COL["yoke_plates"]),
           part("Two M8 countersunk screws, nuts inside", lo("standoff_screws"), "#111827"),
           part("Petal tabs", lo("tabs"), COL["tabs"])],
      "rim stand-off (right side)", "The tube is clamped end to end between the rim band and the yoke plate by two screws",
      elev=25, azim=-60, size=(8, 6))
    # 11 holder arm on the upright
    at = D["arm_top"]
    b = (740, 900, -50, 50, at - 90, at + 15)
    J(11, [part("Upright", win(C["uprights"].shape, *b), COL["uprights"]),
           part("Holder arm", win(C["arms"].shape, *b), COL["arms"]),
           part("Arm bracket", win(C["arm_brackets"].shape, *b), COL["arm_brackets"]),
           part("Axle plate (top)", win(C["axle_plates"].shape, *b), COL["axle_plates"]),
           part("M8 bolts", win(C["holder_bolts"].shape, *b), "#111827")],
      "holder arm on the upright (right side)", "The arm rests on the top of the upright and on the bracket's flat leg",
      elev=22, azim=-55, size=(8, 6))
    # 12 ring on the arm, handle on the ring, cut open
    b = (120, 260, -50, 50, at - 40, D["ring_top"] + 30)
    J(12, [part("Holder arm", win(C["arms"].shape, *b), COL["arms"]),
           part("Holder ring", win(C["ring"].shape, *b), COL["ring"]),
           part("Canner wall and handle", win(C["body"].shape, *b), COL["body"]),
           part("Jacket", win(C["jacket"].shape, *b), COL["jacket"]),
           part("M8 bolt", win(C["holder_bolts"].shape, *b), "#111827")],
      "canner handle on the holder ring (right side), cut open", "The handle rests on the ring; the jacket clears the ring by 5 mm",
      cut="+Y", elev=15, azim=-70, size=(8, 6))
    # 13 gnomon bracket on the rim (dish frame)
    g = rot_z(loc("gnomon"), -270)
    rimr = rot_z(loc("rim"), -270)
    pet = rot_z(loc("petals"), -270)
    b = (640, 840, -90, 90, zr0 - 25, zr0 + 220)
    J(13, [part("Rim band", rimr & M.bx(*b), COL["rim"]), part("Gnomon bracket, target and pin", g & M.bx(*b), COL["gnomon"]),
           part("Petal edge", pet & M.bx(*b), COL["petals"])],
      "gnomon on the rim band", "The pin is parallel to the dish axis; the pin's shadow on the target shows the aim",
      elev=25, azim=-140, size=(8, 6))
    # 14 logger box and thermocouple
    b = (850, 940, -60, 60, P["LOGGER_Z"] - 20, P["LOGGER_Z"] + 230)
    J(14, [part("Upright", win(C["uprights"].shape, *b), COL["uprights"]),
           part("Logger box (IP65)", win(C["logger_box"].shape, *b), COL["logger_box"]),
           part("Power bank inside", win(C["power_bank"].shape, *b), COL["power_bank"]),
           part("Logger board", win(C["logger_board"].shape, *b), COL["logger_board"]),
           part("Lock stud head", win(C["lock_studs"].shape, *b), COL["lock_studs"]),
           part("Sensor cable", win(C["cable"].shape, *b), "#111827")],
      "logger box on the right upright, cut open", "Two screws through the back of the box into the upright, below the lock stud",
      cut="+Y", elev=20, azim=-30, size=(8, 6))
    return out


# ----------------------------------------------------------------- steps
def steps(which=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if which and str(n) not in which:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        print("step", n, flush=True)

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    g = lambda k, name=None: cp(k, name)  # noqa: E731
    base = [g("cross_rails"), g("castors")]
    st(1, [g("cross_rails", "Cross rails, upside down on the floor")], [mv(g("castors", "Castors (4)"), (0, 0, -150))],
       "castors onto the cross rails", "Rails upside down; each castor on four M8 bolts, nuts on the rail; brake pedals outward",
       elev=-25, azim=-60)
    st(2, base, [mv(g("side_rails", "Side rails (2)"), (0, 0, 180))], "side rails across the cross rails",
       "Rails right way up; each side rail across both ends; two M8 bolts at each crossing, drilled through both",
       elev=25, azim=-55, label_done=False)
    frame = base + [g("side_rails")]
    st(3, frame, [mv(g("uprights", "Uprights (2)"), (0, 0, 300)), mv(g("foot_brackets", "Foot brackets (4)"), (0, 0, 150))],
       "uprights onto the side rails", "Upright on the middle of each side rail; brackets front and back; held plumb by a helper",
       elev=22, azim=-55, label_done=False)
    frame = frame + [g("uprights"), g("foot_brackets")]
    st(4, frame, [mv(g("braces", "Braces (4)"), (0, 0, 120))], "braces",
       "Front braces on the outer faces, back braces on the inner faces; one M10 through both at the top, one at each foot",
       elev=20, azim=-50, label_done=False)
    frame = frame + [g("braces")]
    apl = kids("axle_plates")
    left_plate = [k for k in apl if k.bounding_box().center().X < 0][0]
    right_plate = [k for k in apl if k.bounding_box().center().X > 0][0]
    st(5, frame, [mv(part("Left axle plate", left_plate, COL["axle_plates"]), (250, 0, 0))], "left axle plate",
       "On the inner face of the left upright, M10 bolt at the top; the stud hole and axle hole line up with the upright",
       elev=20, azim=-35, label_done=False)
    # dish build on the floor, face up (dish frame, no tilt)
    dl = lambda k: L[k][1]  # noqa: E731
    pk = lambda k, name, col=None: part(name, dl(k), col or COL[k])  # noqa: E731
    st(6, [pk("hub", "Hub plate, on a level stand")], [mv(pk("ribs", "Ribs (12)"), (0, 0, 150)),
                                                     mv(pk("hub_clips", "Rib clips at the hub (12)"), (0, 0, 60))],
       "ribs onto the hub plate", "Dish built face up on a level floor; each rib propped on its jig; one clip and two M5 bolts each",
       elev=35, azim=-60, label_done=True)
    st(7, [pk("hub", "Hub"), pk("ribs", "Ribs"), pk("hub_clips", "Clips")],
       [mv(pk("rim", "Rim band"), (0, 0, 200)), mv(pk("rim_clips", "Rim clips (12)"), (0, 0, 120))],
       "rim band onto the rib ends", "Rim band round the rib ends, joint strap at a rib; each rib end held by a clip",
       elev=35, azim=-60, label_done=False)
    frame_d = [pk("hub", "Hub"), pk("ribs", "Ribs"), pk("hub_clips", "Clips"), pk("rim", "Rim"), pk("rim_clips", "Clips")]
    st(8, frame_d, [mv(part("Petals with their flanges and tabs (12)", CF([dl("petals"), dl("flanges"), dl("tabs")]), COL["petals"]), (0, 0, 250))],
       "petals onto the ribs", "Opposite petals first; flanges outside the ribs; rivet every 50 mm; tabs riveted inside the rim band",
       elev=35, azim=-60, label_done=False)
    dish_d = frame_d + [part("Petals", CF([dl("petals"), dl("flanges"), dl("tabs")]), "#D1D5DB")]
    st(9, dish_d, [mv(pk("gnomon", "Gnomon on its bracket"), (0, -150, 80))], "gnomon onto the rim band",
       "Midway between two ribs; two M6 bolts through the band; the pin parallel to the dish axis",
       elev=30, azim=-60, label_done=False)
    dish_d = dish_d + [pk("gnomon", "Gnomon")]
    st(10, dish_d, [mv(pk("standoffs", "Rim stand-offs (2)"), (0, 0, 0)),
                    mv(part("Yoke plates (2)", dl("yoke_plates"), COL["yoke_plates"]), (0, 0, 0))],
       "stand-offs and yoke plates onto the rim band", "Opposite each other, 90 degrees from the gnomon; two M8 countersunk screws each, nuts inside",
       elev=25, azim=-40, label_done=False)
    # into the stand: dish lift unit, face up (elevation 90)
    C90 = M.build_components(P, elev=90)
    unit = CF([C90[k].shape for k in ("petals", "flanges", "tabs", "ribs", "hub", "rim", "hub_clips", "rim_clips", "gnomon",
                                         "yoke_plates", "standoffs", "standoff_screws")])
    st(11, frame + [part("Left axle plate", left_plate, "#D1D5DB")], [mv(part("Dish lift unit, face up", unit, COL["petals"]), (0, 0, 650))],
       "dish into the stand", "Two people lower it from above, face up, until the yoke plates' axle holes line up with the uprights",
       elev=22, azim=-55, label_done=False)
    unit_p = part("Dish", unit, "#D1D5DB")
    st(12, frame + [part("Left axle plate", left_plate, "#D1D5DB"), unit_p], [mv(part("Right axle plate", right_plate, COL["axle_plates"]), (0, 0, 300))],
       "right axle plate", "Slid down between the yoke plate and the right upright; M10 bolt at the top",
       elev=22, azim=-35, label_done=False)
    piv = CF([C90[k].shape for k in ("axles", "collars", "thrust_washers")])
    frame2 = frame + [g("axle_plates"), unit_p]
    def sides(shape):
        import build123d as bb
        sol = list(shape.solids())
        L_ = bb.Compound([x for x in sol if x.center().X < 0]); R_ = bb.Compound([x for x in sol if x.center().X > 0])
        return L_, R_
    pl_, pr_ = sides(piv)
    st(13, frame2, [mv(part("Left axle, washer, collars", pl_, COL["axles"]), (-220, 0, 0)),
                    mv(part("Right axle, washer, collars", pr_, COL["axles"]), (220, 0, 0))],
       "axles, thrust washers and collars", "Each axle pushed in from outside through the upright, plate, washer and yoke plate; grease; collars set",
       elev=18, azim=-30, label_done=False)
    sl_, sr_ = sides(C["lock_studs"].shape)
    pl2, pr2 = sides(C["drop_pins"].shape)
    st(14, frame2 + [part("Axles", piv, "#D1D5DB")], [mv(part("Left lock stud, spacer, star knob", sl_, COL["lock_studs"]), (-200, 0, 0)),
                                                       mv(part("Right lock stud, spacer, star knob", sr_, COL["lock_studs"]), (200, 0, 0)),
                                                       mv(part("Left drop pin on its lanyard", pl2, COL["drop_pins"]), (-320, 0, -60)),
                                                       mv(part("Right drop pin on its lanyard", pr2, COL["drop_pins"]), (320, 0, -60))],
       "lock studs, star knobs and drop pins", "Studs in from outside through upright, plate and slot; then each drop pin in from outside through the hole that shows in the plate slot",
       elev=18, azim=-30, label_done=False)
    frame3 = frame2 + [part("Axles", piv, "#D1D5DB"), g("lock_studs"), g("drop_pins")]
    st(15, frame3, [mv(part("Holder arms and brackets", S("arms", "arm_brackets"), COL["arms"]), (0, 0, 220))],
       "holder arms", "Brackets on the inner faces of the uprights, then each arm on the upright's top and its bracket; M8 bolts",
       elev=22, azim=-50, label_done=False)
    frame4 = frame3 + [part("Arms", S("arms", "arm_brackets"), "#D1D5DB")]
    st(16, frame4, [mv(g("ring", "Holder ring"), (0, 0, 200))], "holder ring",
       "On the inner ends of both arms; one M8 bolt into each arm", elev=25, azim=-50, label_done=False)
    frame5 = frame4 + [g("ring")]
    st(17, frame5, [mv(part("Logger box with power bank and board", S("logger_box", "power_bank", "logger_board"), COL["logger_box"]), (200, 0, 0))],
       "logger box", "On the outer face of the right upright, below the lock stud; two screws through the back of the box",
       elev=18, azim=-30, label_done=False)
    frame6 = frame5 + [part("Logger", S("logger_box", "power_bank", "logger_board"), "#D1D5DB")]
    st(18, frame6, [mv(part("Canner with jacket, thermocouple, water and basket", S("body", "jacket", "thermocouple", "water", "basket"), COL["body"]), (0, 0, 350))],
       "canner into the holder ring", "Lowered straight down through the ring until both handles rest on it; dish turned away from the sun",
       elev=25, azim=-55, label_done=False)
    frame7 = frame6 + [part("Canner", S("body", "jacket", "thermocouple"), "#D1D5DB")]
    st(19, frame7, [mv(part("Lid with its factory gauge and relief valve", S("lid", "gauge", "relief"), COL["lid"]), (0, 0, 220)),
                    mv(part("Adapter plate with probe gland and transducer", S("adapter", "gland", "transducer"), COL["adapter"]), (0, 0, 220)),
                    mv(g("cable", "Sensor cable"), (0, 0, 0))],
       "lid, adapter plate and sensor cable", "Adapter plate on the lid's vent-pipe hole, maker's vent pipe on top; lid closed as the maker says; cable plugged in",
       elev=25, azim=-55, label_done=False)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps}
    what = [a for a in args if a in fns]
    nums = [a for a in args if a not in fns]
    for w in what:
        r = fns[w](nums) if w in ("sheets", "joints", "steps") else fns[w]()
        print(w, "->", r if not isinstance(r, list) else len(r))
