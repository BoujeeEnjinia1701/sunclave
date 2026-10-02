"""SunClave parametric model (build123d), TRL 3, constructable design (SCL-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks (contacts, clearances,
                                       tilt sweep) and print the masses taken from the model

Coordinates in mm, Z up, ground at Z = 0. The tilt (elevation) axis runs along X through the
focal point F. The level pot holder is fixed to the stand, so the cooker never tilts; the dish,
ribs, rim, yoke plates and gnomon turn about the same axis on two fixed axles. Azimuth is set by
turning the whole stand on its four locking castors. The pose shown has the sun SUN_ELEV degrees
above the horizon toward -Y.

Design for construction (SCL-DDR-003, 2026-10-01): every part below can be cut, bent, drilled
or bought, and every joint is a bolt, rivet or screw through faces that touch. The changes from
the concept model are listed in docs/decisions/0003-design-for-construction.md.

Lid fittings (items 8 to 10) are shown at the positions they would take on the lid. The model
does not decide how they are mounted: drilling the maker's lid, a cooker with factory ports, or
an adapter plate is open for Amish (design decisions register, SCL-DEC-001).

Sizes are checked in SCL-CAL-001 (docs/04-calcs/sizing.py), which imports this file.
"""
import math
import sys
from pathlib import Path

from build123d import (Axis, Box, BuildLine, BuildPart, BuildSketch, Compound, Cylinder, Plane, Polygon,
                       Polyline, Pos, Rot, Solid, Vector, export_step, export_stl, extrude, make_face, revolve)

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # 1 reflector: paraboloid of 12 petals
    "D_DISH": 1400.0,        # aperture diameter
    "FOCAL": 500.0,          # focal length
    "REFL_T": 0.5,           # reflector sheet thickness (modelled at REFL_T_MODEL for visibility)
    "REFL_T_MODEL": 3.0,
    "N_PETALS": 12,
    "HUB_R0": 75.0,          # petals start at this radius (the hub and the cooker's shadow cover the centre)
    "FLANGE": 12.0,          # petal edge flange folded down along each rib, riveted through the rib
    "FLANGE_R0": 90.0,       # flanges start at this radius
    "TAB": (30.0, 12.0),     # rim tabs: width x depth, two per petal, riveted inside the rim band
    # 2 ribs (on edge), rim band, hub plate and clips (steel)
    "RIB_W": 20.0, "RIB_T": 3.0,       # rib depth normal to the dish x thickness
    "RIB_R0": 55.0,                    # ribs start at this radius, over the hub plate
    "RIB_PHASE": 15.0,                 # ribs at 15 + 30 k degrees, clear of the yoke stand-offs at 0 and 180
    "RIM_W": 25.0, "RIM_T": 4.0,       # rim band: axial height x radial thickness
    "HUB_D": 200.0, "HUB_T": 4.0,
    "CLIP": (20.0, 3.0),               # rib clips: 20 x 20 x 3 angle
    # tilt range: dish-axis elevation (equal to sun elevation when aimed)
    "ELEV_MIN": 15.0, "ELEV_MAX": 90.0,
    "SUN_ELEV": 50.0,                  # pose shown in the model and media
    # focal point and pivot axis height above ground
    "F_Z": 950.0,
    # 3 yoke: a 6 mm steel plate each side turning on a fixed axle, with a fan carrying the lock slot
    "YOKE_T": 6.0, "YOKE_W": 60.0, "YOKE_HUB_R": 40.0,
    "FAN_R": (125.0, 175.0), "SLOT_R": 150.0, "SLOT_W": 11.0,
    "STANDOFF": (50.0, 25.0, 2.5),     # rectangular tube: tangential x axial x wall
    "STANDOFF_BOLT_Y": 15.0,
    "LOCK_Z": -150.0,                  # lock stud below the axis
    "PLATE_BOLT_Z": 80.0,              # upper bolt of the axle plate above the axis
    "AXLE_D": 20.0, "COLLAR": (40.0, 12.0),
    "THRUST_T": 2.0,                   # PTFE thrust washer between the yoke plate and the axle plate
    "AXLE_PLATE": (6.0, 70.0, 270.0),  # thickness x width (Y) x height (Z), centred 30 mm below the axis
    # legacy names kept for product_model.py (appearance model, updated on Amish's Mac)
    "YOKE_R": 10.0, "QUAD_R": 175.0, "QUAD_T": 6.0,
    # 4 stand: timber frame, steel axle plates, castors
    "UPR_X": 840.0,                    # upright and side-rail centreline, each side of the dish axis
    "BASE_Y": 1100.0,                  # side-rail length along Y
    "RAIL_W": 70.0, "RAIL_H": 35.0,    # cross rails along X, laid flat
    "RAIL_EXT": 40.0,                  # cross rails run on past the side rails, for bolt end distance
    "SIDE_W": 45.0, "SIDE_H": 70.0,    # side rails along Y, on edge, on top of the cross rails
    "UPR_W": 45.0, "UPR_D": 70.0,      # uprights: 45 along X, 70 along Y
    "BRACE_W": 45.0, "BRACE_T": 35.0,  # diagonal braces, lapped on the upright and side rail faces
    "BRACE_Z": 520.0,                  # brace top bolt height on the upright
    "BRACE_Y": 470.0,                  # brace foot bolt, along the side rail
    "CASTOR_D": 75.0, "CASTOR_H": 102.0,   # wheel diameter and mounting height of a 75 mm castor
    "CASTOR_X": 790.0,                 # castor centres, inboard of the side rails
    "CASTOR_LOCKS": 4,                 # locking castors (all four, SCL-DDR-002 item 16)
    # 6 cooker: 12 L household aluminum pressure cooker (decided vessel, SCL-DDR-001 item 4)
    "POT_ID": 280.0, "POT_IH": 200.0,  # inside diameter and depth
    "POT_WALL": 4.0, "POT_BASE": 6.0,
    "LID_D": 300.0, "LID_T": 5.0,
    "HANDLE": (229.0, 40.0, 16.0, 28.0),   # handle reach from the axis, width, thickness, underside below the rim
    "BARE_BAND": 80.0,                 # blackened wall band above the base left uninsulated to catch spill
    # 5 level pot holder, fixed to the stand: a flat steel ring under the handles on two tube arms
    "RING_R": (174.0, 204.0), "HOLDER_T": 4.0,   # ring inner and outer radius, plate thickness
    "HOLDER_W": 25.0, "ARM_WALL": 2.0,           # square tube arm size and wall
    "HOLDER_Z": 178.0,                 # ring top above the focal plane (the handle underside)
    # 11 jacket
    "JKT_T": 25.0,
    # 12 water and 13 basket
    "WATER_L": 1.5,
    "TRIVET_H": 40.0,
    "BASKET_D": 250.0, "BASKET_H": 150.0,
    # 10 Pt100 probe: tip height above the cooker floor and radius from the axis
    "PROBE_TIP_Z": 110.0, "PROBE_X": 30.0, "PROBE_Y": 70.0,
    # 14 logger box (bought IP65 box) on the +X upright's outer face, power bank inside
    "LOGGER": (65.0, 80.0, 180.0), "LOGGER_Z": 600.0,
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
    FZ = p["F_Z"]
    z_lr = (p["CASTOR_H"], p["CASTOR_H"] + p["RAIL_H"])                 # cross rails
    z_sr = (z_lr[1], z_lr[1] + p["SIDE_H"])                              # side rails
    ring_top = FZ + pot_oh - p["HANDLE"][3]
    arm_top = ring_top - p["HOLDER_T"]
    upr_top = arm_top - p["HOLDER_W"]
    xi = p["UPR_X"] - p["UPR_W"] / 2                                     # upright inner face
    xo = p["UPR_X"] + p["UPR_W"] / 2                                     # upright outer face
    x_plate = xi - p["AXLE_PLATE"][0]                                    # axle plate inner face
    x_yoke = x_plate - p["THRUST_T"] - p["YOKE_T"]                       # yoke plate inner face
    return {"R": R, "depth": depth, "rim_angle": rim_angle, "pot_or": pot_or, "pot_oh": pot_oh,
            "jkt_or": pot_or + p["JKT_T"], "base_x": 2 * (xo + p["RAIL_EXT"]), "z_lr": z_lr, "z_sr": z_sr,
            "ring_top": ring_top, "arm_top": arm_top, "upr_top": upr_top, "z_arm": arm_top - p["HOLDER_W"] / 2,
            "xi": xi, "xo": xo, "x_plate": x_plate, "x_yoke": x_yoke,
            "rim_r": R + p["RIM_T"], "rim_z": (depth - p["RIM_W"], depth),
            "standoff_r": f - (depth - p["RIM_W"] / 2),
            "water_depth": p["WATER_L"] * 1e6 / (math.pi * (p["POT_ID"] / 2) ** 2)}


def tilt_of(elev):
    """Dish-axis tilt from vertical for a given sun elevation (degrees)."""
    return 90.0 - elev


# ---------------------------------------------------------------- primitives
def bx(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(r, h, z, x=0.0, y=0.0):
    return Pos(x, y, z + h / 2) * Cylinder(r, h)


def zcyl(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def xcyl(x0, x1, y, z, r):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def ycyl(x, y0, y1, z, r):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, abs(y1 - y0))


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


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def mirror_x(shape):
    return shape.mirror(Plane.YZ)


def _para(r, f):
    return r * r / (4 * f)


def _normal(r, f):
    """Unit normal of the paraboloid profile in (r, z), pointing to the front (toward the focus)."""
    n = (-r / (2 * f), 1.0)
    L = math.hypot(*n)
    return n[0] / L, n[1] / L


def radial_slab(theta_deg, t0, t1, pts_rz):
    """A flat plate in the radial plane at angle theta: polygon pts (r, z), tangential from t0 to t1."""
    th = math.radians(theta_deg)
    u = Vector(math.cos(th), math.sin(th), 0)
    v = Vector(-math.sin(th), math.cos(th), 0)
    pl = Plane(origin=v * t1, x_dir=u, z_dir=-v)
    area = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts_rz, pts_rz[1:] + pts_rz[:1]))
    if area < 0:                                   # keep the face normal along -v whatever the winding
        pts_rz = list(reversed(pts_rz))
    face = pl * Polygon(*pts_rz, align=None)
    return extrude(face, amount=t1 - t0)


def _rect(r0, r1, z0, z1):
    return [(r0, z0), (r1, z0), (r1, z1), (r0, z1)]


def rib_angles(p=PARAMS):
    return [p["RIB_PHASE"] + 360.0 * k / p["N_PETALS"] for k in range(p["N_PETALS"])]


# ---------------------------------------------------------------- dish, in its own frame
def dish_profile(p=PARAMS):
    """Numbers the dish parts share: back surface z, hub plate face, rib end radius."""
    f, t = p["FOCAL"], p["REFL_T_MODEL"]
    zb = lambda r: _para(r, f) - t  # noqa: E731
    r_end = p["D_DISH"] / 2 - 0.5
    # rib back edge over the hub: lowest point of the rib between RIB_R0 and the clip end
    lows = []
    for i in range(30):
        r0 = p["RIB_R0"] + i * 1.5
        nr, nz = _normal(r0, f)
        lows.append(zb(r0) - p["RIB_W"] * nz)
    hub_front = min(lows) - 0.3
    return {"zb": zb, "r_end": r_end, "hub_front": hub_front}


def _rib_poly(p, r0, r1, depth, n=48, inset=0.03):
    """(r, z) polygon of a strip that starts on the back of the reflector and goes `depth` along the
    normal into the back, from radius r0 to r1 (front edge points)."""
    f = p["FOCAL"]
    zb = dish_profile(p)["zb"]
    front, back = [], []
    for i in range(n + 1):
        r = r0 + (r1 - r0) * i / n
        nr, nz = _normal(r, f)
        z = zb(r) - inset
        front.append((r, z))
        back.append((r - depth * nr, z - depth * nz))
    return front + list(reversed(back))


def dish_components(p=PARAMS):
    """Dish-frame parts: vertex at the origin, axis +Z. Returns {key: (name, shape, bom)}."""
    R, f = p["D_DISH"] / 2, p["FOCAL"]
    t = p["REFL_T_MODEL"]
    dp = dish_profile(p)
    zb, r_end = dp["zb"], dp["r_end"]
    out = {}
    angs = rib_angles(p)
    clip_l, clip_t = p["CLIP"]
    zr0, zr1 = R ** 2 / (4 * f) - p["RIM_W"], R ** 2 / (4 * f)
    big = Pos(0, 0, 0) * Cylinder(r_end, 2000)

    # 1 petals: the revolved sheet split at each rib, with flanges along the ribs and tabs at the rim
    n = 48
    r0 = p["HUB_R0"]
    outer = [(r0 + (R - r0) * i / n, _para(r0 + (R - r0) * i / n, f)) for i in range(n + 1)]
    inner = [(x, z - t) for x, z in reversed(outer)]
    with BuildPart() as refl:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*(outer + inner), close=True)
            make_face()
        revolve(axis=Axis.Z)
    sheet = refl.part
    gap = p["RIB_T"] / 2 + 1.0                     # sheet stops over the flange
    for a in angs:
        sheet = sheet - (Rot(0, 0, a) * Pos(R / 2 + 50, 0, 150) * Box(R + 100, 2 * gap, 600))
    flanges = []
    fpoly = _rib_poly(p, p["FLANGE_R0"], R, p["FLANGE"])
    for a in angs:
        for s in (-1, 1):
            t0, t1 = (p["RIB_T"] / 2, gap) if s > 0 else (-gap, -p["RIB_T"] / 2)
            flanges.append(radial_slab(a, t0, t1, fpoly))
    flange = fuse(flanges) & big
    tabs = []
    tw, td = p["TAB"]
    zt1 = zb(R - 1.2) - 0.05
    for a in angs:
        for da in (10.0, 20.0):
            tabs.append(Rot(0, 0, a + da) * bx(R - 0.17 - 1.0, R - 0.17, -tw / 2, tw / 2, zt1 - td, zt1))
    out["petals"] = ("Reflector petals (12)", sheet, 1)
    out["flanges"] = ("Petal flanges along the ribs", flange, 1)
    out["tabs"] = ("Petal tabs at the rim", Compound(tabs), 1)

    # 2 ribs, hub, rim band and clips
    rp = _rib_poly(p, p["RIB_R0"], R, p["RIB_W"])
    ribs = [radial_slab(a, -p["RIB_T"] / 2, p["RIB_T"] / 2, rp) & big for a in angs]
    out["ribs"] = ("Ribs (12)", Compound(ribs), 2)
    hz = dp["hub_front"]
    out["hub"] = ("Hub plate", _zcyl(p["HUB_D"] / 2, p["HUB_T"], hz - p["HUB_T"]), 2)
    out["rim"] = ("Rim band", _zcyl(R + p["RIM_T"], p["RIM_W"], zr0) - _zcyl(R, p["RIM_W"] + 2, zr0 - 1), 2)
    hub_clips, rim_clips = [], []
    for a in angs:
        hc = radial_slab(a, p["RIB_T"] / 2, p["RIB_T"] / 2 + clip_l, _rect(66, 79, hz, hz + clip_t))
        hc = hc + radial_slab(a, p["RIB_T"] / 2, p["RIB_T"] / 2 + clip_t, _rect(66, 79, hz + clip_t, hz + clip_l))
        hub_clips.append(hc)
        zc0, zc1 = zr0, zr0 + 13
        o = gap                                      # rim clip sits over the petal flange
        e = R - math.sqrt(R * R - (o + clip_l) ** 2) + 0.05    # the flat leg meets the curved band at its outer end
        rc = radial_slab(a, o, o + clip_l, _rect(R - clip_t - e, R - e, zc0, zc1))
        rc = rc + radial_slab(a, o, o + clip_t, _rect(R - 10 - e, R - clip_t - e, zc0, zc1))
        rim_clips.append(rc)
    out["hub_clips"] = ("Hub clips (12)", Compound(hub_clips), 2)
    out["rim_clips"] = ("Rim clips (12)", Compound(rim_clips), 2)

    # 16 gnomon: angle bracket on the rim band at the bottom of the dish (-Y), target plate, pin
    rr = R + p["RIM_T"]
    gb = (bx(rr, rr + 4, -20, 20, zr1 - 40, zr1) + bx(rr + 4, rr + 40, -20, 20, zr1 - 4, zr1))
    plate = bx(R, R + 120, -60, 60, zr1, zr1 + 3)
    pin = zcyl(R + 60, 0, zr1 + 3, zr1 + 183, 4)
    gn = Rot(0, 0, 270) * Compound([gb, plate, pin])
    out["gnomon"] = ("Sighting gnomon on its bracket", gn, 16)
    return out


def dish_local(p=PARAMS):
    """Reflector, frame (ribs, rim, hub, clips) and gnomon in the dish frame (for product_model.py)."""
    c = dish_components(p)
    return (Compound([c["petals"][1], c["flanges"][1], c["tabs"][1]]), Compound([c[k][1] for k in ("ribs", "hub", "rim", "hub_clips", "rim_clips")]),
            c["gnomon"][1])


# ---------------------------------------------------------------- dish placement
def axis_dir(p=PARAMS, elev=None):
    elev = p["SUN_ELEV"] if elev is None else elev
    t = math.radians(tilt_of(elev))
    return Vector(0, -math.sin(t), math.cos(t))


def vertex(p=PARAMS, elev=None):
    return Vector(0, 0, p["F_Z"]) - axis_dir(p, elev) * p["FOCAL"]


def to_world(shape, p=PARAMS, elev=None):
    """Place a dish-frame shape: rotate about X by the tilt, then move the vertex to V."""
    elev = p["SUN_ELEV"] if elev is None else elev
    t = tilt_of(elev)
    V = vertex(p, elev)
    return Pos(V.X, V.Y, V.Z) * Rot(t, 0, 0) * shape


def point_world(pt, p=PARAMS, elev=None):
    """Dish-frame point to world coordinates (same transform as to_world)."""
    elev = p["SUN_ELEV"] if elev is None else elev
    t = math.radians(tilt_of(elev))
    V = vertex(p, elev)
    x, y, z = pt
    return (V.X + x, V.Y + y * math.cos(t) - z * math.sin(t), V.Z + y * math.sin(t) + z * math.cos(t))


# ---------------------------------------------------------------- yoke (turns with the dish)
def yoke_plate_2d(p=PARAMS):
    """The yoke plate laid flat in its own (u, v) frame: origin on the tilt axis, the arm along -v
    toward the rim stand-off, the fan toward -u. Returns a build123d Face with its holes."""
    from build123d import Circle as C_, Rectangle as R_
    D = derived(p)
    L = D["standoff_r"]
    w, hr = p["YOKE_W"], p["YOKE_HUB_R"]
    r_in, r_out = p["FAN_R"]
    face = C_(hr) + Pos(0, -L / 2) * R_(w, L) + Pos(0, -L) * C_(w / 2)
    # fan: annular sector from -80 to -175 degrees (measured from +u toward +v)
    a0, a1 = -175.0, -80.0
    pts = []
    for i in range(41):
        a = math.radians(a0 + (a1 - a0) * i / 40)
        pts.append((r_out * math.cos(a), r_out * math.sin(a)))
    for i in range(41):
        a = math.radians(a1 - (a1 - a0) * i / 40)
        pts.append((r_in * math.cos(a), r_in * math.sin(a)))
    fan = Polygon(*pts, align=None)
    face = face + fan
    # holes: axle (reamed to 20.5), lock slot, stand-off screws (countersunk)
    face = face - C_(p["AXLE_D"] / 2 + 0.25)
    s0, s1 = -165.0, -90.0
    sp = []
    for i in range(31):
        a = math.radians(s0 + (s1 - s0) * i / 30)
        sp.append(((p["SLOT_R"] + p["SLOT_W"] / 2) * math.cos(a), (p["SLOT_R"] + p["SLOT_W"] / 2) * math.sin(a)))
    for i in range(31):
        a = math.radians(s1 - (s1 - s0) * i / 30)
        sp.append(((p["SLOT_R"] - p["SLOT_W"] / 2) * math.cos(a), (p["SLOT_R"] - p["SLOT_W"] / 2) * math.sin(a)))
    face = face - Polygon(*sp, align=None)
    for a in (s0, s1):
        face = face - Pos(p["SLOT_R"] * math.cos(math.radians(a)), p["SLOT_R"] * math.sin(math.radians(a))) * C_(p["SLOT_W"] / 2)
    for s in (-1, 1):
        face = face - Pos(s * p["STANDOFF_BOLT_Y"], -L) * C_(4.5)
    return face


def yoke_components(p=PARAMS):
    """Yoke parts in the dish frame (vertex at origin, axis +Z), both sides."""
    D = derived(p)
    f = p["FOCAL"]
    out = {}
    face = yoke_plate_2d(p)
    plates, offs, offb = [], [], []
    so_t, so_a, so_w = p["STANDOFF"]
    zc = (D["rim_z"][0] + D["rim_z"][1]) / 2
    rr = D["rim_r"]
    x0 = D["x_yoke"]
    # plate frame: u along dish +y, v along dish +z, normal along +x; the -X plate is its mirror image
    pl = Plane(origin=(x0, 0, f), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    yp = extrude(pl * face, amount=p["YOKE_T"])
    xyo = x0 + p["YOKE_T"]                                              # yoke plate outer face
    so = bx(rr, x0, -so_t / 2, so_t / 2, zc - so_a / 2, zc + so_a / 2) - bx(rr - 1, x0 + 1, -so_t / 2 + so_w, so_t / 2 - so_w,
                                                                          zc - so_a / 2 + so_w, zc + so_a / 2 - so_w)
    plates += [yp, mirror_x(yp)]
    offs += [so, mirror_x(so)]
    for y in (-p["STANDOFF_BOLT_Y"], p["STANDOFF_BOLT_Y"]):
        b = xcyl(p["D_DISH"] / 2 - 4, x0 + p["YOKE_T"], y, zc, 4)          # M8 countersunk screw
        b = b + xcyl(p["D_DISH"] / 2 - 7, p["D_DISH"] / 2, y, zc, 6.5)    # nyloc nut inside the band
        offb += [b, mirror_x(b)]
    out["yoke_plates"] = ("Yoke plates (2)", Compound(plates), 3)
    out["standoffs"] = ("Rim stand-offs (2)", Compound(offs), 3)
    out["standoff_screws"] = ("Stand-off screws, M8 countersunk", Compound(offb), 3)
    return out


# ---------------------------------------------------------------- fixed parts
def stand_components(p=PARAMS):
    D = derived(p)
    FZ = p["F_Z"]
    out = {}
    xi, xo, xp, xy = D["xi"], D["xo"], D["x_plate"], D["x_yoke"]
    BY = p["BASE_Y"]
    zl0, zl1 = D["z_lr"]
    zs0, zs1 = D["z_sr"]
    yr = BY / 2 - p["RAIL_W"] / 2

    def both(sh):
        return [sh, mirror_x(sh)]

    xe = xo + p["RAIL_EXT"]
    out["cross_rails"] = ("Cross rails (2)", Compound([bx(-xe, xe, s * yr - p["RAIL_W"] / 2, s * yr + p["RAIL_W"] / 2, zl0, zl1)
                                                       for s in (-1, 1)]), 4)
    out["side_rails"] = ("Side rails (2)", Compound(both(bx(xi, xo, -BY / 2, BY / 2, zs0, zs1))), 4)
    up = bx(xi, xo, -p["UPR_D"] / 2, p["UPR_D"] / 2, zs1, D["upr_top"])
    for z, d in ((FZ, p["AXLE_D"] + 0.5), (FZ + p["LOCK_Z"], 10.5), (FZ + p["PLATE_BOLT_Z"], 10.5), (p["BRACE_Z"], 10.5),
                 (D["arm_top"] - p["HOLDER_W"] - 20, 8.5)):
        up = up - xcyl(xi - 1, xo + 1, 0, z, d / 2)
    out["uprights"] = ("Uprights (2)", Compound(both(up)), 4)
    # braces: front brace on the outer face, back brace on the inner face, one bolt through both at the top
    braces = []
    foot = (p["BRACE_Y"], (zs0 + zs1) / 2)
    top = (0.0, p["BRACE_Z"])
    for sy, xr in ((-1, (xo, xo + p["BRACE_T"])), (1, (xi - p["BRACE_T"], xi))):
        a = (sy * foot[0], foot[1]); b = top
        d = math.hypot(b[0] - a[0], b[1] - a[1]); u = ((b[0] - a[0]) / d, (b[1] - a[1]) / d)
        e0 = (a[0] - 20 * u[0], a[1] - 20 * u[1]); e1 = (b[0] + 25 * u[0], b[1] + 25 * u[1])
        x = (xr[0] + xr[1]) / 2
        br = _bar((x, e0[0], e0[1]), (x, e1[0], e1[1]), p["BRACE_T"], p["BRACE_W"], side=(1, 0, 0))
        braces += both(br)
    out["braces"] = ("Braces (4)", Compound(braces), 4)
    # castors: plate, swivel, fork, wheel, brake pedal; centres inboard of the side rails
    cas = []
    for sy in (-1, 1):
        cx, cy = p["CASTOR_X"], sy * yr
        H = p["CASTOR_H"]
        r = p["CASTOR_D"] / 2
        c = (bx(cx - 30, cx + 30, cy - 30, cy + 30, H - 5, H) + zcyl(cx, cy, H - 14, H - 5, 26)
             + bx(cx - 18, cx - 14, cy - 22, cy + 22, r - 6, H - 14) + bx(cx + 14, cx + 18, cy - 22, cy + 22, r - 6, H - 14)
             + bx(cx - 18, cx + 18, cy - 22, cy + 22, H - 20, H - 14)
             + xcyl(cx - 12.5, cx + 12.5, cy, r, r)
             + bx(cx - 12, cx + 12, cy + sy * 22, cy + sy * 48, 0.7 * p["CASTOR_D"] - 4, 0.7 * p["CASTOR_D"] + 4))
        cas += both(c)
    out["castors"] = ("Locking castors (4)", Compound(cas), 4)
    # foot brackets: bought 50 x 50 x 3 angle brackets, 40 wide, on the front and back faces of each upright
    fb = []
    for sy in (-1, 1):
        y0 = sy * p["UPR_D"] / 2
        v = bx(p["UPR_X"] - 20, p["UPR_X"] + 20, min(y0, y0 + sy * 3), max(y0, y0 + sy * 3), zs1 + 3, zs1 + 50)
        h = bx(p["UPR_X"] - 20, p["UPR_X"] + 20, min(y0, y0 + sy * 50), max(y0, y0 + sy * 50), zs1, zs1 + 3)
        fb += both(v + h)
    out["foot_brackets"] = ("Foot brackets (4)", Compound(fb), 4)
    # axle plates (6 mm steel) on the inner face of each upright, with the axle and its collars
    t, w, h = p["AXLE_PLATE"]
    zc = FZ - 30
    ap = bx(xp, xi, -w / 2, w / 2, zc - h / 2, zc + h / 2)
    for z, d in ((FZ, p["AXLE_D"] + 0.5), (FZ + p["LOCK_Z"], 11.0), (FZ + p["PLATE_BOLT_Z"], 11.0)):
        ap = ap - xcyl(xp - 1, xi + 1, 0, z, d / 2)
    out["axle_plates"] = ("Axle plates (2)", Compound(both(ap)), 4)
    cd, cw = p["COLLAR"]
    ax = xcyl(xy - cw, xo + cw + 2, 0, FZ, p["AXLE_D"] / 2)
    out["axles"] = ("Axles (2)", Compound(both(ax)), 4)
    col = (xcyl(xy - cw, xy, 0, FZ, cd / 2) - xcyl(xy - cw - 1, xy + 1, 0, FZ, p["AXLE_D"] / 2)) + \
          (xcyl(xo, xo + cw, 0, FZ, cd / 2) - xcyl(xo - 1, xo + cw + 1, 0, FZ, p["AXLE_D"] / 2))
    out["collars"] = ("Axle collars (4)", Compound(both(col)), 4)
    tw = xcyl(xp - p["THRUST_T"], xp, 0, FZ, 25) - xcyl(xp - p["THRUST_T"] - 1, xp + 1, 0, FZ, p["AXLE_D"] / 2 + 0.25)
    out["thrust_washers"] = ("PTFE thrust washers (2)", Compound(both(tw)), 4)
    # lock studs (M10 x 80) with a star knob, and the upper plate bolts (M10 with a nut inside)
    zl = FZ + p["LOCK_Z"]
    stud = (xcyl(xy - 18, xo, 0, zl, 5) + xcyl(xo, xo + 8, 0, zl, 9.5)
            + (xcyl(xp - p["THRUST_T"], xp, 0, zl, 12) - xcyl(xp - p["THRUST_T"] - 1, xp + 1, 0, zl, 5))
            + (xcyl(xy - 2, xy, 0, zl, 10) - xcyl(xy - 3, xy + 1, 0, zl, 5))
            + (xcyl(xy - 22, xy - 2, 0, zl, 20) - xcyl(xy - 23, xy - 1, 0, zl, 5)))
    out["lock_studs"] = ("Lock studs and star knobs (2)", Compound(both(stud)), 3)
    zb_ = FZ + p["PLATE_BOLT_Z"]
    pb = xcyl(xp - 8, xo, 0, zb_, 5) + xcyl(xo, xo + 8, 0, zb_, 9.5) + (xcyl(xp - 8, xp, 0, zb_, 9.5) - xcyl(xp - 9, xp + 1, 0, zb_, 5))
    out["plate_bolts"] = ("Axle plate bolts (2)", Compound(both(pb)), 4)
    # bolts through the timber (M10 brace bolts, M8 foot and crossing bolts), for the joint pictures
    tb = []
    bt = xcyl(xi - p["BRACE_T"], xo + p["BRACE_T"], 0, p["BRACE_Z"], 5)
    bt = bt + xcyl(xo + p["BRACE_T"], xo + p["BRACE_T"] + 7, 0, p["BRACE_Z"], 9.5) + xcyl(xi - p["BRACE_T"] - 8, xi - p["BRACE_T"], 0, p["BRACE_Z"], 9.5)
    tb += both(bt)
    for sy, xr in ((-1, (xo, xo + p["BRACE_T"])), (1, (xi - p["BRACE_T"], xi))):
        x_out = xr[1] if sy < 0 else xr[0]
        x_in = xi if sy < 0 else xo
        y, z = sy * foot[0], foot[1]
        b = xcyl(min(x_out, x_in), max(x_out, x_in), y, z, 5)
        b = b + (xcyl(x_out, x_out + 7, y, z, 9.5) if sy < 0 else xcyl(x_out - 7, x_out, y, z, 9.5))
        b = b + (xcyl(x_in - 8, x_in, y, z, 9.5) if sy < 0 else xcyl(x_in, x_in + 8, y, z, 9.5))
        tb += both(b)
    for sy in (-1, 1):                                    # crossing bolts: two M8 per corner
        for dx, dy in ((-12, 0), (12, -20)):
            x, y = p["UPR_X"] + dx, sy * yr + sy * dy
            b = zcyl(x, y, zl0 - 6, zs1 + 6, 4) + zcyl(x, y, zs1, zs1 + 6, 7) + zcyl(x, y, zl0 - 6, zl0, 7)
            tb += both(b)
    for sy in (-1, 1):                                    # foot bracket bolts
        b = zcyl(p["UPR_X"], sy * 65, zs0 - 7, zs1 + 9, 4) + zcyl(p["UPR_X"], sy * 65, zs1 + 3, zs1 + 9, 7) + zcyl(p["UPR_X"], sy * 65, zs0 - 7, zs0, 7)
        tb += both(b)
    b = ycyl(p["UPR_X"], -p["UPR_D"] / 2 - 9, p["UPR_D"] / 2 + 9, zs1 + 28, 4)
    tb += both(b)
    out["stand_bolts"] = ("Stand bolts", Compound(tb), 17)
    return out


def holder_components(p=PARAMS):
    D = derived(p)
    out = {}
    ri, ro = p["RING_R"]
    rt, at = D["ring_top"], D["arm_top"]
    aw, wall = p["HOLDER_W"], p["ARM_WALL"]
    xb = (ri + ro) / 2
    ring = zcyl(0, 0, at, rt, ro) - zcyl(0, 0, at - 1, rt + 1, ri)
    for s in (-1, 1):
        ring = ring - zcyl(s * xb, 0, at - 1, rt + 1, 4.5)
    out["ring"] = ("Holder ring", ring, 5)
    xi, xo = D["xi"], D["xo"]
    x0 = ri + 2
    arm = bx(x0, xo, -aw / 2, aw / 2, at - aw, at) - bx(x0 - 1, xo + 1, -aw / 2 + wall, aw / 2 - wall, at - aw + wall, at - wall)
    out["arms"] = ("Holder arms (2)", Compound([arm, mirror_x(arm)]), 5)
    # bracket: 40 x 40 x 4 angle, 40 wide, on the upright's inner face, under the arm
    z1 = at - aw
    br = bx(xi - 4, xi, -20, 20, z1 - 40, z1) + bx(xi - 40, xi - 4, -20, 20, z1 - 4, z1)
    out["arm_brackets"] = ("Arm brackets (2)", Compound([br, mirror_x(br)]), 5)
    hb = []
    for s in (1, -1):
        b = zcyl(xb, 0, at - aw - 6, rt + 6, 4) + zcyl(xb, 0, rt, rt + 6, 7) + zcyl(xb, 0, at - aw - 6, at - aw, 7)
        b = b + zcyl(xi - 20, 0, z1 - 10, at + 6, 4) + zcyl(xi - 20, 0, at, at + 6, 7) + zcyl(xi - 20, 0, z1 - 10, z1 - 4, 7)
        b = b + xcyl(xi - 10, xo + 8, 0, z1 - 20, 4) + xcyl(xi - 10, xi - 4, 0, z1 - 20, 7) + xcyl(xo, xo + 8, 0, z1 - 20, 7)
        hb.append(b if s > 0 else mirror_x(b))
    out["holder_bolts"] = ("Holder bolts", Compound(hb), 17)
    return out


def vessel_components(p=PARAMS):
    D = derived(p)
    FZ = p["F_Z"]
    out = {}
    ro = D["pot_or"]
    ih, wall, bt = p["POT_IH"], p["POT_WALL"], p["POT_BASE"]
    oh = D["pot_oh"]
    hx, hw, ht, hd = p["HANDLE"]
    body = _zcyl(ro, oh, FZ) - _zcyl(p["POT_ID"] / 2, ih + 1, FZ + bt)
    for s in (-1, 1):                                                # handles on the outside of the wall
        hdl = bx(ro - 2, hx, -hw / 2, hw / 2, FZ + oh - hd, FZ + oh - hd + ht) if s > 0 else \
            bx(-hx, -(ro - 2), -hw / 2, hw / 2, FZ + oh - hd, FZ + oh - hd + ht)
        body = body + (hdl - _zcyl(p["POT_ID"] / 2, ih + 1, FZ + bt))
    out["body"] = ("Pressure cooker body, 12 L", body, 6)
    zl = FZ + oh
    lid = (_zcyl(p["LID_D"] / 2, p["LID_T"], zl) + _zcyl(40, 12, zl + p["LID_T"])
           + _zcyl(5, 40, zl + p["LID_T"])
           + _zcyl(16, 22, zl + p["LID_T"] + 22)
           + Pos(0, ro + 60, zl + p["LID_T"] + 8) * Box(40, 110, 16))
    out["lid"] = ("Lid with weighted regulator", lid, 7)
    zt = zl + p["LID_T"]
    out["gauge"] = ("Pressure gauge", _zcyl(7, 45, zt, 75, -55) + Pos(75, -55, zt + 95) * Rot(90, 0, 0) * Cylinder(50, 30), 8)
    out["relief"] = ("Independent relief valve", _zcyl(11, 40, zt, -80, 40) + _zcyl(17, 14, zt + 40, -80, 40), 9)
    tip = FZ + bt + p["PROBE_TIP_Z"]
    px, py = p["PROBE_X"], p["PROBE_Y"]
    gl = (_zcyl(9, 30, zt, px, py) + _zcyl(1.5, zt - tip, tip, px, py)
          + _tube((px + 9, py, zt + 22), (px + 60, py, zt + 22), 5))
    out["gland"] = ("Lid gland, Pt100 probe and tee", gl, 10)
    out["transducer"] = ("Pressure transducer on the tee", zcyl(px + 60, py, zt + 27, zt + 87, 11) + zcyl(px + 60, py, zt + 87, zt + 102, 7), 14)
    zj = FZ + p["BARE_BAND"]
    hj = oh - p["BARE_BAND"] - 30
    jk = _zcyl(D["jkt_or"], hj, zj) - _zcyl(ro, hj + 2, zj - 1)
    straps = [_zcyl(D["jkt_or"] + 1, 20, z) - _zcyl(D["jkt_or"], 22, z - 1) for z in (zj + 12, zj + hj - 32)]
    out["jacket"] = ("Insulated jacket with two straps", Compound([jk] + straps), 11)
    wd = D["water_depth"]
    out["water"] = ("Water charge, 1.5 L", _zcyl(p["POT_ID"] / 2 - 0.5, wd, FZ + bt), 12)
    rb = p["BASKET_D"] / 2
    zb = FZ + bt + p["TRIVET_H"]
    basket = (_zcyl(rb, p["BASKET_H"], zb) - _zcyl(rb - 2, p["BASKET_H"], zb + 2))
    trivet = _zcyl(rb + 5, 5, zb - 5) - _zcyl(rb - 15, 7, zb - 6)
    for k in range(3):
        a = 2 * math.pi * k / 3
        trivet = trivet + _zcyl(4, p["TRIVET_H"] - 5, FZ + bt, (rb - 10) * math.cos(a), (rb - 10) * math.sin(a))
    out["basket"] = ("Instrument basket and trivet", Compound([basket, trivet]), 13)
    out["load"] = ("Instrument load (not in BOM)", Pos(-40, -20, zb + 2 + 30) * Box(150, 110, 60), 0)
    # base thermocouple: a stainless band clamp on the bare band, 10 mm above the base, tip on the -X side
    tc = (_zcyl(ro + 1.2, 10, FZ + 10) - _zcyl(ro, 12, FZ + 9)) + bx(-ro - 9, -ro - 1.2, -6, 6, FZ + 8, FZ + 22)
    out["thermocouple"] = ("Base thermocouple on its band clamp", tc, 14)
    return out


def logger_components(p=PARAMS):
    D = derived(p)
    FZ = p["F_Z"]
    out = {}
    lx, ly, lz = p["LOGGER"]
    xo = D["xo"]
    z0 = p["LOGGER_Z"]
    box = bx(xo, xo + lx, -ly / 2, ly / 2, z0, z0 + lz) - bx(xo + 2.5, xo + lx - 2.5, -ly / 2 + 2.5, ly / 2 - 2.5, z0 + 2.5, z0 + lz - 2.5)
    gland = zcyl(xo + lx / 2, 0, z0 + lz, z0 + lz + 14, 9)
    out["logger_box"] = ("Logger box (IP65) with display", Compound([box, gland]), 14)
    out["power_bank"] = ("USB power bank, in the logger box", bx(xo + 4, xo + 22, -35, 35, z0 + 10, z0 + 150), 15)
    out["logger_board"] = ("Logger board and modules", bx(xo + 26, xo + 40, -30, 30, z0 + 20, z0 + 160), 14)
    # cable: out of the gland, up beside the upright, along the top of the arm, up to the transducer
    zt = FZ + D["pot_oh"] + p["LID_T"]
    xc = xo + lx / 2
    at = D["arm_top"]
    tx, ty = p["PROBE_X"] + 60, p["PROBE_Y"]
    pts = [(xc, 0, z0 + lz + 14), (xc, 0, at + 3), (240, 0, at + 3), (240, 0, zt + 130), (tx, ty, zt + 130), (tx, ty, zt + 102)]
    cab = [_tube(a, b, 3) for a, b in zip(pts[:-1], pts[1:])]
    out["cable"] = ("Sensor cable", Compound(cab), 14)
    return out


# ---------------------------------------------------------------- assembly
class Comp:
    def __init__(self, key, name, shape, bom, moving):
        self.key, self.name, self.shape, self.bom, self.moving = key, name, shape, bom, moving


MOVING = ("petals", "flanges", "tabs", "ribs", "hub", "rim", "hub_clips", "rim_clips", "gnomon", "yoke_plates", "standoffs", "standoff_screws")


_CACHE = {}


def _local(p):
    key = repr(sorted(p.items()))
    if key not in _CACHE:
        mov = {**dish_components(p), **yoke_components(p)}
        fix = {}
        for fn in (stand_components, holder_components, vessel_components, logger_components):
            fix.update(fn(p))
        _CACHE[key] = (mov, fix)
    return _CACHE[key]


def build_components(p=PARAMS, elev=None):
    """Every component in world coordinates: {key: Comp}."""
    elev = p["SUN_ELEV"] if elev is None else elev
    mov, fix = _local(p)
    C = {}
    for k, (n, s, b) in mov.items():
        C[k] = Comp(k, n, to_world(s, p, elev), b, True)
    for k, (n, s, b) in fix.items():
        C[k] = Comp(k, n, s, b, False)
    return C


BOM_NAMES = {1: "Reflector, 12 aluminum petals", 2: "Dish ribs, rim, hub and clips", 3: "Tilt yoke and locks",
             4: "Timber stand with castors", 5: "Level pot holder (fixed to stand)", 6: "Pressure cooker body, 12 L",
             7: "Lid with weighted regulator", 8: "Pressure gauge", 9: "Independent relief valve",
             10: "Lid gland, Pt100 probe and tee", 11: "Insulated jacket", 12: "Water charge, 1.5 L",
             13: "Instrument basket and trivet", 14: "Cycle logger", 15: "USB power bank, in the logger box",
             16: "Sighting gnomon", 0: "Instrument load (not in BOM)"}


def build_parts(p=PARAMS, elev=None, C=None):
    """Return {bom_no: (name, shape)} for the modelled BOM lines, plus key 0 for the instrument load.
    Bolts (BOM line 17) are drawn with the parts they hold."""
    C = C or build_components(p, elev)
    groups = {}
    for c in C.values():
        b = c.bom
        if b == 17:
            b = 4 if c.key == "stand_bolts" else 5
        groups.setdefault(b, []).append(c.shape)
    return {b: (BOM_NAMES[b], Compound(v) if len(v) > 1 else v[0]) for b, v in groups.items()}


UNITS = {   # lift units for handling (R16) and separate STEP files
    "sunclave-dish": (1, 2, 3, 16),               # tilting dish, ribs, rim, yoke plates, gnomon
    "sunclave-stand": (4, 5),                      # timber stand, holder, axles, plates
    "sunclave-vessel": (6, 7, 8, 9, 10, 11, 12, 13),
}


def assembly(parts=None):
    parts = parts or build_parts()
    return Compound([parts[k][1] for k in sorted(parts)])


# ---------------------------------------------------------------- masses from the model
DENSITY = {"steel": 7.85e-6, "al": 2.70e-6, "timber": 0.50e-6, "ss": 7.9e-6}   # kg/mm3
MATERIAL = {   # key: (material, factor applied to the modelled volume, or a fixed mass in kg)
    "petals": ("al", None), "flanges": (None, 0.0), "tabs": (None, 0.0), "ribs": ("steel", 1.0), "hub": ("steel", 1.0), "rim": ("steel", 1.0),
    "hub_clips": ("steel", 1.0), "rim_clips": ("steel", 1.0), "gnomon": ("steel", 1.0),
    "yoke_plates": ("steel", 1.0), "standoffs": ("steel", 1.0), "standoff_screws": ("steel", 1.0),
    "cross_rails": ("timber", 1.0), "side_rails": ("timber", 1.0), "uprights": ("timber", 1.0), "braces": ("timber", 1.0),
    "castors": (None, 4 * 0.45), "foot_brackets": ("steel", 1.0), "axle_plates": ("steel", 1.0), "axles": ("steel", 1.0),
    "collars": ("steel", 1.0), "thrust_washers": (None, 0.02), "lock_studs": (None, 2 * 0.12), "plate_bolts": ("steel", 1.0), "stand_bolts": ("steel", 1.0),
    "ring": ("steel", 1.0), "arms": ("steel", 1.0), "arm_brackets": ("steel", 1.0), "holder_bolts": ("steel", 1.0),
}


def petal_mass(p=PARAMS):
    """Reflector petals at the real sheet thickness, with flanges and tabs (kg)."""
    R, f = p["D_DISH"] / 2, p["FOCAL"]
    rs = [p["HUB_R0"] + (R - p["HUB_R0"]) * i / 400 for i in range(401)]
    area = 0.0
    for a, b in zip(rs[:-1], rs[1:]):
        r = (a + b) / 2
        area += 2 * math.pi * r * math.hypot(b - a, _para(b, f) - _para(a, f))
    s_rib = sum(math.hypot(b - a, _para(b, f) - _para(a, f)) for a, b in zip(rs[:-1], rs[1:]) if a >= p["FLANGE_R0"])
    area += 2 * p["N_PETALS"] * s_rib * p["FLANGE"] + 2 * p["N_PETALS"] * p["TAB"][0] * p["TAB"][1]
    return area * p["REFL_T"] * DENSITY["al"]


def masses(p=PARAMS, C=None):
    C = C or build_components(p)
    m = {}
    for k, c in C.items():
        if k == "petals":
            m[k] = petal_mass(p)
        elif k in MATERIAL:
            mat, fac = MATERIAL[k]
            m[k] = fac if mat is None else c.shape.volume * DENSITY[mat] * fac
    return m


# ---------------------------------------------------------------- constructability checks
def _vol(a, b_):
    try:
        ba, bb = a.bounding_box(), b_.bounding_box()
        if (ba.min.X > bb.max.X or bb.min.X > ba.max.X or ba.min.Y > bb.max.Y or bb.min.Y > ba.max.Y
                or ba.min.Z > bb.max.Z or bb.min.Z > ba.max.Z):
            return 0.0
        return (a & b_).volume
    except Exception:
        return float("nan")


def _bbgap(a, b_):
    ba, bb = a.bounding_box(), b_.bounding_box()
    d = [max(bb.min.X - ba.max.X, ba.min.X - bb.max.X, 0), max(bb.min.Y - ba.max.Y, ba.min.Y - bb.max.Y, 0),
         max(bb.min.Z - ba.max.Z, ba.min.Z - bb.max.Z, 0)]
    return math.sqrt(sum(x * x for x in d))


def _gap(a, b_, need=None):
    """Shortest distance between two shapes; when need is given and the bounding boxes are already
    further apart than need, the bounding-box gap is returned (a lower bound) to save time."""
    try:
        if need is not None:
            g = _bbgap(a, b_)
            if g >= need:
                return g
        return a.distance_to(b_)
    except Exception:
        return float("nan")


VERBOSE = False


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart. Returns (description, overlap mm3, gap mm,
    expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect, tol=0.6):
        v = _vol(a, b_)
        gp = _gap(a, b_, None if expect == "touch" else expect)
        ok = v < 5.0 and (gp <= tol if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))
        if VERBOSE:
            print(f"  {'ok  ' if ok else 'FAIL'} {desc:70s} overlap {v:8.1f} mm3  gap {gp:7.2f} mm  need {expect}", flush=True)

    # dish
    chk("Ribs behind the petal sheet", S("ribs"), S("petals"), 0.0)
    chk("Petal flanges against the ribs (rivets through)", S("flanges"), S("ribs"), "touch")
    chk("Hub clips on the hub plate", S("hub_clips"), S("hub"), "touch")
    chk("Hub clips against the ribs", S("hub_clips"), S("ribs"), "touch")
    chk("Rim clips against the rim band", S("rim_clips"), S("rim"), "touch")
    chk("Rim clips over the petal flanges", S("rim_clips"), S("flanges"), "touch")
    chk("Petal tabs inside the rim band", S("tabs"), S("rim"), "touch")
    chk("Petal tabs under the petal edge", S("tabs"), S("petals"), "touch")
    chk("Ribs clear of the rim band", S("ribs"), S("rim"), 0.3)
    chk("Ribs clear of the hub plate", S("ribs"), S("hub"), 0.0)
    chk("Gnomon bracket on the rim band", S("gnomon"), S("rim"), "touch")
    chk("Stand-offs against the rim band", S("standoffs"), S("rim"), "touch")
    chk("Stand-offs against the yoke plates", S("standoffs"), S("yoke_plates"), "touch")
    chk("Stand-offs clear of the petal tabs", S("standoffs"), S("tabs"), 1.0)
    chk("Stand-off screws clear of the petal tabs", S("standoff_screws"), S("tabs"), 0.5)
    # pivot and lock
    chk("Thrust washers on the axle plates", S("thrust_washers"), S("axle_plates"), "touch")
    chk("Yoke plates on the thrust washers", S("yoke_plates"), S("thrust_washers"), "touch")
    chk("Yoke plates clear of the axle plates (2 mm)", S("yoke_plates"), S("axle_plates"), 1.9)
    chk("Axles through the yoke plates", S("axles"), S("yoke_plates"), "touch")
    chk("Axle plates on the uprights", S("axle_plates"), S("uprights"), "touch")
    chk("Axles in their holes through the uprights", S("axles"), S("uprights"), "touch")
    chk("Lock studs in their holes through the uprights", S("lock_studs"), S("uprights"), "touch")
    chk("Collars on the axles", S("collars"), S("axles"), "touch")
    chk("Inner collars against the yoke plates", S("collars"), S("yoke_plates"), "touch")
    chk("Lock studs through the yoke slot", S("lock_studs"), S("yoke_plates"), "touch")
    chk("Yoke plates clear of the uprights", S("yoke_plates"), S("uprights"), 6.0)
    chk("Stand-off screws clear of the uprights", S("standoff_screws"), S("uprights"), 3.0)
    # stand
    chk("Side rails on the cross rails", S("side_rails"), S("cross_rails"), "touch")
    chk("Uprights on the side rails", S("uprights"), S("side_rails"), "touch")
    chk("Braces on the uprights", S("braces"), S("uprights"), "touch")
    chk("Braces on the side rails", S("braces"), S("side_rails"), "touch")
    chk("Braces clear of the cross rails", S("braces"), S("cross_rails"), 0.0)
    chk("Castors under the cross rails", S("castors"), S("cross_rails"), "touch")
    chk("Castors clear of the side rails", S("castors"), S("side_rails"), 1.0)
    chk("Foot brackets on the uprights and side rails", S("foot_brackets"), S("uprights"), "touch")
    chk("Foot brackets on the side rails", S("foot_brackets"), S("side_rails"), "touch")
    # holder and vessel
    chk("Holder arms on the uprights", S("arms"), S("uprights"), "touch")
    chk("Holder arms on their brackets", S("arms"), S("arm_brackets"), "touch")
    chk("Arm brackets on the uprights", S("arm_brackets"), S("uprights"), "touch")
    chk("Arm brackets clear of the axle plates", S("arm_brackets"), S("axle_plates"), 2.0)
    chk("Ring on the arms", S("ring"), S("arms"), "touch")
    chk("Cooker handles on the ring", S("body"), S("ring"), "touch")
    chk("Jacket clear of the ring", S("jacket"), S("ring"), 3.0)
    chk("Jacket on the cooker", S("jacket"), S("body"), "touch")
    chk("Lid on the cooker", S("lid"), S("body"), "touch")
    chk("Thermocouple clamp on the cooker", S("thermocouple"), S("body"), "touch")
    chk("Transducer on the tee", S("transducer"), S("gland"), "touch")
    chk("Basket clear of the cooker wall", S("basket"), S("body") - _zcyl(200, 10, p["F_Z"] - 1), 2.0)
    # logger
    chk("Logger box on the upright", S("logger_box"), S("uprights"), "touch")
    chk("Power bank inside the logger box", S("power_bank"), S("logger_box"), "touch", tol=2.6)
    chk("Logger box clear of the braces", S("logger_box"), S("braces"), 10.0)
    chk("Logger box clear of the lock stud head", S("logger_box"), S("lock_studs"), 5.0)
    chk("Cable clear of the cooker handles", S("cable"), S("body"), 3.0)
    chk("Cable clear of the gauge and relief valve", S("cable"), S("gauge") + S("relief"), 3.0)

    # tilt sweep: every moving part clear of every fixed part from 15 to 90 degrees
    fixed = ["cross_rails", "side_rails", "uprights", "braces", "castors", "axle_plates", "collars", "plate_bolts",
             "thrust_washers", "lock_studs", "ring", "arms", "arm_brackets", "holder_bolts", "body", "lid", "gauge", "relief",
             "gland", "transducer", "jacket", "logger_box", "cable", "thermocouple", "foot_brackets", "stand_bolts"]
    allow = {("yoke_plates", "thrust_washers"): 0.0, ("yoke_plates", "collars"): 0.0, ("yoke_plates", "lock_studs"): 0.0,
             ("yoke_plates", "axle_plates"): 1.9}
    for el in (15, 30, 45, 60, 75, 90):
        Ce = build_components(p, elev=el)
        worst, bad = None, []
        for mk in MOVING:
            for fk in fixed:
                a_, b_ = Ce[mk].shape, Ce[fk].shape
                need = allow.get((mk, fk), 5.0)
                g0 = _bbgap(a_, b_)
                if g0 >= need and worst is not None and g0 - need >= worst[0]:
                    continue
                v = _vol(a_, b_)
                g = _gap(a_, b_, need) if v < 5.0 else 0.0
                if v >= 5.0 or g < need - 1e-6:
                    bad.append(f"{mk}/{fk}")
                if (mk, fk) not in allow and (worst is None or g - need < worst[0]):
                    worst = (g - need, mk, fk, v, g, need)
        if VERBOSE:
            print(f"  tilt {el}: closest {worst[1]} to {worst[2]} gap {worst[4]:.1f}; problems {bad}", flush=True)
        rows.append((f"Tilt {el} deg: every moving part clear; closest {Ce[worst[1]].name} to {Ce[worst[2]].name}",
                     worst[3], worst[4], worst[5], not bad))
        dz = min(Ce[mk].shape.bounding_box().min.Z for mk in MOVING)
        rows.append((f"Tilt {el} deg: lowest dish point above the ground", 0.0, dz, 50.0, dz >= 50.0))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    n_ok = sum(1 for r in rows if r[4])
    for d, v, g, e, ok in rows:
        print(f"  {'ok  ' if ok else 'FAIL'} {d:70s} overlap {v:8.1f} mm3  gap {g:7.2f} mm  need {e}")
    print(f"{n_ok} of {len(rows)} checks pass")
    return n_ok == len(rows)


if __name__ == "__main__":
    if "--check" in sys.argv:
        VERBOSE = "-v" in sys.argv
        ok = print_checks()
        C = build_components()
        m = masses(C=C)
        tot = sum(m.values())
        for k, v in sorted(m.items(), key=lambda kv: -kv[1]):
            print(f"  mass {k:18s} {v:6.2f} kg")
        print(f"  modelled structure (not the vessel, logger or hardware estimates) {tot:.1f} kg")
        sys.exit(0 if ok else 1)
    C = build_components()
    parts = build_parts(C=C)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    asm = assembly(parts)
    shapes = {"sunclave-assembly": asm}
    for name, keys in UNITS.items():
        shapes[name] = Compound([parts[k][1] for k in keys])
    for name, shp in shapes.items():
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    bb = asm.bounding_box()
    d = derived()
    print(f"assembly bounding box: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"dish depth {d['depth']:.0f} mm, rim angle {d['rim_angle']:.1f} deg, water depth {d['water_depth']:.1f} mm")
    for k in sorted(parts):
        print(f"  item {k:2d}  {parts[k][0]:40s} volume {sum(x.volume for x in parts[k][1].solids()) / 1e6:7.3f} L")
    print("wrote cad/step/*.step and cad/stl/*.stl")
