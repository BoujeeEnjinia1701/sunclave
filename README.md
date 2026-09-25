# SunClave

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $400 USD · **Difficulty:** 3 of 5

Solar concentrator that heats a modified pressure-cooker autoclave, with a validated temperature and time logger to prove each cycle.

![SunClave concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Rural clinics lack power to sterilize instruments in an autoclave. Close to 1 billion people are served by health facilities with no or unreliable electricity, and where instruments are steamed in a pressure cooker on a fire, nothing records whether each load reached sterilizing conditions. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A 1.4 m parabolic dish of aluminum petals focuses about 700 W of sunlight onto the blackened base of a 12 L pressure cooker that hangs level at the focus while the dish tilts around it. A cycle logger reads a Pt100 probe in the load zone and an absolute pressure transducer, checks that the chamber holds saturated steam, times the hold and shows PASS or FAIL for each cycle. First-order estimates: about 35 to 60 min from cold to 121 °C and about three cycles on a clear day. A 103 kPa (15 psi) cooker reaches 121 °C only below about 300 m altitude, and the parts cost about $437 against the $400 budget; both are open decisions in the [review note](docs/REVIEW.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md)

## Key components

- 1.4 m petal dish on a tilting yoke and castored stand
- 12 L aluminum pressure cooker with weighted regulator, level holder and insulated jacket
- Pressure gauge and independent relief valve
- Pt100 load-zone probe and absolute pressure transducer through a lid gland
- Solar-powered cycle logger with pass or fail per cycle
- Shadow gnomon for aiming without looking at the sun

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person. This design involves concentrated sunlight that can burn skin and eyes and start fires, and heat and pressurized steam. Keep operating pressure and water volume below local boiler and pressure vessel code thresholds, fit a certified relief valve, and never operate it unattended.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SCL-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SCL-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
