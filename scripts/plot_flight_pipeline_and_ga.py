#!/usr/bin/env python3
"""
plot_flight_pipeline_and_ga.py

Generates:
1. Figure 5: Scientific Knowledge Gap Retirement, Ground Simulation Standards,
   and Flight Instrumentation Trade Space
2. Graphical Abstract for Life Sciences in Space Research
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

def generate_figure_5():
    fig = plt.figure(figsize=(11.5, 9.4), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.35], width_ratios=[1.0, 1.0], hspace=0.28, wspace=0.24)

    # -------------------------------------------------------------
    # Panel (a): 3-Chamber Ground Simulation Standards (Scientific Rigor)
    # -------------------------------------------------------------
    ax_cham = fig.add_subplot(gs[0, 0])
    ax_cham.axis('off')
    ax_cham.set_xlim(0, 100)
    ax_cham.set_ylim(0, 100)
    ax_cham.set_title('Methodological Ground Simulation Standards (3-Chamber Parity)', weight='bold', pad=10, fontsize=8.8)
    ax_cham.text(0.00, 1.03, 'a', transform=ax_cham.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    chambers = [
        ("Chamber 1: Geomagnetic Baseline (GMF)", "45–50 µT Ambient Terrestrial Field", "#e3f2fd", "#1565c0", "Terrestrial environmental control (calibrated local vector)"),
        ("Chamber 2: Near-Null Field Simulation (NNMF)", "<10 nT (Shielded / Actively Cancelled)", "#ffebee", "#c62828", "Lunar surface magnetic simulation (<0.8 nT ambient void)"),
        ("Chamber 3: Matched Bifilar Sham Control", "Opposing windings; net B = 0", "#fff3e0", "#e65100", "Controls for ohmic heat, acoustic vibration & power-supply ripple")
    ]

    for idx, (c_name, b_field, bg, border, desc) in enumerate(chambers):
        y_top = 88 - idx * 28
        b = patches.FancyBboxPatch((3, y_top - 24), 94, 24, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=border, facecolor=bg, lw=1.2)
        ax_cham.add_patch(b)
        ax_cham.text(7, y_top - 6.5, c_name, fontsize=7.8, weight='bold', color=border, va='center')
        ax_cham.text(7, y_top - 13.0, f"Magnetic Regime: {b_field}", fontsize=7.0, weight='bold', color='#212121', va='center')
        ax_cham.text(7, y_top - 19.0, f"Experimental Purpose: {desc}", fontsize=6.8, color='#424242', va='center')

    # -------------------------------------------------------------
    # Panel (b): Hardware Self-Magnetic Assessment Protocol (Power-State Mapping)
    # -------------------------------------------------------------
    ax_rescue = fig.add_subplot(gs[0, 1])
    ax_rescue.axis('off')
    ax_rescue.set_xlim(0, 100)
    ax_rescue.set_ylim(0, 100)
    ax_rescue.set_title('Hardware Self-Magnetic Assessment Protocol (Power-State Mapping)', weight='bold', pad=10, fontsize=8.8)
    ax_rescue.text(0.00, 1.03, 'b', transform=ax_rescue.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    r_box = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                   edgecolor="#0277bd", facecolor="#e1f5fe", lw=1.2)
    ax_rescue.add_patch(r_box)
    ax_rescue.text(50, 92.5, "Subsystem Power-State Magnetic Characterization & Deconvolution", 
                   fontsize=7.8, weight='bold', color='#01579b', ha='center', va='center')

    subsystems = [
        ("Subsystem 1: LED PAR Lighting Array (0–400 µmol/m²/s)",
         "Power: 0 to 25 W (DC driver current 0.1–1.8 A)",
         "Induced Field: ΔB_LED ≈ 2–15 µT; proportional to photon flux; balanced routing minimizes loop area",
         "#1565c0"),
        ("Subsystem 2: Fluidic & Nutrient Delivery Pumps / Valves",
         "Power: 0 to 8 W (peristaltic/piezo motor pulses, 0.5–1.5 A peak)",
         "Induced Field: ΔB_pump ≈ 8–35 µT; transient DC spikes during scheduled root module irrigation cycles",
         "#00838f"),
        ("Subsystem 3: Thermal Control (Heaters & Thermoelectric Coolers)",
         "Power: 0 to 30 W (resistive strips / TEC elements, 1.0–2.5 A continuous)",
         "Induced Field: ΔB_thermal ≈ 12–48 µT; dominant DC contributor during cold lunar nights; bifilar loops required",
         "#d84315"),
        ("Subsystem 4: Avionics, Telemetry & Sensor Power Bus",
         "Power: 3 to 12 W (quiescent flight computer + RF comm transmission)",
         "Induced Field: ΔB_bus ≈ 0.5–4 µT; static baseline shift + RF ripple; mapped via quiescent baseline calibration",
         "#6a1b9a")
    ]

    y_s = 88.0
    for s_title, s_pow, s_field, col in subsystems:
        sb = patches.FancyBboxPatch((5, y_s - 17.5), 90, 17.0, boxstyle="round,pad=0,rounding_size=2",
                                    edgecolor=col, facecolor='#ffffff', lw=1.0)
        ax_rescue.add_patch(sb)
        ax_rescue.text(8, y_s - 4.5, s_title, fontsize=7.1, weight='bold', color=col, va='center')
        ax_rescue.text(8, y_s - 9.5, s_pow, fontsize=6.6, weight='bold', color='#212121', va='center')
        ax_rescue.text(8, y_s - 14.0, s_field, fontsize=6.3, color='#424242', va='center')
        y_s -= 19.5

    # Bottom transfer function banner
    tf_banner = patches.FancyBboxPatch((5, 3.0), 90, 7.5, boxstyle="round,pad=0,rounding_size=2",
                                       edgecolor="#0288d1", facecolor="#ffffff", lw=1.0)
    ax_rescue.add_patch(tf_banner)
    ax_rescue.text(50, 6.75, r"$\mathbf{B}_{\mathrm{ambient}}(t) = \mathbf{B}_{\mathrm{sensor}}(t) - \sum_k \Delta\mathbf{B}_k(P_k(t))$ : Computational Self-Field Subtraction",
                   fontsize=6.8, weight='bold', color='#01579b', ha='center', va='center')

    # -------------------------------------------------------------
    # Panel (c): Post-Flight Phenotypic Disambiguation Framework (Full Width)
    # -------------------------------------------------------------
    ax_matrix = fig.add_subplot(gs[1, :])
    ax_matrix.axis('off')
    ax_matrix.set_xlim(0, 100)
    ax_matrix.set_ylim(0, 100)
    ax_matrix.set_title('Post-Flight Phenotypic Risk Disambiguation Framework', weight='bold', pad=10, fontsize=8.8)
    ax_matrix.text(0.00, 1.03, 'c', transform=ax_matrix.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    m_outer = patches.FancyBboxPatch((1, 2), 98, 96, boxstyle="round,pad=0,rounding_size=3",
                                     edgecolor="#5e35b1", facecolor="#f3e5f5", lw=1.2)
    ax_matrix.add_patch(m_outer)
    ax_matrix.text(50, 93.0, "Operational Multi-Stressor Disambiguation Matrix for Space Plant Biology", 
                   fontsize=8.4, weight='bold', color='#4a148c', ha='center', va='center')

    # 3 Large Side-by-Side Columns
    columns = [
        ("Near-Null Magnetic Field (<0.8 nT)", "#ffebee", "#c62828", 2.5, 30.5,
         "Cryptochrome flavin radical pairs (FAD/TrpH•+);\nmitochondrial [4Fe-4S] cluster electron transfer.",
         "• Emergence lag (Δt50 = +12 to 36 h); capacity -10 to -30%\n"
         "• Repressed chlorophyll (HEMA1, POR) & anthocyanin (CHS)\n"
         "• Mitochondrial ROS leak; induction of AOX1D & CAT3\n"
         "• Normal nuclear DNA integrity (zero γ-H2AX foci)",
         "• Correlate with sample-level 3-axis canopy magnetometry\n"
         "• Fully rescued by 45 µT vector re-application\n"
         "• Completely insensitive to 1g centrifuge spinning",
         "[Diagnostic: Rescued by 45 µT | Insensitive to 1g]"),

        ("Lunar Partial Gravity (0.166 g)", "#e8f5e9", "#2e7d32", 34.75, 30.5,
         "Columella statolith sedimentation kinetics;\nmechanosensitive ion channels (MSL); PIN polar auxin.",
         "• Germination capacity & greening rate are normal\n"
         "• Directional root skewing, waving, & loss of g-angle\n"
         "• Cell wall remodeling (pectin demethylesterification)\n"
         "• Normal CRY signaling; localized apoplastic ROS (RBOH)",
         "• Fully rescued to Earth phenotype by 1g centrifuge\n"
         "• Differential 1g vs µg controls in flight centrifuge\n"
         "• Completely unaffected by magnetic vector modulation",
         "[Diagnostic: Rescued by 1g | Insensitive to B-field]"),

        ("Deep-Space Radiation (GCR / SPE)", "#fff3e0", "#e65100", 67.0, 30.5,
         "Nuclear & organellar DNA double-strand breaks;\nradiolytic hydroxyl free radical (OH•) overflow.",
         "• Severe DNA double-strand breaks & γ-H2AX foci\n"
         "• ATM/ATR activation; chromosome aberrations & G2/M arrest\n"
         "• Widespread systemic oxidative stress & lipid peroxidation\n"
         "• Emergence fails only at acute lethal doses (>50 Gy)",
         "• Independent of magnetic field or gravity vector\n"
         "• Strictly correlates with canopy radiation dosimeters\n"
         "• Mitigated by shielding & chemical radioprotectants",
         "[Diagnostic: Correlates with Dosimeter | DNA Breaks]")
    ]

    for title, bg_col, edge_col, x_pos, width, target, pheno, strat, tag in columns:
        col_box = patches.FancyBboxPatch((x_pos, 5), width, 84, boxstyle="round,pad=0,rounding_size=2",
                                         edgecolor=edge_col, facecolor='#ffffff', lw=1.1)
        ax_matrix.add_patch(col_box)
        
        # Header banner inside column
        hb = patches.FancyBboxPatch((x_pos, 81), width, 8, boxstyle="round,pad=0,rounding_size=2",
                                    edgecolor=edge_col, facecolor=bg_col, lw=1.0)
        ax_matrix.add_patch(hb)
        ax_matrix.text(x_pos + width/2, 85.0, title, fontsize=7.2, weight='bold', color=edge_col, ha='center', va='center')
        
        # Section 1: Target
        ax_matrix.text(x_pos + 1.2, 77.0, "Primary Biophysical Target:", fontsize=6.8, weight='bold', color=edge_col)
        ax_matrix.text(x_pos + 1.2, 70.5, target, fontsize=6.3, color='#37474f', linespacing=1.2)
        
        # Section 2: Diagnostic Phenotype
        ax_matrix.text(x_pos + 1.2, 63.0, "Diagnostic Phenotypic Markers:", fontsize=6.8, weight='bold', color=edge_col)
        ax_matrix.text(x_pos + 1.2, 45.0, pheno, fontsize=6.2, color='#212121', linespacing=1.25)
        
        # Section 3: Disambiguation Strategy
        ax_matrix.text(x_pos + 1.2, 28.0, "Disambiguation & Rescue Strategy:", fontsize=6.8, weight='bold', color=edge_col)
        ax_matrix.text(x_pos + 1.2, 17.0, strat, fontsize=6.2, color='#37474f', linespacing=1.25)
        
        # Bottom tag
        tag_b = patches.FancyBboxPatch((x_pos + 1.0, 6.2), width - 2.0, 5.0, boxstyle="round,pad=0,rounding_size=1.5",
                                       edgecolor=edge_col, facecolor=bg_col, lw=0.8)
        ax_matrix.add_patch(tag_b)
        ax_matrix.text(x_pos + width/2, 8.7, tag, fontsize=6.0, weight='bold', color=edge_col, ha='center', va='center')

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
    
    ax.text(17, 84.5, "• Moon lacks global core dynamo\n• Artemis South Pole: < 0.8 nT\n  (Deep near-null magnetic void)\n• Microclimatic field variation",
            fontsize=9.0, color='#212121', ha='center', va='top', linespacing=1.42)
    
    mid_box1 = patches.FancyBboxPatch((3.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#0288d1", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box1)
    ax.text(17, 63.5, "Payload Field Architecture:", fontsize=9.6, weight='bold', color='#01579b', ha='center', va='center')
    ax.text(17, 42.5, "Btotal = Bcrust + Bext + Blander\n\nLander Avionics (50–500 µT)\nSwamps Ambient Lunar HMF\n──► In Situ Sensor Required",
            fontsize=9.0, color='#37474f', ha='center', va='center', linespacing=1.55)

    badge_box1 = patches.FancyBboxPatch((4.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#0288d1", facecolor='white', lw=1.0)
    ax.add_patch(badge_box1)
    ax.text(17, 12.0, "Planetary Environment:\nExtreme Lunar HMF (<0.8 nT)", fontsize=9.4, weight='bold', color="#01579b", ha='center', va='center', linespacing=1.35)

    # Card 2: The First 5 Days of Growth
    c2 = patches.FancyBboxPatch((35, 3), 30, 93, boxstyle="round,pad=0,rounding_size=3",
                                edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.2)
    ax.add_patch(c2)
    hp2 = patches.FancyBboxPatch((36.5, 86.5), 27, 8.0, boxstyle="round,pad=0,rounding_size=2",
                                 edgecolor="#2e7d32", facecolor="#1b5e20", lw=0.8)
    ax.add_patch(hp2)
    ax.text(50, 90.5, "2. FIRST 5 DAYS OF GROWTH", fontsize=9.6, weight='bold', color='white', ha='center', va='center')

    ax.text(50, 84.5, "• 0–72 h Heterotrophic Bottleneck\n• Peroxisomal beta-oxidation\n• Mitochondrial restart burst\n• Plastid greening transition",
            fontsize=9.0, color='#212121', ha='center', va='top', linespacing=1.42)

    mid_box2 = patches.FancyBboxPatch((36.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#2e7d32", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box2)
    ax.text(50, 63.5, "Empirical Phenotypes in NNMF:", fontsize=9.6, weight='bold', color='#1b5e20', ha='center', va='center')
    ax.text(50, 42.5, "• Viability: -10 to -30% (# Plants)\n• Velocity: Δt50 = +16 h Lag\n• Dry Biomass: -28.5% Penalty\n• Pigments: HEMA1, CHLH, POR\n  & HY5 Repressed (-1.8 to -2.5x)",
            fontsize=9.0, color='#37474f', ha='center', va='center', linespacing=1.55)

    badge_box2 = patches.FancyBboxPatch((37.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#2e7d32", facecolor='white', lw=1.0)
    ax.add_patch(badge_box2)
    ax.text(50, 12.0, "Developmental Penalty:\nViability, Speed, Pigments", fontsize=9.4, weight='bold', color="#1b5e20", ha='center', va='center', linespacing=1.35)

    # Card 3: Multi-Stressor Nexus & Scientific Framework
    c3 = patches.FancyBboxPatch((68, 3), 30, 93, boxstyle="round,pad=0,rounding_size=3",
                                edgecolor="#c2185b", facecolor="#fce4ec", lw=1.2)
    ax.add_patch(c3)
    hp3 = patches.FancyBboxPatch((69.5, 86.5), 27, 8.0, boxstyle="round,pad=0,rounding_size=2",
                                 edgecolor="#c2185b", facecolor="#880e4f", lw=0.8)
    ax.add_patch(hp3)
    ax.text(83, 90.5, "3. RISK & SCIENCE FRAMEWORK", fontsize=9.6, weight='bold', color='white', ha='center', va='center')

    ax.text(83, 84.5, "• Exploration Atmosphere (8.2 psia)\n• Elevated CO2 (1200–3000 ppm)\n• GCR Ionizing Radiation (1 Gy)\n• Shared organellar bioenergetics",
            fontsize=9.0, color='#212121', ha='center', va='top', linespacing=1.42)

    mid_box3 = patches.FancyBboxPatch((69.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#c2185b", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box3)
    ax.text(83, 63.5, "Rigorous Science & Flight Strategy:", fontsize=9.6, weight='bold', color='#880e4f', ha='center', va='center')
    ax.text(83, 42.5, "• Ground Rigor: 3-chamber & bifilar\n  sham controls + causal rescue\n• Flight Payloads: Realistic 3-axis\n  canopy magnetic vector logging\n• Science: Phenotype disambiguation",
            fontsize=9.0, color='#37474f', ha='center', va='center', linespacing=1.55)

    badge_box3 = patches.FancyBboxPatch((70.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#c2185b", facecolor='white', lw=1.0)
    ax.add_patch(badge_box3)
    ax.text(83, 12.0, "Operational Translation:\nGround Rigor & Flight Logging", fontsize=9.4, weight='bold', color="#880e4f", ha='center', va='center', linespacing=1.35)

    out_pdf = OUT_DIR / 'Graphical_Abstract_LSSR.pdf'
    out_png = OUT_DIR / 'Graphical_Abstract_LSSR.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Graphical Abstract successfully created at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    generate_figure_5()
    generate_graphical_abstract()
