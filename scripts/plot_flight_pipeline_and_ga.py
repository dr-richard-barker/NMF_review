#!/usr/bin/env python3
"""
plot_flight_pipeline_and_ga.py

Generates:
1. Figure 6: Scientific Knowledge Gap Retirement, Ground Simulation Standards,
   and Flight Instrumentation Trade Space
2. Graphical Abstract for npj Microgravity / Space Plant Biology
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_cache'

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.0,
    'axes.labelsize': 8.5,
    'axes.titlesize': 9.5,
    'xtick.labelsize': 7.5,
    'ytick.labelsize': 7.5,
    'legend.fontsize': 7.5,
    'figure.titlesize': 10.5,
    'mathtext.fontset': 'dejavusans'
})

OUT_DIR = Path('/Users/drb_laptop/Documents/NMF_review/figures')
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_figure_6():
    fig = plt.figure(figsize=(11.8, 9.6), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.35], width_ratios=[1.0, 1.0], hspace=0.28, wspace=0.24)

    # -------------------------------------------------------------
    # Panel (a): 3-Chamber Ground Simulation Standards (Scientific Rigor)
    # -------------------------------------------------------------
    ax_cham = fig.add_subplot(gs[0, 0])
    ax_cham.axis('off')
    ax_cham.set_xlim(0, 100)
    ax_cham.set_ylim(100)
    ax_cham.set_title('Methodological Ground Simulation Standards (3-Chamber Parity)', weight='bold', pad=10, fontsize=8.8)
    ax_cham.text(0.00, 1.03, 'a', transform=ax_cham.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    chambers = [
        ("Chamber 1: Geomagnetic Baseline (GMF Control)", 
         "45–50 µT Ambient Terrestrial Field (calibrated local vector)", 
         "#e3f2fd", "#1565c0", 
         "Terrestrial environmental reference; unshielded Helmholtz/growth chamber"),
        ("Chamber 2: Near-Null Field Simulation (NNMF Active)", 
         "<10 nT active cancellation or <1 nT shielded core (residual |B| < 1 nT)", 
         "#ffebee", "#c62828", 
         "Lunar surface magnetic simulation (<0.82 nT ambient crustal void)"),
        ("Chamber 3: Matched Bifilar Sham Control (Artifact Isolation)", 
         "Opposing windings; net coil field B_coil ≈ 0; ambient GMF (45–50 µT) retained", 
         "#fff3e0", "#e65100", 
         "Equal current, zero coil vector; isolates ohmic Joule heat (ΔT), vibration & ripple")
    ]

    for idx, (c_name, b_field, bg, border, desc) in enumerate(chambers):
        y_top = 88 - idx * 24.5
        b = patches.FancyBboxPatch((3, y_top - 21.5), 94, 21.5, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=border, facecolor=bg, lw=1.2)
        ax_cham.add_patch(b)
        ax_cham.text(6, y_top - 5.5, c_name, fontsize=7.6, weight='bold', color=border, va='center')
        ax_cham.text(6, y_top - 11.5, f"Magnetic Regime: {b_field}", fontsize=6.8, weight='bold', color='#212121', va='center')
        ax_cham.text(6, y_top - 17.0, f"Experimental Purpose: {desc}", fontsize=6.5, color='#424242', va='center')

    # Environmental parity tolerance banner
    tol_box = patches.FancyBboxPatch((3, 3.5), 94, 10.5, boxstyle="round,pad=0,rounding_size=2",
                                     edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.0)
    ax_cham.add_patch(tol_box)
    ax_cham.text(50, 10.2, "Environmental Parity Verification Tolerances (6-Point Acceptance)", 
                 fontsize=7.2, weight='bold', color='#1b5e20', ha='center', va='center')
    ax_cham.text(50, 6.0, r"T: $\pm$0.3°C  |  RH: $\pm$2%  |  CO$_2$: $\pm$50 ppm  |  PAR: $\pm$5 $\mu$mol m$^{-2}$ s$^{-1}$  |  Airflow: $\pm$0.05 m/s", 
                 fontsize=6.7, color='#212121', ha='center', va='center')

    # -------------------------------------------------------------
    # Panel (b): Hardware Self-Magnetic Assessment Protocol (Power-State Mapping)
    # -------------------------------------------------------------
    ax_rescue = fig.add_subplot(gs[0, 1])
    ax_rescue.axis('off')
    ax_rescue.set_xlim(0, 100)
    ax_rescue.set_ylim(0, 100)
    ax_rescue.set_title('Payload Self-Magnetic Calibration & Transfer Deconvolution', weight='bold', pad=10, fontsize=8.8)
    ax_rescue.text(0.00, 1.03, 'b', transform=ax_rescue.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    r_box = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                   edgecolor="#0277bd", facecolor="#e1f5fe", lw=1.2)
    ax_rescue.add_patch(r_box)
    ax_rescue.text(50, 93.0, "Subsystem Current Deconvolution & Uncertainty Budget", 
                   fontsize=7.8, weight='bold', color='#01579b', ha='center', va='center')

    subsystems = [
        ("Subsystem 1: LED PAR Lighting Array (0–400 µmol/m²/s)",
         "Power: 0–25 W (DC current 0.1–1.8 A) | Coupling: S_LED ≈ 8.3 µT/A",
         "Induced Field: ΔB_LED ≈ 2–15 µT DC offset; PWM ripple ~20 nT_RMS at 1 kHz; twisted harness",
         "#1565c0"),
        ("Subsystem 2: Fluidic & Nutrient Delivery Pumps / Valves",
         "Power: 0–8 W (pulsed current 0.5–1.5 A peak) | Coupling: S_pump ≈ 23.3 µT/A",
         "Induced Field: ΔB_pump ≈ 8–35 µT transient DC pulses during scheduled 10-s root irrigation cycles",
         "#00838f"),
        ("Subsystem 3: Thermal Control (Heaters & Thermoelectric Coolers)",
         "Power: 0–30 W (resistive/TEC 1.0–2.5 A continuous) | Coupling: S_thermal ≈ 19.2 µT/A",
         "Induced Field: ΔB_thermal ≈ 12–48 µT continuous DC; dominant during lunar night; bifilar traces mandatory",
         "#d84315"),
        ("Subsystem 4: Avionics, Telemetry & Sensor Power Bus",
         "Power: 3–12 W (quiescent flight bus 0.2–0.8 A) | Coupling: S_bus ≈ 5.0 µT/A",
         "Induced Field: ΔB_bus ≈ 0.5–4 µT static DC baseline shift + high-frequency RF telemetry EMI",
         "#6a1b9a")
    ]

    y_s = 88.0
    for s_title, s_pow, s_field, col in subsystems:
        sb = patches.FancyBboxPatch((5, y_s - 17.5), 90, 17.0, boxstyle="round,pad=0,rounding_size=2",
                                    edgecolor=col, facecolor='#ffffff', lw=1.0)
        ax_rescue.add_patch(sb)
        ax_rescue.text(8, y_s - 4.5, s_title, fontsize=7.1, weight='bold', color=col, va='center')
        ax_rescue.text(8, y_s - 9.5, s_pow, fontsize=6.5, weight='bold', color='#212121', va='center')
        ax_rescue.text(8, y_s - 14.0, s_field, fontsize=6.2, color='#424242', va='center')
        y_s -= 19.5

    # Bottom transfer function banner
    tf_banner = patches.FancyBboxPatch((5, 3.5), 90, 8.5, boxstyle="round,pad=0,rounding_size=2",
                                       edgecolor="#0288d1", facecolor="#ffffff", lw=1.0)
    ax_rescue.add_patch(tf_banner)
    ax_rescue.text(50, 8.8, r"$\mathbf{B}_{\mathrm{ambient}}(t) = \mathbf{B}_{\mathrm{sensor}}(t) - \sum_k \mathbf{S}_k \cdot I_k(t)$  |  Uncertainty Budget: $\pm 2-5$ nT RMS",
                   fontsize=6.8, weight='bold', color='#01579b', ha='center', va='center')
    ax_rescue.text(50, 5.2, r"Resolves sub-nT lunar signal against 2–48 $\mu$T DC spacecraft baseline via calibrated transfer matrices $\mathbf{S}_k$",
                   fontsize=6.2, color='#424242', ha='center', va='center')

    # -------------------------------------------------------------
    # Panel (c): Post-Flight Phenotypic Disambiguation Framework (Full Width)
    # -------------------------------------------------------------
    ax_matrix = fig.add_subplot(gs[1, :])
    ax_matrix.axis('off')
    ax_matrix.set_xlim(0, 100)
    ax_matrix.set_ylim(0, 100)
    ax_matrix.set_title('Post-Flight Phenotypic Risk Disambiguation Matrix (Operational Decision Framework)', weight='bold', pad=10, fontsize=8.8)
    ax_matrix.text(0.00, 1.03, 'c', transform=ax_matrix.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    m_outer = patches.FancyBboxPatch((1, 2), 98, 96, boxstyle="round,pad=0,rounding_size=3",
                                     edgecolor="#5e35b1", facecolor="#f3e5f5", lw=1.2)
    ax_matrix.add_patch(m_outer)
    ax_matrix.text(50, 93.2, "Operational Multi-Stressor Disambiguation Matrix (Evidence Tiers & Validation Endpoints)", 
                   fontsize=8.4, weight='bold', color='#4a148c', ha='center', va='center')

    # 3 Large Side-by-Side Columns
    columns = [
        ("Near-Null Magnetic Field (<1 nT)", "#ffebee", "#c62828", 2.5, 30.5,
         "Cryptochrome flavin radical pairs (FAD/TrpH•+);\nmitochondrial [4Fe-4S] cluster electron transfer.",
         "• Emergence lag (Δt50 = +12 to 36 h); capacity -10 to -30%\n"
         "• Repressed chlorophyll (HEMA1, POR) & anthocyanin (CHS)\n"
         "• Mitochondrial ROS leak; induction of AOX1D & CAT3\n"
         "• Normal nuclear DNA integrity (zero γ-H2AX foci)",
         "• Evidence Tier: Tier 1 (Germination/Greening) & Tier 2\n"
         "• Time Window: Phase I (0–72 h) & Phase II (72–120 h)\n"
         "• Flight Modality: Active vector coil or Permalloy shield\n"
         "• Rescue Validation: Fully rescued by 45 µT; 1g-insensitive",
         "[Diagnostic: Rescued by 45 µT | Insensitive to 1g]"),

        ("Lunar Partial Gravity (0.166 g)", "#e8f5e9", "#2e7d32", 34.75, 30.5,
         "Columella statolith sedimentation kinetics;\nmechanosensitive ion channels (MSL); PIN polar auxin.",
         "• Germination capacity & greening rate are normal\n"
         "• Directional root skewing, waving, & loss of g-angle\n"
         "• Cell wall remodeling (pectin demethylesterification)\n"
         "• Normal CRY signaling; localized apoplastic ROS (RBOH)",
         "• Evidence Tier: Tier 1 (Root Plagiotropism / Cytoskeleton)\n"
         "• Time Window: Continuous 0–120 h post-radicle emergence\n"
         "• Flight Modality: On-board 1g centrifuge control rotor\n"
         "• Rescue Validation: Fully rescued by 1g rotor; B-insensitive",
         "[Diagnostic: Rescued by 1g | Insensitive to B-field]"),

        ("Deep-Space Radiation (GCR / SPE)", "#fff3e0", "#e65100", 67.0, 30.5,
         "Nuclear & organellar DNA double-strand breaks;\nradiolytic hydroxyl free radical (OH•) overflow.",
         "• Severe DNA double-strand breaks & γ-H2AX foci\n"
         "• ATM/ATR activation; chromosome aberrations & G2/M arrest\n"
         "• Widespread systemic oxidative stress & lipid peroxidation\n"
         "• Low-dose GCR (60–100 mGy/yr): negligible 5-day penalty\n"
         "• Acute SPE (>0.5 Gy): catastrophic cell cycle arrest",
         "• Evidence Tier: Tier 1 (Dosimetry / γ-H2AX) & Tier 2\n"
         "• Time Window: Chronic GCR accumulation vs SPE event\n"
         "• Flight Modality: Silicon dosimeter / radioprotectant\n"
         "• Rescue Validation: Independent of B-field and 1g centrifuge",
         "[Diagnostic: Correlates with Dosimeter | DNA Breaks]")
    ]

    for title, bg_col, edge_col, x_pos, width, target, pheno, strat, tag in columns:
        col_box = patches.FancyBboxPatch((x_pos, 4.5), width, 85, boxstyle="round,pad=0,rounding_size=2",
                                         edgecolor=edge_col, facecolor='#ffffff', lw=1.1)
        ax_matrix.add_patch(col_box)
        
        # Header banner inside column
        hb = patches.FancyBboxPatch((x_pos, 82), width, 7.5, boxstyle="round,pad=0,rounding_size=2",
                                    edgecolor=edge_col, facecolor=bg_col, lw=1.0)
        ax_matrix.add_patch(hb)
        ax_matrix.text(x_pos + width/2, 85.7, title, fontsize=7.2, weight='bold', color=edge_col, ha='center', va='center')
        
        # Section 1: Target
        ax_matrix.text(x_pos + 1.2, 78.5, "Primary Biophysical Target:", fontsize=6.8, weight='bold', color=edge_col)
        ax_matrix.text(x_pos + 1.2, 72.0, target, fontsize=6.2, color='#37474f', linespacing=1.2)
        
        # Section 2: Diagnostic Phenotype
        ax_matrix.text(x_pos + 1.2, 65.5, "Diagnostic Phenotypic Markers:", fontsize=6.8, weight='bold', color=edge_col)
        ax_matrix.text(x_pos + 1.2, 47.5, pheno, fontsize=6.1, color='#212121', linespacing=1.25)
        
        # Section 3: Disambiguation Strategy
        ax_matrix.text(x_pos + 1.2, 30.5, "Operational Strategy & Validation:", fontsize=6.8, weight='bold', color=edge_col)
        ax_matrix.text(x_pos + 1.2, 18.0, strat, fontsize=6.1, color='#37474f', linespacing=1.25)
        
        # Bottom tag
        tag_b = patches.FancyBboxPatch((x_pos + 1.0, 5.8), width - 2.0, 4.8, boxstyle="round,pad=0,rounding_size=1.5",
                                       edgecolor=edge_col, facecolor=bg_col, lw=0.8)
        ax_matrix.add_patch(tag_b)
        ax_matrix.text(x_pos + width/2, 8.2, tag, fontsize=6.0, weight='bold', color=edge_col, ha='center', va='center')

    fig.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.96, hspace=0.28, wspace=0.22)
    for prefix in ['Fig5', 'Fig6']:
        out_pdf = OUT_DIR / f'{prefix}_flight_validation_risk_pipeline.pdf'
        out_png = OUT_DIR / f'{prefix}_flight_validation_risk_pipeline.png'
        fig.savefig(out_pdf, bbox_inches='tight')
        fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 6 successfully created in {OUT_DIR}")

def generate_graphical_abstract():
    fig = plt.figure(figsize=(11.5, 5.0), dpi=300)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.88])
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Main Title
    fig.text(0.5, 0.95, 'Near-Null Magnetic Fields in Lunar Plant Biology: The First 5 Days of Growth', 
             fontsize=13.5, weight='bold', ha='center', color='#0d47a1')

    # Card 1: Lunar Magnetic Reality
    c1 = patches.FancyBboxPatch((2, 3), 30, 93, boxstyle="round,pad=0,rounding_size=3",
                                edgecolor="#0288d1", facecolor="#e1f5fe", lw=1.2)
    ax.add_patch(c1)
    hp1 = patches.FancyBboxPatch((3.5, 86.5), 27, 8.0, boxstyle="round,pad=0,rounding_size=2",
                                 edgecolor="#0288d1", facecolor="#01579b", lw=0.9)
    ax.add_patch(hp1)
    ax.text(17, 90.5, "1. LUNAR MAGNETIC REALITY", fontsize=9.6, weight='bold', color='white', ha='center', va='center')
    
    ax.text(17, 84.5, "• Moon lacks global core dynamo\n• Artemis South Pole: 0.40–0.82 nT\n  (Crustal proxy at 30 km altitude)\n• Deep near-null magnetic void (<1 nT)",
            fontsize=8.8, color='#212121', ha='center', va='top', linespacing=1.38)
    
    mid_box1 = patches.FancyBboxPatch((3.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#0288d1", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box1)
    ax.text(17, 63.5, "Payload Field Architecture:", fontsize=9.4, weight='bold', color='#01579b', ha='center', va='center')
    ax.text(17, 42.5, "B_total = B_crust + B_ext + B_lander\n\nSpacecraft DC (2–48 µT) vs\nAC Ripple (15–50 nT_RMS)\nSwamps Ambient Lunar Void\n──► 3-Axis In Situ Logging Mandatory",
            fontsize=8.5, color='#37474f', ha='center', va='center', linespacing=1.45)

    badge_box1 = patches.FancyBboxPatch((4.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#0288d1", facecolor='white', lw=1.0)
    ax.add_patch(badge_box1)
    ax.text(17, 12.0, "Planetary Environment:\nDeep Near-Null Void (<1 nT)", fontsize=9.2, weight='bold', color="#01579b", ha='center', va='center', linespacing=1.3)

    # Card 2: The First 5 Days of Growth
    c2 = patches.FancyBboxPatch((35, 3), 30, 93, boxstyle="round,pad=0,rounding_size=3",
                                edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.2)
    ax.add_patch(c2)
    hp2 = patches.FancyBboxPatch((36.5, 86.5), 27, 8.0, boxstyle="round,pad=0,rounding_size=2",
                                 edgecolor="#2e7d32", facecolor="#1b5e20", lw=0.8)
    ax.add_patch(hp2)
    ax.text(50, 90.5, "2. FIRST 5 DAYS OF GROWTH", fontsize=9.6, weight='bold', color='white', ha='center', va='center')

    ax.text(50, 84.5, "• Phase I (0–72 h): Heterotrophic\n  peroxisome & lipid catabolism\n• Phase II (72–120 h): Greening\n  photomorphogenic transition",
            fontsize=8.8, color='#212121', ha='center', va='top', linespacing=1.38)

    mid_box2 = patches.FancyBboxPatch((36.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#2e7d32", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box2)
    ax.text(50, 63.5, "Empirical Phenotypes in NNMF:", fontsize=9.4, weight='bold', color='#1b5e20', ha='center', va='center')
    ax.text(50, 42.5, "• Viability: -10 to -30% (Table 3)\n• Velocity: Δt50 = +16 h Lag\n• Dry Biomass: -28.5% Penalty\n• Pigments: HEMA1, CHLH, POR\n  & HY5 Repressed (-1.8 to -2.5x)\n• Mitigated by Fe-EDTA & Sucrose",
            fontsize=8.5, color='#37474f', ha='center', va='center', linespacing=1.45)

    badge_box2 = patches.FancyBboxPatch((37.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#2e7d32", facecolor='white', lw=1.0)
    ax.add_patch(badge_box2)
    ax.text(50, 12.0, "Developmental Penalty:\nViability, Speed, Pigments", fontsize=9.2, weight='bold', color="#1b5e20", ha='center', va='center', linespacing=1.3)

    # Card 3: Multi-Stressor Nexus & Scientific Framework
    c3 = patches.FancyBboxPatch((68, 3), 30, 93, boxstyle="round,pad=0,rounding_size=3",
                                edgecolor="#c2185b", facecolor="#fce4ec", lw=1.2)
    ax.add_patch(c3)
    hp3 = patches.FancyBboxPatch((69.5, 86.5), 27, 8.0, boxstyle="round,pad=0,rounding_size=2",
                                 edgecolor="#c2185b", facecolor="#880e4f", lw=0.8)
    ax.add_patch(hp3)
    ax.text(83, 90.5, "3. SCIENCE & FLIGHT RIGOR", fontsize=9.6, weight='bold', color='white', ha='center', va='center')

    ax.text(83, 84.5, "• Multi-Stressor Disambiguation:\n  NNMF (<1 nT) vs Lunar g (0.166 g)\n  vs Chronic GCR (60–100 mGy/yr)\n• Distinct bioenergetic targets",
            fontsize=8.8, color='#212121', ha='center', va='top', linespacing=1.38)

    mid_box3 = patches.FancyBboxPatch((69.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#c2185b", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box3)
    ax.text(83, 63.5, "Operational Flight Standards:", fontsize=9.4, weight='bold', color='#880e4f', ha='center', va='center')
    ax.text(83, 42.5, "• Ground: 3-Chamber & Bifilar\n  Sham Controls (net B_coil ≈ 0)\n• Flight: In Situ 3-Axis Canopy\n  Magnetometry & Deconvolution\n• Verification: 45 µT Active Rescue",
            fontsize=8.5, color='#37474f', ha='center', va='center', linespacing=1.45)

    badge_box3 = patches.FancyBboxPatch((70.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#c2185b", facecolor='white', lw=1.0)
    ax.add_patch(badge_box3)
    ax.text(83, 12.0, "Operational Standards:\nGround Rigor & Flight Logging", fontsize=9.2, weight='bold', color="#880e4f", ha='center', va='center', linespacing=1.3)

    out_pdf = OUT_DIR / 'Graphical_Abstract_LSSR.pdf'
    out_png = OUT_DIR / 'Graphical_Abstract_LSSR.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')

    # Also save npj Microgravity named files
    fig.savefig(OUT_DIR / 'Graphical_Abstract_npj_Microgravity.pdf', bbox_inches='tight')
    fig.savefig(OUT_DIR / 'Graphical_Abstract_npj_Microgravity.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Graphical Abstract successfully created at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    generate_figure_6()
    generate_graphical_abstract()
