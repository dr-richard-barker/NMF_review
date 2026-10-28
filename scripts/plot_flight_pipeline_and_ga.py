#!/usr/bin/env python3
"""
plot_flight_pipeline_and_ga.py

Generates:
1. Figure 5: Flight Validation, Causal Rescue & Artemis Payload Decision Pipeline
2. Graphical Abstract for Life Sciences in Space Research
"""

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
    fig = plt.figure(figsize=(11.5, 9.2), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.1], width_ratios=[1.15, 1.0], hspace=0.30, wspace=0.22)

    # -------------------------------------------------------------
    # Panel (a): 3-Chamber Ground Simulation Standards
    # -------------------------------------------------------------
    ax_cham = fig.add_subplot(gs[0, 0])
    ax_cham.axis('off')
    ax_cham.set_xlim(0, 100)
    ax_cham.set_ylim(0, 100)
    ax_cham.set_title('(a) Methodological Ground Simulation & Chamber Parity', weight='bold')

    chambers = [
        ("Chamber 1: GMF Control", "45–50 µT Ambient GMF", "#e3f2fd", "#1565c0", "Terrestrial baseline"),
        ("Chamber 2: Near-Null (NNMF)", "<10 nT (Shielded/Cancelled)", "#ffebee", "#c62828", "Lunar simulation"),
        ("Chamber 3: Sham Control", "Current matched; B = 0", "#fff3e0", "#e65100", "Controls ohmic heat & EMI")
    ]

    for idx, (c_name, b_field, bg, border, desc) in enumerate(chambers):
        y_top = 88 - idx * 28
        b = patches.FancyBboxPatch((4, y_top - 24), 92, 24, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=border, facecolor=bg, lw=1.2)
        ax_cham.add_patch(b)
        ax_cham.text(8, y_top - 6.5, c_name, fontsize=7.6, weight='bold', color=border, va='center')
        ax_cham.text(8, y_top - 13.0, f"Magnetic Regime: {b_field}", fontsize=7.0, weight='bold', color='#212121', va='center')
        ax_cham.text(8, y_top - 19.0, f"Control Purpose: {desc}", fontsize=6.8, color='#424242', va='center')

    # -------------------------------------------------------------
    # Panel (b): Active Causal Rescue Architecture
    # -------------------------------------------------------------
    ax_rescue = fig.add_subplot(gs[0, 1])
    ax_rescue.axis('off')
    ax_rescue.set_xlim(0, 100)
    ax_rescue.set_ylim(0, 100)
    ax_rescue.set_title('(b) Active Causal Rescue Validation Protocol', weight='bold')

    r_box = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                   edgecolor="#2e7d32", facecolor="#f1f8e9", lw=1.2)
    ax_rescue.add_patch(r_box)
    ax_rescue.text(50, 91.5, "Causal Rescue Inside Magnetic Shielding", fontsize=7.8, weight='bold', color='#1b5e20', ha='center', va='center')

    steps = [
        ("Step 1: Hypomagnetic Exposure", "<10 nT inside µ-metal shield", "Elicits germination & pigment phenotype", "#c62828"),
        ("Step 2: Vector Re-application", "45 µT active vector restored", "Re-applied via triaxial Helmholtz coils", "#1565c0"),
        ("Step 3: Biological Reversal", "Phenotype rescued to GMF level", "Formally proves magnetic causality", "#2e7d32")
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

    # Footnote safely inside r_box
    ax_rescue.text(50, 7.5, "Rules out microclimatic, volatile, or enclosure artifacts",
                   fontsize=6.8, weight='bold', color='#1b5e20', ha='center', va='center')

    # -------------------------------------------------------------
    # Panel (c): Predeclared Artemis Flight Decision Gates
    # -------------------------------------------------------------
    ax_gates = fig.add_subplot(gs[1, :])
    ax_gates.axis('off')
    ax_gates.set_xlim(0, 100)
    ax_gates.set_ylim(0, 100)
    ax_gates.set_title('(c) Predeclared Flight Decision Framework for Lunar Agricultural Payloads (LEAF / BLSS)', fontsize=9.5, weight='bold')

    gates = [
        ("GREEN GATE: Nominal (Retire Risk)", "#e8f5e9", "#2e7d32", 
         "• Germination rate drop < 5%\n• Emergence delay (Δt50) < 6 h\n• Fv/Fm photochemical yield nominal\n• No significant biomass penalty",
         "Retire hypomagnetic risk from critical path.\nProceed with standard autonomous operations,\nambient LED photoperiods, & baseline harvest."),
        ("AMBER GATE: Operational Shift", "#fffde7", "#fbc02d",
         "• Germination rate drop 5–20%\n• Emergence delay (Δt50) 6–24 h\n• 10–25% reduction in seedling biomass\n• Moderate chlorosis / delayed greening",
         "Adjust mission schedule:\n• Increase seed sowing density by 15–20%\n• Extend growth duration prior to harvest\n• Boost blue-light ratio for photomorphogenesis."),
        ("RED GATE: Hazard Mitigation", "#ffebee", "#d32f2f",
         "• Germination capacity drop > 20%\n• Severe emergence failure (Δt50 > 24 h)\n• Severe ROS leak & photosynthetic failure\n• > 30% collapse in harvestable yield",
         "Mandate hardware & biological mitigation:\n• Deploy low-power active bias coils (40–50 µT)\n• Switch to stress-tolerant crop cultivars\n• Supplement feed with antioxidant cofactors.")
    ]

    for idx, (g_name, bg, border, thresh, action) in enumerate(gates):
        x_left = 2.5 + idx * 32.5
        b = patches.FancyBboxPatch((x_left, 4), 31.5, 91, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=border, facecolor=bg, lw=1.3)
        ax_gates.add_patch(b)
        ax_gates.text(x_left + 15.75, 90.0, g_name, fontsize=8.8, weight='bold', color=border, ha='center', va='center')
        
        # Section 1: Empirical Thresholds
        ax_gates.text(x_left + 2.5, 84.5, "Empirical Thresholds:", fontsize=8.3, weight='bold', color='#212121', va='top')
        ax_gates.text(x_left + 2.5, 78.5, thresh, fontsize=7.8, color='#333333', va='top', linespacing=1.4)
        
        # Action line separator
        ax_gates.plot([x_left + 2, x_left + 29.5], [46, 46], color=border, lw=0.9, linestyle='--')
        
        # Section 2: Flight Operational Action
        ax_gates.text(x_left + 2.5, 42.5, "Flight Operational Action:", fontsize=8.3, weight='bold', color='#1a237e', va='top')
        ax_gates.text(x_left + 2.5, 36.5, action, fontsize=7.8, color='#1a237e', va='top', linespacing=1.4)

    fig.subplots_adjust(top=0.95, bottom=0.06, left=0.06, right=0.96, hspace=0.28, wspace=0.22)
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
    ax.text(17, 42.5, "Btotal = Bcrust + Bext + Blander\n\nLander Avionics (50–500 µT)\nSwamps Ambient Lunar HMF\n──► Strict Shielding Required",
            fontsize=9.0, color='#37474f', ha='center', va='center', linespacing=1.55)

    badge_box1 = patches.FancyBboxPatch((4.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#0288d1", facecolor='white', lw=1.0)
    ax.add_patch(badge_box1)
    ax.text(17, 12.0, "Core Concept 1:\nPhysical Reality of Lunar HMF", fontsize=9.4, weight='bold', color="#01579b", ha='center', va='center', linespacing=1.35)

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
    ax.text(50, 42.5, "• Viability: -20% (# Seedlings)\n• Velocity: Δt50 = +16 h Lag\n• Dry Biomass: -28.5% Loss\n• Pigments: HEMA1, CHLH, POR\n  & HY5 Repressed (-1.8 to -2.5x)",
            fontsize=9.0, color='#37474f', ha='center', va='center', linespacing=1.55)

    badge_box2 = patches.FancyBboxPatch((37.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#2e7d32", facecolor='white', lw=1.0)
    ax.add_patch(badge_box2)
    ax.text(50, 12.0, "Core Concepts 2, 3, 4:\nViability, Speed, Pigments", fontsize=9.4, weight='bold', color="#1b5e20", ha='center', va='center', linespacing=1.35)

    # Card 3: Multi-Stressor Nexus & Flight Decisions
    c3 = patches.FancyBboxPatch((68, 3), 30, 93, boxstyle="round,pad=0,rounding_size=3",
                                edgecolor="#c2185b", facecolor="#fce4ec", lw=1.2)
    ax.add_patch(c3)
    hp3 = patches.FancyBboxPatch((69.5, 86.5), 27, 8.0, boxstyle="round,pad=0,rounding_size=2",
                                 edgecolor="#c2185b", facecolor="#880e4f", lw=0.8)
    ax.add_patch(hp3)
    ax.text(83, 90.5, "3. MULTI-STRESSOR NEXUS", fontsize=9.6, weight='bold', color='white', ha='center', va='center')

    ax.text(83, 84.5, "• Exploration Atmosphere (8.2 psia)\n• Elevated CO2 (1200–3000 ppm)\n• GCR Ionizing Radiation (1 Gy)\n• Shared organellar bioenergetics",
            fontsize=9.0, color='#212121', ha='center', va='top', linespacing=1.42)

    mid_box3 = patches.FancyBboxPatch((69.5, 21.5), 27, 45.5, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#c2185b", facecolor="#ffffff", lw=1.0)
    ax.add_patch(mid_box3)
    ax.text(83, 63.5, "Mitochondrial Hub & Flight Action:", fontsize=9.6, weight='bold', color='#880e4f', ha='center', va='center')
    ax.text(83, 42.5, "• Coregulated: AOX1D & CAT3 (+)\n• Cross-Kingdom: Parallels\n  astronaut mitochondrial stress\n• Flight Operations: Predeclared\n  Gates (Green / Amber / Red)",
            fontsize=9.0, color='#37474f', ha='center', va='center', linespacing=1.55)

    badge_box3 = patches.FancyBboxPatch((70.5, 4.5), 25, 15.0, boxstyle="round,pad=0,rounding_size=2",
                                        edgecolor="#c2185b", facecolor='white', lw=1.0)
    ax.add_patch(badge_box3)
    ax.text(83, 12.0, "Core Concept 5:\nCO2 ↔ O2 ↔ ROS Nexus", fontsize=9.4, weight='bold', color="#880e4f", ha='center', va='center', linespacing=1.35)

    out_pdf = OUT_DIR / 'Graphical_Abstract_LSSR.pdf'
    out_png = OUT_DIR / 'Graphical_Abstract_LSSR.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Graphical Abstract successfully created at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    generate_figure_5()
    generate_graphical_abstract()
