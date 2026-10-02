"""SunClave general arrangement drawing SCL-DWG-001 (Rev P3).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SCL-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses SCL-DWG-010. Figures quoted in the notes come
from SCL-CAL-001 (python docs/04-calcs/sizing.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assembly, build_parts, derived  # noqa: E402

parts = build_parts()
asm = assembly(parts)
bb = asm.bounding_box()
d = derived()

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="SunClave", title="General arrangement, TRL 3 model", dwg_no="SCL-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-10-01", concept=True, scale=1 / 20,
          material="Aluminum reflector, steel dish frame and yoke, treated timber stand. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (SCL-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Recommendations accepted by Amish (DDR-002): four locking castors, notes", "2026-09-25", "AC"),
                     ("P3", "Constructable design (SCL-DDR-003): joints, pivots, locks, holder, clips", "2026-10-01", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 40, 140, 64, label="Isometric view", sublabel="Not to scale; dish at 50 deg sun elevation")
s.add_notes("Key dimensions (mm) and data", [
    f"Overall {bb.size.X:.0f} W x {bb.size.Y:.0f} D x {bb.size.Z:.0f} H at 50 deg elevation",
    f"Dish {P['D_DISH']:.0f} dia, f = {P['FOCAL']:.0f}, depth {d['depth']:.0f}, rim angle {d['rim_angle']:.0f} deg",
    f"Focus and tilt axis {P['F_Z']:.0f} above ground; elevation {P['ELEV_MIN']:.0f} to {P['ELEV_MAX']:.0f} deg",
    f"Base {d['base_x']:.0f} x {P['BASE_Y']:.0f}, bolted timber; uprights at +/-{P['UPR_X']:.0f}; {P['CASTOR_LOCKS']} locking castors",
    f"Cooker 12 L, {P['POT_ID']:.0f} ID x {P['POT_IH']:.0f} deep; base on the focal plane",
    f"Black base and {P['BARE_BAND']:.0f} mm wall band; {P['JKT_T']:.0f} mm jacket above",
    f"Basket {P['BASKET_D']:.0f} x {P['BASKET_H']:.0f} on {P['TRIVET_H']:.0f} trivet; 1.5 L water",
    "Holder ring fixed to the stand; yoke plates turn on fixed 20 mm axles",
    "Two friction locks: star knobs on M10 studs in 150 mm radius slots",
    "Regulator 103.4 kPa gauge; relief 125 kPa gauge or less",
    "Lid fittings: mounting method open (design decisions register)",
    "About 44.7 kg empty (limit 45); largest piece about 16 kg",
    "Vessel is a hot zone; mark a 2 m keep-out (R11)",
    "At risk at TRL 3: R4, R15. See SCL-CAL-001 v0.3; build plan SCL-BLD-001",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=118, width=140)
s.save(ROOT / "cad/drawings/SCL-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SCL-DWG-001.svg, .pdf, .png")
