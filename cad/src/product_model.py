"""SunClave product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders, built on the constructable model (SCL-DDR-003) and the
decisions of 2026-10-02: a 1.4 m dish of 12 polished aluminium petals riveted to painted steel ribs,
rim band and hub plate, with a hub cap; the gnomon on its bracket on the rim band; the two 6 mm
yoke plates with their lock fans, drop pin holes and rim stand-offs; the treated timber stand (cross
rails, side rails on edge, uprights, lapped braces, foot brackets) with steel axle plates, axles,
collars, PTFE washers, lock studs with star knobs, drop pins on lanyards and four locking castors;
the fixed pot holder (plate ring, arms, brackets); the pressure canner of about 12 L with its
blackened base band, handles, aluminised jacket and straps; the lid with its weighted regulator,
overpressure plug, factory dial gauge and factory relief valve; the vent-stem adapter plate carrying
the Pt100 gland and the pressure transducer; the logger box with an OLED readout, buttons, a lit
green PASS light and a teal name band; and the cable from the logger to the transducer. Inside the
canner: water charge, stainless basket on its trivet and a wrapped instrument pack. Inside the
logger box: the logger board and the USB power bank. Context is a compact paved ground patch.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research and educational prototype, not a medical device.

Every part is either a component of cad/src/model.py (build_components, dish_components,
yoke_components) placed as there, or an appearance detail sized from PARAMS and derived():
the petal rivets and hub cap, the canner's rolled rim, black band and handle grips, the jacket
seams, the gauge dial face and the logger's display, buttons and labels. Axes as model.py: Z up,
ground at Z = 0, tilt axis along X through the focal point, sun toward -Y at SUN_ELEV.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived, dish_components, yoke_components, build_components, to_world, tilt_of, _para, rib_angles

TITLE = "SunClave: solar steam sterilizer with a cycle logger"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); petal dish tilted to a "
             "sun 50 deg high on its yoke plates, pressure canner held level at its focus on the fixed holder "
             "ring, logger with the green PASS light on the right upright"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): reflector petals, ribs, "
             "rim and hub, gnomon, yoke plates and stand-offs, timber stand with axle plates, locks, drop pins "
             "and castors, pot holder, canner, jacket, basket, lid with factory gauge and relief valve, "
             "vent-stem adapter plate with gland and transducer, logger and power bank"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 22, "az": -48,
     "note": "Detail from the front right and above (about 22 deg elevation): pressure canner at the focus "
             "on its level holder ring, with the blackened base band, jacket, factory gauge and relief valve, "
             "weighted regulator and the vent-stem adapter plate carrying the probe gland and transducer; "
             "dish and stand not shown"},
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
    C = build_components(P)                              # world placement, as model.py
    DC = dish_components(P)

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    def sh(key):
        return C[key].shape

    W = lambda s: to_world(s, P)                         # dish frame to world (as model.py)
    tt = math.radians(tilt_of(P["SUN_ELEV"]))
    ax = (0.0, -math.sin(tt), math.cos(tt))              # dish axis in the world

    def radial(phi, dist, lift=0.0):
        """World explode offset: `dist` outward along the local direction phi, plus `lift` along the axis."""
        c, s_ = math.cos(phi), math.sin(phi)
        return (dist * c, dist * s_ * math.cos(tt) + lift * ax[1], dist * s_ * math.sin(tt) + lift * ax[2])

    # ============================================================ dish (BOM 1, 2, 16)
    n = P["N_PETALS"]
    angs = rib_angles(P)
    sheet = DC["petals"][1]
    flanges = list(DC["flanges"][1].solids())
    tabs = list(DC["tabs"][1].solids())
    sols = sorted(sheet.solids(), key=lambda q: math.atan2(q.center().Y, q.center().X) % (2 * math.pi))
    for i, sol in enumerate(sols):
        phi = math.atan2(sol.center().Y, sol.center().X)
        a0 = math.radians(angs[0]) + 2 * math.pi * round(((phi - math.radians(angs[0])) % (2 * math.pi)) / (2 * math.pi / n) - 0.5) / n
        mine = [q for q in flanges + tabs
                if abs(((math.atan2(q.center().Y, q.center().X) - phi + math.pi) % (2 * math.pi)) - math.pi) < math.pi / n]
        ex = radial(phi, 230.0, 60.0)
        add(f"Reflector petal {i + 1} (aluminum)", W(Compound([sol] + mine)), C_REFL, "metal", 1, "shell", ex)
        rv = []
        for side, aa in ((1, a0), (-1, a0 + 2 * math.pi / n)):      # a rivet row along each rib the petal meets
            off = side * (P["RIB_T"] / 2 + 1.0 + 4.0)
            for rr in (140, 250, 360, 470, 580, 675):
                x = rr * math.cos(aa) - off * math.sin(aa)
                y = rr * math.sin(aa) + off * math.cos(aa)
                rv.append((Pos(x, y, _para(rr, f) - 1.2) * Sphere(3.0)) & Pos(x, y, _para(rr, f) + 5) * Box(10, 10, 10))
        add(f"Petal {i + 1} rivets", W(Compound(rv)), C_ZINC, "metal", 2, "shell", ex)

    E_HUB = radial(0.0, 0.0, 160.0)
    hubcap = _zcyl(0, 0, _para(P["HUB_R0"], f) - 2, P["HUB_R0"] + 6, 6)
    hubcap = _fillet_try(hubcap, _top(hubcap), [3.0, 2.0])
    add("Petal hub cap", W(hubcap), C_HUBCAP, "metal", 2, "shell", E_HUB)
    frame = Compound([DC[k][1] for k in ("ribs", "hub", "rim", "hub_clips", "rim_clips")])
    add("Dish ribs, rim band, hub plate and clips (painted steel)", W(frame), C_STEEL, "painted", 2, "shell", (0, 0, 0))
    E_GN = radial(-math.pi / 2, 300.0, 200.0)
    gparts = list(DC["gnomon"][1])                        # bracket, target plate, pin (model.py)
    add("Gnomon bracket", W(gparts[0]), C_STEEL, "painted", 16, "shell", E_GN)
    add("Gnomon target plate", W(gparts[1]), C_WHITE, "painted", 16, "shell", E_GN)
    add("Gnomon pin", W(gparts[2]), C_STAINLESS, "metal", 16, "shell", E_GN)

    # ============================================================ yoke plates and stand-offs (BOM 3)
    add("Yoke plates with lock fans and drop pin holes (painted steel)", sh("yoke_plates"), C_STEEL, "painted", 3, "shell", (0, 0, 0))
    add("Rim stand-offs (painted steel tube)", sh("standoffs"), C_STEEL, "painted", 3, "shell", (0, 0, 0))
    add("Stand-off screws", sh("standoff_screws"), C_ZINC, "metal", 17, "shell", (0, 0, 0))

    # ============================================================ timber stand, pivots and locks (BOM 3, 4)
    E_STAND = (0, 0, -650)
    add("Timber stand frame (treated timber)", Compound([sh(k) for k in ("cross_rails", "side_rails", "uprights", "braces")]),
        C_TIMBER, "wood", 4, "shell", E_STAND)
    add("Foot brackets (galvanised)", sh("foot_brackets"), C_ZINC, "metal", 4, "shell", E_STAND)
    add("Stand bolts", sh("stand_bolts"), C_ZINC, "metal", 17, "shell", E_STAND)
    add("Locking castors", sh("castors"), C_DARK, "rubber", 4, "shell", E_STAND)
    E_PIV = (0, 0, -330)
    add("Axle plates (painted steel)", sh("axle_plates"), C_BLOCK, "painted", 4, "shell", E_PIV)
    add("Axles, collars and plate bolts", Compound([sh("axles"), sh("collars"), sh("plate_bolts")]), C_ZINC, "metal", 4, "shell", E_PIV)
    add("PTFE thrust washers", sh("thrust_washers"), C_WHITE, "plastic", 4, "shell", E_PIV)
    add("Lock studs and star knobs", sh("lock_studs"), C_BLACK, "rubber", 3, "shell", E_PIV)
    add("Drop pins on lanyards", sh("drop_pins"), C_ACCENT, "metal", 3, "shell", E_PIV)

    # ============================================================ level pot holder (BOM 5)
    E_HOLD = (0, 0, -160)
    add("Pot holder ring (painted steel)", sh("ring"), C_STEEL, "painted", 5, "internal", E_HOLD)
    add("Pot holder arms and brackets", Compound([sh("arms"), sh("arm_brackets")]), C_STEEL, "painted", 5, "shell", E_HOLD)
    add("Holder bolts", sh("holder_bolts"), C_ZINC, "metal", 17, "shell", E_HOLD)

    # ============================================================ pressure canner (BOM 6, 7, 11)
    VX = -1350.0                                         # exploded view: vessel stack beside the dish
    E_POT = (VX, 0, 20)
    ro = D["pot_or"]
    ih, bt = P["POT_IH"], P["POT_BASE"]
    oh = D["pot_oh"]
    body = _zcyl(0, 0, FZ, ro, oh)
    body = _fillet_try(body, _bottom(body), [8.0, 5.0])
    body -= _zcyl(0, 0, FZ + bt, P["POT_ID"] / 2, ih + 1)
    body += _zcyl(0, 0, FZ + oh - 6, ro + 3, 6) - _zcyl(0, 0, FZ + oh - 7, ro - 1, 8)
    add("Pressure canner body, about 12 L (aluminum)", body, C_ALU, "metal", 6, "internal", E_POT)
    band = _zcyl(0, 0, FZ - 0.6, ro + 0.6, P["BARE_BAND"] + 0.6) - _zcyl(0, 0, FZ + 0.5, ro - 0.2, P["BARE_BAND"] + 2)
    band = _fillet_try(band, _bottom(band), [8.0, 5.0])
    add("Blackened base and wall band", band, C_BLACKBAND, "painted", 6, "internal", E_POT)
    hx, hw, ht, hd = P["HANDLE"]
    hz = FZ + oh - hd + ht / 2                           # handle underside on the ring, as model.py
    brk = [_box(s * (ro + 12), 0, hz, 28, hw, ht) for s in (-1, 1)]
    add("Canner handle brackets", Compound(brk), C_STAINLESS, "metal", 6, "internal", E_POT)
    grips = []
    for s in (-1, 1):
        g = _box(s * (ro + 26 + (hx - ro - 26) / 2), 0, hz, hx - ro - 26, hw - 4, ht)
        grips.append(_fillet_try(g, g.edges(), [6.0, 4.0, 2.0]))
    add("Canner handle grips (phenolic)", Compound(grips), C_GRIP, "plastic", 6, "internal", E_POT)
    add("Base thermocouple on its band clamp", sh("thermocouple"), C_STAINLESS, "metal", 14, "internal", E_POT)

    # insulated jacket with stitched seams and two straps
    zj = FZ + P["BARE_BAND"]
    hj = oh - P["BARE_BAND"] - 30
    jor = D["jkt_or"]
    jk = _zcyl(0, 0, zj, jor, hj)
    jk = _fillet_try(jk, list(_top(jk)) + list(_bottom(jk)), [8.0, 5.0])
    jk -= _zcyl(0, 0, zj - 1, ro + 0.5, hj + 2)
    for dz in (12, hj - 12):
        jk -= _zcyl(0, 0, zj + dz - 0.4, jor + 2, 0.8) - _zcyl(0, 0, zj + dz - 1, jor - 1.2, 2)
    jk -= _box(0, -jor, zj + hj / 2, 1.2, 4, hj - 30)    # vertical closure seam
    add("Insulated jacket (aluminized cloth)", jk, C_JACKET, "fabric", 11, "internal", (VX, 0, -200))
    straps = [_zcyl(0, 0, z, jor + 1.2, 20) - _zcyl(0, 0, z - 1, jor - 0.5, 22) for z in (zj + 12, zj + hj - 32)]
    add("Jacket straps", Compound(straps), C_STRAP, "fabric", 11, "internal", (VX, 0, -200))

    # lid with gasket line, handle, overpressure plug, vent pipe and weighted regulator (as model.py)
    E_LID = (VX, 0, 420)
    zl = FZ + oh
    zt = zl + P["LID_T"]
    lid = _zcyl(0, 0, zl, P["LID_D"] / 2, P["LID_T"])
    lid = _fillet_try(lid, _top(lid), [2.5, 1.5])
    lid += _zcyl(0, 0, zt - 1, 40, 13)
    lid -= _zcyl(0, 0, zl + 1.2, P["LID_D"] / 2 + 2, 0.8) - _zcyl(0, 0, zl, P["LID_D"] / 2 - 1.2, 3)
    lid -= _zcyl(0, 0, zl - 1, P["LID_PORT_D"] / 2, P["LID_T"] + 15)
    add("Canner lid (aluminum)", lid, C_ALU, "metal", 7, "internal", E_LID)
    lh = _box(0, ro + 60, zt + 8, 40, 110, 16)
    lh = _fillet_try(lh, lh.edges(), [6.0, 4.0, 2.0])
    add("Lid handle (phenolic)", lh, C_GRIP, "plastic", 7, "internal", E_LID)
    add("Overpressure plug (rubber)", _zcyl(*P["PLUG_POS"], zt, 7, 4), C_BLACK, "rubber", 7, "internal", E_LID)
    al, aw_, ah = P["ADAPTER"]
    za = zt + 12 + ah
    vx = P["VENT_X"]
    add("Vent pipe (as supplied)", _zcyl(vx, 0, za, 5, 30), C_STAINLESS, "metal", 7, "internal", E_LID)
    reg = _zcyl(vx, 0, za + 12, 16, 22)
    reg = _fillet_try(reg, _top(reg), [5.0, 3.0])
    reg += _zcyl(vx, 0, za + 34, 5, 8)
    add("Weighted regulator", reg, C_STAINLESS, "metal", 7, "internal", (VX, 0, 580))

    # factory gauge and relief valve (BOM 8, 9), on the lid as supplied
    E_G = (VX, -60, 500)
    gx, gy = P["GAUGE_POS"]
    gr = P["GAUGE_DIAL"] / 2
    gzz = zt + 35 + gr
    add("Factory gauge stem", _zcyl(gx, gy, zt, 6, 35) + _hex_z(gx, gy, zt + 4, 16, 8), C_BRASS, "metal", 8, "internal", E_G)
    case = _ycyl(gx, gy, gzz, gr, 25)
    case = _fillet_try(case, case.edges(), [4.0, 2.5])
    case -= _ycyl(gx, gy - 12.5, gzz, gr - 4, 6)
    add("Factory gauge case", case, C_STAINLESS, "metal", 8, "internal", E_G)
    yf = gy - 10.5
    add("Gauge dial", _ycyl(gx, yf, gzz, gr - 4, 1.0), C_DIAL, "paper", 8, "internal", E_G)
    marks = []
    for k in range(13):
        a = math.radians(-135 + 22.5 * k)
        r0 = gr - 12 if k % 2 == 0 else gr - 9
        mid = (r0 + gr - 6) / 2
        marks.append(Pos(gx + mid * math.sin(a), yf - 0.7, gzz + mid * math.cos(a)) * Rot(0, math.degrees(a), 0)
                     * Box(1.3 if k % 2 == 0 else 0.8, 0.4, gr - 6 - r0))
    add("Gauge scale marks", Compound(marks), C_INK, "paper", 8, "internal", E_G)
    ndl = Pos(gx, yf - 1.4, gzz) * Rot(0, -48, 0) * Pos(0, 0, 13) * Box(2.0, 0.6, 28) + _ycyl(gx, yf - 1.6, gzz, 3.0, 1.4)
    add("Gauge needle", ndl, C_BLACK, "plastic", 8, "internal", E_G)
    add("Gauge glass", _ycyl(gx, gy - 13.5, gzz, gr - 4, 1.2), C_GLASS, "clear", 8, "internal", (VX, -100, 500))
    rx, ry = P["RELIEF_POS"]
    rv = _hex_z(rx, ry, zt, 18, 6) + _zcyl(rx, ry, zt + 6, 8, 16) + _zcyl(rx, ry, zt + 22, 11, 8)
    rv = _fillet_try(rv, _top(rv), [2.5, 1.5])
    add("Factory relief valve", rv, C_BRASS, "metal", 9, "internal", (VX, 0, 500))

    # vent-stem adapter plate (BOM 10) with the Pt100 gland and the pressure transducer (BOM 14)
    E_AD = (VX, 0, 470)
    add("Vent-stem adapter plate (stainless)", sh("adapter"), C_STAINLESS, "metal", 10, "internal", E_AD)
    px, py = P["PROBE_X"], P["PROBE_Y"]
    tip = FZ + bt + P["PROBE_TIP_Z"]
    gl = _hex_z(px, py, za, 18, 8) + _zcyl(px, py, za + 8, 8, 22)
    gl = _fillet_try(gl, _top(gl), [2.0, 1.0])
    add("Probe gland (brass)", gl, C_BRASS, "metal", 10, "internal", E_AD)
    add("Pt100 probe sheath", _zcyl(px, py, tip, 1.5, za + 38 - tip), C_STAINLESS, "metal", 10, "internal", E_AD)
    tx = P["TRANSDUCER_X"]
    tr = _hex_z(tx, 0, za, 20, 8) + _zcyl(tx, 0, za + 8, 11, 52)
    tr = _fillet_try(tr, _top(tr), [2.5, 1.5])
    add("Pressure transducer (stainless)", tr, C_STAINLESS, "metal", 14, "internal", (VX, 0, 540))
    add("Transducer connector", _zcyl(tx, 0, za + 60, 7, 15), C_DARK, "plastic", 14, "internal", (VX, 0, 540))

    # water, basket and trivet, wrapped instrument load (inside the canner)
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
    lxs, lys, lzs = P["LOGGER"]
    xo = D["xo"]
    x1 = xo + lxs                                         # front face, away from the upright
    z0, z1 = P["LOGGER_Z"], P["LOGGER_Z"] + lzs
    zm, ly, bw, bh = (z0 + z1) / 2, 0.0, lys, lzs
    base_o = _box(xo + (lxs - 12) / 2, ly, zm, lxs - 12, bw, bh)
    base_o = _fillet_try(base_o, base_o.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    base = base_o - _box(xo + (lxs - 12) / 2 + 3, ly, zm, lxs - 12, bw - 6, bh - 6)
    add("Logger box (IP65)", base, C_SHELL, "plastic", 14, "shell", E_LOG)
    lid_o = _box(x1 - 6, ly, zm, 12, bw, bh)
    lid_o = _fillet_try(lid_o, lid_o.edges().filter_by(Axis.X), [8.0, 6.0, 4.0])
    lidl = lid_o - _box(x1 - 9, ly, zm, 12, bw - 6, bh - 6)
    add("Logger lid", lidl, C_SHELL2, "plastic", 14, "shell", (E_LOG[0] + 120, 0, 0))
    ls = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            q = _xcyl(x1 + 0.6, ly + sy * (bw / 2 - 8), zm + sz * (bh / 2 - 8), 3.0, 1.2)
            ls.append(q - _box(x1 + 1.2, ly + sy * (bw / 2 - 8), zm + sz * (bh / 2 - 8), 1.0, 3.6, 0.8))
    add("Logger lid screws", Compound(ls), C_ZINC, "metal", 17, "shell", (E_LOG[0] + 160, 0, 0))
    EP = (E_LOG[0] + 180, 0, 0)
    oz = z1 - 36
    bez = _box(x1 + 2, ly, oz, 4, 64, 36)
    bez = _fillet_try(bez, bez.edges().filter_by(Axis.X), [3.0, 2.0])
    bez -= _box(x1 + 4, ly, oz + 1, 1.0, 52, 26)
    add("OLED display bezel", bez, C_BLACK, "plastic", 14, "shell", EP)
    add("OLED display glass", _box(x1 + 3.3, ly, oz + 1, 0.6, 52, 26), "#0E1216", "screen", 14, "shell", EP)
    xr = x1 + 3.75
    readout = (_box(xr, ly + 8, oz + 6, 0.3, 28, 9) + _box(xr, ly - 16, oz + 8, 0.3, 11, 4)
               + _box(xr, ly - 16, oz + 3, 0.3, 11, 2) + _box(xr, ly, oz - 7, 0.3, 42, 2.5))
    add("OLED readout (lit)", readout, C_OLED, "emissive", 14, "shell", EP)
    bz_ = oz - 40
    bts, bzl = [], []
    for dy in (-22, 0):
        b = _xcyl(x1 + 2.5, ly + dy, bz_, 6.5, 5.0)
        bts.append(_fillet_try(b, b.faces().sort_by(Axis.X)[-1].edges(), [1.5, 1.0]))
        bzl.append(_xcyl(x1 + 0.9, ly + dy, bz_, 8.5, 1.8) - _xcyl(x1 + 0.9, ly + dy, bz_, 7.0, 3.0))
    add("Logger buttons", Compound(bts), C_ACCENT, "plastic", 14, "shell", EP)
    add("Logger button bezels", Compound(bzl), C_DARK, "plastic", 14, "shell", EP)
    for k, (col, mat, nm) in enumerate([(C_LED_G, "emissive", "PASS light, green (lit)"),
                                        (C_LED_R, "plastic", "FAIL light, red")]):
        yy = ly + 16 + 13 * k
        cap = (Pos(x1 + 1.2, yy, bz_) * Sphere(3.0)) & _box(x1 + 3.2, yy, bz_, 4.0, 8, 8)
        add(nm, _xcyl(x1 + 0.6, yy, bz_, 3.4, 1.2) + cap, col, mat, 14, "shell", EP)
    add("Buzzer grille", Compound([_xcyl(x1 + 0.2, ly - 24 + 6 * k, bz_ - 22, 1.5, 0.4) for k in range(5)]), C_DARK, "plastic", 14, "shell", EP)
    add("Logger name band", _box(x1 + 0.2, ly, z0 + 18, 0.4, bw - 20, 7), C_ACCENT, "painted", 14, "shell", EP)
    add("Logger rating label", _box(x1 + 0.2, ly, z0 + 42, 0.4, 60, 20), C_WHITE, "paper", 14, "shell", EP)
    ink = (_box(x1 + 0.45, ly - 15, z0 + 47, 0.3, 24, 5) + _box(x1 + 0.45, ly + 3, z0 + 40, 0.3, 44, 1.8)
           + _box(x1 + 0.45, ly, z0 + 35, 0.3, 50, 1.8))
    add("Logger label print", ink, C_INK, "paper", 14, "shell", EP)
    add("Logger cable gland", Compound(list(sh("logger_box"))[1:]), C_DARK, "plastic", 17, "shell", (E_LOG[0], 0, 0))
    EB = (E_LOG[0] + 60, 0, 0)
    add("Logger board", sh("logger_board"), C_PCB, "plastic", 14, "accessory", EB)
    add("USB power bank, 10,000 mAh", sh("power_bank"), C_BANK, "plastic", 15, "accessory", (E_LOG[0] + 60, 0, -170))
    add("Logger cable to the transducer", sh("cable"), C_BLACK, "rubber", 14, "shell", (0, 0, 0))

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
