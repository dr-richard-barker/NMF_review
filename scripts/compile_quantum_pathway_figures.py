#!/usr/bin/env python3
"""
compile_quantum_pathway_figures.py

Generates Figure 3 for Life Sciences in Space Research:
Quantum Molecular Biology of the 0–5 Day Window (Seed Germination & Organellar Bioenergetics).
Panels:
(a) QBM-06 Pathway: Reserve Mobilization, Peroxisomal Beta-Oxidation & Mitochondrial Respiration (0–72 h)
(b) Evidentiary Tier Hierarchy (T1 Demonstrated to T4 Context) & Biophysical Timescale Constraints
(c) Organellar Electron Transport Hubs: Chloroplast PETC (PSII/PSI) & Mitochondrial ETC with AOX Bypass
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

# Okabe-Ito Colorblind-safe palette for Tiers
OKABE = {
    'T1': '#000000',  # Heavy Black
    'T2': '#0072B2',  # Solid Blue
    'T3': '#D55E00',  # Dashed Vermillion
    'T4': '#999999'   # Hairline Grey
}

def main():
    fig = plt.figure(figsize=(11.8, 9.8), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1.0], width_ratios=[1.25, 1.0], hspace=0.30, wspace=0.22)

    # -------------------------------------------------------------
    # Panel (a): QBM-06 Seed Germination Pathway (0–72 h Heterotrophy)
    # -------------------------------------------------------------
    ax_qbm = fig.add_subplot(gs[0, :])
    ax_qbm.axis('off')
    ax_qbm.set_xlim(0, 100)
    ax_qbm.set_ylim(0, 100)
    ax_qbm.set_title('Seed Germination Before Photosynthesis (QBM-06): The 0–72 h Heterotrophic Energy Bottleneck', weight='bold', fontsize=8.8, pad=10)
    ax_qbm.text(0.00, 1.03, 'a', transform=ax_qbm.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    # Draw compartment lanes (Peroxisome, Mitochondrial Matrix, Cellular Energy/Redox, Organism Endpoint)
    lanes = [
        ("Peroxisome / Oil Body\n(TAG Mobilization)", 3, 25, "#fff8e1", "#ff8f00"),
        ("Mitochondrial Matrix\n(Respiration & Fe-S)", 28, 48, "#e8eaf6", "#3f51b5"),
        ("Cellular Energy & Redox\n(ATP / ROS Feedback)", 51, 74, "#e0f2f1", "#00897b"),
        ("Organism Outcome\n(Radicle Emergence)", 77, 97, "#fbe9e7", "#d84315")
    ]
    
    for l_title, x1, x2, bg, border in lanes:
        lane_box = patches.FancyBboxPatch((x1, 8), x2 - x1, 84, boxstyle="round,pad=0.4",
                                          edgecolor=border, facecolor=bg, lw=1.2, alpha=0.9)
        ax_qbm.add_patch(lane_box)
        ax_qbm.text((x1 + x2)/2, 87, l_title, fontsize=7.6, weight='bold', color=border, ha='center')

    # Nodes in Lane 1 (Peroxisome)
    # TAG Lipase (SDP1) [T4]
    n_sdp1 = patches.FancyBboxPatch((5, 62), 18, 16, boxstyle="round,pad=0.2",
                                    edgecolor=OKABE['T4'], facecolor='white', lw=1.0)
    ax_qbm.add_patch(n_sdp1)
    ax_qbm.text(14, 73, "TAG Lipase (SDP1)", fontsize=7.4, weight='bold', ha='center')
    ax_qbm.text(14, 66, "Oil body hydrolysis\n[T4 Context]", fontsize=6.7, color='#666666', ha='center')

    # Beta-Oxidation [T3]
    n_beta = patches.FancyBboxPatch((5, 38), 18, 16, boxstyle="round,pad=0.2",
                                    edgecolor=OKABE['T3'], facecolor='white', lw=1.4, linestyle='--')
    ax_qbm.add_patch(n_beta)
    ax_qbm.text(14, 49, "Beta-Oxidation", fontsize=7.4, weight='bold', color=OKABE['T3'], ha='center')
    ax_qbm.text(14, 42, "Acyl-CoA oxidase\nH2O2 source [T3 Plausible]", fontsize=6.7, ha='center')

    # Glyoxylate Cycle [T4]
    n_glyox = patches.FancyBboxPatch((5, 14), 18, 16, boxstyle="round,pad=0.2",
                                     edgecolor=OKABE['T4'], facecolor='white', lw=1.0)
    ax_qbm.add_patch(n_glyox)
    ax_qbm.text(14, 25, "Glyoxylate Cycle", fontsize=7.4, weight='bold', ha='center')
    ax_qbm.text(14, 18, "ICL / MLS enzymes\nMalate shunt [T4]", fontsize=6.7, color='#666666', ha='center')

    # Nodes in Lane 2 (Mitochondria)
    # Acetyl-CoA [T4]
    n_acoa = patches.FancyBboxPatch((30, 62), 16, 16, boxstyle="round,pad=0.2",
                                    edgecolor=OKABE['T4'], facecolor='white', lw=1.0)
    ax_qbm.add_patch(n_acoa)
    ax_qbm.text(38, 73, "Acetyl-CoA", fontsize=7.4, weight='bold', ha='center')
    ax_qbm.text(38, 66, "TCA substrate\n[T4 Context]", fontsize=6.7, color='#666666', ha='center')

    # Aconitase [T3]
    n_acont = patches.FancyBboxPatch((30, 38), 16, 16, boxstyle="round,pad=0.2",
                                     edgecolor=OKABE['T3'], facecolor='white', lw=1.4, linestyle='--')
    ax_qbm.add_patch(n_acont)
    ax_qbm.text(38, 49, "Aconitase", fontsize=7.4, weight='bold', color=OKABE['T3'], ha='center')
    ax_qbm.text(38, 42, "[4Fe-4S] sentinel\nRedox-vulnerable [T3]", fontsize=6.7, ha='center')

    # Complex I & Complex IV [T2/T3]
    n_c1 = patches.FancyBboxPatch((30, 14), 16, 16, boxstyle="round,pad=0.2",
                                  edgecolor=OKABE['T2'], facecolor='white', lw=1.5)
    ax_qbm.add_patch(n_c1)
    ax_qbm.text(38, 25, "Complex I & IV", fontsize=7.4, weight='bold', color=OKABE['T2'], ha='center')
    ax_qbm.text(38, 18, "FMN + 8 Fe/S; COX\nProton gradient [T2]", fontsize=6.7, ha='center')

    # Nodes in Lane 3 (Energy & Redox)
    # ATP / ADP Ratio [T2]
    n_atp = patches.FancyBboxPatch((53, 62), 19, 16, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T2'], facecolor='white', lw=1.5)
    ax_qbm.add_patch(n_atp)
    ax_qbm.text(62.5, 73, "ATP / ADP Ratio", fontsize=7.4, weight='bold', color=OKABE['T2'], ha='center')
    ax_qbm.text(62.5, 66, "Sets germination pace\nEnergy state [T2]", fontsize=6.7, ha='center')

    # Mitochondrial ROS & Superoxide [T2]
    n_ros = patches.FancyBboxPatch((53, 38), 19, 16, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T2'], facecolor='white', lw=1.5)
    ax_qbm.add_patch(n_ros)
    ax_qbm.text(62.5, 49.5, "Mitochondrial ROS", fontsize=7.2, weight='bold', color=OKABE['T2'], ha='center')
    ax_qbm.text(62.5, 42.0, "Superoxide & H2O2\nRedox window [T2]", fontsize=6.6, ha='center')

    # Cytochrome c [T4]
    n_cytc = patches.FancyBboxPatch((53, 14), 19, 16, boxstyle="round,pad=0.2",
                                    edgecolor=OKABE['T4'], facecolor='white', lw=1.0)
    ax_qbm.add_patch(n_cytc)
    ax_qbm.text(62.5, 25, "Cytochrome c", fontsize=7.4, weight='bold', ha='center')
    ax_qbm.text(62.5, 18, "Retrograde signaling\nABI4 / ABA axis [T4]", fontsize=6.7, color='#666666', ha='center')

    # Node in Lane 4 (Outcome)
    n_rad = patches.FancyBboxPatch((79, 32), 16, 28, boxstyle="round,pad=0.3",
                                   edgecolor="#d84315", facecolor="#fbe9e7", lw=1.6)
    ax_qbm.add_patch(n_rad)
    ax_qbm.text(87, 53, "RADICLE\nEMERGENCE", fontsize=7.8, weight='bold', color="#bf360c", ha='center')
    ax_qbm.text(87, 41, "0–72 h Phenotype:\n• Germination Rate\n• Emergence Speed\n• Seedling Vigor",
                fontsize=6.8, ha='center', color="#d84315")

    # Connective arrows (strictly box-edge to box-edge, zero text collision)
    ax_qbm.annotate('', xy=(14, 54), xytext=(14, 62), arrowprops=dict(arrowstyle='->', lw=1.2, color='#e65100'))
    ax_qbm.annotate('', xy=(14, 30), xytext=(14, 38), arrowprops=dict(arrowstyle='->', lw=1.2, color='#e65100'))
    ax_qbm.annotate('', xy=(30, 70), xytext=(23, 70), arrowprops=dict(arrowstyle='->', lw=1.2, color='#3f51b5'))
    ax_qbm.annotate('', xy=(38, 54), xytext=(38, 62), arrowprops=dict(arrowstyle='->', lw=1.2, color='#3f51b5'))
    ax_qbm.annotate('', xy=(38, 30), xytext=(38, 38), arrowprops=dict(arrowstyle='->', lw=1.2, color='#3f51b5'))
    ax_qbm.annotate('', xy=(53, 70), xytext=(46, 22), arrowprops=dict(arrowstyle='->', lw=1.2, color='#00897b', linestyle='--'))
    ax_qbm.annotate('', xy=(53, 46), xytext=(46, 22), arrowprops=dict(arrowstyle='->', lw=1.2, color='#d32f2f'))
    ax_qbm.annotate('', xy=(79, 46), xytext=(72, 70), arrowprops=dict(arrowstyle='->', lw=1.4, color='#2e7d32'))
    ax_qbm.annotate('', xy=(79, 46), xytext=(72, 46), arrowprops=dict(arrowstyle='->', lw=1.4, color='#d84315'))

    # -------------------------------------------------------------
    # Panel (b): Evidentiary Tiers & Biophysical Timescales
    # -------------------------------------------------------------
    ax_tier = fig.add_subplot(gs[1, 0])
    ax_tier.axis('off')
    ax_tier.set_xlim(0, 100)
    ax_tier.set_ylim(0, 100)
    ax_tier.set_title('Evidentiary Tiers & Biophysical Timescale Constraints', weight='bold', fontsize=8.8, pad=10)
    ax_tier.text(0.00, 1.03, 'b', transform=ax_tier.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    # Draw 4 Tier Legend Cards (Cleanly distributed from y=48 to y=96)
    tier_defs = [
        ("T1: Demonstrated Field Effect", "Solid black border (2.0 pt); applied field directly measured on biomolecule (e.g. CRY1/2 radical pair)", OKABE['T1'], '-', 85),
        ("T2: Inferred from Complex", "Solid blue border (1.5 pt); demonstrated for containing pathway (e.g. AOX buffering, Fv/Fm, Ferritin)", OKABE['T2'], '-', 72),
        ("T3: Plausible Physical Route", "Dashed vermillion border (1.5 pt); spin/quantum mechanism plausible but unmeasured in vivo (e.g. Complex III Qo)", OKABE['T3'], '--', 59),
        ("T4: Contextual Scaffold", "Hairline grey border (0.8 pt); structural/metabolic scaffold lacking magnetic claim", OKABE['T4'], '-', 46)
    ]
    
    for t_name, t_desc, col, ls, y_pos in tier_defs:
        b = patches.FancyBboxPatch((2, y_pos), 96, 11, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor=col, facecolor='#fafafa', lw=1.3 if col != OKABE['T4'] else 0.8, linestyle=ls)
        ax_tier.add_patch(b)
        ax_tier.text(5, y_pos + 7.5, t_name, fontsize=7.4, weight='bold', color=col, va='center')
        ax_tier.text(5, y_pos + 3.0, t_desc, fontsize=6.7, color='#424242', va='center')

    # Timescale comparison box (Bottom: y=3 to 41, height 38)
    t_box = patches.FancyBboxPatch((2, 3), 96, 38, boxstyle="round,pad=0,rounding_size=2",
                                   edgecolor="#5e35b1", facecolor="#ede7f6", lw=1.0)
    ax_tier.add_patch(t_box)
    ax_tier.text(50, 36.5, "PHYSICAL TIMESCALE CRITERION FOR MAGNETIC RECEPTION", fontsize=7.6, weight='bold', color="#4527a0", ha='center', va='center')
    
    timescale_bullets = [
        "• Zeeman Precession (50 µT GMF): vL ≈ 1.4 MHz (τL ≈ 714 ns) — Attenuated to <8 kHz in Lunar HMF",
        "• Radical-Pair Spin Coherence: τcoh ~ 1 µs [MATCHES GMF / Attenuated in HMF]",
        "• PSII Primary Charge Separation: ~200 ps [10^6× TOO FAST FOR DIRECT MF EFFECT]",
        "• Complex III Qo Semiquinone-Rieske: Exchange coupling J ~ GHz >> GMF [Refutes runaway ROS leak]"
    ]
    y_bullet = 28.5
    for bullet in timescale_bullets:
        ax_tier.text(50, y_bullet, bullet, fontsize=6.6, color="#212121", ha='center', va='center')
        y_bullet -= 6.8

    # -------------------------------------------------------------
    # Panel (c): Organellar Bioenergetics (Chloroplast & Mitochondria)
    # -------------------------------------------------------------
    ax_org = fig.add_subplot(gs[1, 1])
    ax_org.axis('off')
    ax_org.set_xlim(0, 100)
    ax_org.set_ylim(0, 100)
    ax_org.set_title('Organellar Bioenergetics & Respiratory Buffering', weight='bold', fontsize=8.8, pad=10)
    ax_org.text(0.00, 1.03, 'c', transform=ax_org.transAxes, fontsize=11, weight='bold', va='bottom', ha='left')

    # Chloroplast PETC Box (Top)
    chl_box = patches.FancyBboxPatch((2, 52), 96, 46, boxstyle="round,pad=0.3",
                                     edgecolor="#2e7d32", facecolor="#f1f8e9", lw=1.2)
    ax_org.add_patch(chl_box)
    ax_org.text(50, 92, "Chloroplast Photosynthetic Electron Transport (QBM-02)", fontsize=7.6, weight='bold', color="#1b5e20", ha='center')
    
    # Nodes: PSII, Cyt b6f, PSI, Ferredoxin
    p_ps2 = patches.FancyBboxPatch((5, 60), 20, 26, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T2'], facecolor='white', lw=1.4)
    ax_org.add_patch(p_ps2)
    ax_org.text(15, 78, "PSII (P680)", fontsize=7.4, weight='bold', color=OKABE['T2'], ha='center')
    ax_org.text(15, 66, "Open: 200 ps\nClosed: 1O2 / 3Chl*\n[T2 Inferred]", fontsize=6.6, ha='center')

    p_cyt = patches.FancyBboxPatch((28, 60), 20, 26, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T3'], facecolor='white', lw=1.4, linestyle='--')
    ax_org.add_patch(p_cyt)
    ax_org.text(38, 78, "Cyt b6f Rieske", fontsize=7.4, weight='bold', color=OKABE['T3'], ha='center')
    ax_org.text(38, 66, "[2Fe-2S] cluster\nQ-cycle H+ pump\n[T3 Plausible]", fontsize=6.6, ha='center')

    p_ps1 = patches.FancyBboxPatch((51, 60), 20, 26, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T2'], facecolor='white', lw=1.4)
    ax_org.add_patch(p_ps1)
    ax_org.text(61, 78, "PSI (P700)", fontsize=7.4, weight='bold', color=OKABE['T2'], ha='center')
    ax_org.text(61, 66, "P700•+ A1•- pair\nFX/FA/FB Fe-S\n[T2 Inferred]", fontsize=6.6, ha='center')

    p_fdx = patches.FancyBboxPatch((74, 60), 22, 26, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T2'], facecolor='white', lw=1.4)
    ax_org.add_patch(p_fdx)
    ax_org.text(85, 78, "Ferredoxin & FNR", fontsize=7.4, weight='bold', color=OKABE['T2'], ha='center')
    ax_org.text(85, 66, "NADPH formation\nCyclic flow (PGR5)\n[T2 Inferred]", fontsize=6.6, ha='center')

    # Mitochondrial Respiration & AOX Box (Bottom)
    mit_box = patches.FancyBboxPatch((2, 2), 96, 46, boxstyle="round,pad=0.3",
                                     edgecolor="#c2185b", facecolor="#fce4ec", lw=1.2)
    ax_org.add_patch(mit_box)
    ax_org.text(50, 42, "Mitochondrial Respiration & AOX Safety Valve (QBM-01)", fontsize=7.6, weight='bold', color="#880e4f", ha='center')

    p_c1 = patches.FancyBboxPatch((5, 10), 26, 26, boxstyle="round,pad=0.2",
                                  edgecolor=OKABE['T2'], facecolor='white', lw=1.4)
    ax_org.add_patch(p_c1)
    ax_org.text(18, 28, "Complex I & III", fontsize=7.4, weight='bold', color=OKABE['T2'], ha='center')
    ax_org.text(18, 16, "NADH oxidation; Fe-S\nMajor superoxide leak\n[T2 Inferred]", fontsize=6.6, ha='center')

    p_aox = patches.FancyBboxPatch((35, 10), 30, 26, boxstyle="round,pad=0.2",
                                   edgecolor=OKABE['T2'], facecolor='#ffebee', lw=1.6)
    ax_org.add_patch(p_aox)
    ax_org.text(50, 29.5, "ALTERNATIVE OXIDASE", fontsize=7.1, weight='bold', color="#b71c1c", ha='center')
    ax_org.text(50, 24.0, "(AOX Bypass)", fontsize=6.6, weight='bold', color="#b71c1c", ha='center')
    ax_org.text(50, 15.5, "Cyanide-resistant bypass\nBypasses CIII/IV; vents e-\nDampens ROS runaway [T2]", fontsize=6.5, ha='center')

    p_c4 = patches.FancyBboxPatch((69, 10), 27, 26, boxstyle="round,pad=0.2",
                                  edgecolor=OKABE['T4'], facecolor='white', lw=1.0)
    ax_org.add_patch(p_c4)
    ax_org.text(82.5, 28, "Complex IV (COX)", fontsize=7.4, weight='bold', ha='center')
    ax_org.text(82.5, 16, "Heme a3 / CuB\nHigh O2 affinity\n[T4 Context]", fontsize=6.6, color='#666666', ha='center')

    fig.subplots_adjust(top=0.95, bottom=0.06, left=0.06, right=0.96, hspace=0.28, wspace=0.22)
    for prefix in ['Fig3', 'Fig4']:
        out_pdf = OUT_DIR / f'{prefix}_quantum_biology_0to5day_pathways.pdf'
        out_png = OUT_DIR / f'{prefix}_quantum_biology_0to5day_pathways.png'
        fig.savefig(out_pdf, bbox_inches='tight')
        fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 4 successfully created in {OUT_DIR}")

if __name__ == '__main__':
    main()
