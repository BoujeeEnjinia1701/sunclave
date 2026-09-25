"""SunClave concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm, ground at Z = 0. The elevation (tilt) axis runs along X through the
focal point F, so the pressure cooker hangs level at the focus while the dish tilts about it.
The dish is shown aimed at a sun 50 degrees above the horizon toward -Y (the viewer side).
Azimuth is set by turning the whole stand on its castors.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, cutaway_parts, _render, ROOT

# ---------------- key parameters ----------------
D_DISH = 1400.0            # reflector aperture diameter (SK14 class)
R_AP = D_DISH / 2
FOCAL = 500.0              # focal length of the paraboloid
R_CURV = 2 * FOCAL         # spherical-cap stand-in for the paraboloid (massing only)
SUN_ELEV = 50.0            # sun elevation for the pose shown
TILT = 90.0 - SUN_ELEV     # dish axis tilt from vertical
F_Z = 950.0                # focal point height = pot bottom height
POT_R, POT_H = 150.0, 250.0  # 12 L class aluminum pressure cooker (about 300 x 250 mm)
UPR_X = 840.0              # stand uprights, outside the dish rim

t = math.radians(TILT)
AX = Vector(0, -math.sin(t), math.cos(t))       # dish axis (toward the sun)
F = Vector(0, 0, F_Z)
V = F - AX * FOCAL                              # dish vertex


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def dish_local_to_world(shape):
    """Local frame: vertex at origin, axis +Z. Rotating about X by TILT maps +Z onto AX."""
    return Pos(V.X, V.Y, V.Z) * Rot(TILT, 0, 0) * shape


def sag(r):
    return R_CURV - math.sqrt(R_CURV ** 2 - r ** 2)


def local_pt(r, ang, dz=0.0):
    return Vector(r * math.cos(ang), r * math.sin(ang), sag(r) + dz)


def to_world(p):
    """Same transform as dish_local_to_world, for points."""
    y = p.Y * math.cos(t) - p.Z * math.sin(t)
    z = p.Y * math.sin(t) + p.Z * math.cos(t)
    return (V.X + p.X, V.Y + y, V.Z + z)


# ---------------- 1 Reflector: 12 polished aluminum petals on a spherical-cap massing ----------------
cap = (Pos(0, 0, R_CURV) * (Sphere(R_CURV) - Sphere(R_CURV - 6))) & Pos(0, 0, 200) * Cylinder(R_AP, 400)
reflector = dish_local_to_world(cap)

# 2 Dish ribs and rim ring (steel), on the back of the petals
ribs = None
for k in range(12):
    a = math.radians(k * 30)
    p0, p1, p2 = local_pt(20, a, -45), local_pt(R_AP / 2, a, -45), local_pt(R_AP - 10, a, -45)
    seg = tube3(to_world(p0), to_world(p1), 9) + tube3(to_world(p1), to_world(p2), 9)
    ribs = seg if ribs is None else ribs + seg
rim = dish_local_to_world(Pos(0, 0, sag(R_AP) - 20) * (Cylinder(R_AP + 12, 20) - Cylinder(R_AP - 8, 22)))
hub = dish_local_to_world(Pos(0, 0, -30) * Cylinder(70, 20))
dish_frame = ribs + rim + hub

# 3 Tilt yoke: arms from the pivots at F down to the dish rim at +/- X
rim_x = to_world(local_pt(R_AP, 0.0, -10))            # rim point on +X
yoke = None
for s in (-1, 1):
    arm = (tube3((s * UPR_X, 0, F_Z), (s * (R_AP + 40), rim_x[1], rim_x[2]), 16)
           + tube3((s * (R_AP + 40), rim_x[1], rim_x[2]), (s * (R_AP + 5), rim_x[1], rim_x[2]), 16))
    yoke = arm if yoke is None else yoke + arm
yoke = yoke + tube3((-UPR_X, 0, F_Z), (-UPR_X + 60, 0, F_Z), 22) + tube3((UPR_X - 60, 0, F_Z), (UPR_X, 0, F_Z), 22)
# tilt lock: slotted quadrant plate on the -X upright
quad = Pos(-UPR_X - 30, 0, F_Z - 110) * Box(8, 260, 160)
yoke = yoke + quad

# 4 Stand: base frame with castors and two uprights to the pivots
BX, BY = 2 * UPR_X + 160, 1100.0
base = (Pos(0, -BY / 2, 60) * Box(BX, 50, 50) + Pos(0, BY / 2, 60) * Box(BX, 50, 50)
        + Pos(-BX / 2 + 25, 0, 60) * Box(50, BY, 50) + Pos(BX / 2 - 25, 0, 60) * Box(50, BY, 50))
stand = base
for s in (-1, 1):
    stand = stand + tube3((s * UPR_X, 0, 85), (s * UPR_X, 0, F_Z + 60), 22)
    stand = stand + tube3((s * UPR_X, -BY / 2 + 25, 85), (s * UPR_X, 0, 600), 14)
    stand = stand + tube3((s * UPR_X, BY / 2 - 25, 85), (s * UPR_X, 0, 600), 14)
    stand = stand + Pos(s * UPR_X, 0, F_Z + 60) * Box(70, 70, 40)       # pivot bearing block
for sx in (-1, 1):
    for sy in (-1, 1):
        stand = stand + Pos(sx * (BX / 2 - 25), sy * (BY / 2), 30) * Rot(0, 90, 0) * Cylinder(30, 25)

# 5 Pot holder: level ring and two hanger arms from the pivot axis
ring = Pos(0, 0, F_Z + 70) * (Cylinder(POT_R + 28, 18) - Cylinder(POT_R, 20))
holder = ring + tube3((-UPR_X + 60, 0, F_Z + 60), (-POT_R - 20, 0, F_Z + 70), 12) \
              + tube3((POT_R + 20, 0, F_Z + 70), (UPR_X - 60, 0, F_Z + 60), 12)

# 6 Pressure cooker body (aluminum, blackened base), 7 lid with weight regulator
WALL = 4.0
pot = Pos(0, 0, F_Z + POT_H / 2) * (Cylinder(POT_R, POT_H) - Pos(0, 0, WALL) * Cylinder(POT_R - WALL, POT_H))
lid = (Pos(0, 0, F_Z + POT_H + 6) * Cylinder(POT_R + 8, 12)
       + Pos(0, 0, F_Z + POT_H + 18) * Cylinder(40, 14)
       + Pos(0, 0, F_Z + POT_H + 35) * Cylinder(14, 20)                    # weighted regulator
       + Pos(0, POT_R + 40, F_Z + POT_H + 16) * Box(70, 90, 18)            # handles
       + Pos(0, -POT_R - 40, F_Z + POT_H + 16) * Box(70, 90, 18))
LID_TOP = F_Z + POT_H + 12

# 8 Pressure gauge on a lid fitting
gauge = (Pos(70, -55, LID_TOP + 20) * Cylinder(8, 40)
         + Pos(70, -55, LID_TOP + 90) * Rot(90, 0, 0) * Cylinder(50, 30))
# 9 Independent spring relief valve
relief = Pos(-75, 45, LID_TOP + 22) * Cylinder(12, 44) + Pos(-75, 45, LID_TOP + 50) * Cylinder(18, 12)
# 10 Lid gland with Pt100 probe and a pressure pigtail to the transducer
gland = (Pos(30, 90, LID_TOP + 18) * Cylinder(10, 36)
         + Pos(30, 90, F_Z + 150) * Cylinder(3, 2 * (LID_TOP - F_Z - 150)))    # probe into the load zone

# 11 Insulated jacket around the upper wall (the base stays bare to take the focus)
jacket = Pos(0, 0, F_Z + 90 + (POT_H - 90) / 2) * (Cylinder(POT_R + 35, POT_H - 90) - Cylinder(POT_R + 1, POT_H))

# 12 Water charge, 13 instrument basket on a trivet
water = Pos(0, 0, F_Z + WALL + 12) * Cylinder(POT_R - WALL - 1, 24)
basket = (Pos(0, 0, F_Z + 40 + 90) * (Cylinder(POT_R - 16, 180) - Pos(0, 0, 3) * Cylinder(POT_R - 19, 180))
          + Pos(0, 0, F_Z + 34) * (Cylinder(POT_R - 12, 10) - Cylinder(POT_R - 30, 12)))
instruments = Pos(0, 0, F_Z + 73) * Box(170, 110, 60)

# 14 Cycle logger box (Pt100 front end, pressure transducer, display, SD), 15 its solar panel
LOG = (UPR_X + 70, -40, 1130)
logger = Pos(*LOG) * Box(60, 150, 110) + Pos(LOG[0] - 35, LOG[1], LOG[2]) * Box(12, 40, 40)
cable = (tube3((LOG[0], LOG[1] + 60, LOG[2] + 40), (LOG[0], 90, LOG[2] + 110), 4)
         + tube3((LOG[0], 90, LOG[2] + 110), (30, 90, LOG[2] + 110), 4)
         + tube3((30, 90, LOG[2] + 110), (30, 90, LID_TOP + 36), 4))
logger = logger + cable
panel = Pos(LOG[0] + 30, LOG[1], LOG[2] + 120) * Rot(-35, 0, 0) * Box(140, 200, 8) \
        + tube3((LOG[0] + 30, LOG[1], LOG[2] + 55), (LOG[0] + 30, LOG[1], LOG[2] + 115), 6)

# 16 Sighting gnomon on the rim: a pin parallel to the dish axis casting a shadow on a target
g0 = to_world(local_pt(R_AP - 40, math.radians(90), 0))
gn = tube3(g0, (g0[0] + AX.X * 180, g0[1] + AX.Y * 180, g0[2] + AX.Z * 180), 6)
tgt = Pos(*g0) * Rot(TILT, 0, 0) * Box(120, 120, 4)
sight = gn + tgt

parts = [
    Part("Reflector, polished aluminum petals", reflector, "#C7D2DC", 1, (0, -1000, -300)),
    Part("Dish ribs, rim and hub", dish_frame, "#6B7280", 2, (0, -1800, -600)),
    Part("Tilt yoke and quadrant lock", yoke, "#D4A017", 3, (0, 700, -350)),
    Part("Stand with castors", stand, "#374151", 4, (0, 0, -900)),
    Part("Level pot holder", holder, "#A16207", 5, (0, 0, 250)),
    Part("Pressure cooker body, 12 L", pot, "#1F2937", 6, (0, 0, 600)),
    Part("Lid with weighted regulator", lid, "#9CA3AF", 7, (0, 0, 1600)),
    Part("Pressure gauge", gauge, "#94A3B8", 8, (350, 0, 1850)),
    Part("Independent relief valve", relief, "#DC2626", 9, (-300, 0, 1850)),
    Part("Lid gland, Pt100 probe and pigtail", gland, "#7C3AED", 10, (0, 0, 2000)),
    Part("Insulated jacket", jacket, "#FDE68A", 11, (750, 0, 600)),
    Part("Water charge, 1.5 L", water, "#38BDF8", 12, (0, 0, 950)),
    Part("Instrument basket and trivet", basket, "#0F766E", 13, (0, 0, 1250)),
    Part("Cycle logger", logger, "#115E59", 14, (700, 0, 300)),
    Part("Logger solar panel, 5 W", panel, "#1E3A8A", 15, (800, 0, 750)),
    Part("Sighting gnomon", sight, "#EA580C", 16, (900, 300, 1000)),
    Part("Instrument load (not in BOM)", instruments, "#E5E7EB", None, (0, 0, 1250)),
]

render_all(
    parts, project="SunClave", title="Solar steam sterilizer concept", dwg_no="SCL-DWG-010",
    key_figures=["1.4 m dish, about 700 W to the pot at 750 W/m² DNI (estimate)",
                 "12 L cooker, 103 kPa gauge (15 psi): 121 °C at sea level",
                 "About 35 to 60 min heat-up, 30 min hold (estimate)",
                 "About 3 cycles per clear day (estimate)",
                 "Logger: Pt100 plus pressure, checks saturated steam",
                 "About $437 in parts (indicative)"],
    cut=False,  # cutaway rendered below, zoomed on the pressure vessel
    flow={"title": "power during heat-up at 700 W/m² DNI, W (all values are estimates)", "unit": "W",
          "stages": [("Sun on 1.54 m² dish", 1080), ("Onto pot base", 790), ("Absorbed by pot", 710),
                     ("Into the load", 610)],
          "losses": [(0, "Reflectance, spillage, shading", 290), (1, "Reflected off base", 80),
                     (2, "Pot surface loss (mean)", 100)]},
)

# Cutaway of the pressure vessel only. The parts are lowered to Z = 0 first because the kit's
# half-space cutter is centered on Z = 0 and would miss parts that sit about 1 m up.
VESSEL = {6, 7, 8, 9, 10, 11, 12, 13, None}
vessel = [Part(p.name, Pos(0, 0, -F_Z) * p.shape, p.color, p.bom) for p in parts if p.bom in VESSEL]
_render(cutaway_parts(vessel), ROOT / "media" / "cutaway.png", azim=-90, elev=18,
        title="SunClave: cutaway of the pressure vessel",
        note="6 cooker body, 7 lid, 9 relief valve, 10 Pt100 probe, 11 jacket, 12 water, 13 basket with instrument load")

# Tidy renderer scratch folders
import shutil
for d in (Path("media") / "_views", Path("media") / "_views_fig"):
    shutil.rmtree(d, ignore_errors=True)
