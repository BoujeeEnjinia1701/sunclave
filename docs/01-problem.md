---
doc_id: SCL-PRB-001
title: SunClave problem statement
project: SunClave
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, context, constraints, out of scope, cited prior work, open questions)
---

# SunClave problem statement

Clinics without reliable electricity cannot run an electric autoclave, so reusable instruments are often boiled, soaked in chemicals or steamed in an unmonitored pressure cooker, and nobody can show afterward that a given load reached sterilizing conditions. SunClave aims to supply the heat from the sun and, just as important, a record of every cycle.

> **Safety:** SunClave is a research and educational prototype. It is not a medical device, has not been cleared or approved by any regulator, and must not be relied on to sterilize instruments used on patients. It concentrates sunlight to a burning intensity and generates pressurized steam at about 121 °C (250 °F).

## The problem

Steam under pressure is the standard way to sterilize heat-tolerant instruments. The CDC gives minimum exposure times of 30 min at 121 °C for wrapped instruments in a gravity-displacement sterilizer ([CDC, Table 7](https://www.cdc.gov/infection-control/hcp/disinfection-and-sterilization/steam-sterilization-cycle-times.html)), and IARC's WHO-aligned manual for low-resource clinics gives 20 min at 121 to 132 °C for unwrapped instruments and 30 min for small wrapped packs ([IARC colposcopy manual, chapter 14](https://screening.iarc.fr/colpochap.php?chap=14.php&lang=1)). WHO's reprocessing manual describes the whole cycle of cleaning, packing, sterilizing and monitoring that a clinic needs ([WHO, 2016](https://iris.who.int/handle/10665/250232)).

The energy is the first barrier. WHO and partners estimate that close to 1 billion people in low- and lower-middle-income countries are served by health-care facilities with no electricity or unreliable electricity; in sub-Saharan Africa about 15 % of facilities have no electricity at all and only about 40 % have a reliable supply ([WHO fact sheet, 2023](https://www.who.int/news-room/fact-sheets/detail/electricity-in-health-care-facilities)). A small electric autoclave draws 1.5 to 3 kW for an hour or more per cycle, far beyond a clinic's solar lighting system.

The evidence is the second barrier. A household pressure cooker on a fire can reach sterilizing conditions if instruments sit above the water and the cycle is long enough, but results depend on the vessel, its seal and the operator, and constant monitoring with biological indicators is recommended ([Baez, pressure cookers for clinical instruments](https://cdn.ymaws.com/sites/adint.site-ym.com/resource/resmgr/NewsArticles/Use_of_pressure_cookers_for_.pdf?hhSearchTerms=%22pressure%22)). Clinics rarely have a thermometer inside the vessel, let alone a record per load.

A third, less obvious barrier is altitude. A cooker regulated at 103 kPa (15 psi) above ambient reaches 121 °C only near sea level. At 1,800 m (Nairobi) the same cooker reaches only about 118 °C (SCL-PRC-001 gives the calculation), which is not a 121 °C cycle.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Nurse or clinical officer running a rural health post | Sterilize a small daily set of reusable instruments (delivery, suturing, dressing, minor procedure kits) without grid power or fuel | Health post or dispensary, 5 to 30 patients a day, one or two staff |
| Midwife at a maternity unit or birthing center | Sterile delivery kits for each birth, including at night from a stock sterilized in the day | Births at any hour; kits stored wrapped |
| Facility in-charge and district supervisor | Evidence that each load reached temperature and time, for audits and infection-control reviews | Paper registers today; periodic supervision visits |
| Dental or eye outreach team | Sterilize instruments at a temporary site for a few days | Mobile camps, school or church halls |
| Biomedical technician or local fabricator | Build, repair and calibrate the unit with local materials and tools | District workshop, hand tools, basic welding |

### Operating environment

- **Sun:** clear-sky direct normal irradiance (DNI) of 600 to 900 W/m² around midday in much of the tropics and subtropics in the dry season, with long cloudy or hazy spells in the rains ([Global Solar Atlas](https://globalsolaratlas.info/)). Concentrators use only direct sun, so an overcast day yields no cycles.
- **Altitude:** sea level to about 2,400 m; many East African facilities are at 1,000 to 2,000 m.
- **Climate:** ambient 10 to 40 °C, wind to 10 m/s, dust, occasional rain while a cycle runs.
- **Water:** clean water available but not always distilled; hard water scales vessels.
- **Supply chain:** aluminum household pressure cookers, steel tube, aluminum sheet and basic electronics modules are available in regional towns; certified medical parts are not.

## Constraints

- Garage-buildable prototype, about $400 USD in parts (`project.yaml`).
- Uses a commercially made pressure vessel rated for its working pressure. No homemade pressure vessel.
- Buildable and repairable by a district workshop with hand tools, a drill and simple welding or bolted joints.
- Operable by one trained person; movable by two.
- Every cycle is recorded automatically, independent of the operator's notes, with a pass or fail result.
- Research and educational prototype only: it must not be presented as a medical device or as a substitute for a certified sterilizer.

## Out of scope

- Regulatory clearance, certification or clinical deployment.
- Hollow, lumened or porous loads (textile packs, tubing, handpieces), which need active air removal that a pressure cooker cannot provide.
- Pre-cleaning and washer-disinfection; SunClave assumes instruments arrive cleaned.
- Heat storage for night-time or cloudy-day cycles (a possible later variant).
- Medical waste treatment.

## Prior work

- **Capteur Soleil solar autoclave (Kaseman et al., 2012).** A 2 m² semi-parabolic aluminum concentrator heated 14 L and 24 L All-American sterilizers above 121 °C for 30 min in all 27 trials, confirmed by thermometer, indicator tape and biological indicators. Heat-up averaged 93 to 183 min depending on the run ([AJTMH](https://www.ajtmh.org/view/journals/tpmd/87/4/article-p602.xml)). This is the closest precedent and shows the concept works; SunClave adds a smaller dish, a lower-cost cooker and an electronic cycle record.
- **Rice University nanoparticle solar autoclave (Neumann et al., 2013).** Light-absorbing nanoparticles in water generated steam directly under a Fresnel lens and passed sterilization tests ([PNAS](https://www.pnas.org/doi/10.1073/pnas.1310131110); [summary](https://sciencedaily.com/releases/2013/07/130722141552.htm)). It needs specialist materials that local workshops cannot make.
- **SK14 parabolic solar cooker.** A 1.4 m dish of reflective aluminum segments delivering about 700 W at 750 W/m², sold as a kit and widely used for cooking ([EG-Solar SK14](https://eg-solar.de/en/produkt/sk14/)). SunClave borrows its size and petal construction.
- **Pressure cookers as sterilizers.** Studies show household cookers can reach sterilizing conditions with a platform above the water and biological-indicator monitoring ([Baez](https://cdn.ymaws.com/sites/adint.site-ym.com/resource/resmgr/NewsArticles/Use_of_pressure_cookers_for_.pdf?hhSearchTerms=%22pressure%22)).
- **Small sterilizer standards.** EN 13060 defines small steam sterilizers, with type N cycles limited to unwrapped solid products ([EN 13060-3, type N](https://standards.globalspec.com/std/10364805/nen-en-13060-3)). SunClave's load limits follow the same logic, without any claim of compliance.
- **Review of solar-thermal autoclaves.** A 2021 review surveys collector types for autoclaves ([ResearchGate](https://www.researchgate.net/publication/352191747_Review_of_solar-thermal_collectors_powered_autoclave_for_the_sterilization_of_medical_equipment)).

## Open questions

- Which partner and first site (a district health office, a maternity program, a university biomedical engineering department, or an outreach dental team)? Proposed, awaiting Amish.
- How large is a typical daily load, and are packs wrapped or unwrapped? This sets vessel size and hold time.
- What is the site altitude? Above about 300 m a 103 kPa cooker cannot reach 121 °C, which forces a design choice (see SCL-PRC-001).
- What backup heat source is used on cloudy days (wood, charcoal or LPG), and should the logger also record those cycles? Assumed yes.
- Who would own the cycle records, and in what form do supervisors want them (printed ticket, register entry, phone export)?

## User research and co-design

This design is for health workers in settings the author is not part of, so requirements must come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, cycle count, altitude and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
