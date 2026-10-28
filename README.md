# Near-Null Magnetic Fields in Lunar Plant Biology: The First Five Days of Seedling Growth, Multi-Stressor Bioenergetics, and Implications for Artemis Agriculture

[![Journal](https://img.shields.io/badge/Target%20Journal-Life%20Sciences%20in%20Space%20Research-blue.svg)](https://www.sciencedirect.com/journal/life-sciences-in-space-research)
[![Mission](https://img.shields.io/badge/Artemis%20III-LEAF%20Payload-orange.svg)](https://www.nasa.gov/missions/artemis/artemis-3/)
[![GitHub Pages](https://img.shields.io/badge/Live%20Showcase-CoSE%20Portal-darkgreen.svg)](https://dr-richard-barker.github.io/NMF_review/)
[![ABAI QC](https://img.shields.io/badge/ABAI%20QC-Verified%20Clear-brightgreen.svg)](#astrobotany-ai-abai-qc-verification)
[![Zenodo](https://img.shields.io/badge/Zenodo-FAIR%20Scaffold%20Ready-blueviolet.svg)](#zenodo-deposition--fair-sharing)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Executive Summary & Central Thesis

As space exploration transitions from short-duration low Earth orbit (LEO) expeditions to sustained surface exploration under NASA's **Artemis program**, Bioregenerative Life Support Systems (BLSS) and autonomous plant growth chambers represent indispensable operational infrastructure. While biological architectures routinely monitor microgravity, partial gravity ($0.166\ g$), ionizing radiation, hypobaric pressure, and LED spectra, **the ambient magnetic field has historically been treated as an uncontrolled, unmonitored background variable**.

On Earth, plants evolved exclusively under the protective geodynamo of the dipolar geomagnetic field ($25\text{--}65\ \mu\text{T}$). On the lunar surface and across Artemis South Polar exploration candidate sites, **this magnetic environment collapses into an extreme near-null magnetic field (NNMF; $<0.8\text{ nT}$)**.

This repository hosts the complete review manuscript, processed datasets, high-resolution figures, and reproduction pipeline for our submission to ***Life Sciences in Space Research* (Elsevier / COSPAR)**. We refocus the literature specifically on the **first five days of seedling growth (0–120 hours)**—the mission-critical bottleneck that determines whether a space crop successfully germinates, de-etiolates, and establishes autotrophic competence.

---

## The 5 Core Concepts

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE 5 CORE CONCEPTS                                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Lunar Near-Null Reality: Candidate Artemis landing sites reside in <0.8 nT voids    │
│    (>30,000× weaker than Earth's geomagnetic field; Figure 1).                         │
│                                                                                        │
│ 2. Suppressed Germination Capacity: Geomagnetic shielding reduces total viable         │
│    seedling germination count across crops (Figure 2a).                                │
│                                                                                        │
│ 3. Retarded Emergence Velocity: Emergence speed is delayed by 12–36 hours (t50 lag),   │
│    dampening early vegetative vigor and reducing biomass yields by 20–30% (Figure 2b). │
│                                                                                        │
│ 4. Repressed Pigment Biosynthesis: Cryptochrome (CRY1/CRY2) and HY5 transcriptional    │
│    signaling dysregulation represses chlorophyll and anthocyanin accumulation          │
│    during initial greening (Figure 2c, Figure 3).                                      │
│                                                                                        │
│ 5. Multi-Stressor Nexus & Astronaut Parallels: Hypomagnetic stress converges on the    │
│    mitochondrial CO2 ↔ O2 ↔ ROS equilibrium with radiation and exploration atmospheres,│
│    inducing Alternative Oxidase (AOX1D) and directly mirroring mitochondrial           │
│    dysregulation documented in human astronauts (Figure 4).                            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Architecture

```text
NMF_review/
├── manuscript/
│   ├── Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md  # Complete review manuscript
│   └── references_LSSR.bib                              # Audited BibTeX library (79 references)
├── figures/
│   ├── Fig1_lunar_magnetic_environment_montage.png/.pdf # Lunar field maps & landing sites
│   ├── Fig2_first_5_days_germination_pigments.png/.pdf  # Day 0–5 kinetics & pigments
│   ├── Fig3_quantum_biology_0to5day_pathways.png/.pdf   # Cryptochrome radical pair pathway
│   ├── Fig4_multistressor_co2_o2_ros_nexus.png/.pdf     # Mitochondrial CO2-O2-ROS nexus
│   ├── Fig5_flight_validation_risk_pipeline.png/.pdf    # LEAF risk-retirement framework
│   └── Graphical_Abstract_LSSR.png/.pdf                 # Graphical abstract
├── data/
│   ├── lunar_mag_field_grid.csv                         # 1° resolution lunar crustal field
│   ├── landing_sites_magnetic.csv                       # Field magnitudes at 23 lunar sites
│   ├── seedling_kinetics_summary.csv                    # Day 0–5 germination kinetics
│   └── multiomics_overlap_osd782_nnmf.csv               # Transcriptomic stress overlap
├── tables/
│   ├── Table1_site_magnetic_values.csv                  # Exploration sites magnetic summary
│   ├── Table2_biology_literature.csv                    # Empirical NNMF biological findings
│   └── Table3_flight_decision_matrix.csv                # Predeclared LEAF decision gates
├── scripts/
│   ├── assemble_lunar_field_montage.py                  # Produces Fig 1
│   ├── plot_first_5_days_kinetics_pigments.py           # Produces Fig 2
│   ├── compile_quantum_pathway_figures.py               # Produces Fig 3
│   ├── plot_multistressor_co2_o2_ros.py                 # Produces Fig 4
│   ├── plot_flight_pipeline_and_ga.py                   # Produces Fig 5 & Graphical Abstract
│   ├── export_presentation_subpanels.py                 # Exports standalone subpanel graphics
│   ├── build_presentation_deck.py                       # Generates editable 16:9 PPTX deck
│   ├── build_lssr_docx.py                               # Word manuscript builder with figures
│   ├── run_abai_qc_audit.py                             # Automated 5-check ABAI quality audit
│   └── prepare_zenodo.py                                # Generates MANIFEST.tsv & CHECKSUMS
├── presentation/                                        # Presentation assets
│   └── assets/subpanels/                                # 22 standalone 300 DPI subpanels
├── docs/                                                # GitHub Pages (CoSE theme)
│   ├── index.html                                       # Interactive web portal
│   ├── cose/                                            # CoSE header, rail, style, & sites.js
│   └── assets/                                          # Web-optimized figures & diagrams
├── Near_Null_Magnetic_Fields_Lunar_Plant_Biology_LSSR_Review.docx # Compiled Word submission doc
├── Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx # Editable 16:9 PowerPoint deck
├── CITATION.cff                                         # CFF v1.2.0 metadata
├── .zenodo.json                                         # Zenodo deposit schema
├── MANIFEST.tsv                                         # Byte-exact payload inventory
├── CHECKSUMS.sha256                                     # SHA-256 integrity verification
├── LICENSE                                              # Dual CC-BY-4.0 & MIT license
├── Makefile                                             # Automation reproduction commands
└── README.md                                            # Repository overview
```

---

## Reproduction & Pipeline Execution

All figures, data tables, and manuscript formats are fully reproducible via standard Makefile targets.

### Prerequisites

A Python 3.10+ environment with `matplotlib`, `numpy`, `pandas`, `scipy`, `Pillow`, and `pandoc`:

```bash
# Clone repository
git clone https://github.com/dr-richard-barker/NMF_review.git
cd NMF_review

# Run full reproduction pipeline
make all
```

### Individual Makefile Targets

- `make figures` — Re-executes Python plotting routines and re-renders all 5 main figures plus the graphical abstract in 300 DPI raster (`.png`) and vector (`.pdf`).
- `make docx` — Compiles `manuscript/Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md` into the publication Word document with embedded high-resolution figures.
- `make presentation` — Decomposes figure montages into standalone subpanels and compiles the publication-grade, editable 16:9 widescreen PowerPoint presentation (`Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx`).
- `make abai-qc` — Runs the AstroBotany AI quality control audit, checking for zero blocklisted strings, validating DOIs against the CrossRef API, and ensuring data traceability.
- `make zenodo-prep` — Re-scans the repository and re-generates `MANIFEST.tsv` and `CHECKSUMS.sha256`.
- `make verify` — Validates file integrity against `CHECKSUMS.sha256`.

---

## AstroBotany AI (ABAI) QC Verification

This repository has completed and passed all 5 automated quality control checks:

1. **Rule Blocklist Sweep:** Passed (0 forbidden strings detected across all markdown, scripts, and bibtex files).
2. **Bibliographic CrossRef Audit:** Passed (All DOIs independently verified against `api.crossref.org`; historical citation errors corrected).
3. **Data Traceability:** Passed (All plotted values trace strictly to processed CSV tables in `data/`; zero untracked synthetic mock data).
4. **NASA Open Science Accession Mapping:** Passed (Validated cross-references to NASA OSDR studies `OSD-782`, `OSD-8`, and `OSD-27`).
5. **Compilation Deliverables Verification:** Passed (All 12 figure files present and non-empty; Word document compiled with embedded figures).

---

## Editable PowerPoint Presentation Deck (16:9 Widescreen)

This repository includes a publication-grade, 16:9 widescreen presentation deck designed for lab meetings, project reviews, and conference presentations:
👉 **[`Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx`](Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx)**

### Key Features of the Deck:
- **15 Structured Slides:** Full narrative arc from the lunar $<0.8\text{ nT}$ void to Day 0–5 seedling kinetics, quantum cryptochrome mechanisms, the $\text{CO}_2 \leftrightarrow \text{O}_2 \leftrightarrow \text{ROS}$ nexus, and Artemis LEAF risk-retirement.
- **Deconstructed, Editable Montages:** Figure montages (Figures 1–5 and Graphical Abstract) are not flattened raster images. Each subpanel is an **independent, repositionable graphic component** accompanied by **native editable PowerPoint text boxes** for panel letters `(a)`, `(b)`, `(c)`, `(d)`, headers, and metric callouts.
- **Deep-Dive Mechanism Slides:** Large-format views of critical subpanels paired with analytical takeaways and biological pathways.
- **Native Styled Table:** Table 3 (Artemis LEAF Flight Decision Matrix) is built as a native PowerPoint table with colored indicator cells (Green / Amber / Red gates).
- **Comprehensive Presenter Script:** Every slide includes detailed, structured presenter notes covering the primary narrative, quantitative numbers, and anticipated questions.
- **Standalone Subpanel Assets:** All 22 individual subpanels are exported in high-resolution (300 DPI) under `presentation/assets/subpanels/`.

---

## Interactive Web Portal (CoSE Theme)

The findings, figures, and full manuscript are deployed on GitHub Pages using the **Collaborative Science Environment (CoSE)** theme:
👉 **[https://dr-richard-barker.github.io/NMF_review/](https://dr-richard-barker.github.io/NMF_review/)**

Features of the web portal:
- Interactive executive summary and Core Concepts grid
- High-resolution modal figure viewer with full multi-panel captions
- Live searchable data tables (Lunar Exploration Sites, Biological Literature Matrix, Flight Decision Matrix)
- In-browser manuscript reader with anchored section navigation and complete bibliography
- Seamless cross-site navigation rail integrating into Dr. Richard Barker's Astrobotany and Deep Space Agriculture portfolios

---

## Zenodo Deposition & FAIR Sharing

This repository is formatted for 1-click archiving on **Zenodo**:
- **Deposit Schema:** `.zenodo.json` adheres to Zenodo REST API specifications.
- **Citation Metadata:** `CITATION.cff` provides machine-readable Citation File Format v1.2.0 metadata.
- **Manifest:** `MANIFEST.tsv` lists file paths, byte sizes, SHA-256 hashes, and functional descriptions.
- **Integrity Check:** Verify all payload files with:
  ```bash
  shasum -a 256 -c CHECKSUMS.sha256
  ```

---

## Authors & Affiliations

- **D. Marshall Porterfield** $^{1,*}$ (`porterf@purdue.edu`)
- **Richard J. Barker** $^{1,*}$ (`dr.richard.barker@gmail.com`, [ORCID: 0000-0001-5681-9857](https://orcid.org/0000-0001-5681-9857))
- **Caue Borlina** $^{2}$
- **Aubrey O’Rourke** $^{2}$
- **Adriana Sanchez** $^{1}$
- **Manisha Dagar** $^{1}$
- **Sofia Leiva Aldana** $^{1}$
- **Ray Wheeler** $^{3}$
- **Gioia Massa** $^{4}$
- **Barbara Demmig-Adams** $^{5}$
- **Marta Peirats-Llobet** $^{1}$
- **Pamela Flores** $^{1}$
- **Anirudha Dixit** $^{1}$
- **Christine Chamberlain** $^{6}$

$^{1}$ Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN 47907, USA  
$^{2}$ Department of Earth, Atmospheric, and Planetary Sciences, Purdue University, West Lafayette, IN 47907, USA  
$^{3}$ NASA John F. Kennedy Space Center, Exploration Research and Technology Programs, FL 32899, USA  
$^{4}$ NASA John F. Kennedy Space Center, Space Crop Production, FL 32899, USA  
$^{5}$ Department of Ecology and Evolutionary Biology, University of Colorado Boulder, Boulder, CO 80309, USA  
$^{6}$ Space Lab Technologies, LLC, Boulder, CO 80301, USA  

$^*$ Corresponding Authors.

---

## Citation

```bibtex
@article{Porterfield_Barker_2026_NNMF,
  author       = {Porterfield, D. Marshall and Barker, Richard J. and Borlina, Caue and
                  O'Rourke, Aubrey and Sanchez, Adriana and Dagar, Manisha and
                  Leiva Aldana, Sofia and Wheeler, Ray and Massa, Gioia and
                  Demmig-Adams, Barbara and Peirats-Llobet, Marta and Flores, Pamela and
                  Dixit, Anirudha and Chamberlain, Christine},
  title        = {Near-Null Magnetic Fields in Lunar Plant Biology: The First Five Days of Seedling Growth, Multi-Stressor Bioenergetics, and Implications for Artemis Agriculture},
  journal      = {Life Sciences in Space Research},
  year         = {2026},
  note         = {In review / Preprint available at https://dr-richard-barker.github.io/NMF_review/},
  url          = {https://github.com/dr-richard-barker/NMF_review}
}
```
