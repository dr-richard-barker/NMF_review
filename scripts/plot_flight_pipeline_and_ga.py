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
    fig = plt.figure(figsize=(11.5, 9.6), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.25], width_ratios=[1.05, 1.0], hspace=0.30, wspace=0.22)

    # -------------------------------------------------------------
    # Panel (a): 3-Chamber Ground Simulation Standards (Scientific Rigor)
    # -------------------------------------------------------------
    ax_cham = fig.add_subplot(gs[0, 0])
    ax_cham.axis('off')
    ax_cham.set_xlim(0, 100)
    ax_cham.set_ylim(0, 100)
    ax_cham.set_title('(a) Methodological Ground Simulation & Chamber Parity', weight='bold')

    chambers = [
        ("Chamber 1: Geomagnetic Control (GMF)", "45–50 µT Ambient Terrestrial Field", "#e3f2fd", "#1565c0", "Terrestrial environmental baseline"),
        ("Chamber 2: Near-Null Field (NNMF)", "<10 nT (Shielded / Actively Cancelled)", "#ffebee", "#c62828", "Lunar surface magnetic simulation"),
        ("Chamber 3: Matched Bifilar Sham Control", "Opposing windings; net B = 0", "#fff3e0", "#e65100", "Controls for ohmic heat, vibration & EMI")
    ]

    for idx, (c_name, b_field, bg, border, desc) in enumerate(chambers):
        y_top = 88 - idx * 28
        b = patches.FancyBboxPatch((3, y_top - 24), 94, 24, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=border, facecolor=bg, lw=1.2)
        ax_cham.add_patch(b)
        ax_cham.text(7, y_top - 6.5, c_name, fontsize=7.6, weight='bold', color=border, va='center')
        ax_cham.text(7, y_top - 13.0, f"Magnetic Regime: {b_field}", fontsize=7.0, weight='bold', color='#212121', va='center')
        ax_cham.text(7, y_top - 19.0, f"Experimental Purpose: {desc}", fontsize=6.8, color='#424242', va='center')

    # -------------------------------------------------------------
    # Panel (b): In Situ Causal Reversal Protocol (Laboratory Rescue)
    # -------------------------------------------------------------
    ax_rescue = fig.add_subplot(gs[0, 1])
    ax_rescue.axis('off')
    ax_rescue.set_xlim(0, 100)
    ax_rescue.set_ylim(0, 100)
    ax_rescue.set_title('(b) In Situ Causal Reversal Protocol (Proof of Concept)', weight='bold')

    r_box = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                   edgecolor="#2e7d32", facecolor="#f1f8e9", lw=1.2)
    ax_rescue.add_patch(r_box)
    ax_rescue.text(50, 91.5, "Three-Step Causal Proof Inside Magnetic Shielding", fontsize=7.8, weight='bold', color='#1b5e20', ha='center', va='center')

    steps = [
        ("Step 1: Hypomagnetic Exposure", "<10 nT inside µ-metal shield", "Elicits emergence lag, chlorosis & ROS leakage", "#c62828"),
        ("Step 2: Vector Re-application", "45 µT active vector restored in situ", "Re-applied via internal triaxial Helmholtz coils", "#1565c0"),
        ("Step 3: Biological Phenotype Rescue", "Phenotype restored to GMF baseline", "Definitively proves direct magnetic causality", "#2e7d32")
    ]

    y_s = 76
    for s_title, s_cond, s_res, col in steps:
        sb = patches.FancyBboxPatch((6, y_s - 18), 88, 18, boxstyle="round,pad=0,rounding_size=2",
                                    edgecolor=col, facecolor='#ffffff', lw=1.0)
        ax_rescue.add_patch(sb)
        ax_rescue.text(10, y_s - 5.0, s_title, fontsize=7.4, weight='bold', color=col, va='center')
        ax_rescue.text(10, y_s - 10.5, s_cond, fontsize=6.8, weight='bold', color='#212121', va='center')
        ax_rescue.text(10, y_s - 15.0, s_res, fontsize=6.6, color='#555555', va='center')
        y_s -= 23

    ax_rescue.text(50, 7.5, "Definitively rules out microclimatic, ethylene, or enclosure artifacts",
                   fontsize=6.8, weight='bold', color='#1b5e20', ha='center', va='center')

    # -------------------------------------------------------------
    # Panel (c): Flight Payload Trade Space: Science Gaps vs. Payload Constraints
    # -------------------------------------------------------------
    ax_trade = fig.add_subplot(gs[1, 0])
    ax_trade.axis('off')
    ax_trade.set_xlim(0, 100)
    ax_trade.set_ylim(100)
    ax_trade.set_title('(c) Flight Payload Trade Space: Science Gaps vs. Engineering Realities', weight='bold')

    outer_trade = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                         edgecolor="#0288d1", facecolor="#e1f5fe", lw=1.2)
    ax_trade.add_patch(outer_trade)

    # Box 1: Realistic Payload Accommodation
    b1 = patches.FancyBboxPatch((5, 52), 90, 42, boxstyle="round,pad=0,rounding_size=2",
                                edgecolor="#1565c0", facecolor="#ffffff", lw=1.0)
    ax_trade.add_patch(b1)
    ax_trade.text(8, 88.0, "Realistic Flight Payload Accommodation (Recommended):", fontsize=7.8, weight='bold', color='#0d47a1')
    ax_trade.text(8, 70.0, 
                  "• Passive 3-axis magnetic sensing (miniature fluxgate or AMR)\n"
                  "• Canopy-level environmental vector logging (Bx, By, Bz, |B|)\n"
                  "• Minimal resource budget: < 1 W electrical power, grams mass\n"
                  "• Continuous logging captures spacecraft DC avionics & stray fields\n"
                  "• Enables post-flight correlative science & phenotype attribution",
                  fontsize=6.8, color='#263238', linespacing=1.35)

    # Box 2: Beyond Typical Flight Envelope
    b2 = patches.FancyBboxPatch((5, 6), 90, 42, boxstyle="round,pad=0,rounding_size=2",
                                edgecolor="#c62828", facecolor="#ffffff", lw=1.0)
    ax_trade.add_patch(b2)
    ax_trade.text(8, 42.0, "Exceeds Typical Flight Payload Resource Budgets (Ground-Only):", fontsize=7.8, weight='bold', color='#b71c1c')
    ax_trade.text(8, 24.0,
                  "• Active triaxial Helmholtz cancellation / bias coil hardware\n"
                  "• Heavy copper coil mass, high continuous power draw & Joule heat\n"
                  "• Severe spacecraft electromagnetic interference (EMI) certification\n"
                  "• Complex in-flight closed-loop vector control systems\n"
                  "• Best reserved for terrestrial laboratory analogues & ground testing",
                  fontsize=6.8, color='#263238', linespacing=1.35)

    # -------------------------------------------------------------
    # Panel (d): Post-Flight Phenotypic Disambiguation Matrix
    # -------------------------------------------------------------
    ax_matrix = fig.add_subplot(gs[1, 1])
    ax_matrix.axis('off')
    ax_matrix.set_xlim(0, 100)
    ax_matrix.set_ylim(0, 100)
    ax_matrix.set_title('(d) Post-Flight Phenotypic Disambiguation Framework', weight='bold')

    m_outer = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                     edgecolor="#5e35b1", facecolor="#ede7f6", lw=1.2)
    ax_matrix.add_patch(m_outer)
    ax_matrix.text(50, 92.0, "Differentiating Environmental Stressors in Lunar Agricultural Payloads", 
                   fontsize=7.8, weight='bold', color='#4527a0', ha='center', va='center')

    stressors = [
        ("Near-Null Magnetic Field (<10 nT)", "#ffebee", "#c62828",
         "• Emergence lag (Δt50 = +12–36 h); capacity drop 10–30%\n"
         "• Repressed chlorophyll (HEMA1, POR) & anthocyanins (CHS)\n"
         "• Mitochondrial ROS leak (AOX1D, CAT3); intact nuclear DNA\n"
         "• Diagnostic: Rescued by 45 µT vector; insensitive to 1g spin"),
        
        ("Lunar Partial Gravity (0.166 g)", "#e8f5e9", "#2e7d32",
         "• Normal germination capacity; minimal emergence lag\n"
         "• Directional skewing, random root waving, cell wall remodeling\n"
         "• Normal plastid greening; apoplastic ROS (RBOHD/F)\n"
         "• Diagnostic: Rescued by 1g centrifuge; insensitive to B-field"),
        
        ("Deep-Space Ionizing Radiation (GCR)", "#fff3e0", "#e65100",
         "• Emergence failure only at lethal doses; apical arrest\n"
         "• Severe DNA double-strand breaks, γ-H2AX foci & ATM/ATR\n"
         "• Widespread systemic oxidative damage & lipid peroxidation\n"
         "• Diagnostic: Mitigated by shielding; correlated with dosimeter")
    ]

    y_m = 75
    for s_title, s_bg, s_border, s_desc in stressors:
        box = patches.FancyBboxPatch((5, y_m - 23), 90, 23, boxstyle="round,pad=0,rounding_size=2",
                                     edgecolor=s_border, facecolor=s_bg, lw=1.0)
        ax_matrix.add_patch(box)
        ax_matrix.text(8, y_m - 4.5, s_title, fontsize=7.2, weight='bold', color=s_border, va='center')
        ax_matrix.text(8, y_m - 14.0, s_desc, fontsize=6.3, color='#212121', va='center', linespacing=1.25)
        y_m -= 26

    fig.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.96, hspace=0.28, wspace=0.22)
    out_pdf = OUT_DIR / 'Fig5_flight_validation_risk_pipeline.pdf'
    out_png = OUT_DIR / 'Fig5_flight_validation_risk_pipeline.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 5 successfully created at:\n  {out_png}\n  {out_pdf}")

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
