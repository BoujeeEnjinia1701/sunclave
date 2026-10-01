"""SunClave concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; figures come from SCL-CAL-001
(python docs/04-calcs/sizing.py). Not for fabrication.

The kit's cutaway cutter is centered on Z = 0, so the vessel parts are lowered to Z = 0
before cutting and rendered with the kit's cutaway_parts and _render directly.
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DIR = HERE.parents[1]
sys.path.insert(0, str(ROOT_DIR / ".kit"))
sys.path.insert(0, str(HERE))
from build123d import Pos  # noqa: E402
from concept import Part, render_all, cutaway_parts, _render, ROOT  # noqa: E402
from model import PARAMS as P, build_parts  # noqa: E402

STYLE = {   # bom: (colour, exploded-view offset in mm)
    1: ("#C7D2DC", (0, -900, 100)),
    2: ("#6B7280", (0, -2100, -500)),
    3: ("#D4A017", (0, -300, 700)),
    4: ("#A16207", (0, 1300, -1500)),
    5: ("#374151", (0, 0, 350)),
    6: ("#1F2937", (0, 0, 600)),
    7: ("#9CA3AF", (0, 0, 1500)),
    8: ("#94A3B8", (600, 0, 1800)),
    9: ("#DC2626", (-600, 0, 1800)),
    10: ("#7C3AED", (-450, 250, 1000)),
    11: ("#FDE68A", (750, 0, 600)),
    12: ("#38BDF8", (0, 0, 950)),
    13: ("#0F766E", (0, 0, 1250)),
    14: ("#115E59", (700, 0, 300)),
    15: ("#1E3A8A", (1100, 0, 250)),
    16: ("#EA580C", (0, -1500, 1300)),
    0: ("#E5E7EB", (0, 0, 1250)),
}

model = build_parts()
parts = [Part(name, shape, STYLE[k][0], k or None, STYLE[k][1]) for k, (name, shape) in sorted(model.items(), key=lambda kv: (kv[0] == 0, kv[0]))]

if __name__ == "__main__":
    render_all(
        parts, project="SunClave", title="Solar steam sterilizer concept", dwg_no="SCL-DWG-010",
        key_figures=["1.4 m dish: about 670 W absorbed at 700 W/m² DNI, 60 deg sun (SCL-CAL-001)",
                     "12 L cooker, 103.4 kPa gauge: 121.0 °C at sea level only",
                     "Cold start to end of 30 min hold about 80 min (estimate)",
                     "About 4 cycles in a 6 h clear window (estimate)",
                     "Logger: Pt100 plus pressure, checks saturated steam",
                     "About $440 in parts against $450 (indicative)"],
        cut=False,
        flow={"title": "power during heat-up at 700 W/m² DNI, W (SCL-CAL-001 central estimates)", "unit": "W",
              "stages": [("Sun on 1.54 m² dish", 1078), ("Reflected, unshaded", 819), ("Onto the vessel", 784),
                         ("Absorbed", 669), ("Into the load", 484)],
              "losses": [(0, "Shading and reflectance", 258), (1, "Spillage", 36), (2, "Reflected off paint", 115),
                         (3, "Surface loss (mean)", 184)]},
    )

    # Cutaway of the pressure vessel only, lowered to Z = 0 for the kit's cutter.
    VESSEL = {6, 7, 8, 9, 10, 11, 12, 13, None}
    vessel = [Part(p.name, Pos(0, 0, -P["F_Z"]) * p.shape, p.color, p.bom) for p in parts if p.bom in VESSEL]
    _render(cutaway_parts(vessel), ROOT / "media" / "cutaway.png", azim=-90, elev=18,
            title="SunClave: cutaway of the pressure vessel",
            note="6 cooker body, 7 lid, 9 relief valve, 10 Pt100 probe, 11 jacket, 12 water, 13 basket with load")

    for d in ("_views", "_views_fig"):
        shutil.rmtree(ROOT_DIR / "media" / d, ignore_errors=True)
