"""SunClave product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a 1.4 m dish of 12 polished aluminum petals with
visible petal seams, rivet rows over the ribs and a hub cap; painted steel ribs, rim and hub; the
sighting gnomon with its target rings; the tilt yoke with bearing collars, a slotted quadrant with
tick marks and the lock lever and knob; the treated timber stand with rounded arrises, carriage
bolts, steel bearing blocks and four locking castors with teal brake pedals; the level pot holder;
the 12 L aluminum cooker with its blackened base band, black handle grips, aluminized jacket with
stitched seams and straps, lid with gasket line, handle and weighted regulator; the pressure gauge
with dial, ticks, red zone, needle and clear glass; the brass relief valve and lid gland; the
pressure transducer on the tee; the logger enclosure with an OLED readout, buttons, a lit green
PASS light, a teal name band and cable glands; and the cable from the logger to the lid. Inside
the cooker: water charge, stainless basket on its trivet and a wrapped instrument pack. Inside the
logger enclosure: the logger board and the USB power bank. Context is a compact paved ground patch.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research and educational prototype, not a medical device.

Every main dimension and interface comes from PARAMS, derived(), dish_local(), to_world(),
point_world() and build_parts() in model.py. Axes as model.py: Z up, ground at Z = 0, tilt axis
along X through the focal point, sun toward -Y at SUN_ELEV. Differences from model.py (the logger
enclosure drawn tall enough to hold the power bank, and the pressure transducer shown on the tee)
are recorded in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, dish_local, to_world, point_world, tilt_of, _para

TITLE = "SunClave: solar steam sterilizer with a cycle logger"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); petal dish tilted to a "
             "sun 50 deg high, pressure cooker held level at its focus, logger with the green PASS light on "
             "the right upright"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): reflector petals, ribs "
             "and rim, gnomon, tilt yoke and quadrant lock, timber stand and castors, pot holder, cooker, "
             "jacket, basket, lid, gauge, relief valve, probe gland and transducer, logger and power bank"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 22, "az": -48,
     "note": "Detail from the front right and above (about 22 deg elevation): pressure cooker at the focus "
             "on its level holder ring, with the blackened base band, jacket, gauge, relief valve, weighted "
             "regulator, probe gland and transducer; dish and stand not shown"},
]

# Colours (restrained product palette; kit accent)
C_REFL = "#DCE1E6"       # polished aluminum petals
C_HUBCAP = "#9EA5AD"
C_STEEL = "#3A3F46"      # painted steel ribs, rim, yoke, holder
C_BLOCK = "#4B5159"
C_ZINC = "#B8BEC6"
C_TIMBER = "#B8895A"
C_ALU = "#C9CED4"        # cooker aluminum
C_BLACKBAND = "#1D1F23"  # high-temperature matte black
C_GRIP = "#1C1F24"
C_JACKET = "#C4C8CC"     # aluminized glass cloth
C_STRAP = "#2B2F36"
C_ACCENT = "#0F766E"
C_BRASS = "#C9A227"
C_STAINLESS = "#B3B9C0"
C_DIAL = "#F4F4F2"
C_INK = "#2B2F36"
C_RED = "#B42318"
C_GLASS = "#DCEBF5"
C_SHELL = "#E9EAEC"
C_SHELL2 = "#C9CDD3"
C_DARK = "#2B2F36"
C_BLACK = "#16181C"
C_OLED = "#5EEAD4"
C_LED_G = "#22C55E"
C_LED_R = "#5E1C1C"
C_PCB = "#166534"
C_CHIP = "#111827"
C_BANK = "#30343A"
C_WATER = "#CFE6F2"
C_WRAP = "#7FA39B"       # instrument wrap
C_WHITE = "#F2F2EF"
C_GROUND = "#D9D5CC"
C_GROUND2 = "#CFCAC0"

# Logger enclosure drawn tall enough to hold the power bank (see docs/REVIEW.md)
LOGGER_Z0 = 862.0


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z0, r, h):
    """Z cylinder from z0 up by h (h may be negative)."""
    return Pos(x, y, z0 + h / 2) * Cylinder(r, abs(h))


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _seg(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        s = _seg(a, c, r)
        out = s if out is None else out + s
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _bar_f(a, b, w, t, side=(1, 0, 0), r=4.0):
    """Rectangular timber or steel bar from a to b (as model._bar), long edges rounded."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    x = d.normalized()
    s = Vector(*side)
    s = (s - x * s.dot(x)).normalized()
    z = x.cross(s)
    bx = Box(d.length, w, t)
    bx = _fillet_try(bx, bx.edges().filter_by(Axis.X), [r, r / 2])
    return Plane(origin=a + d * 0.5, x_dir=x, z_dir=z) * bx


def _hex_z(x, y, z0, af, h):
    return Pos(x, y, z0) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, h, sgn=1):
    """Hex prism along X starting at x, extruded toward sgn*X."""
    pl = Plane(origin=(x, y, z), x_dir=(0, 1, 0), z_dir=(sgn, 0, 0))
    return extrude(pl * RegularPolygon(af / 1.732, 6), amount=h)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def product_parts(P=PARAMS):
    D = derived(P)
    R, f, FZ = D["R"], P["FOCAL"], P["F_Z"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    W = lambda s: to_world(s, P)                         # dish frame to world (as model.py)

    # ============================================================ dish (BOM 1, 2, 16)
    reflector, frame, gnomon = dish_local(P)
    t = P["REFL_T_MODEL"]
    seams = None
    for k in range(P["N_PETALS"] // 2):
        a = 180.0 * k / (P["N_PETALS"] // 2)
        slab = Rot(0, 0, a) * Pos(0, 0, D["depth"] / 2) * Box(2 * R + 60, 2.4, D["depth"] + 60)
        seams = slab if seams is None else seams + slab
    petals = reflector - seams - _zcyl(0, 0, -20, P["HUB_R0"] - 10, 60)
    tt = math.radians(tilt_of(P["SUN_ELEV"]))
    ax = (0.0, -math.sin(tt), math.cos(tt))              # dish axis in the world

    def radial(phi, dist, lift=0.0):
        """World explode offset: `dist` outward along the local direction phi, plus `lift` along the axis."""
        c, s_ = math.cos(phi), math.sin(phi)
        return (dist * c, dist * s_ * math.cos(tt) + lift * ax[1], dist * s_ * math.sin(tt) + lift * ax[2])

    # rivets pair up along each seam; each rivet goes with the petal it is set in
    rv_by_petal = {k: [] for k in range(P["N_PETALS"])}
    n = P["N_PETALS"]
    for k in range(n):
        a = 2 * math.pi * k / n
        for rr in (140, 250, 360, 470, 580, 675):
            for side in (-1, 1):
                off = side * 9.0
                x = rr * math.cos(a) - off * math.sin(a)
                y = rr * math.sin(a) + off * math.cos(a)
                rv = Pos(x, y, _para(rr, f) - 1.2) * Sphere(3.4)
                rv_by_petal[k if side > 0 else (k - 1) % n].append(rv & Pos(x, y, _para(rr, f) + 5) * Box(10, 10, 10))
    sols = sorted(petals.solids(), key=lambda q: math.atan2(q.center().Y, q.center().X) % (2 * math.pi))
    for i, sol in enumerate(sols):
        phi = math.atan2(sol.center().Y, sol.center().X)
        k = int(round((phi % (2 * math.pi)) / (2 * math.pi / n) - 0.5)) % n
        ex = radial(phi, 230.0, 60.0)
        add(f"Reflector petal {i + 1} (aluminum)", W(sol), C_REFL, "metal", 1, "shell", ex)
        add(f"Petal {i + 1} rivets", W(Compound(rv_by_petal[k])), C_ZINC, "metal", 2, "shell", ex)

    E_HUB = radial(0.0, 0.0, 160.0)
    hubcap = _zcyl(0, 0, -2, P["HUB_R0"] - 4, 7)
    hubcap = _fillet_try(hubcap, _top(hubcap), [3.0, 2.0])
    add("Petal hub cap", W(hubcap), C_HUBCAP, "metal", 2, "shell", E_HUB)
    hb = []
    for k in range(6):
        a = 2 * math.pi * (k + 0.5) / 6
        hb.append(_zcyl(48 * math.cos(a), 48 * math.sin(a), 5, 5.0, 3.0))
    add("Hub cap bolts", W(Compound(hb)), C_ZINC, "metal", 17, "shell", radial(0.0, 0.0, 220.0))

    add("Dish ribs, rim and hub (painted steel)", W(frame), C_STEEL, "painted", 2, "shell", (0, 0, 0))
    E_GN = radial(-math.pi / 2, 300.0, 200.0)

    # gnomon: target plate with rings, pin parallel to the axis (as model.py)
    gy = -(R - 60)
    gz = _para(R - 60, f)
    plate = Pos(0, gy, gz + 2) * Box(120, 120, 4)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Z), [6.0, 4.0])
    add("Gnomon target plate", W(plate), C_WHITE, "painted", 16, "shell", E_GN)
    rings = (_zcyl(0, gy, gz + 4, 36, 0.6) - _zcyl(0, gy, gz + 3, 32, 3)) \
        + (_zcyl(0, gy, gz + 4, 20, 0.6) - _zcyl(0, gy, gz + 3, 17.5, 3))
    add("Gnomon target rings", W(rings), C_ACCENT, "painted", 16, "shell", E_GN)
    pin = _zcyl(0, gy, gz + 4, 4, 180)
    pin = _fillet_try(pin, _top(pin), [2.0, 1.0])
    pin += _zcyl(0, gy, gz + 4, 9, 6)
    add("Gnomon pin", W(pin), C_STAINLESS, "metal", 16, "shell", E_GN)

    # ============================================================ yoke and quadrant lock (BOM 3)
    E_YOKE = (0, 0, 0)
    xb = P["UPR_X"] - P["UPR_W"] / 2 - 40
    rim_pt = point_world((R + P["RIM_T"] + 12, 0, _para(R, f) - P["RIM_W"] / 2), P)
    arms, collars = [], []
    for s in (-1, 1):
        a = (s * xb, 0, FZ)
        b = (s * rim_pt[0], rim_pt[1], rim_pt[2])
        arms.append(_seg(a, b, P["YOKE_R"]))
        arms.append(Pos(*b) * Sphere(P["YOKE_R"] + 2))
        c = _seg((s * (xb - 5), 0, FZ), (s * (xb + 40), 0, FZ), 20)
        collars.append(c)
        collars.append(_seg((s * (xb + 12), 0, FZ), (s * (xb + 12), 0, FZ + 26), 4.5))   # grease nipple boss
    add("Tilt yoke arms", Compound(arms), C_STEEL, "painted", 3, "shell", E_YOKE)
    add("Yoke bearing collars", Compound(collars), C_ZINC, "metal", 3, "shell", E_YOKE)
    tq = math.radians(tilt_of(P["SUN_ELEV"]))
    lever = (-xb - 20, 0.8 * P["QUAD_R"] * math.sin(tq), FZ - 0.8 * P["QUAD_R"] * math.cos(tq))
    add("Quadrant lock lever", _seg((-xb - 20, 0, FZ), lever, 8), C_ZINC, "metal", 3, "shell", E_YOKE)
    knob = Pos(*lever) * Rot(0, 90, 0) * Cylinder(14, 30)
    knob = _fillet_try(knob, knob.edges(), [4.0, 2.5])
    for k in range(10):
        a = 2 * math.pi * k / 10
        knob -= _xcyl(lever[0], lever[1] + 14.5 * math.cos(a), lever[2] + 14.5 * math.sin(a), 1.6, 20)
    add("Quadrant lock knob", knob, C_BLACK, "rubber", 3, "shell", E_YOKE)

    # ============================================================ timber stand (BOM 4)
    E_STAND = (0, 0, -650)
    BX, BY = D["base_x"], P["BASE_Y"]
    zc = P["CASTOR_D"] + 5
    rw, rh = P["RAIL_W"], P["RAIL_H"]
    ztop = FZ + P["HOLDER_Z"] + 20
    timber = []
    for s in (-1, 1):
        timber.append(_bar_f((-BX / 2, s * (BY / 2 - rw / 2), zc + rh / 2), (BX / 2, s * (BY / 2 - rw / 2), zc + rh / 2),
                             rw, rh, side=(0, 1, 0)))
        timber.append(_bar_f((s * P["UPR_X"], -(BY / 2 - rw), zc + rh / 2), (s * P["UPR_X"], BY / 2 - rw, zc + rh / 2),
                             rw, rh, side=(1, 0, 0)))
    for s in (-1, 1):
        x = s * P["UPR_X"]
        timber.append(_bar_f((x, 0, zc + rh), (x, 0, ztop), P["UPR_W"], P["UPR_D"], side=(1, 0, 0), r=5.0))
        for sy in (-1, 1):
            timber.append(_bar_f((x, sy * (BY / 2 - rw), zc + rh), (x, sy * P["UPR_D"] / 2, P["BRACE_Z"]),
                                 P["BRACE_W"], P["BRACE_T"], side=(1, 0, 0), r=4.0))
    add("Timber stand frame (treated timber)", Compound(timber), C_TIMBER, "wood", 4, "shell", E_STAND)

    # carriage bolts on the outer faces of the uprights and rails
    cb = []
    for s in (-1, 1):
        xo = s * (P["UPR_X"] + P["UPR_W"] / 2)
        for (y, z) in [(-12, zc + rh + 300), (12, zc + rh + 330), (0, P["BRACE_Z"] - 25)]:
            d = _xcyl(xo + s * 1.5, y, z, 7.5, 3.0)
            cb.append(d)
        for sy in (-1, 1):
            yo = sy * BY / 2
            for x in (s * (P["UPR_X"] - 18), s * (P["UPR_X"] + 18)):
                cb.append(_ycyl(x, yo + sy * 1.5, zc + rh / 2, 7.5, 3.0))
    add("Carriage bolts", Compound(cb), C_ZINC, "metal", 17, "shell", E_STAND)

    # steel bearing blocks with stub axles; bolt heads on the outer upright faces
    bk, bolts = [], []
    for s in (-1, 1):
        blk = Box(40, 80, 90)
        blk = _fillet_try(blk, blk.edges().filter_by(Axis.X), [6.0, 4.0])
        bk.append(Pos(s * (P["UPR_X"] - P["UPR_W"] / 2 - 20), 0, FZ) * blk)
        xo = s * (P["UPR_X"] + P["UPR_W"] / 2)
        for y in (-18, 18):
            for z in (-30, 30):
                bolts.append(_hex_x(xo, y, FZ + z, 13.0, 6.0, s))
        bolts.append(_xcyl(xo + s * 5, 0, FZ, 12.5, 10))                # axle end cap
    add("Bearing blocks (painted steel)", Compound(bk), C_BLOCK, "painted", 4, "shell", E_STAND)
    add("Bearing block bolts and axle caps", Compound(bolts), C_ZINC, "metal", 4, "shell", E_STAND)

    # slotted quadrant plate on the -X upright, with tick marks
    qx = -xb - 26
    quad = _xcyl(qx, 0, FZ, P["QUAD_R"], P["QUAD_T"]) - _box(qx, 0, FZ + P["QUAD_R"] / 2 + 10, 20,
                                                              2 * P["QUAD_R"] + 10, P["QUAD_R"] + 10)
    slot = (_xcyl(qx, 0, FZ, 0.8 * P["QUAD_R"] + 9, 20) - _xcyl(qx, 0, FZ, 0.8 * P["QUAD_R"] - 9, 22)) \
        & _box(qx, 0, FZ - 90, 20, 2 * P["QUAD_R"] - 60, 150)
    quad -= slot
    add("Quadrant plate (slotted)", quad, C_BLOCK, "painted", 4, "shell", E_STAND)
    ticks = []
    for k in range(9):
        a = math.radians(-80 + 20 * k)
        r0, r1 = 0.8 * P["QUAD_R"] + 14, P["QUAD_R"] - 6 if k % 2 == 0 else P["QUAD_R"] - 14
        mid = (r0 + r1) / 2
        ticks.append(Pos(qx + P["QUAD_T"] / 2 + 0.3, mid * math.sin(a), FZ - mid * math.cos(a)) * Rot(-math.degrees(a), 0, 0)
                     * Box(0.6, 3.0, r1 - r0))
    add("Quadrant tick marks", Compound(ticks), C_WHITE, "painted", 4, "shell", E_STAND)

    # four locking castors (all lock, SCL-DDR-002)
    wheels, forks, pedals = [], [], []
    cr = P["CASTOR_D"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * (BX / 2 - 60), sy * (BY / 2 - 60)
            wh = _xcyl(cx, cy, cr, cr, 25)
            wh = _fillet_try(wh, wh.edges(), [5.0, 3.0])
            wheels.append(wh)
            fk = _box(cx, cy, P["CASTOR_D"] + 2, 60, 60, 6)
            fk = _fillet_try(fk, fk.edges().filter_by(Axis.Z), [6.0, 3.0])
            fk += _zcyl(cx, cy, P["CASTOR_D"] - 12, 20, 13)
            for s2 in (-1, 1):
                fk += _box(cx + s2 * 16, cy, cr + 18, 3, 34, 44)
            fk += _xcyl(cx, cy, cr, 8, 40)
            forks.append(fk)
            pd = _box(cx, cy + sy * (cr + 12), 0.7 * P["CASTOR_D"], 24, 30, 8)
            pd = _fillet_try(pd, pd.edges().filter_by(Axis.Y), [2.5, 1.5])
            pedals.append(pd)
    add("Castor wheels", Compound(wheels), C_BLACK, "rubber", 4, "shell", E_STAND)
    add("Castor forks and plates", Compound(forks), C_ZINC, "metal", 4, "shell", E_STAND)
    add("Castor brake pedals", Compound(pedals), C_ACCENT, "painted", 4, "shell", E_STAND)

    # ============================================================ level pot holder (BOM 5)
    ro = D["pot_or"]
    zr = FZ + P["HOLDER_Z"]
    ring = _zcyl(0, 0, zr - P["HOLDER_W"], ro + 30, P["HOLDER_W"]) - _zcyl(0, 0, zr - P["HOLDER_W"] - 1, ro + 2,
                                                                          P["HOLDER_W"] + 2)
    add("Pot holder ring", ring, C_STEEL, "painted", 5, "internal", (0, 0, 0))
    harms = []
    for s in (-1, 1):
        harms.append(_bar_f((s * (ro + 28), 0, zr - P["HOLDER_W"] / 2),
                            (s * (P["UPR_X"] - P["UPR_W"] / 2), 0, zr - P["HOLDER_W"] / 2),
                            P["HOLDER_W"], P["HOLDER_W"], side=(0, 1, 0), r=2.5))
        harms.append(_hex_x(s * (P["UPR_X"] + P["UPR_W"] / 2), 0, zr - P["HOLDER_W"] / 2, 13.0, 6.0, s))
    add("Pot holder arms", Compound(harms), C_STEEL, "painted", 5, "shell", (0, 0, 0))

    # ============================================================ cooker (BOM 6, 7, 11)
    VX = -1350.0                                         # exploded view: vessel stack beside the dish
    E_POT = (VX, 0, 20)
    ih, wall, bt = P["POT_IH"], P["POT_WALL"], P["POT_BASE"]
    oh = D["pot_oh"]
    body = _zcyl(0, 0, FZ, ro, oh)
    body = _fillet_try(body, _bottom(body), [8.0, 5.0])
    body -= _zcyl(0, 0, FZ + bt, P["POT_ID"] / 2, ih + 1)
    rim = _zcyl(0, 0, FZ + oh - 6, ro + 3, 6) - _zcyl(0, 0, FZ + oh - 7, ro - 1, 8)
    body += rim
    add("Pressure cooker body, 12 L (aluminum)", body, C_ALU, "metal", 6, "internal", E_POT)
    band = _zcyl(0, 0, FZ - 0.6, ro + 0.6, P["BARE_BAND"] + 0.6) - _zcyl(0, 0, FZ + 0.5, ro - 0.2, P["BARE_BAND"] + 2)
    band = _fillet_try(band, _bottom(band), [8.0, 5.0])
    add("Blackened base and wall band", band, C_BLACKBAND, "painted", 6, "internal", E_POT)

    # body handles: brackets and black grips, same span and height as model.py
    hz = FZ + oh - 20
    brk = [_box(s * (ro + 12), 0, hz, 28, 40, 16) for s in (-1, 1)]
    add("Body handle brackets", Compound(brk), C_STAINLESS, "metal", 6, "internal", E_POT)
    grips = []
    for s in (-1, 1):
        g = _box(s * (ro + 53), 0, hz, 64, 36, 18)
        g = _fillet_try(g, g.edges(), [7.0, 5.0, 3.0])
        grips.append(g)
    add("Body handle grips (phenolic)", Compound(grips), C_GRIP, "plastic", 6, "internal", E_POT)

    # insulated jacket with stitched seams and two straps
    zj = FZ + P["BARE_BAND"]
    hj = oh - P["BARE_BAND"] - 30
    jor = D["jkt_or"]
    jk = _zcyl(0, 0, zj, jor, hj)
    jk = _fillet_try(jk, list(_top(jk)) + list(_bottom(jk)), [8.0, 5.0])
    jk -= _zcyl(0, 0, zj - 1, ro + 0.5, hj + 2)
    for dz in (12, hj - 12):
        jk -= _zcyl(0, 0, zj + dz - 0.4, jor + 2, 0.8) - _zcyl(0, 0, zj + dz - 1, jor - 1.2, 2)
    jk -= _box(0, -jor, zj + hj / 2, 1.2, 4, hj - 30)                # vertical closure seam
    add("Insulated jacket (aluminized cloth)", jk, C_JACKET, "fabric", 11, "internal", (VX, 0, -200))
    straps = []
    for dz in (hj * 0.32, hj * 0.68):
        straps.append(_zcyl(0, 0, zj + dz - 9, jor + 1.2, 18) - _zcyl(0, 0, zj + dz - 10, jor - 0.5, 20))
    add("Jacket straps", Compound(straps), C_STRAP, "fabric", 11, "internal", (VX, 0, -200))
    buck = [_box(0, -jor - 2.5, zj + dz, 22, 3, 22) - _box(0, -jor - 3.5, zj + dz, 14, 3, 12)
            for dz in (hj * 0.32, hj * 0.68)]
    add("Jacket strap buckles", Compound(buck), C_STAINLESS, "metal", 11, "internal", (VX, 0, -200))

    # lid with gasket line, handle and weighted regulator (as model.py)
    E_LID = (VX, 0, 420)
    zl = FZ + oh
    lid = _zcyl(0, 0, zl, P["LID_D"] / 2, P["LID_T"])
    lid = _fillet_try(lid, _top(lid), [2.5, 1.5])
    lid += _zcyl(0, 0, zl + P["LID_T"] - 1, 40, 13)
    lid = _fillet_try(lid, [e for e in _top(lid)], [3.0, 2.0])
    lid -= _zcyl(0, 0, zl + 1.2, P["LID_D"] / 2 + 2, 0.8) - _zcyl(0, 0, zl, P["LID_D"] / 2 - 1.2, 3)
    add("Lid (aluminum)", lid, C_ALU, "metal", 7, "internal", E_LID)
    zt = zl + P["LID_T"]
    lh = _box(0, ro + 60, zt + 8, 40, 110, 16)
    lh = _fillet_try(lh, lh.edges(), [6.0, 4.0, 2.0])
    add("Lid handle (phenolic)", lh, C_GRIP, "plastic", 7, "internal", E_LID)
    vent = _zcyl(0, 0, zt, 5, 40)
    add("Vent pipe", vent, C_STAINLESS, "metal", 7, "internal", E_LID)
    reg = _zcyl(0, 0, zt + 22, 16, 22)
    reg = _fillet_try(reg, _top(reg), [5.0, 3.0])
    reg += _zcyl(0, 0, zt + 44, 5, 8)
    reg = _fillet_try(reg, _top(reg), [2.0, 1.0])
    add("Weighted regulator", reg, C_STAINLESS, "metal", 7, "internal", (VX, 0, 580))

    # ============================================================ lid fittings (BOM 8 to 10)
    # pressure gauge, 100 mm dial facing -Y (as model.py)
    E_G = (VX, -60, 500)
    gx, gyy, gzz = 75, -55, zt + 95
    stem = _zcyl(gx, gyy, zt, 7, 45) + _hex_z(gx, gyy, zt + 6, 19, 10)
    add("Gauge stem and siphon fitting", stem, C_BRASS, "metal", 8, "internal", E_G)
    case = _ycyl(gx, gyy, gzz, 50, 30)
    case = _fillet_try(case, case.edges(), [4.0, 2.5])
    case -= _ycyl(gx, gyy - 15, gzz, 45, 6)
    case += _zcyl(gx, gyy, gzz - 56, 9, 12)
    add("Gauge case (stainless)", case, C_STAINLESS, "metal", 8, "internal", E_G)
    yf = gyy - 12.5
    add("Gauge dial", _ycyl(gx, yf, gzz, 45, 1.0), C_DIAL, "paper", 8, "internal", E_G)
    marks = []
    for k in range(13):
        a = math.radians(-135 + 22.5 * k)
        rr0 = 34 if k % 2 == 0 else 37
        mid = (rr0 + 41) / 2
        marks.append(Pos(gx + mid * math.sin(a), yf - 0.7, gzz + mid * math.cos(a)) * Rot(0, math.degrees(a), 0)
                     * Box(1.4 if k % 2 == 0 else 0.9, 0.4, 41 - rr0))
    add("Gauge scale marks", Compound(marks), C_INK, "paper", 8, "internal", E_G)
    rz = (_ycyl(gx, yf - 0.6, gzz, 41, 0.3) - _ycyl(gx, yf - 0.6, gzz, 37.5, 1)) \
        & (Pos(gx, yf, gzz) * Rot(0, 90 + 20, 0) * Pos(0, 0, 25) * Box(60, 10, 50))
    add("Gauge red zone", rz, C_RED, "painted", 8, "internal", E_G)
    ndl = Pos(gx, yf - 1.4, gzz) * Rot(0, -48, 0) * Pos(0, 0, 16) * Box(2.2, 0.6, 36) + _ycyl(gx, yf - 1.6, gzz, 3.5, 1.4)
    add("Gauge needle", ndl, C_BLACK, "plastic", 8, "internal", E_G)
    glass = _ycyl(gx, gyy - 16.5, gzz, 45, 1.5)
    add("Gauge glass", glass, C_GLASS, "clear", 8, "internal", (VX, -100, 500))

    # independent relief valve (brass)
    rv = _hex_z(-80, 40, zt, 22, 10) + _zcyl(-80, 40, zt + 10, 11, 30) + _zcyl(-80, 40, zt + 40, 17, 14)
    rv = _fillet_try(rv, _top(rv), [3.0, 2.0])
    rv += _zcyl(-80, 40, zt + 54, 4, 8)
    rv += Pos(-80, 40, zt + 66) * Rot(90, 0, 0) * (Cylinder(9, 3) - Cylinder(6, 4))
    add("Independent relief valve (brass)", rv, C_BRASS, "metal", 9, "internal", (VX, 0, 500))

    # lid gland, Pt100 probe and tee (as model.py), pressure transducer on the tee end
    px, py = P["PROBE_X"], P["PROBE_Y"]
    tip = FZ + bt + P["PROBE_TIP_Z"]
    gl = _hex_z(px, py, zt, 18, 8) + _zcyl(px, py, zt + 8, 9, 22)
    gl = _fillet_try(gl, _top(gl), [2.0, 1.0])
    gl += _seg((px, py, zt + 22), (px + 60, py, zt + 22), 5)
    gl += _hex_x(px + 52, py, zt + 22, 14, 10, 1)
    add("Lid gland and tee (brass)", gl, C_BRASS, "metal", 10, "internal", (VX, 0, 500))
    probe = _zcyl(px, py, tip, 1.5, zt + 30 - tip)
    add("Pt100 probe sheath", probe, C_STAINLESS, "metal", 10, "internal", (VX, 0, 500))
    tx = px + 60
    tr = _zcyl(tx, py, zt + 16, 11, 60)
    tr = _fillet_try(tr, _top(tr), [2.5, 1.5])
    tr += _hex_z(tx, py, zt + 10, 20, 8)
    add("Pressure transducer (stainless)", tr, C_STAINLESS, "metal", 14, "internal", (VX, 0, 540))
    tg = _hex_z(tx, py, zt + 76, 14, 5) + _zcyl(tx, py, zt + 81, 5.5, 8)
    add("Transducer connector", tg, C_DARK, "plastic", 14, "internal", (VX, 0, 540))

    # water, basket and trivet, wrapped instrument load (inside the cooker)
    wd = D["water_depth"]
    add("Water charge, 1.5 L", _zcyl(0, 0, FZ + bt, P["POT_ID"] / 2 - 0.5, wd), C_WATER, "clear", 12,
        "internal", (VX, 0, 20))
    rb = P["BASKET_D"] / 2
    zb = FZ + bt + P["TRIVET_H"]
    bsk = _zcyl(0, 0, zb, rb, P["BASKET_H"]) - _zcyl(0, 0, zb + 2, rb - 2, P["BASKET_H"])
    bsk += _zcyl(0, 0, zb - 5, rb + 5, 5) - _zcyl(0, 0, zb - 6, rb - 15, 7)
    for k in range(24):                                   # perforated wall (wire basket texture)
        a = 2 * math.pi * k / 24
        for z in (zb + 40, zb + 85):
            bsk -= Pos(rb * math.cos(a), rb * math.sin(a), z) * Rot(0, 90, math.degrees(a)) * Box(28, 16, 8)
    bsk += _zcyl(0, 0, zb + P["BASKET_H"] - 4, rb + 2, 4) - _zcyl(0, 0, zb + P["BASKET_H"] - 5, rb - 2, 6)
    for k in range(3):
        a = 2 * math.pi * k / 3
        bsk += _zcyl((rb - 10) * math.cos(a), (rb - 10) * math.sin(a), FZ + bt, 4, P["TRIVET_H"] - 5)
    add("Instrument basket and trivet (stainless)", bsk, C_STAINLESS, "metal", 13, "internal", (VX, 0, 220))
    pack = _box(-40, -20, zb + 2 + 30, 150, 110, 60)
    pack = _fillet_try(pack, pack.edges(), [10.0, 6.0, 3.0])
    add("Wrapped instrument pack (not in BOM)", pack, C_WRAP, "fabric", None, "internal", (VX, 0, 360))
    tape = _box(-40, -20, zb + 2 + 30, 152, 22, 62) - _box(-40, -20, zb + 2 + 30, 146, 30, 56)
    add("Indicator tape (not in BOM)", tape, C_WHITE, "paper", None, "internal", (VX, 0, 360))

    # ============================================================ cycle logger (BOM 14, 15)
    E_LOG = (420, 0, 0)
    lx = P["UPR_X"] + P["UPR_W"] / 2 + 30
    lz = FZ + 40
    ly = -40
    x0, x1 = lx - 30, lx + 30                              # 875 .. 935, as model.py
    z0, z1 = LOGGER_Z0, lz + 55                            # top at 1045 as model.py; bottom lowered for the bank
    zm = (z0 + z1) / 2
    bw, bh = 150.0, z1 - z0
    base_o = _box(lx - 6, ly, zm, 48, bw, bh)
    base_o = _fillet_try(base_o, base_o.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    base = base_o - _box(lx - 3, ly, zm, 48, bw - 6, bh - 6)
    for dz in (-60, -30, 0, 30, 60):                       # grip ribs on the sides
        for sy in (-1, 1):
            base -= _box(lx - 10, ly + sy * bw / 2, zm + dz, 30, 1.6, 2.0)
    add("Logger enclosure (IP65)", base, C_SHELL, "plastic", 14, "shell", E_LOG)
    lid_o = _box(x1 - 6, ly, zm, 12, bw, bh)
    lid_o = _fillet_try(lid_o, lid_o.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    lid_o = _fillet_try(lid_o, lid_o.faces().sort_by(Axis.X)[-1].edges(), [2.5, 1.5])
    lidl = lid_o - _box(x1 - 9, ly, zm, 12, bw - 6, bh - 6)
    add("Logger lid", lidl, C_SHELL2, "plastic", 14, "shell", (E_LOG[0] + 120, 0, 0))
    # lid screws
    ls = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            s = _xcyl(x1 + 0.6, ly + sy * (bw / 2 - 9), zm + sz * (bh / 2 - 9), 3.4, 1.2)
            s -= _box(x1 + 1.2, ly + sy * (bw / 2 - 9), zm + sz * (bh / 2 - 9), 1.0, 4.0, 0.8)
            ls.append(s)
    add("Logger lid screws", Compound(ls), C_ZINC, "metal", 17, "shell", (E_LOG[0] + 160, 0, 0))
    EP = (E_LOG[0] + 180, 0, 0)
    oz = z1 - 42
    bez = _box(x1 + 2, ly, oz, 4, 70, 40)
    bez = _fillet_try(bez, bez.edges().filter_by(Axis.X), [3.0, 2.0])
    bez -= _box(x1 + 4, ly, oz + 1, 1.0, 54, 28)
    add("OLED display bezel", bez, C_BLACK, "plastic", 14, "shell", EP)
    add("OLED display glass", _box(x1 + 3.3, ly, oz + 1, 0.6, 54, 28), "#0E1216", "screen", 14, "shell", EP)
    xr = x1 + 3.75
    readout = (_box(xr, ly + 8, oz + 6, 0.3, 30, 10) + _box(xr, ly - 17, oz + 8, 0.3, 12, 4)
               + _box(xr, ly - 17, oz + 3, 0.3, 12, 2) + _box(xr, ly, oz - 8, 0.3, 44, 2.5))
    add("OLED readout (lit)", readout, C_OLED, "emissive", 14, "shell", EP)
    bz_ = oz - 42
    bts = []
    for dy in (-24, 0):
        b = _xcyl(x1 + 2.5, ly + dy, bz_, 7.0, 5.0)
        b = _fillet_try(b, b.faces().sort_by(Axis.X)[-1].edges(), [1.5, 1.0])
        bts.append(b)
    add("Logger buttons", Compound(bts), C_ACCENT, "plastic", 14, "shell", EP)
    bzl = [_xcyl(x1 + 0.9, ly + dy, bz_, 9.0, 1.8) - _xcyl(x1 + 0.9, ly + dy, bz_, 7.4, 3.0) for dy in (-24, 0)]
    add("Logger button bezels", Compound(bzl), C_DARK, "plastic", 14, "shell", EP)
    for k, (col, mat, nm) in enumerate([(C_LED_G, "emissive", "PASS light, green (lit)"),
                                        (C_LED_R, "plastic", "FAIL light, red")]):
        yy = ly + 22 + 14 * k
        cap = (Pos(x1 + 1.2, yy, bz_) * Sphere(3.0)) & _box(x1 + 3.2, yy, bz_, 4.0, 8, 8)
        dome = _xcyl(x1 + 0.6, yy, bz_, 3.4, 1.2) + cap
        add(nm, dome, col, mat, 14, "shell", EP)
    grille = [_xcyl(x1 + 0.2, ly - 36 + 6 * k, bz_ - 22, 1.6, 0.4) for k in range(5)]
    add("Buzzer grille", Compound(grille), C_DARK, "plastic", 14, "shell", EP)
    band_ = _box(x1 + 0.2, ly, z0 + 20, 0.4, bw - 30, 7)
    add("Logger name band", band_, C_ACCENT, "painted", 14, "shell", EP)
    lab = _box(x1 + 0.2, ly, z0 + 44, 0.4, 70, 22)
    add("Logger rating label", lab, C_WHITE, "paper", 14, "shell", EP)
    ink = (_box(x1 + 0.45, ly - 18, z0 + 49, 0.3, 26, 5) + _box(x1 + 0.45, ly + 4, z0 + 42, 0.3, 50, 1.8)
           + _box(x1 + 0.45, ly, z0 + 37, 0.3, 58, 1.8))
    add("Logger label print", ink, C_INK, "paper", 14, "shell", EP)

    # cable glands: top (lid cable), bottom (base thermocouple and USB)
    gls = []
    for (y, z, sgn) in [(30, z1, 1), (ly - 30, z0, -1), (ly + 20, z0, -1)]:
        g = _hex_z(lx - 6, y, z if sgn > 0 else z - 5, 20, 5) + _zcyl(lx - 6, y, z + sgn * 5, 7.5, sgn * 7)
        gls.append(g)
    add("Logger cable glands", Compound(gls), C_DARK, "plastic", 17, "shell", (E_LOG[0], 0, 0))

    # mounting straps round the upright
    mb = [_box(P["UPR_X"] + 3, 0, z, P["UPR_W"] + 8, P["UPR_D"] + 6, 16) - _box(P["UPR_X"], 0, z, P["UPR_W"], P["UPR_D"], 20)
          for z in (z0 + 25, z1 - 25)]
    add("Logger mounting straps", Compound(mb), C_ZINC, "metal", 17, "shell", (0, 0, 0))

    # logger board and power bank inside the enclosure (exploded view only)
    EB = (E_LOG[0] + 60, 0, 0)
    pcb = _box(lx - 22, ly, z1 - 55, 1.6, 120, 80)
    add("Logger board", pcb, C_PCB, "plastic", 14, "accessory", EB)
    chips = (_box(lx - 17, ly - 20, z1 - 45, 8, 50, 26) + _box(lx - 18, ly + 30, z1 - 40, 6, 22, 18)
             + _box(lx - 18, ly + 30, z1 - 70, 6, 22, 16) + _box(lx - 18, ly - 30, z1 - 78, 4, 24, 12))
    add("Logger modules (ESP32, MAX31865, ADS1115, RTC)", chips, C_CHIP, "plastic", 14, "accessory", EB)
    sd = _box(lx - 18.5, ly + 2, z1 - 82, 3, 16, 14)
    add("microSD holder", sd, C_ZINC, "metal", 14, "accessory", EB)
    bank = _box(lx, ly, lz - 90, 50, 140, 60)            # as model.py
    bank = _fillet_try(bank, bank.edges().filter_by(Axis.X), [8.0, 5.0])
    add("USB power bank, 10,000 mAh", bank, C_BANK, "plastic", 15, "accessory", (E_LOG[0] + 60, 0, -170))

    # cable from the logger to the transducer on the lid (route as model.py)
    cz = zt + 120
    cable = _pipe([(lx - 6, 30, z1 + 12), (lx - 6, 30, cz - 30), (lx - 36, 30, cz), (tx + 30, py, cz),
                   (tx, py, cz - 30), (tx, py, zt + 89)], 3.0)
    add("Logger cable to the transducer", cable, C_BLACK, "rubber", 14, "shell", (0, 0, 0))

    # ============================================================ context: paved ground patch
    gx0, gx1 = -1030.0, 1080.0
    gy0, gy1 = -660.0, 790.0
    gnd = _box((gx0 + gx1) / 2, (gy0 + gy1) / 2, -20, gx1 - gx0, gy1 - gy0, 40)
    gnd = _fillet_try(gnd, _top(gnd), [6.0, 3.0])
    nx, ny = 4, 3
    for i in range(1, nx):
        x = gx0 + (gx1 - gx0) * i / nx
        gnd -= _box(x, (gy0 + gy1) / 2, 0, 6, gy1 - gy0 + 10, 6)
    for j in range(1, ny):
        y = gy0 + (gy1 - gy0) * j / ny
        gnd -= _box((gx0 + gx1) / 2, y, 0, gx1 - gx0 + 10, 6, 6)
    add("Paved ground patch", gnd, C_GROUND, "paper", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:48s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
