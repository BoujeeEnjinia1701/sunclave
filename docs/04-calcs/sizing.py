"""SunClave TRL 3 sizing and first-principles checks (SCL-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.

Geometry comes from PARAMS in cad/src/model.py and prices from bom/bom.csv, so the
model, the drawing SCL-DWG-001 and the note agree. Everything here is a paper estimate
for a research and educational prototype, not a medical device. Nothing is measured.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, point_world  # noqa: E402

D = derived(P)
SIGMA = 5.670374e-8
G = 9.81
OUT = []          # (section, quantity, value) lines for the log
RESULTS = []      # requirement rows


def say(msg=""):
    print(msg)


# ---------------------------------------------------------------- 1. Water and air properties
def psat_kpa(t_c):
    """Saturation pressure of water, IAPWS-IF97 region 4 (kPa)."""
    n = [0.11670521452767e4, -0.72421316703206e6, -0.17073846940092e2, 0.12020824702470e5,
         -0.32325550322333e7, 0.14915108613530e2, -0.48232657361591e4, 0.40511340542057e6,
         -0.23855557567849, 0.65017534844798e3]
    T = t_c + 273.15
    th = T + n[8] / (T - n[9])
    A = th ** 2 + n[0] * th + n[1]
    B = n[2] * th ** 2 + n[3] * th + n[4]
    C = n[5] * th ** 2 + n[6] * th + n[7]
    return 1000 * (2 * C / (-B + math.sqrt(B * B - 4 * A * C))) ** 4


def tsat_c(p_kpa):
    """Saturation temperature of water, IAPWS-IF97 region 4 (degrees C)."""
    n = [0.11670521452767e4, -0.72421316703206e6, -0.17073846940092e2, 0.12020824702470e5,
         -0.32325550322333e7, 0.14915108613530e2, -0.48232657361591e4, 0.40511340542057e6,
         -0.23855557567849, 0.65017534844798e3]
    b = (p_kpa / 1000) ** 0.25
    E = b * b + n[2] * b + n[5]
    F = n[0] * b * b + n[3] * b + n[6]
    Gg = n[1] * b * b + n[4] * b + n[7]
    Dd = 2 * Gg / (-F - math.sqrt(F * F - 4 * E * Gg))
    return (n[9] + Dd - math.sqrt((n[9] + Dd) ** 2 - 4 * (n[8] + n[9] * Dd))) / 2 - 273.15


def p_amb_kpa(h_m):
    """ICAO standard atmosphere, troposphere."""
    return 101.325 * (1 - 2.25577e-5 * h_m) ** 5.25588


def hfg(t_c):
    """Latent heat of water, kJ/kg, linear between steam-table values at 100 and 125 degrees C."""
    return 2256.4 + (2188.1 - 2256.4) * (t_c - 100) / 25


P_REG = 103.4       # kPa gauge, 15 psi weighted regulator
P_RELIEF = 125.0    # kPa gauge, independent relief valve set point (R8)
Z_VALUE = 10.0      # K, assumed for equivalent exposure (not validated)
T_REF = 121.0

# ---------------------------------------------------------------- 2. Scenarios
SCEN = {
    "favourable":   dict(rho=0.88, slope=6e-3, alpha=0.95, wind=1.0),
    "central":      dict(rho=0.85, slope=10e-3, alpha=0.92, wind=2.0),
    "unfavourable": dict(rho=0.78, slope=15e-3, alpha=0.88, wind=3.0),
}
DNI = 700.0          # W/m2, design case
T_AMB = 25.0
ELEV_DESIGN = 60.0   # sun elevation for the design case (degrees)
SUN_HALF = 4.65e-3   # rad, solar disc half-angle (pillbox sunshape)
RATE = 15.0          # degrees per hour, worst-case apparent sun motion
RETARGET_MIN = 12.0  # minutes between retargets (R14, relaxed from 15 min by SCL-DDR-002 item 13)
TRANSDUCER_KPA = 300.0  # absolute pressure transducer span (SCL-DDR-002 item 18; was 500 kPa)
MASS_MAX = 45.0      # kg, R16 total (relaxed from 40 kg by SCL-DDR-002 item 14)
TRIM_HOLD_MIN = 40.0  # logger trim reminder when the computed hold exceeds this (SCL-DDR-002 item 17)
N_RAYS = 60000

A_AP = math.pi * D["R"] ** 2 / 1e6          # m2


def optics(elev, sc, delta=0.0, ddir="elev", seed=1, flux_map=False):
    """Monte Carlo ray trace of the dish onto the level cooker. Returns fractions of DNI x aperture area."""
    rng = np.random.default_rng(seed)
    R, f = D["R"], P["FOCAL"]
    FZ = P["F_Z"]
    ro, rj = D["pot_or"], D["jkt_or"]
    band = P["BARE_BAND"]
    ztop = FZ + D["pot_oh"] - 30
    N = N_RAYS
    r = R * np.sqrt(rng.random(N)); ph = 2 * np.pi * rng.random(N)
    x, y = r * np.cos(ph), r * np.sin(ph); z = r * r / (4 * f)
    n0 = np.stack([-x / (2 * f), -y / (2 * f), np.ones(N)], 1)
    n0 /= np.linalg.norm(n0, axis=1)[:, None]
    t1 = np.stack([-np.sin(ph), np.cos(ph), np.zeros(N)], 1)
    t2 = np.cross(n0, t1)
    g = rng.normal(0, sc["slope"], (N, 2))
    n = n0 + g[:, :1] * t1 + g[:, 1:] * t2
    n /= np.linalg.norm(n, axis=1)[:, None]
    # sun direction (toward the sun) in the dish frame with pillbox sunshape and pointing error
    a = SUN_HALF * np.sqrt(rng.random(N)); b = 2 * np.pi * rng.random(N)
    ex, ey = a * np.cos(b), a * np.sin(b)
    dr = math.radians(delta)
    if ddir == "elev":
        ey = ey + dr
    else:
        ex = ex + dr
    s = np.stack([np.tan(ex), np.tan(ey), np.ones(N)], 1)
    s /= np.linalg.norm(s, axis=1)[:, None]
    din = -s
    dout = din - 2 * np.sum(din * n, 1)[:, None] * n
    # to world
    t = math.radians(90 - elev)
    ct, st = math.cos(t), math.sin(t)
    V = np.array([0.0, f * st, FZ - f * ct])

    def rot(v):
        return np.stack([v[:, 0], v[:, 1] * ct - v[:, 2] * st, v[:, 1] * st + v[:, 2] * ct], 1)
    Pw = rot(np.stack([x, y, z], 1)) + V
    Sw = rot(s)
    Dw = rot(dout)

    # shading of the incoming sun by the vessel, holder ring and holder arms
    r_sh = ro + 30
    shaded = _hits_cyl(Pw, Sw, r_sh, FZ, FZ + D["pot_oh"] + 60)
    z_arm = FZ + P["HOLDER_Z"] - P["HOLDER_W"] / 2
    shaded |= _hits_box(Pw, Sw, (-P["UPR_X"], P["UPR_X"]), (-10, 10), (z_arm - 12.5, z_arm + 12.5))

    # receiver: base disk, bare band (absorbing), jacket (lost)
    INF = np.full(N, np.inf)
    with np.errstate(divide="ignore", invalid="ignore"):
        lb = np.where(Dw[:, 2] > 1e-9, (FZ - Pw[:, 2]) / Dw[:, 2], np.inf)
    hb = Pw + lb[:, None] * Dw
    ok = (lb > 0) & (hb[:, 0] ** 2 + hb[:, 1] ** 2 <= ro ** 2)
    l_base = np.where(ok, lb, INF)
    l_band, zb = _cyl_entry(Pw, Dw, ro)
    l_band = np.where((zb >= FZ) & (zb <= FZ + band), l_band, INF)
    l_jk, zj = _cyl_entry(Pw, Dw, rj)
    l_jk = np.where((zj >= FZ + band) & (zj <= ztop), l_jk, INF)
    with np.errstate(divide="ignore", invalid="ignore"):
        la = np.where(Dw[:, 2] > 1e-9, (FZ + band - Pw[:, 2]) / Dw[:, 2], np.inf)
    ha = Pw + la[:, None] * Dw
    ra = ha[:, 0] ** 2 + ha[:, 1] ** 2
    l_ann = np.where((la > 0) & (ra >= ro ** 2) & (ra <= rj ** 2), la, INF)
    L = np.stack([l_base, l_band, l_jk, l_ann], 1)
    first = np.argmin(L, 1)
    hit = np.isfinite(L.min(1))
    # incidence angle on the absorbing surfaces
    cos_base = np.clip(Dw[:, 2], 0, 1)
    hp = Pw + np.where(np.isfinite(l_band), l_band, 0)[:, None] * Dw
    rad = hp[:, :2] / ro
    cos_band = np.clip(-(rad[:, 0] * Dw[:, 0] + rad[:, 1] * Dw[:, 1]), 0, 1)
    cosi = np.where(first == 0, cos_base, cos_band)
    th = np.degrees(np.arccos(np.clip(cosi, 0, 1)))
    alpha = sc["alpha"] * np.where(th <= 60, 1.0, 1 - 0.5 * (th - 60) / 30)
    live = ~shaded
    on_abs = live & hit & (first <= 1)
    on_vessel = live & hit
    res = {
        "unshaded": live.mean(),
        "reflected": sc["rho"] * live.mean(),
        "onto_vessel": sc["rho"] * on_vessel.mean(),
        "onto_absorber": sc["rho"] * on_abs.mean(),
        "absorbed": sc["rho"] * np.where(on_abs, alpha, 0).mean(),
        "base_share": (on_abs & (first == 0)).sum() / max(on_abs.sum(), 1),
    }
    if flux_map:
        m = on_abs & (first == 0)
        hx, hy = hb[m, 0], hb[m, 1]
        w = 20.0
        H, _, _ = np.histogram2d(hx, hy, bins=int(2 * ro / w), range=[[-ro, ro], [-ro, ro]])
        per_ray = DNI * A_AP * sc["rho"] / N          # W per ray on the aperture, after reflectance
        res["peak_flux"] = H.max() * per_ray / (w / 1000) ** 2
        res["mean_flux_base"] = m.sum() * per_ray / (math.pi * (ro / 1000) ** 2)
    return res


def _cyl_entry(Pw, Dw, r):
    a = Dw[:, 0] ** 2 + Dw[:, 1] ** 2
    b = 2 * (Pw[:, 0] * Dw[:, 0] + Pw[:, 1] * Dw[:, 1])
    c = Pw[:, 0] ** 2 + Pw[:, 1] ** 2 - r * r
    disc = b * b - 4 * a * c
    with np.errstate(invalid="ignore", divide="ignore"):
        l = (-b - np.sqrt(disc)) / (2 * a)
    l = np.where((disc > 0) & (a > 1e-12) & (l > 0), l, np.inf)
    z = Pw[:, 2] + np.where(np.isfinite(l), l, 0) * Dw[:, 2]
    return l, z


def _hits_cyl(Pw, Sw, r, z0, z1):
    """Ray P + l S (l > 0) passes through the vertical cylinder of radius r between z0 and z1."""
    a = Sw[:, 0] ** 2 + Sw[:, 1] ** 2
    b = 2 * (Pw[:, 0] * Sw[:, 0] + Pw[:, 1] * Sw[:, 1])
    c = Pw[:, 0] ** 2 + Pw[:, 1] ** 2 - r * r
    disc = b * b - 4 * a * c
    hit = np.zeros(len(Pw), bool)
    with np.errstate(invalid="ignore", divide="ignore"):
        sq = np.sqrt(np.maximum(disc, 0))
        l1 = np.where(a > 1e-12, (-b - sq) / (2 * a), -np.inf)
        l2 = np.where(a > 1e-12, (-b + sq) / (2 * a), np.inf)
    vert = a <= 1e-12
    inside_now = c <= 0
    l1 = np.where(vert, np.where(inside_now, 0, np.inf), np.maximum(l1, 0))
    l2 = np.where(vert, np.where(inside_now, np.inf, -np.inf), l2)
    valid = (disc > 0) | vert
    # z range along the segment inside the infinite cylinder
    za = Pw[:, 2] + l1 * Sw[:, 2]
    zb = Pw[:, 2] + np.minimum(l2, 1e7) * Sw[:, 2]
    lo, hi = np.minimum(za, zb), np.maximum(za, zb)
    hit = valid & (l2 > l1) & (hi >= z0) & (lo <= z1)
    return hit


def _hits_box(Pw, Sw, xr, yr, zr):
    """Slab test: ray P + l S (l > 0) meets the axis-aligned box."""
    lo = np.zeros(len(Pw)); hi = np.full(len(Pw), np.inf)
    for k, (a, b) in enumerate((xr, yr, zr)):
        d = Sw[:, k]; p = Pw[:, k]
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = (a - p) / d; t2 = (b - p) / d
        par = np.abs(d) < 1e-12
        inside = (p >= a) & (p <= b)
        tmin = np.where(par, np.where(inside, -np.inf, np.inf), np.minimum(t1, t2))
        tmax = np.where(par, np.where(inside, np.inf, -np.inf), np.maximum(t1, t2))
        lo = np.maximum(lo, tmin); hi = np.minimum(hi, tmax)
    return hi >= lo


# ---------------------------------------------------------------- 3. Vessel masses and areas
RHO_AL, RHO_ST, RHO_TIMBER = 2700.0, 7850.0, 500.0
ri, ro = P["POT_ID"] / 2000, D["pot_or"] / 1000
m_body = RHO_AL * (math.pi * ro ** 2 * P["POT_BASE"] / 1000 + 2 * math.pi * ro * P["POT_IH"] / 1000 * P["POT_WALL"] / 1000)
m_lid = RHO_AL * math.pi * (P["LID_D"] / 2000) ** 2 * P["LID_T"] / 1000
m_fit = 0.10 + 0.35 + 0.20 + 0.25      # regulator, gauge, relief valve, gland with probe and tee (kg, typical)
M_INSTR, M_BASKET = 2.0, 0.5
C_AL, C_SS, C_BRASS, C_W = 0.90, 0.50, 0.38, 4.19   # kJ/(kg K)
A_LID = math.pi * (P["LID_D"] / 2000) ** 2
A_BASE = math.pi * ro ** 2
A_BAND = 2 * math.pi * ro * P["BARE_BAND"] / 1000
H_JKT = (D["pot_oh"] - P["BARE_BAND"] - 30) / 1000
A_TOPBAND = 2 * math.pi * ro * 0.030          # bare wall above the jacket, under the lid rim
A_FIT = 0.03                                   # handles, fittings, gauge: extra bare area (assumption)
C_VESSEL = (m_body + m_lid) * C_AL + m_fit * C_BRASS + M_INSTR * C_SS + M_BASKET * C_SS    # kJ/K, without water


def h_conv(v):
    """Watmuff, Charters and Proctor (1977) wind convection coefficient, W/(m2 K)."""
    return 2.8 + 3.0 * v


def loss_w(T, wind, detail=False):
    """Heat loss from the vessel at uniform temperature T (degrees C), ambient T_AMB."""
    Ta = T_AMB + 273.15
    hc = h_conv(wind)

    def bare(area, eps, Ts):
        Tk = Ts + 273.15
        return area * (hc * (Ts - T_AMB) + eps * SIGMA * (Tk ** 4 - Ta ** 4))
    base_T = T + 5.0
    q_base = bare(A_BASE + A_BAND, 0.90, base_T)          # blackened base and band
    q_lid = bare(A_LID + A_TOPBAND, 0.20, T)              # oxidized aluminum
    q_fit = bare(A_FIT, 0.50, T - 10)
    # jacket: 25 mm mineral wool, aluminized cloth skin (eps 0.3)
    r1, r2 = ro, D["jkt_or"] / 1000
    Ts = T_AMB + 5
    for _ in range(50):
        km = 0.040 + 0.0002 * ((T + Ts) / 2 - 50)
        Rw = math.log(r2 / r1) / (2 * math.pi * km * H_JKT)
        Ao = 2 * math.pi * r2 * H_JKT + math.pi * (r2 ** 2 - r1 ** 2)
        Tsk = Ts + 273.15
        ho = hc + 0.3 * SIGMA * (Tsk ** 2 + Ta ** 2) * (Tsk + Ta)
        q = (T - T_AMB) / (Rw + 1 / (ho * Ao))
        Ts = T_AMB + q / (ho * Ao)
    q_jkt = q
    tot = q_base + q_lid + q_fit + q_jkt
    if detail:
        return tot, dict(base_band=q_base, lid=q_lid, fittings=q_fit, jacket=q_jkt, jacket_skin_T=Ts)
    return tot


# ---------------------------------------------------------------- 4. Cycle simulation
def cycle(q_abs_fn, wind, alt_m=0.0, hold_ref_min=30.0, water_l=None, T0=T_AMB, t_start=0.0, dt=5.0, trim=False):
    """Simulate one cycle. q_abs_fn(t_s) gives absorbed power (W) at absolute time t_s.
    Returns a dict of phase times (min), water used (kg) and the regulated temperature."""
    water = P["WATER_L"] if water_l is None else water_l
    pa = p_amb_kpa(alt_m)
    Tb = tsat_c(pa)
    Tr = tsat_c(pa + P_REG)
    hold = hold_ref_min * 10 ** ((T_REF - Tr) / Z_VALUE) if Tr < T_REF else hold_ref_min
    T, t, mw = T0, t_start, water
    tt = {}
    # a) heat to boiling with the vent open
    while T < Tb:
        C = C_VESSEL + mw * C_W
        T += (q_abs_fn(t) - loss_w(T, wind)) * dt / (C * 1000)
        t += dt
        if t - t_start > 6 * 3600:
            return None
    tt["to_boil"] = (t - t_start) / 60
    # b) purge 5 min of free steaming
    t_p = 0.0
    while t_p < 300:
        mw -= max(q_abs_fn(t) - loss_w(Tb, wind), 0) * dt / (hfg(Tb) * 1000)
        t += dt; t_p += dt
    purge_kg = water - mw
    # c) regulator fitted: heat to the regulated temperature
    t1 = t
    while T < Tr:
        C = C_VESSEL + mw * C_W
        T += (q_abs_fn(t) - loss_w(T, wind)) * dt / (C * 1000)
        t += dt
        if t - t_start > 6 * 3600:
            return None
    tt["to_reg"] = (t - t1) / 60
    t_heat = t
    # d) hold, surplus vented through the regulator (no trimming unless trim=True)
    t_h = 0.0
    while t_h < hold * 60:
        s = q_abs_fn(t) - loss_w(Tr, wind)
        if trim:
            s = min(s, 50.0)
        mw -= max(s, 0) * dt / (hfg(Tr) * 1000)
        t += dt; t_h += dt
    # e) dish off the sun, cool to zero gauge by losses alone
    C = C_VESSEL + mw * C_W
    t_cool = C * 1000 * (Tr - Tb) / loss_w((Tr + Tb) / 2, wind) / 60
    return dict(to_boil=tt["to_boil"], heat=(t_heat - t_start) / 60, hold=hold, total=(t - t_start) / 60, cool=t_cool,
                purge_kg=purge_kg, water_left=mw, Tr=Tr, Tb=Tb, t_end=t, hold_used=water - purge_kg - mw)


def mean_absorbed(elev, sc, interval_min=RETARGET_MIN):
    """Mean absorbed fraction over a retarget interval: pointing error grows from 0 at RATE."""
    dmax = RATE * interval_min / 60
    ds = np.linspace(0, dmax, 6)
    vals = [0.5 * (optics(elev, sc, d, "elev")["absorbed"] + optics(elev, sc, d, "az")["absorbed"]) for d in ds]
    return float(np.mean(vals))


def sun_elev(lat, dec, hour):
    la, de = math.radians(lat), math.radians(dec)
    h = math.radians(15 * (hour - 12))
    return math.degrees(math.asin(math.sin(la) * math.sin(de) + math.cos(la) * math.cos(de) * math.cos(h)))


# ================================================================== main
if __name__ == "__main__":
    np.set_printoptions(precision=3)
    say("SCL-CAL-001 SunClave sizing (python docs/04-calcs/sizing.py)")
    say("=" * 72)

    # ---------- geometry
    say("\n1. Geometry from cad/src/model.py")
    say(f"  aperture {P['D_DISH']:.0f} mm, area {A_AP:.3f} m2, focal length {P['FOCAL']:.0f} mm, depth {D['depth']:.0f} mm, rim angle {D['rim_angle']:.1f} deg")
    R, f = D["R"] / 1000, P["FOCAL"] / 1000
    A_para = 8 * math.pi * f ** 2 / 3 * ((1 + R ** 2 / (4 * f ** 2)) ** 1.5 - 1)
    say(f"  reflector surface {A_para:.2f} m2 (paraboloid); cut sheet with 5 % offcut {A_para * 1.05:.2f} m2")
    vol_in = math.pi * ri ** 2 * P["POT_IH"] / 1000 * 1000
    say(f"  cooker inside {P['POT_ID']:.0f} x {P['POT_IH']:.0f} mm = {vol_in:.1f} L; outside diameter {2 * D['pot_or']:.0f} mm")
    say(f"  water 1.5 L is {D['water_depth']:.1f} mm deep; trivet {P['TRIVET_H']:.0f} mm leaves {P['TRIVET_H'] - D['water_depth']:.1f} mm clearance to the basket")
    head = P["POT_IH"] - P["TRIVET_H"] - P["BASKET_H"]
    say(f"  basket {P['BASKET_D']:.0f} x {P['BASKET_H']:.0f} mm; radial clearance {(P['POT_ID'] - P['BASKET_D']) / 2:.0f} mm; headroom under the lid rim {head:.0f} mm")
    say(f"  vessel masses: body {m_body:.2f} kg, lid {m_lid:.2f} kg, fittings {m_fit:.2f} kg; heat capacity without water {C_VESSEL:.2f} kJ/K")

    # ---------- saturation and altitude
    say("\n2. Steam temperature and altitude (IAPWS-IF97, ICAO standard atmosphere)")
    alts = [0, 250, 500, 1000, 1500, 1800, 2400]
    T0 = tsat_c(p_amb_kpa(0) + P_REG)
    say(f"  sea level: ambient {p_amb_kpa(0):.1f} kPa, boiling {tsat_c(p_amb_kpa(0)):.1f} C, at {P_REG} kPa gauge {T0:.2f} C")
    lo, hi = -500.0, 3000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if tsat_c(p_amb_kpa(mid) + P_REG) >= T_REF else (lo, mid)
    h121 = lo
    say(f"  a {P_REG} kPa regulator reaches {T_REF} C up to {h121:.0f} m only")
    alt_rows = []
    for h in alts:
        pa = p_amb_kpa(h); Tr = tsat_c(pa + P_REG)
        pg = psat_kpa(T_REF) - pa
        f20 = 20 * 10 ** ((T_REF - Tr) / Z_VALUE) if Tr < T_REF else 20
        f30 = 30 * 10 ** ((T_REF - Tr) / Z_VALUE) if Tr < T_REF else 30
        alt_rows.append((h, pa, tsat_c(pa), Tr, pg, f20, f30))
        say(f"  {h:5.0f} m  ambient {pa:6.1f} kPa  boil {tsat_c(pa):5.1f} C  steam {Tr:6.2f} C  gauge for 121 C {pg:5.1f} kPa  hold 20/30 min -> {f20:4.0f}/{f30:4.0f} min")
    T_relief = tsat_c(p_amb_kpa(0) + P_RELIEF)
    say(f"  relief valve at {P_RELIEF} kPa gauge: {T_relief:.1f} C at sea level (R1 upper limit 124 C)")

    # ---------- optics
    say("\n3. Optics: Monte Carlo ray trace onto the level cooker (60,000 rays)")
    sc = SCEN["central"]
    opt_rows = {}
    for el in (15, 30, 45, 60, 75, 90):
        o = optics(el, sc)
        opt_rows[el] = o
        say(f"  elevation {el:2d} deg: unshaded {o['unshaded']:.3f}, onto vessel {o['onto_vessel']:.3f}, onto black {o['onto_absorber']:.3f}, "
            f"absorbed {o['absorbed']:.3f} ({o['absorbed'] * DNI * A_AP:.0f} W), base share {o['base_share']:.2f}")
    od = optics(ELEV_DESIGN, sc, flux_map=True)
    flow = dict(sun=DNI * A_AP, reflected=od["reflected"] * DNI * A_AP, vessel=od["onto_vessel"] * DNI * A_AP,
                black=od["onto_absorber"] * DNI * A_AP, absorbed=od["absorbed"] * DNI * A_AP)
    say(f"  design case (elevation {ELEV_DESIGN:.0f}): sun {flow['sun']:.0f} W, reflected unshaded {flow['reflected']:.0f} W, onto vessel {flow['vessel']:.0f} W, "
        f"onto black surfaces {flow['black']:.0f} W, absorbed {flow['absorbed']:.0f} W")
    say(f"  optical efficiency to absorbed {od['absorbed']:.3f}; peak flux on the base {od['peak_flux'] / 1000:.0f} kW/m2, mean over base {od['mean_flux_base'] / 1000:.1f} kW/m2")
    for name, s in SCEN.items():
        o = optics(ELEV_DESIGN, s)
        say(f"  {name:12s}: absorbed fraction {o['absorbed']:.3f} = {o['absorbed'] * DNI * A_AP:.0f} W")
    # pointing tolerance
    say("  pointing error (central, elevation 60): absorbed fraction")
    base0 = od["absorbed"]
    tol = None
    prev = (0.0, 1.0)
    for dd in np.arange(0.0, 8.01, 0.5):
        v = 0.5 * (optics(ELEV_DESIGN, sc, dd, "elev")["absorbed"] + optics(ELEV_DESIGN, sc, dd, "az")["absorbed"])
        rel = v / base0
        say(f"    {dd:3.1f} deg: {v:.3f} ({rel * 100:5.1f} % of on-target)")
        if tol is None and rel < 0.90:
            tol = prev[0] + (0.90 - prev[1]) / (rel - prev[1]) * (dd - prev[0])
        prev = (dd, rel)
    t_tol = tol / RATE * 60
    say(f"  90 % point: {tol:.1f} deg, reached after {t_tol:.0f} min of sun motion at {RATE:.0f} deg/h")
    off = None
    for dd in np.arange(5, 40.1, 1.0):
        v = optics(ELEV_DESIGN, sc, dd, "elev")["absorbed"]
        if v < 0.05 * base0:
            off = dd; break
    say(f"  absorbed power falls below 5 % of on-target at a tilt error of {off:.0f} deg (R9: turn the dish this far)")

    # ---------- losses
    say("\n4. Heat loss from the vessel (design case wind 2 m/s, ambient 25 C)")
    for T in (60.0, 100.0, 121.0):
        tot, dd = loss_w(T, sc["wind"], True)
        say(f"  at {T:5.1f} C: total {tot:5.0f} W (base and band {dd['base_band']:.0f}, lid {dd['lid']:.0f}, fittings {dd['fittings']:.0f}, jacket {dd['jacket']:.0f}); jacket skin {dd['jacket_skin_T']:.0f} C")

    # ---------- design cycle
    say(f"\n5. Design cycle, sea level, 30 min hold, retarget every {RETARGET_MIN:.0f} min")
    cyc = {}
    for name, s in SCEN.items():
        qa = mean_absorbed(ELEV_DESIGN, s) * DNI * A_AP
        c = cycle(lambda t, q=qa: q, s["wind"])
        cyc[name] = (qa, c)
        say(f"  {name:12s}: mean absorbed {qa:4.0f} W; cold start to 121 C {c['heat']:5.1f} min (to boiling {c['to_boil']:.1f});"
            f" to end of hold {c['total']:5.1f} min; water left {c['water_left']:.2f} kg; cool-down {c['cool']:.0f} min")
    qa_c, cc = cyc["central"]
    loss_heat = loss_w(0.5 * (T_AMB + cc["Tr"]), sc["wind"])
    say(f"  central: purge {cc['purge_kg']:.3f} kg, hold {cc['hold_used']:.3f} kg of steam; mean loss during heat-up about {loss_heat:.0f} W")
    say(f"  flow diagram (design case, on target): sun {flow['sun']:.0f} W, reflected {flow['reflected']:.0f} W, onto vessel {flow['vessel']:.0f} W, "
        f"absorbed {flow['absorbed']:.0f} W, into the load {flow['absorbed'] - loss_heat:.0f} W; losses: shading and reflectance {flow['sun'] - flow['reflected']:.0f}, "
        f"spillage {flow['reflected'] - flow['vessel']:.0f}, reflected off the paint {flow['vessel'] - flow['absorbed']:.0f}, surface loss {loss_heat:.0f}")
    c20 = cycle(lambda t: qa_c, sc["wind"], hold_ref_min=20)
    say(f"  central, 20 min hold (unwrapped): {c20['total']:.1f} min")
    at600 = cycle(lambda t: qa_c * 600 / DNI, sc["wind"])
    say(f"  central at 600 W/m2: {at600['total']:.1f} min to end of hold")
    hi = optics(ELEV_DESIGN, SCEN["favourable"])["absorbed"] * 1000 * A_AP
    cw = cycle(lambda t: hi, SCEN["favourable"]["wind"])
    say(f"  worst water case (favourable optics, 1000 W/m2, no trimming): water left {cw['water_left']:.2f} kg")
    # altitude cycles (option B, decided)
    say("  option B at altitude (central, 30 min reference hold):")
    alt_cyc = {}
    for h in (0, 1000, 1800, 2400):
        c = cycle(lambda t: qa_c, sc["wind"], alt_m=h)
        c_hi = cycle(lambda t: hi, SCEN["favourable"]["wind"], alt_m=h)
        alt_cyc[h] = (c, c_hi)
        say(f"    {h:4d} m: steam {c['Tr']:.1f} C, hold {c['hold']:.0f} min, cycle {c['total']:.0f} min, water left {c['water_left']:.2f} kg "
            f"(at 1000 W/m2 with favourable optics {c_hi['water_left']:.2f} kg)")
    ct = cycle(lambda t: hi, SCEN["favourable"]["wind"], alt_m=1800, trim=True)
    say(f"  1,800 m, 1000 W/m2, dish trimmed to about 50 W of venting during the hold: water left {ct['water_left']:.2f} kg")
    ct24 = cycle(lambda t: hi, SCEN["favourable"]["wind"], alt_m=2400, trim=True)
    say(f"  2,400 m, 1000 W/m2, dish trimmed the same way: water left {ct24['water_left']:.2f} kg")
    say(f"  trimming rule (decided): the logger shows a trim reminder whenever the computed hold exceeds {TRIM_HOLD_MIN:.0f} min;"
        f" untrimmed, the 46 min hold at 1,000 m leaves {alt_cyc[1000][1]['water_left']:.2f} kg in strong sun")

    # ---------- day
    say("\n6. Cycles in the clear-day window, 09:00 to 15:00 solar time")
    day = {}
    for label, lat, dec, dni in (("equator, equinox, 700 W/m2", 0.0, 0.0, 700.0),
                                 ("15 N, winter solstice, 700 W/m2", 15.0, -23.44, 700.0),
                                 ("equator, equinox, 600 W/m2", 0.0, 0.0, 600.0)):
        els = {e: None for e in (15, 30, 45, 60, 75, 90)}
        tab = {e: mean_absorbed(e, sc) for e in els}
        xs = sorted(tab)

        def q_of(ts, lat=lat, dec=dec, dni=dni):
            e = max(15.0, sun_elev(lat, dec, ts / 3600))
            return float(np.interp(e, xs, [tab[k] for k in xs])) * dni * A_AP
        t = 9 * 3600.0
        Tstart = T_AMB
        n = 0
        times = []
        while True:
            c = cycle(q_of, sc["wind"], T0=Tstart, t_start=t)
            if c is None or c["t_end"] > 15 * 3600:
                break
            n += 1
            times.append((t / 3600, c["t_end"] / 3600))
            t = c["t_end"] + (c["cool"] + 10) * 60
            # warm restart: pot and remaining water at the local boiling point, fresh instruments and top-up water at 25 C
            Cp = (m_body + m_lid) * C_AL + m_fit * C_BRASS + M_BASKET * C_SS
            mix = (Cp * c["Tb"] + c["water_left"] * C_W * c["Tb"] + (1.5 - c["water_left"]) * C_W * T_AMB + M_INSTR * C_SS * T_AMB) / (Cp + 1.5 * C_W + M_INSTR * C_SS)
            Tstart = mix
        day[label] = (n, times)
        say(f"  {label}: {n} complete cycles; " + ", ".join(f"{a:.2f} to {b:.2f} h" for a, b in times))
    say(f"  warm restart temperature about {Tstart:.0f} C")

    # ---------- measurement
    say("\n7. Measurement (R7, R12)")
    t121 = 121.0
    a_pt = 3.9083e-3; b_pt = -5.775e-7
    R_T = 100 * (1 + a_pt * t121 + b_pt * t121 ** 2)
    dRdT = 100 * (a_pt + 2 * b_pt * t121)
    e_class = 0.15 + 0.002 * t121
    e_ref01 = R_T * 0.001 / dRdT
    e_ref005 = R_T * 0.0005 / dRdT
    e_adc = 430 / 2 ** 15 / dRdT
    u01 = math.sqrt(e_class ** 2 + e_ref01 ** 2 + e_adc ** 2)
    u005 = math.sqrt(e_class ** 2 + e_ref005 ** 2 + e_adc ** 2)
    say(f"  Pt100 at 121 C: {R_T:.2f} ohm, {dRdT:.4f} ohm/K; class A {e_class:.2f} K; 0.1 % reference resistor {e_ref01:.2f} K; 0.05 % {e_ref005:.2f} K; 15-bit step {e_adc:.3f} K")
    say(f"  temperature uncertainty (root sum square): {u01:.2f} K with a 0.1 % reference, {u005:.2f} K with 0.05 %")
    p_abs = p_amb_kpa(0) + P_REG
    dTdp = (tsat_c(p_abs + 1) - tsat_c(p_abs - 1)) / 2
    e_p = 0.01 * TRANSDUCER_KPA
    u_sat = math.sqrt((dTdp * e_p) ** 2 + u005 ** 2)
    say(f"  pressure 1 % of {TRANSDUCER_KPA:.0f} kPa = {e_p:.1f} kPa; dTsat/dp {dTdp:.3f} K/kPa at {p_abs:.0f} kPa -> {dTdp * e_p:.2f} K; saturation check uncertainty {u_sat:.2f} K")
    # air fraction for a 2 K deficit
    for dT in (2.0, u_sat, 2.0 + u_sat):
        x_air = 1 - psat_kpa(tsat_c(p_abs) - dT) / p_abs
        say(f"  a {dT:.2f} K deficit means {x_air * 100:.1f} % air by volume in the chamber")
    dTdp_b = (tsat_c(p_amb_kpa(0) + 1) - tsat_c(p_amb_kpa(0) - 1)) / 2
    u500 = math.sqrt((dTdp * 5.0) ** 2 + u005 ** 2)
    say(f"  with the 0.05 % reference: saturation check {u_sat:.2f} K on the decided 0 to {TRANSDUCER_KPA:.0f} kPa transducer, {u500:.2f} K on the earlier 0 to 500 kPa (5 kPa)")
    say(f"  highest absolute pressure in normal use {p_amb_kpa(0) + P_REG:.0f} kPa, at relief lift {p_amb_kpa(0) + P_RELIEF:.0f} kPa, inside the {TRANSDUCER_KPA:.0f} kPa span;"
        " the transducer's overpressure rating must exceed the relief set point")
    say(f"  check uncertainty is {u_sat / 2 * 100:.0f} % of the 2 K threshold (a 3:1 ratio needs 33 % or less)")
    say(f"  field check in boiling water: {dTdp_b:.3f} K/kPa, so a {e_p:.0f} kPa pressure error is {dTdp_b * e_p:.1f} K and a 0.2 kPa barometer {dTdp_b * 0.2:.2f} K")

    # ---------- pressure safety
    say("\n8. Pressure safety (R8), both lid options")
    q_max = optics(90, SCEN["favourable"])["absorbed"] * 1000 * A_AP
    m_max = q_max / (hfg(121) * 1000)

    def choked(p_kpa, T_c, d_mm, cd):
        k, Rv = 1.30, 461.5
        A = math.pi * (d_mm / 2000) ** 2
        return cd * A * p_kpa * 1000 * math.sqrt(k / (Rv * (T_c + 273.15))) * (2 / (k + 1)) ** ((k + 1) / (2 * (k - 1)))
    p_rel = p_amb_kpa(0) + P_RELIEF
    cap_relief = choked(p_rel, tsat_c(p_rel), 4.0, 0.6)
    cap_vent = choked(p_amb_kpa(0) + P_REG, T0, 3.0, 0.6)
    say(f"  worst steam generation: {q_max:.0f} W absorbed at 1000 W/m2, no losses -> {m_max * 1000:.2f} g/s")
    say(f"  regulator vent, 3 mm bore (assumed), Cd 0.6: {cap_vent * 1000:.2f} g/s = {cap_vent / m_max:.1f} x worst generation")
    say(f"  relief valve, 4 mm seat (assumed), Cd 0.6, at {P_RELIEF} kPa gauge: {cap_relief * 1000:.2f} g/s = {cap_relief / m_max:.1f} x worst generation")
    d_min = 2 * math.sqrt(m_max / (0.6 * cap_relief / (0.6 * math.pi * (0.002) ** 2)) / math.pi) * 1000
    say(f"  smallest relief seat that passes worst generation: {d_min:.1f} mm")
    F_reg = P_REG * 1000 * math.pi * ri ** 2
    F_rel = P_RELIEF * 1000 * math.pi * ri ** 2
    say(f"  lid load: {F_reg / 1000:.1f} kN at {P_REG} kPa, {F_rel / 1000:.1f} kN at {P_RELIEF} kPa (over the {P['POT_ID']:.0f} mm bore)")
    holes = {"gauge and transducer tee (1/4 NPT, 11.1 mm tap drill)": (75, -55, 11.1),
             "relief valve (1/4 NPT, 11.1 mm tap drill)": (-80, 40, 11.1),
             "Pt100 gland (1/8 NPT, 8.7 mm tap drill)": (P["PROBE_X"], P["PROBE_Y"], 8.7)}
    pts = list(holes.values()) + [(0, 0, 10.0)]
    lig = min(math.hypot(a[0] - b[0], a[1] - b[1]) - (a[2] + b[2]) / 2 for i, a in enumerate(pts) for b in pts[i + 1:])
    edge = min(ri * 1000 - math.hypot(h[0], h[1]) - h[2] / 2 for h in holes.values())
    area_frac = sum(math.pi * (h[2] / 2) ** 2 for h in holes.values()) / (math.pi * (ri * 1000) ** 2)
    say(f"  option (i) drill the maker's lid: 3 new holes, {sum(h[2] for h in holes.values()):.1f} mm of drilled diameter, {area_frac * 100:.2f} % of the lid area;"
        f" smallest ligament {lig:.0f} mm; smallest distance to the bore {edge:.0f} mm")
    say("  option (ii) factory ports or an adapter plate on the regulator stem: 0 new holes in the maker's lid;"
        f" the adapter must keep a vent bore of 3 mm or more ({cap_vent * 1000:.2f} g/s) and leave the overpressure plug untouched")

    # ---------- boil-dry and base temperature
    say("\n9. Boil-dry (R10) and base temperature")
    surplus = qa_c - loss_w(cc["Tr"], sc["wind"])
    t_dry = cc["water_left"] * hfg(121) * 1000 / surplus / 60
    say(f"  surplus at 121 C {surplus:.0f} W; after a 30 min hold the {cc['water_left']:.2f} kg left would boil dry in {t_dry:.0f} min if the dish stayed on the sun")
    mu, rl, rv, sig, cp, pr, csf = 2.3e-4, 943.0, 1.12, 0.0548, 4245.0, 1.44, 0.013
    qpk = od["peak_flux"] * sc["alpha"]
    dT_nb = (qpk / (mu * hfg(121) * 1000 * math.sqrt(G * (rl - rv) / sig))) ** (1 / 3) * csf * hfg(121) * 1000 * pr / cp
    say(f"  Rohsenow nucleate boiling at the peak absorbed flux {qpk / 1000:.0f} kW/m2: base {dT_nb:.1f} K above the water, so about {T0 + dT_nb:.0f} C")
    say(f"  alarm at 140 C: margin {140 - (T0 + dT_nb) - 2.2:.1f} K after a 2.2 K type K tolerance")
    Tk = 400.0
    for _ in range(200):
        q_out = (A_BASE + A_BAND) * (0.9 * SIGMA * (Tk ** 4 - (T_AMB + 273.15) ** 4) + h_conv(sc["wind"]) * (Tk - T_AMB - 273.15))
        Tk += (qa_c - q_out) / 50
    say(f"  dry base under full sun, losing heat only from the black base and band, would settle near {Tk - 273.15:.0f} C (mean, before hot spots)")

    # ---------- masses, wind, stability
    say("\n10. Masses, handling pieces and wind stability (R15, R16)")
    # dish group in the dish frame: (mass, local z of centroid)
    rs = np.linspace(0, D["R"], 400)
    zs = rs ** 2 / (4 * P["FOCAL"])
    ds = np.sqrt(1 + (rs / (2 * P["FOCAL"])) ** 2)
    zc_refl = float(np.trapezoid(zs * rs * ds, rs) / np.trapezoid(rs * ds, rs))
    m_refl = A_para * P["REFL_T"] / 1000 * RHO_AL
    r_rib = np.linspace(P["HUB_R0"], D["R"] - 10, 200)
    z_rib = r_rib ** 2 / (4 * P["FOCAL"])
    s_rib = float(np.trapezoid(np.sqrt(1 + (r_rib / (2 * P["FOCAL"])) ** 2), r_rib)) / 1000
    m_ribs = P["N_PETALS"] * s_rib * P["RIB_W"] * P["RIB_T"] / 1e6 * RHO_ST
    zc_rib = float(np.mean(z_rib)) - 15
    m_rim = 2 * math.pi * (D["R"] + 2) / 1000 * P["RIM_W"] * P["RIM_T"] / 1e6 * RHO_ST
    m_hub = math.pi * (P["HUB_D"] / 2000) ** 2 * P["HUB_T"] / 1000 * RHO_ST
    m_gn = 0.12 * 0.12 * 0.002 * RHO_ST + 0.2
    xb = P["UPR_X"] - P["UPR_W"] / 2 - 40
    rim_w = point_world((D["R"] + P["RIM_T"] + 12, 0, D["depth"] - P["RIM_W"] / 2))
    arm_len = math.dist((xb, 0, P["F_Z"]), rim_w) / 1000
    m_yoke = 2 * arm_len * 0.86 + 2 * 0.35 + 0.5     # two arms of 20 x 20 x 1.5 tube, two collars, lock lever and knob
    m_fast = 0.8                                     # rivets and bolts on the dish
    dish_items = [(m_refl, zc_refl), (m_ribs, zc_rib), (m_rim, D["depth"]), (m_hub, -20), (m_gn, D["depth"]), (m_fast, 150)]
    m_dish_tilt = sum(m for m, _ in dish_items)
    zc_dish = sum(m * z for m, z in dish_items) / m_dish_tilt
    # stand
    BX, BY = D["base_x"] / 1000, P["BASE_Y"] / 1000
    v_rails = 2 * BX * P["RAIL_W"] * P["RAIL_H"] / 1e6 + 2 * (BY - 2 * P["RAIL_W"] / 1000) * P["RAIL_W"] * P["RAIL_H"] / 1e6
    h_up = (P["F_Z"] + P["HOLDER_Z"] + 20 - P["CASTOR_D"] - 5 - P["RAIL_H"]) / 1000
    v_up = 2 * h_up * P["UPR_W"] * P["UPR_D"] / 1e6
    brace = math.hypot(BY / 2 - P["RAIL_W"] / 1000, (P["BRACE_Z"] - P["CASTOR_D"] - 40) / 1000)
    v_br = 4 * brace * P["BRACE_W"] * P["BRACE_T"] / 1e6
    m_timber = (v_rails + v_up + v_br) * RHO_TIMBER
    m_quad = math.pi * (P["QUAD_R"] / 1000) ** 2 / 2 * P["QUAD_T"] / 1000 * RHO_ST
    m_stand = m_timber + 2 * 1.2 + m_quad + 4 * 0.45 + 0.8      # bearing blocks with stub axles, quadrant, castors, bolts
    m_holder = math.pi * (2 * D["pot_or"] + 60) / 1000 * 0.025 * 0.004 * RHO_ST + 2 * (P["UPR_X"] - D["pot_or"] - 60) / 1000 * 1.36
    m_jkt = (math.pi * ((D["jkt_or"] / 1000) ** 2 - ro ** 2) * H_JKT) * 100 + 2 * math.pi * D["jkt_or"] / 1000 * H_JKT * 0.25
    m_vessel = m_body + m_lid + m_fit + m_jkt + M_BASKET
    m_logger = 0.9
    groups = {"dish, ribs, rim and gnomon": m_dish_tilt, "yoke": m_yoke, "stand with quadrant and castors": m_stand,
              "pot holder": m_holder, "vessel with fittings, jacket and basket": m_vessel, "logger and power bank": m_logger}
    m_empty = sum(groups.values())
    for k, v in groups.items():
        say(f"  {k:42s} {v:5.1f} kg")
    say(f"  timber in the stand {m_timber:.1f} kg; empty total {m_empty:.1f} kg; loaded (+1.5 kg water, +2.0 kg instruments) {m_empty + 3.5:.1f} kg")
    say(f"  yoke arm length {arm_len * 1000:.0f} mm each (bearing collar to rim)")
    zl = P["POT_BASE"] + P["POT_IH"]
    vz = [(math.pi * ro ** 2 * P["POT_BASE"] / 1000 * RHO_AL, P["POT_BASE"] / 2), (m_body - math.pi * ro ** 2 * P["POT_BASE"] / 1000 * RHO_AL, P["POT_BASE"] + P["POT_IH"] / 2),
          (m_lid, zl + 3), (m_fit, zl + 40), (m_jkt, P["BARE_BAND"] + H_JKT * 500), (M_BASKET, P["POT_BASE"] + P["TRIVET_H"] + 40),
          (M_INSTR, P["POT_BASE"] + P["TRIVET_H"] + 32), (1.5, P["POT_BASE"] + D["water_depth"] / 2)]
    z_cgv = sum(m * z for m, z in vz) / sum(m for m, _ in vz)
    say(f"  loaded vessel centre of mass {z_cgv:.0f} mm above the base, which sits on the tilt axis: a holder free to swing on that axis would be top-heavy, so it is fixed")
    pieces = {"dish lift (dish, ribs, rim, gnomon, yoke)": m_dish_tilt + m_yoke,
              "stand with quadrant and castors": m_stand,
              "pot holder and logger (bolted on)": m_holder + m_logger,
              "vessel (empty)": m_vessel}
    for k, v in pieces.items():
        say(f"  piece: {k:44s} {v:5.1f} kg")
    # stability
    rho_air = 1.2
    q10 = 0.5 * rho_air * 10 ** 2
    y_edge = BY / 2 - 0.060
    worst = None
    say("  tipping at 10 m/s (dynamic pressure {:.0f} Pa), about the lee castor line at +/-{:.2f} m:".format(q10, y_edge))
    for el in (15, 30, 45, 60, 75, 90):
        t = math.radians(90 - el)
        cg_d = point_world((0, 0, zc_dish), P, el)
        ap = point_world((0, 0, D["depth"]), P, el)
        cg_y = point_world((D["R"] + 16, 0, D["depth"] - 10), P, el)
        items = [(m_dish_tilt, cg_d[1] / 1000), (m_yoke, 0.5 * cg_y[1] / 1000),
                 (m_stand + m_holder + m_logger, 0.0), (m_vessel + 3.5, 0.0)]
        W = sum(m for m, _ in items) * G
        y_cg = sum(m * y for m, y in items) / sum(m for m, _ in items)
        A_side = 2 / 3 * (D["R"] * 2 / 1000) * D["depth"] / 1000
        A_proj = A_AP * math.sin(t) + A_side * math.cos(t)
        z_ap = ap[2] / 1000
        for wdir, cd in (("-Y onto the reflector", 1.4), ("+Y onto the back", 1.2)):
            F_d = q10 * cd * A_proj
            F_o = q10 * (1.0 * 0.37 * 0.30 + 2.0 * 2 * 0.07 * 1.0)      # vessel and uprights
            M_o = F_d * z_ap + F_o * 0.8
            arm = (y_edge - y_cg) if wdir.startswith("-Y") else (y_edge + y_cg)
            M_r = W * arm
            sf = M_r / M_o
            say(f"    elev {el:2d}, wind {wdir:22s}: force {F_d + F_o:5.0f} N, overturning {M_o:5.0f} N m, restoring {M_r:5.0f} N m, factor {sf:4.2f}")
            if worst is None or sf < worst[0]:
                worst = (sf, el, wdir, F_d + F_o, M_o, M_r, W)
    say(f"  worst: factor {worst[0]:.2f} at elevation {worst[1]} deg, wind {worst[2]}")
    for el in (15, 50, 90):
        cg = point_world((0, 0, zc_dish), P, el)
        dy = math.hypot(cg[1], cg[2] - P["F_Z"]) * math.sin(math.radians(90 - el)) / 1000
        say(f"  gravity torque on the tilt axis at elevation {el:2d}: {m_dish_tilt * G * dy:5.1f} N m (dish centre of mass {math.hypot(cg[1], cg[2] - P['F_Z']):.0f} mm from the axis)")
    mu_c = 0.5
    F_slide2 = mu_c * worst[6] / 2
    F_slide4 = mu_c * worst[6]
    say(f"  sliding: wind force {worst[3]:.0f} N against {F_slide4:.0f} N of grip with the four locked castors (mu 0.5); two would give {F_slide2:.0f} N")

    # ---------- logger power
    say("\n11. Logger power (R13)")
    p_load = 0.20 + 0.025 + 0.066 + 0.017       # ESP32, sensors, OLED, microSD writes (W)
    e_day = p_load * 8 / 0.85
    bank_wh = 10.0 * 3.7 * 0.85 * 0.8
    say(f"  load {p_load:.2f} W for 8 h, 85 % converter -> {e_day:.1f} Wh per operating day")
    say(f"  10,000 mAh bank, 85 % output efficiency, 80 % usable -> {bank_wh:.1f} Wh -> {bank_wh / e_day:.1f} days")
    say(f"  load current at 5 V about {p_load / 0.85 / 5 * 1000:.0f} mA; many banks switch off below 50 to 100 mA")
    rec_kb = 16 * 3 * 3600 / 1000
    say(f"  record: 16 bytes per 1 s sample, up to 3 h -> {rec_kb:.0f} kB per cycle; 4 GB card holds about {4e6 / rec_kb:,.0f} cycles")

    # ---------- cost
    say("\n12. Cost from bom/bom.csv")
    rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
    budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
    parts_cost, excl = 0.0, 0.0
    for r in rows:
        v = float(r["qty"]) * float(r["unit_cost_usd"])
        if r["item"].startswith("18 "):
            excl += v
        else:
            parts_cost += v
    say(f"  parts (all lines except 18) ${parts_cost:.2f}; budget ${budget:.0f}; margin ${budget - parts_cost:.2f}; validation consumables (18) ${excl:.2f}, excluded")

    # ---------- results table
    c = cc
    unf = cyc["unfavourable"][1]
    fav = cyc["favourable"][1]
    n_eq = day["equator, equinox, 700 W/m2"][0]
    n_15 = day["15 N, winter solstice, 700 W/m2"][0]
    n_600 = day["equator, equinox, 600 W/m2"][0]
    c1800 = alt_cyc[1800][0]
    RESULTS += [
        ("R1", "Sterilizing condition (redefined)", f"{T0:.2f} C and {cycle(lambda t: qa_c, sc['wind'])['hold']:.1f} min at 0 m; {c1800['Tr']:.1f} C and {c1800['hold']:.0f} min at 1,800 m",
         "exposure equal to 20/30 min at 121 C (z = 10 C), 115 to 124 C, real temperature recorded",
         "Not verifiable at TRL 3", f"Temperature and hold met by calculation; a 103.4 kPa cooker gives {T0:.2f} C at sea level and less above it; equivalence needs biological indicators"),
        ("R2", "Load capacity", f"basket {P['BASKET_D']:.0f} x {P['BASKET_H']:.0f} mm in a {vol_in:.1f} L cooker; {P['TRIVET_H'] - D['water_depth']:.0f} mm over the water",
         "basket 250 x 150 mm or more; 2.0 kg", "Met", "Model check; TRL 2 basket 270 x 180 mm did not fit a 12 L cooker"),
        ("R3", "Load type", "solid instruments, unwrapped or single-wrapped", "no lumened, hollow or textile loads", "Met", "By definition"),
        ("R4", "Cycle time", f"{c['total']:.0f} min central ({fav['total']:.0f} to {unf['total']:.0f})", "90 min or less",
         "Met" if unf["total"] <= 90 else ("At risk" if c["total"] <= 90 else "Not met"), "Precedent 93 to 183 min heat-up (larger vessels)"),
        ("R5", "Daily throughput", f"{n_eq} (equator), {n_15} (15 N winter), {n_600} (600 W/m2)", "3 or more",
         "Met" if min(n_eq, n_15, n_600) >= 3 else ("At risk" if n_eq >= 3 else "Not met"), "09:00 to 15:00, warm restarts"),
        ("R6", "Cycle record", f"{rec_kb:.0f} kB per cycle; about {4e6 / rec_kb:,.0f} cycles on 4 GB", "1 s logging; 1,000 cycles", "Met", "Design check"),
        ("R7", "Measurement accuracy", f"{u005:.2f} K with the 0.05 % reference ({u01:.2f} K with 0.1 %); pressure {e_p:.0f} kPa (0 to {TRANSDUCER_KPA:.0f} kPa)", "0.5 K; 5 kPa",
         "Met" if u005 <= 0.5 else "At risk", "With the 0.05 % reference now in the BOM; field check needs a barometer, not the logger's own transducer"),
        ("R8", "Pressure safety", f"relief {cap_relief / m_max:.1f} x worst steam generation; vent {cap_vent / m_max:.1f} x", "relief 125 kPa gauge or less; vessel rated by its maker",
         "Met", "Capacity met for both lid options; vessel rating to confirm from the maker for the chosen model"),
        ("R9", "Heat input control", f"power below 5 % at {off:.0f} deg of tilt", "stop within 10 s; dish shaded when parked", "Met", "Parking cover added (item 20)"),
        ("R10", "Boil-dry protection (restated)", f"{c['water_left']:.2f} kg left (design); {cw['water_left']:.2f} kg at 1000 W/m2; with the trimming rule {ct['water_left']:.2f} kg at 1,800 m and {ct24['water_left']:.2f} kg at 2,400 m, 1000 W/m2",
         "0.5 L left in the design case and, with the trimming rule, at altitude; trim reminder; alarm at 140 C",
         "Met" if min(c["water_left"], cw["water_left"], ct["water_left"], ct24["water_left"]) >= 0.5 else "At risk",
         f"Untrimmed, {alt_cyc[1800][1]['water_left']:.2f} kg at 1,800 m; the rule depends on the operator (SCL-DDR-002 item 17)"),
        ("R11", "Burn and glare protection (restated)", f"whole vessel and fittings treated as a hot zone; dish turned {off:.0f} deg off the sun before reaching in; parking cover, goggles and ground keep-out marking in the BOM",
         "vessel and fittings a marked hot zone reached only with the dish off the sun; focus reached only through the dish; eye protection; keep-out marked",
         "Met", "By design review (SCL-DDR-002 item 15); no physical guard, which could not close the light cone without shading the dish"),
        ("R12", "Air-removal check", f"uncertainty {u_sat:.2f} K against the 2 K threshold", "flag a hold more than 2 K below saturation",
         "Met" if u_sat <= 2 / 3 else "At risk",
         f"0 to {TRANSDUCER_KPA:.0f} kPa transducer; sure to flag {100 * (1 - psat_kpa(tsat_c(p_abs) - 2 - u_sat) / p_abs):.0f} % air; may flag from {100 * (1 - psat_kpa(tsat_c(p_abs) - 2 + u_sat) / p_abs):.0f} %"),
        ("R13", "Off-grid logger power (redefined)", f"{bank_wh / e_day:.0f} days on a 10,000 mAh bank", "3 days without charging; USB recharge", "Met", "Bank must not switch off at low load"),
        ("R14", "Tracking effort (relaxed)", f"90 % power held for {t_tol:.0f} min", f"retarget no more often than every {RETARGET_MIN:.0f} min; logger reminder",
         "Met" if t_tol >= RETARGET_MIN else "Not met", "Worst-case sun motion 15 deg/h; relaxed from 15 min (SCL-DDR-002 item 13)"),
        ("R15", "Stability", f"tipping factor {worst[0]:.2f} (worst, elevation {worst[1]} deg)", "does not tip at 10 m/s",
         "Met" if worst[0] >= 1.5 else ("At risk" if worst[0] >= 1.0 else "Not met"),
         f"Sliding: {worst[3]:.0f} N wind vs {F_slide4:.0f} N grip on four locked castors; park face-up in high wind"),
        ("R16", "Portability and build (relaxed)", f"{m_empty:.1f} kg empty; largest piece {max(pieces.values()):.1f} kg", f"{MASS_MAX:.0f} kg or less; pieces 20 kg or less; hand tools, drill, bolts",
         "Met" if m_empty <= MASS_MAX and max(pieces.values()) <= 20 else "Not met", "Total relaxed from 40 kg (SCL-DDR-002 item 14); timber stand heavier than the TRL 2 steel estimate"),
        ("R17", "Cost (redefined)", f"${parts_cost:.0f}", f"${budget:.0f} or less for parts, validation consumables excluded",
         "Met" if parts_cost <= budget else "Not met", "Budget raised to $450 per SCL-DDR-001 item 2"),
    ]
    say("\n13. Requirement status")
    for r in RESULTS:
        say(f"  {r[0]:4s} {r[4]:8s} {r[1]}: {r[2]}")
    with (Path(__file__).parent / "results.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "requirement", "value", "target", "status", "note"])
        w.writerows(RESULTS)
    say("\nwrote docs/04-calcs/results.csv")
