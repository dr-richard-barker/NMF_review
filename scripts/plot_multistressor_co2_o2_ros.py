#!/usr/bin/env python3
"""
plot_multistressor_co2_o2_ros.py

Generates Figure 4 for Life Sciences in Space Research:
Multi-Stressor Convergence: The CO2 <-> O2 <-> ROS Nexus across Hypomagnetic Fields,
Exploration Atmosphere, and Ionizing Radiation.
Panels:
(a) Environmental Stressor Space: Exploration Atmosphere, Lunar HMF, and GCR Radiation
(b) The Mitochondrial & Peroxisomal CO2 <-> O2 <-> ROS Bioenergetic Engine
(c) Multi-Omics Empirical Convergence: Shared Responsive Loci (OSD-782 Radiation vs. Parmagnani 2022 NNMF)
(d) Cross-Kingdom Convergence: Plant BLSS Resilience & Human Astronaut Mitochondrial Health
"""

import json
import numpy as np
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
OVERLAP_FILE = Path('/Users/drb_laptop/Documents/quantum-biology-atlas/results/overlap/record.json')

def main():
    fig = plt.figure(figsize=(11.8, 9.6), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.15], width_ratios=[1.1, 1.15], hspace=0.30, wspace=0.24)

    # -------------------------------------------------------------
    # Panel (a): Environmental Parameters Comparison
    # -------------------------------------------------------------
    ax_env = fig.add_subplot(gs[0, 0])
    ax_env.axis('off')
    ax_env.set_xlim(0, 100)
    ax_env.set_ylim(0, 100)
    ax_env.set_title('(a) Multi-Stressor Space: Exploration Baseline vs. Lunar Reality', weight='bold')

    # Draw table/cards comparing Earth Baseline vs NASA Exploration Atmosphere vs Lunar Ambient
    envs = [
        ("Terrestrial Baseline (1 g)", "#e8f5e9", "#2e7d32", [
            ("Atmospheric Pressure", "101.3 kPa (14.7 psia)"),
            ("Oxygen Fraction (O2)", "21% (21.3 kPa pO2)"),
            ("Carbon Dioxide (CO2)", "420 ppm (0.04 kPa pCO2)"),
            ("Magnetic Field (|B|)", "25–65 µT (Dipolar GMF)"),
            ("Ionizing Radiation", "~1–2 mGy/year (Shielded)")
        ]),
        ("Exploration Enclosure & Lunar Surface", "#ffebee", "#c62828", [
            ("Exploration Pressure", "56.5 kPa (8.2 psia) / 34 kPa"),
            ("Elevated Oxygen (O2)", "34% (19.2 kPa pO2)"),
            ("Elevated CO2", "1200–3000 ppm (0.12–0.30 kPa)"),
            ("Lunar Magnetic Field", "<0.5–1 nT (Near-Null Void)"),
            ("Galactic Cosmic Rad.", "100–380 mGy/year (GCR/SPE)")
        ])
    ]

    for idx, (title, bg, border, rows) in enumerate(envs):
        x_left = 3 if idx == 0 else 51
        b = patches.FancyBboxPatch((x_left, 16), 46, 78, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=border, facecolor=bg, lw=1.2)
        ax_env.add_patch(b)
        ax_env.text(x_left + 23, 90, title, fontsize=7.6, weight='bold', color=border, ha='center', va='center')
        
        y_r = 81
        for param, val in rows:
            ax_env.text(x_left + 3, y_r, param + ":", fontsize=6.9, weight='bold', color='#37474f')
            ax_env.text(x_left + 3, y_r - 4.5, val, fontsize=6.9, color='#212121')
            y_r -= 12.5

    # Bottom summary arrow banner
    bot_b = patches.FancyBboxPatch((3, 3), 94, 10.5, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor="#fbc02d", facecolor="#fffde7", lw=0.9)
    ax_env.add_patch(bot_b)
    ax_env.text(50, 8.25, "STRESSOR CONVERGENCE: Combined physical stressors converge on\nmitochondrial terminal oxidases and reactive oxygen species generation",
                fontsize=7.2, weight='bold', color='#b71c1c', ha='center', va='center', linespacing=1.25)

    # -------------------------------------------------------------
    # Panel (b): The CO2 <-> O2 <-> ROS Nexus & Mitochondrial Engine
    # -------------------------------------------------------------
    ax_nexus = fig.add_subplot(gs[0, 1])
    ax_nexus.axis('off')
    ax_nexus.set_xlim(0, 100)
    ax_nexus.set_ylim(0, 100)
    ax_nexus.set_title('(b) The Organellar CO2 <-> O2 <-> ROS Nexus', weight='bold')

    # Big container box
    box_nex = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                    edgecolor="#00838f", facecolor="#e0f7fa", lw=1.2)
    ax_nexus.add_patch(box_nex)

    # Gas balance inputs (Top)
    ax_nexus.text(50, 91.5, "Exploration Atmosphere Gas Balance (CO2 <-> O2)", fontsize=7.8, weight='bold', color='#006064', ha='center', va='center')
    
    # Left: High CO2 suppression of photorespiration
    c_box = patches.FancyBboxPatch((5, 62), 42, 24, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor="#2e7d32", facecolor="#ffffff", lw=1.0)
    ax_nexus.add_patch(c_box)
    ax_nexus.text(26, 79, "Peroxisomal Shunt", fontsize=7.4, weight='bold', color='#1b5e20', ha='center')
    ax_nexus.text(26, 70, "Elevated CO2 (1000–3000 ppm)\nsuppresses RuBisCO oxygenation\n──► Lowers glycolate H2O2", fontsize=6.6, ha='center')

    # Right: Mitochondrial O2 terminal oxidases
    o_box = patches.FancyBboxPatch((53, 62), 42, 24, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor="#c2185b", facecolor="#ffffff", lw=1.0)
    ax_nexus.add_patch(o_box)
    ax_nexus.text(74, 79, "Mitochondrial Terminal Balance", fontsize=7.4, weight='bold', color='#880e4f', ha='center')
    ax_nexus.text(74, 70, "Altered pO2 & hypobaric diffusion:\n• COX (Complex IV): High affinity\n• AOX (Alt. Oxidase): Low affinity", fontsize=6.6, ha='center')

    # Center: The Radical & ROS Hub
    ros_box = patches.FancyBboxPatch((15, 22), 70, 32, boxstyle="round,pad=0,rounding_size=2",
                                     edgecolor="#d32f2f", facecolor="#ffebee", lw=1.4)
    ax_nexus.add_patch(ros_box)
    ax_nexus.text(50, 48, "CENTRAL ROS & RADICAL CONVERGENCE", fontsize=7.6, weight='bold', color='#b71c1c', ha='center')
    ax_nexus.text(50, 39, "Complex I & III electron leak ──► Superoxide (O2•-) ──► H2O2\nCoupled to Fe-S cluster turnover & GCR radiolytic radicals (OH•)", fontsize=6.8, ha='center')
    ax_nexus.text(50, 29, "Alternative Oxidase (AOX) vents excess redox pressure directly to O2\nCatalase (CAT3) scavenges peroxisomal & mitochondrial H2O2", fontsize=6.7, weight='bold', color='#004d40', ha='center')

    # Connection arrows
    ax_nexus.annotate('', xy=(35, 54), xytext=(26, 62), arrowprops=dict(arrowstyle='->', lw=1.2, color='#1b5e20'))
    ax_nexus.annotate('', xy=(65, 54), xytext=(74, 62), arrowprops=dict(arrowstyle='->', lw=1.2, color='#880e4f'))

    # Bottom takeaway banner
    bot_nex = patches.FancyBboxPatch((5, 4.5), 90, 11.5, boxstyle="round,pad=0,rounding_size=2",
                                     edgecolor="#00838f", facecolor="#ffffff", lw=0.9)
    ax_nexus.add_patch(bot_nex)
    ax_nexus.text(50, 10.25, "Core Concept 5: Hypomagnetic fields, ionizing radiation, and exploration atmospheres\nconverge on the exact same mitochondrial bioenergetic and antioxidant loci",
                  fontsize=6.8, weight='bold', color='#004d40', ha='center', va='center', linespacing=1.25)

    # -------------------------------------------------------------
    # Panel (c): Empirical Multi-Omics Overlap (OSD-782 vs. NNMF)
    # -------------------------------------------------------------
    ax_de = fig.add_subplot(gs[1, 0])
    
    # Data from quantum-biology-atlas/results/overlap/record.json
    # Key loci
    loci = ['AOX1D\n(AT1G32350)', 'CAT3\n(AT1G20630)', 'AOX1A\n(AT3G22370)', 'AOX2\n(AT5G64210)', 'GSTU25\n(AT3G09640)']
    rad_lfc = [3.957, 0.906, 0.702, -2.434, 1.897]    # OSD-782 1 Gy 72h / 24h
    nnmf_lfc = [0.731, 0.941, 0.345, 1.406, -1.089]   # Parmagnani 2022 NNMF (~30 nT)

    y_pos = np.arange(len(loci))
    height = 0.35

    rects1 = ax_de.barh(y_pos - height/2, rad_lfc, height, label='Ionizing Radiation (OSD-782, 1 Gy)', color='#f57c00', edgecolor='black', lw=0.6)
    rects2 = ax_de.barh(y_pos + height/2, nnmf_lfc, height, label='Near-Null Field (NNMF, ~30 nT)', color='#1976d2', edgecolor='black', lw=0.6)

    ax_de.axvline(0, color='black', lw=0.8, linestyle='-')
    ax_de.set_yticks(y_pos)
    ax_de.set_yticklabels(loci, fontsize=7.6)
    ax_de.set_xlabel('Log2 Fold Change (Perturbation vs. Control)')
    ax_de.set_title('(c) Multi-Omics Empirical Overlap (OSDR OSD-782 vs. NNMF)', weight='bold')
    ax_de.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=7.2)
    ax_de.set_xlim(-3.4, 4.6)
    ax_de.grid(axis='x', linestyle=':', alpha=0.6)

    # Annotate concordant shared loci (Clean callouts, zero collision)
    ax_de.text(2.6, 0.28, 'Shared UP (+)', color='#e65100', weight='bold', fontsize=6.8, va='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#f57c00', lw=0.6))
    ax_de.text(1.5, 1 + height/2, 'Shared UP (+)', color='#1565c0', weight='bold', fontsize=6.8, va='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#1976d2', lw=0.6))
    ax_de.text(-1.3, 3.42, 'Divergent Regulation', color='#b71c1c', weight='bold', fontsize=6.8, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#d32f2f', lw=0.6))

    # -------------------------------------------------------------
    # Panel (d): Cross-Kingdom Spaceflight Convergence (Plants vs Humans)
    # -------------------------------------------------------------
    ax_ck = fig.add_subplot(gs[1, 1])
    ax_ck.axis('off')
    ax_ck.set_xlim(0, 100)
    ax_ck.set_ylim(0, 100)
    ax_ck.set_title('(d) Cross-Kingdom Convergence: Plant BLSS & Human Health', weight='bold')

    # Card
    ck_box = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=3",
                                    edgecolor="#6a1b9a", facecolor="#f3e5f5", lw=1.2)
    ax_ck.add_patch(ck_box)
    ax_ck.text(50, 92, "Conserved Spaceflight Mitochondrial Vulnerability", fontsize=7.8, weight='bold', color='#4a148c', ha='center', va='center')

    # Plant side
    p_box = patches.FancyBboxPatch((5, 42), 42, 44, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor="#2e7d32", facecolor="#ffffff", lw=1.0)
    ax_ck.add_patch(p_box)
    ax_ck.text(26, 80, "Plant Space Biology (BLSS)", fontsize=7.4, weight='bold', color='#1b5e20', ha='center')
    ax_ck.text(26, 62, "• Mitochondrial ETC electron leak\n• Alternative Oxidase (AOX) bypass\n• Fe-S biogenesis (AtNFS1) stress\n• 10–30% germination & yield loss\n• Early pigment & chlorosis defect",
                fontsize=6.7, color='#212121', ha='center')

    # Human side
    h_box = patches.FancyBboxPatch((53, 42), 42, 44, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor="#c2185b", facecolor="#ffffff", lw=1.0)
    ax_ck.add_patch(h_box)
    ax_ck.text(74, 80, "Human Astronaut Health", fontsize=7.4, weight='bold', color='#880e4f', ha='center')
    ax_ck.text(74, 62, "• Mitochondrial dysregulation #1 hub\n  (NASA Twins Study; Afshinnekoo 2020)\n• Complex I & III ROS runaway\n• Endothelial oxidative damage\n• Musculoskeletal & immune decay",
                fontsize=6.7, color='#212121', ha='center')

    # Common Bridge Banner (Bottom)
    b_bridge = patches.FancyBboxPatch((5, 5), 90, 31, boxstyle="round,pad=0,rounding_size=2",
                                      edgecolor="#4a148c", facecolor="#ede7f6", lw=1.0)
    ax_ck.add_patch(b_bridge)
    ax_ck.text(50, 29, "THE SHARED MITOCHONDRIAL PARADIGM", fontsize=7.4, weight='bold', color='#311b92', ha='center', va='center')
    ax_ck.text(50, 16.5, "In both plants and humans, removal of the geomagnetic field coupled with ionizing radiation\nand altered atmospheres impairs respiratory electron coupling and triggers ROS overflow.\nPlant bioenergetic resilience directly protects astronaut life support and fresh food supply.",
                fontsize=6.7, color='#1a237e', ha='center', va='center', linespacing=1.3)

    fig.subplots_adjust(top=0.95, bottom=0.07, left=0.08, right=0.96, hspace=0.28, wspace=0.22)
    out_pdf = OUT_DIR / 'Fig4_multistressor_co2_o2_ros_nexus.pdf'
    out_png = OUT_DIR / 'Fig4_multistressor_co2_o2_ros_nexus.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 4 successfully created at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    main()
