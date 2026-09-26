"""SunClave parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL of the assembly and its main lift units into cad/step and cad/stl.

Massing-plus level of detail: correct interfaces and main dimensions, not fabrication
detail. Coordinates in mm, Z up, ground at Z = 0. The tilt (elevation) axis runs along X
through the focal point F. The level pot holder is fixed to the stand, so the cooker never
tilts; the dish, ribs and yoke turn on bearings about the same axis. Azimuth is set by
turning the whole stand on its castors, all four of which lock (SCL-DDR-002). The pose
shown has the sun SUN_ELEV degrees above the horizon toward -Y.

Lid fittings (items 8 to 10) are shown at the positions they would take on the lid. The
model does not decide how they are mounted: drilling the maker's lid, a cooker with
factory ports, or an adapter plate is open for Amish (SCL-DDR-001, open item 5).

Sizes are checked in SCL-CAL-001 (docs/04-calcs/sizing.py), which imports PARAMS from
this file.
"""
import math
from pathlib import Path

from build123d import (Axis, Box, BuildLine, BuildPart, BuildSketch, Compound, Cylinder, Plane, Polyline,
                       Pos, Rot, Solid, Vector, export_step, export_stl, make_face, revolve)

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # 1 reflector: paraboloid of 12 petals
    "D_DISH": 1400.0,        # aperture diameter
    "FOCAL": 500.0,          # focal length
    "REFL_T": 0.5,           # reflector sheet thickness (modelled at REFL_T_MODEL for visibility)
    "REFL_T_MODEL": 3.0,
    "N_PETALS": 12,
    # 2 ribs, rim and hub (steel flat bar)
    "RIB_W": 20.0, "RIB_T": 3.0,       # rib section, depth normal to the dish x thickness
    "RIM_W": 20.0, "RIM_T": 4.0,       # rim ring section
    "HUB_D": 150.0, "HUB_T": 6.0,
    "HUB_R0": 75.0,                    # ribs start at this radius
    # tilt range: dish-axis elevation (equal to sun elevation when aimed)
    "ELEV_MIN": 15.0, "ELEV_MAX": 90.0,
    "SUN_ELEV": 50.0,                  # pose shown in the model and media
    # focal point and pivot axis height above ground
    "F_Z": 950.0,
    # 3 yoke (steel square tube, modelled as round) and quadrant
    "YOKE_R": 10.0, "QUAD_R": 180.0, "QUAD_T": 6.0,
    # 4 stand: timber frame (decided, SCL-DDR-001 item 2), steel bearing blocks, castors
    "UPR_X": 840.0,                    # upright centerline, each side of the dish axis
    "BASE_Y": 1100.0,                  # base depth along Y
    "RAIL_W": 70.0, "RAIL_H": 35.0,    # base rails, laid flat
    "UPR_W": 70.0, "UPR_D": 45.0,      # uprights
    "BRACE_W": 45.0, "BRACE_T": 35.0,  # diagonal braces
    "BRACE_Z": 600.0,                  # brace top height on the upright
    "CASTOR_D": 75.0,
    "CASTOR_LOCKS": 4,                 # locking castors (all four, SCL-DDR-002 item 16)
    # 6 cooker: 12 L household aluminum pressure cooker (decided vessel, SCL-DDR-001 item 4)
    "POT_ID": 280.0, "POT_IH": 200.0,  # inside diameter and depth
    "POT_WALL": 4.0, "POT_BASE": 6.0,
    "LID_D": 300.0, "LID_T": 5.0,
    "BARE_BAND": 80.0,                 # blackened wall band above the base left uninsulated to catch spill
    # 5 level pot holder, fixed to the stand
    "HOLDER_Z": 150.0,                 # ring height above the base (under the body handles)
    "HOLDER_W": 25.0, "HOLDER_T": 4.0,
    # 11 jacket
    "JKT_T": 25.0,
    # 12 water and 13 basket
    "WATER_L": 1.5,
    "TRIVET_H": 40.0,
    "BASKET_D": 250.0, "BASKET_H": 150.0,
    # 10 Pt100 probe: tip height above the cooker floor and radius from the axis
    "PROBE_TIP_Z": 110.0, "PROBE_X": 30.0, "PROBE_Y": 70.0,
}
P = PARAMS


def derived(p=PARAMS):
    """Geometry derived from the parameters (mm, degrees)."""
    R = p["D_DISH"] / 2
    f = p["FOCAL"]
    depth = R ** 2 / (4 * f)
    rim_angle = math.degrees(2 * math.atan(R / (2 * f)))
    pot_or = p["POT_ID"] / 2 + p["POT_WALL"]
    pot_oh = p["POT_IH"] + p["POT_BASE"]
    return {"R": R, "depth": depth, "rim_angle": rim_angle, "pot_or": pot_or, "pot_oh": pot_oh,
            "jkt_or": pot_or + p["JKT_T"], "base_x": 2 * p["UPR_X"] + p["RAIL_W"],
            "water_depth": p["WATER_L"] * 1e6 / (math.pi * (p["POT_ID"] / 2) ** 2)}


def tilt_of(elev):
    """Dish-axis tilt from vertical for a given sun elevation (degrees)."""
    return 90.0 - elev


def _zcyl(r, h, z, x=0.0, y=0.0):
    return Pos(x, y, z + h / 2) * Cylinder(r, h)


def _tube(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _bar(a, b, w, t, side=(1, 0, 0)):
    """Rectangular bar from a to b; w along `side` (made normal to the bar), t along the third axis."""
    a, b = Vector(*a), Vector(*b)
    d = b - a
    x = d.normalized()
    s = Vector(*side)
    s = (s - x * s.dot(x)).normalized()
    z = x.cross(s)
    mid = a + d * 0.5
    return Plane(origin=mid, x_dir=x, z_dir=z) * Box(d.length, w, t)


def _para(r, f):
    return r * r / (4 * f)


def dish_local(p=PARAMS):
    """Reflector, ribs, rim, hub and gnomon in the dish frame: vertex at the origin, axis +Z."""
    R, f = p["D_DISH"] / 2, p["FOCAL"]
    t = p["REFL_T_MODEL"]
    n = 24
    outer = [(R * i / n, _para(R * i / n, f)) for i in range(n + 1)]
    inner = [(x, z - t) for x, z in reversed(outer)]
    with BuildPart() as refl:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*(outer + inner), close=True)
            make_face()
        revolve(axis=Axis.Z)
    reflector = refl.part

    # 2 ribs on the back, following the paraboloid, one under each petal seam
    ribs = []
    for k in range(p["N_PETALS"]):
        a = 2 * math.pi * k / p["N_PETALS"]
        c, s = math.cos(a), math.sin(a)
        rs = [p["HUB_R0"] + (R - 10 - p["HUB_R0"]) * i / 6 for i in range(7)]
        off = t + p["RIB_W"] / 2
        pts = [(r * c, r * s, _para(r, f) - off) for r in rs]
        for a0, b0 in zip(pts[:-1], pts[1:]):
            ribs.append(_bar(a0, b0, p["RIB_T"], p["RIB_W"], side=(-s, c, 0)))
    zr = _para(R, f)
    rim = (_zcyl(R + p["RIM_T"], p["RIM_W"], zr - p["RIM_W"]) - _zcyl(R, p["RIM_W"] + 2, zr - p["RIM_W"] - 1))
    hub = _zcyl(p["HUB_D"] / 2, p["HUB_T"], -t - p["RIB_W"] - p["HUB_T"] + 4)
    frame = Compound(ribs + [rim, hub]).fuse() if False else Compound(ribs + [rim, hub])

    # 16 gnomon on the rim (top of the dish when tilted), pin parallel to the axis over a target plate
    gy = -(R - 60)
    gz = _para(R - 60, f)
    gnomon = Pos(0, gy, gz + 2) * Box(120, 120, 4) + _zcyl(4, 180, gz + 4, 0, gy)
    return reflector, frame, gnomon


def to_world(shape, p=PARAMS, elev=None):
    """Place a dish-frame shape: rotate about X by the tilt, then move the vertex to V."""
    elev = p["SUN_ELEV"] if elev is None else elev
    t = tilt_of(elev)
    V = vertex(p, elev)
    return Pos(V.X, V.Y, V.Z) * Rot(t, 0, 0) * shape


def axis_dir(p=PARAMS, elev=None):
    elev = p["SUN_ELEV"] if elev is None else elev
    t = math.radians(tilt_of(elev))
    return Vector(0, -math.sin(t), math.cos(t))


def vertex(p=PARAMS, elev=None):
    return Vector(0, 0, p["F_Z"]) - axis_dir(p, elev) * p["FOCAL"]


def point_world(pt, p=PARAMS, elev=None):
    """Dish-frame point to world coordinates (same transform as to_world)."""
    elev = p["SUN_ELEV"] if elev is None else elev
    t = math.radians(tilt_of(elev))
    V = vertex(p, elev)
    x, y, z = pt
    return (V.X + x, V.Y + y * math.cos(t) - z * math.sin(t), V.Z + y * math.sin(t) + z * math.cos(t))


def build_parts(p=PARAMS, elev=None):
    """Return {bom_no: (name, shape)} for the modelled BOM lines, plus key 0 for the instrument load."""
    elev = p["SUN_ELEV"] if elev is None else elev
    d = derived(p)
    R, FZ = d["R"], p["F_Z"]
    parts = {}

    reflector, frame, gnomon = dish_local(p)
    parts[1] = ("Reflector, 12 aluminum petals", to_world(reflector, p, elev))
    parts[2] = ("Dish ribs, rim and hub", to_world(frame, p, elev))
    parts[16] = ("Sighting gnomon", to_world(gnomon, p, elev))

    # 3 Yoke: arms from the pivot bearings on the focal axis to the rim at +/- X, and the quadrant lock
    xb = p["UPR_X"] - p["UPR_W"] / 2 - 40          # bearing face inside the uprights
    rim_pt = point_world((R + p["RIM_T"] + 12, 0, _para(R, p["FOCAL"]) - p["RIM_W"] / 2), p, elev)
    yoke = []
    for s in (-1, 1):
        yoke += [_tube((s * xb, 0, FZ), (s * rim_pt[0], rim_pt[1], rim_pt[2]), p["YOKE_R"]),
                 _tube((s * (xb - 5), 0, FZ), (s * (xb + 40), 0, FZ), 20)]          # bearing collar on the stub axle
    tq = math.radians(tilt_of(elev))
    lever = (-xb - 20, 0.8 * p["QUAD_R"] * math.sin(tq), FZ - 0.8 * p["QUAD_R"] * math.cos(tq))
    yoke += [_tube((-xb - 20, 0, FZ), lever, 8), Pos(*lever) * Rot(0, 90, 0) * Cylinder(14, 30)]  # lock lever and knob
    parts[3] = ("Tilt yoke and quadrant lock", Compound(yoke))

    # 4 Stand: timber base rails, cross members, uprights and braces; steel bearing blocks; castors
    BX, BY = d["base_x"], p["BASE_Y"]
    zc = p["CASTOR_D"] + 5                                  # underside of the timber frame
    rw, rh = p["RAIL_W"], p["RAIL_H"]
    stand = [Pos(0, s * (BY / 2 - rw / 2), zc + rh / 2) * Box(BX, rw, rh) for s in (-1, 1)]
    stand += [Pos(s * p["UPR_X"], 0, zc + rh / 2) * Box(rw, BY - 2 * rw, rh) for s in (-1, 1)]
    ztop = FZ + p["HOLDER_Z"] + 20                  # uprights carry the bearings and, above them, the holder arms
    for s in (-1, 1):
        x = s * p["UPR_X"]
        stand.append(Pos(x, 0, (zc + rh + ztop) / 2) * Box(p["UPR_W"], p["UPR_D"], ztop - zc - rh))
        for sy in (-1, 1):
            stand.append(_bar((x, sy * (BY / 2 - rw), zc + rh), (x, sy * p["UPR_D"] / 2, p["BRACE_Z"]),
                              p["BRACE_W"], p["BRACE_T"], side=(1, 0, 0)))
        stand.append(Pos(x - s * (p["UPR_W"] / 2 + 20), 0, FZ) * Box(40, 80, 90))     # steel bearing block, stub axle
        # quadrant plate fixed to the -X upright, slotted arc for the lock
    quad = (Pos(-xb - 20 + 0, 0, FZ) * Rot(0, 90, 0) * Cylinder(p["QUAD_R"], p["QUAD_T"])
            - Pos(-xb - 20, 0, FZ + p["QUAD_R"] / 2) * Box(20, 2 * p["QUAD_R"] + 10, p["QUAD_R"] + 10))
    stand.append(Pos(-6, 0, 0) * quad)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * (BX / 2 - 60), sy * (BY / 2 - 60)
            stand += [Pos(cx, cy, p["CASTOR_D"] / 2) * Rot(0, 90, 0) * Cylinder(p["CASTOR_D"] / 2, 25),
                      Pos(cx, cy, p["CASTOR_D"] + 2) * Box(60, 60, 6)]
    locks = [(sx, sy) for sx in (-1, 1) for sy in (-1, 1)][:int(p["CASTOR_LOCKS"])]
    for sx, sy in locks:                                   # brake pedal on each locking castor, on the outboard side
        cx, cy = sx * (BX / 2 - 60), sy * (BY / 2 - 60)
        stand.append(Pos(cx, cy + sy * (p["CASTOR_D"] / 2 + 12), 0.7 * p["CASTOR_D"]) * Box(24, 30, 8))
    parts[4] = ("Timber stand with castors", Compound(stand))

    # 5 Level pot holder, fixed to the uprights: ring under the body handles and two arms
    ro = d["pot_or"]
    zr = FZ + p["HOLDER_Z"]
    ring = _zcyl(ro + 30, p["HOLDER_W"], zr - p["HOLDER_W"]) - _zcyl(ro + 2, p["HOLDER_W"] + 2, zr - p["HOLDER_W"] - 1)
    arms = [_bar((s * (ro + 28), 0, zr - p["HOLDER_W"] / 2), (s * (p["UPR_X"] - p["UPR_W"] / 2), 0, zr - p["HOLDER_W"] / 2),
                 p["HOLDER_T"] * 5, p["HOLDER_W"], side=(0, 1, 0)) for s in (-1, 1)]
    parts[5] = ("Level pot holder (fixed to stand)", Compound([ring] + arms))

    # 6 Cooker body, 7 lid with weighted regulator and handles
    ih, wall, bt = p["POT_IH"], p["POT_WALL"], p["POT_BASE"]
    oh = d["pot_oh"]
    body = _zcyl(ro, oh, FZ) - _zcyl(p["POT_ID"] / 2, ih + 1, FZ + bt)
    body = body + Pos(0, 0, FZ + oh - 20) * Box(2 * ro + 170, 40, 16)             # body handles rest on the ring
    parts[6] = ("Pressure cooker body, 12 L", body)
    zl = FZ + oh
    lid = (_zcyl(p["LID_D"] / 2, p["LID_T"], zl) + _zcyl(40, 12, zl + p["LID_T"])
           + _zcyl(5, 40, zl + p["LID_T"])                                         # vent pipe
           + _zcyl(16, 22, zl + p["LID_T"] + 22)                                   # weighted regulator
           + Pos(0, ro + 60, zl + p["LID_T"] + 8) * Box(40, 110, 16))              # lid handle
    parts[7] = ("Lid with weighted regulator", lid)
    zt = zl + p["LID_T"]
    # 8 gauge, 9 relief valve, 10 gland with Pt100 probe and tee to the transducer
    parts[8] = ("Pressure gauge", _zcyl(7, 45, zt, 75, -55) + Pos(75, -55, zt + 95) * Rot(90, 0, 0) * Cylinder(50, 30))
    parts[9] = ("Independent relief valve", _zcyl(11, 40, zt, -80, 40) + _zcyl(17, 14, zt + 40, -80, 40))
    tip = FZ + bt + p["PROBE_TIP_Z"]
    gl = (_zcyl(9, 30, zt, p["PROBE_X"], p["PROBE_Y"]) + _zcyl(1.5, zt + 30 - tip, tip, p["PROBE_X"], p["PROBE_Y"])
          + _tube((p["PROBE_X"], p["PROBE_Y"], zt + 22), (p["PROBE_X"] + 60, p["PROBE_Y"], zt + 22), 5))
    parts[10] = ("Lid gland, Pt100 probe and tee", gl)

    # 11 jacket on the upper wall; the blackened lower band and base stay bare
    zj = FZ + p["BARE_BAND"]
    hj = oh - p["BARE_BAND"] - 30
    parts[11] = ("Insulated jacket", _zcyl(d["jkt_or"], hj, zj) - _zcyl(ro + 0.5, hj + 2, zj - 1))

    # 12 water, 13 basket and trivet, 0 instrument load
    wd = d["water_depth"]
    parts[12] = ("Water charge, 1.5 L", _zcyl(p["POT_ID"] / 2 - 0.5, wd, FZ + bt))
    rb = p["BASKET_D"] / 2
    zb = FZ + bt + p["TRIVET_H"]
    basket = (_zcyl(rb, p["BASKET_H"], zb) - _zcyl(rb - 2, p["BASKET_H"], zb + 2)
              + _zcyl(rb + 5, 5, zb - 5) - _zcyl(rb - 15, 7, zb - 6))
    for k in range(3):
        a = 2 * math.pi * k / 3
        basket = basket + _zcyl(4, p["TRIVET_H"] - 5, FZ + bt, (rb - 10) * math.cos(a), (rb - 10) * math.sin(a))
    parts[13] = ("Instrument basket and trivet", basket)
    parts[0] = ("Instrument load (not in BOM)", Pos(-40, -20, zb + 2 + 30) * Box(150, 110, 60))

    # 14 logger box on the +X upright with the power bank inside, cable to the lid
    lx = p["UPR_X"] + p["UPR_W"] / 2 + 30
    lz = FZ + 40
    logger = [Pos(lx, -40, lz) * Box(60, 150, 110),
              _tube((lx, 30, lz + 55), (lx, 30, zt + 120), 3),
              _tube((lx, 30, zt + 120), (p["PROBE_X"] + 60, p["PROBE_Y"], zt + 120), 3),
              _tube((p["PROBE_X"] + 60, p["PROBE_Y"], zt + 120), (p["PROBE_X"] + 60, p["PROBE_Y"], zt + 22), 3)]
    parts[14] = ("Cycle logger", Compound(logger))
    parts[15] = ("USB power bank, in the logger box", Pos(lx, -40, lz - 90) * Box(50, 140, 60))
    return parts


UNITS = {   # lift units for handling (R16) and separate STEP files
    "sunclave-dish": (1, 2, 3, 16),               # tilting dish, ribs, rim, yoke, gnomon
    "sunclave-stand": (4, 5),                      # timber stand, holder, quadrant
    "sunclave-vessel": (6, 7, 8, 9, 10, 11, 12, 13),
}


def assembly(parts=None):
    parts = parts or build_parts()
    return Compound([parts[k][1] for k in sorted(parts)])


if __name__ == "__main__":
    parts = build_parts()
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    asm = assembly(parts)
    shapes = {"sunclave-assembly": asm}
    for name, keys in UNITS.items():
        shapes[name] = Compound([parts[k][1] for k in keys])
    for name, shp in shapes.items():
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"))
    bb = asm.bounding_box()
    d = derived()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"dish depth {d['depth']:.0f} mm, rim angle {d['rim_angle']:.1f} deg, water depth {d['water_depth']:.1f} mm")
    for k in sorted(parts):
        print(f"  item {k:2d}  {parts[k][0]:40s} volume {parts[k][1].volume / 1e6:7.3f} L")
    print("wrote cad/step/*.step and cad/stl/*.stl")
