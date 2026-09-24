# SunClave

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** BioMedical · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $400 USD · **Difficulty:** 3 of 5

Solar concentrator that heats a modified pressure-cooker autoclave, with a validated temperature and time logger to prove each cycle.

## Problem

Rural clinics lack power to sterilize instruments in an autoclave.

## Concept

Solar concentrator that heats a modified pressure-cooker autoclave, with a validated temperature and time logger to prove each cycle.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Parabolic reflector segments
- Pressure cooker rated to 15 psi
- Pressure gauge
- Thermocouple logger
- Tracking stand

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> This is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose, treat or monitor any person. This design involves heat and pressurized steam. Keep operating pressure and water volume below local boiler and pressure vessel code thresholds, fit a certified relief valve, and never operate it unattended.

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
