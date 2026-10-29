# Makefile for Near-Null Magnetic Fields Lunar Plant Biology Review
# Life Sciences in Space Research (LSSR) Submission

PYTHON ?= $(shell which python3)
PANDOC ?= $(shell which pandoc)

# Prefer local virtualenv with scientific & pptx stack if available
LOCAL_VENV = $(CURDIR)/.venv/bin/python
EXTERNAL_VENV = /Users/drb_laptop/Documents/deepspace-seed-stress-decoder/lunar-magnetic-biology/.venv/bin/python

ifneq ("$(wildcard $(LOCAL_VENV))","")
    PY = $(LOCAL_VENV)
else ifneq ("$(wildcard $(EXTERNAL_VENV))","")
    PY = $(EXTERNAL_VENV)
else
    PY = $(PYTHON)
endif

.PHONY: all figures docx presentation site abai-qc zenodo-prep verify clean help

all: figures docx presentation abai-qc zenodo-prep verify

help:
	@echo "Available make targets:"
	@echo "  make all          - Generate figures, docx, presentation, run ABAI QC, and prepare Zenodo"
	@echo "  make figures      - Regenerate all 5 figures and graphical abstract (PNG & PDF)"
	@echo "  make docx         - Compile manuscript markdown to publication Word document with figures"
	@echo "  make presentation - Export subpanels and compile editable 16:9 PowerPoint presentation"
	@echo "  make site         - Sync figure assets to docs/assets/ for GitHub Pages"
	@echo "  make abai-qc      - Execute 5-check AstroBotany AI quality control audit"
	@echo "  make zenodo-prep  - Generate MANIFEST.tsv and CHECKSUMS.sha256 for Zenodo"
	@echo "  make verify       - Verify repository integrity using CHECKSUMS.sha256"
	@echo "  make clean        - Remove temporary files and build artifacts"

figures:
	@echo "==> Generating Figure 1 (Lunar Magnetic Environment)..."
	@$(PY) scripts/assemble_lunar_field_montage.py
	@echo "==> Generating Figure 2 (Day 0-5 Seedling Kinetics & Pigments)..."
	@$(PY) scripts/plot_first_5_days_kinetics_pigments.py
	@echo "==> Generating Figure 3 (Quantum Biology Cryptochrome Pathways)..."
	@$(PY) scripts/compile_quantum_pathway_figures.py
	@echo "==> Generating Figure 4 (Multi-Stressor CO2-O2-ROS Nexus)..."
	@$(PY) scripts/plot_multistressor_co2_o2_ros.py
	@echo "==> Generating Figure 5 & Graphical Abstract (Flight Pipeline)..."
	@$(PY) scripts/plot_flight_pipeline_and_ga.py
	@$(MAKE) site

site:
	@echo "==> Syncing web figures, manuscript docx, tables, and references to docs/assets/..."
	@mkdir -p docs/assets
	@cp figures/*.png docs/assets/
	@cp figures/*.pdf docs/assets/
	@cp Near_Null_Magnetic_Fields_Lunar_Plant_Biology_LSSR_Review.docx docs/assets/
	@cp Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx docs/assets/
	@cp tables/*.csv docs/assets/
	@cp manuscript/references_LSSR.bib docs/assets/
	@echo "Web assets synced successfully."

docx:
	@echo "==> Compiling Word document manuscript..."
	@$(PY) scripts/build_lssr_docx.py
	@echo "Generated Near_Null_Magnetic_Fields_Lunar_Plant_Biology_LSSR_Review.docx"

presentation:
	@echo "==> Exporting standalone presentation subpanels..."
	@$(PY) scripts/export_presentation_subpanels.py
	@echo "==> Building editable 16:9 PowerPoint presentation deck..."
	@$(PY) scripts/build_presentation_deck.py
	@echo "Generated Near_Null_Magnetic_Fields_Lunar_Plant_Biology_Presentation.pptx"

abai-qc:
	@echo "==> Running AstroBotany AI (ABAI) Quality Control Audit..."
	@$(PY) scripts/run_abai_qc_audit.py

zenodo-prep:
	@echo "==> Generating Zenodo MANIFEST.tsv and CHECKSUMS.sha256..."
	@$(PY) scripts/prepare_zenodo.py

verify:
	@echo "==> Verifying SHA-256 checksums..."
	@shasum -a 256 -c CHECKSUMS.sha256

clean:
	@rm -f _temp_for_docx.md
	@rm -f ~$*.docx
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
