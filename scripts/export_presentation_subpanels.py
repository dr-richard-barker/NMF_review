#!/usr/bin/env python3
"""
scripts/export_presentation_subpanels.py

Decomposes Figures 1-5 and the Graphical Abstract into 23 standalone,
high-resolution (300 DPI) subpanel images saved to `presentation/assets/subpanels/`.
These individual graphics allow the PowerPoint deck generator (`build_presentation_deck.py`)
to reconstruct each figure montage with fully separable, repositionable components and
native editable typography.

Usage:
    .venv/bin/python scripts/export_presentation_subpanels.py
"""

import os
import sys
from pathlib import Path

# Ensure cache directory is writable
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_cache'

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 9.0,
    'axes.titlesize': 10.0,
    'xtick.labelsize': 8.0,
    'ytick.labelsize': 8.0,
    'legend.fontsize': 8.0,
    'mathtext.fontset': 'dejavusans'
})

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / 'data'
OUT_DIR = REPO_ROOT / 'presentation' / 'assets' / 'subpanels'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Figure 1 Subpanels
# ---------------------------------------------------------------------------
def export_fig1_subpanels():
    print("Exporting Figure 1 subpanels...")
    df_sites = pd.read_csv(DATA_DIR / 'landing_sites_magnetic.csv')
    df_grid = pd.read_csv(DATA_DIR / 'lunar_mag_field_grid.csv')

    # Fig 1a: Global Crustal Map
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=300)
    lons = np.sort(df_grid['lon'].unique())
    lats = np.sort(df_grid['lat'].unique())
    lon_mesh, lat_mesh = np.meshgrid(lons, lats)
    z_bmag = df_grid.pivot(index='lat', columns='lon', values='Bmag').values
    vmax = np.nanpercentile(z_bmag, 98)
    img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='viridis', vmin=0, vmax=vmax, alpha=0.90, shading='auto')
    
    markers = {'Artemis': '*', 'Apollo': 'o', "Chang'e": 's', 'Chandrayaan': '^'}
    colors = {'Artemis': '#ff1744', 'Apollo': '#ffffff', "Chang'e": '#ffea00', 'Chandrayaan': '#00e5ff'}
    for mission in ['Apollo', "Chang'e", 'Chandrayaan', 'Artemis']:
        sub = df_sites[df_sites['mission'] == mission]
        if not sub.empty:
            ax.scatter(sub['lon'], sub['lat'], marker=markers.get(mission, 'o'),
                       color=colors.get(mission, 'white'), edgecolor='black', linewidth=0.7,
                       s=80 if mission == 'Artemis' else 45, label=f"{mission} ({len(sub)})", zorder=5)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.28), ncol=4, frameon=True, facecolor='white', framealpha=0.9)
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_xlim(0, 360)
    ax.set_ylim(-90, 65)
    cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.035, pad=0.02)
    cbar.set_label('$|\\mathbf{B}|$ at 30 km (nT)')
    rect = patches.Rectangle((0, -90), 360, 10, linewidth=1.2, edgecolor='#ff1744', facecolor='none', linestyle='--', zorder=6)
    ax.add_patch(rect)
    ax.text(180, -78, 'Artemis South Pole Region (B < 1 nT)', color='#ff1744', weight='bold', ha='center', fontsize=7.5,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor='#ff1744'))
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig1a_global_map.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 1b: South Pole Detail
    fig, ax = plt.subplots(figsize=(5.4, 4.4), dpi=300)
    artemis_sites = df_sites[df_sites['mission'] == 'Artemis'].sort_values('Bmag').reset_index(drop=True)
    ax.set_facecolor('#f5f5f7')
    scatter = ax.scatter(artemis_sites['lon'], artemis_sites['lat'], c=artemis_sites['Bmag'], cmap='plasma', s=120,
                         edgecolor='black', linewidth=0.8, vmin=0.3, vmax=0.9, zorder=4)
    for _, row in artemis_sites.iterrows():
        s_name = row['name'].replace('Connecting Ridge Extension', 'Conn. Ridge Ext.').replace('de Gerlache-Kocher Massif', 'de Gerlache-Kocher')
        ax.annotate(f"{s_name}\n({row['Bmag']:.2f} nT)", (row['lon'], row['lat']),
                    fontsize=6.8, ha='left', va='center', xytext=(5, 0), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white', alpha=0.8, edgecolor='#999999', lw=0.4))
    ax.set_xlim(-20, 380)
    ax.set_ylim(-90.5, -83.5)
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.grid(True, linestyle=':', alpha=0.6)
    cbar_pol = plt.colorbar(scatter, ax=ax, orientation='vertical', fraction=0.04, pad=0.02)
    cbar_pol.set_label('$|\\mathbf{B}_{\\mathrm{crust}}|$ (nT)')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig1b_south_pole_artemis.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 1c: Landing Sites Bar Chart
    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=300)
    df_sorted = df_sites.sort_values(['mission', 'Bmag'], ascending=[True, False]).reset_index(drop=True)
    color_map = {'high-field': '#d32f2f', 'moderate': '#f57c00', 'low/null-field': '#1976d2'}
    bar_colors = [color_map.get(c, '#757575') for c in df_sorted['classification']]
    x_pos = np.arange(len(df_sorted))
    ax.bar(x_pos, df_sorted['Bmag'], color=bar_colors, edgecolor='black', linewidth=0.5, alpha=0.9)
    ax.axhline(1.0, color='#f57c00', linestyle='--', linewidth=1.0, label='Near-Null Boundary (1 nT)')
    ax.axhline(5.0, color='#d32f2f', linestyle=':', linewidth=1.0, label='Moderate Swirl (5 nT)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_sorted['name'], rotation=55, ha='right', fontsize=6.8)
    ax.set_ylabel('Crustal Field $|\\mathbf{B}|$ at 30 km (nT)')
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    ax.set_ylim(0, 5.5)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.text(0.03, 0.75, 'Earth GMF: 25,000–65,000 nT\nArtemis Sites: 0.40–0.82 nT (>30,000× lower)',
            transform=ax.transAxes, fontsize=7.5, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1976d2', alpha=0.95))
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig1c_landing_sites_bar.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 1d: Field Superposition Schematic
    fig, ax = plt.subplots(figsize=(5.4, 4.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    eq_rect = patches.FancyBboxPatch((0.5, 7.8), 9.0, 1.8, boxstyle="round,pad=0.2", edgecolor="#0288d1", facecolor="#e1f5fe", lw=1.2)
    ax.add_patch(eq_rect)
    ax.text(5.0, 8.9, r"$\mathbf{B}_{\mathrm{total}}(t, \mathbf{x}) = \mathbf{B}_{\mathrm{crust}} + \mathbf{B}_{\mathrm{ext}} + \mathbf{B}_{\mathrm{lander}} + \mathbf{B}_{\mathrm{payload}} + \mathbf{B}_{\mathrm{control}}$",
            fontsize=8.5, weight='bold', ha='center', va='center', color='#01579b')
    ax.text(5.0, 8.1, "Net Vector Sum Governs Primary Spin-Chemical Biomarkers",
            fontsize=7.2, ha='center', va='center', color='#0277bd', style='italic')
    cham_rect = patches.FancyBboxPatch((0.8, 1.0), 8.4, 6.2, boxstyle="round,pad=0.3", edgecolor="#37474f", facecolor="#eceff1", lw=1.4)
    ax.add_patch(cham_rect)
    ax.text(5.0, 6.7, "Lunar Plant Growth Enclosure (e.g., LEAF / BLSS)", weight='bold', fontsize=8.2, ha='center', color='#263238')
    contributions = [
        (r"$\mathbf{B}_{\mathrm{crust}}$", "0.4 – 0.8 nT", "Lunar South Pole paleomagnetism", "#1565c0"),
        (r"$\mathbf{B}_{\mathrm{ext}}$", "1 – 5 nT", "Solar wind IMF / magnetotail shadow", "#2e7d32"),
        (r"$\mathbf{B}_{\mathrm{lander}}$", "50 – 500 µT", "Lander avionics & DC power buses [Confounder]", "#c62828"),
        (r"$\mathbf{B}_{\mathrm{payload}}$", "15 – 20 nT", "Fans, pumps, heaters, LEDs [Ripple]", "#e65100"),
        (r"$\mathbf{B}_{\mathrm{control}}$", "40 – 50 µT", "Active 3-axis causal rescue coils", "#6a1b9a"),
    ]
    y_start = 5.7
    for symbol, mag, desc, col in contributions:
        ax.text(1.2, y_start, symbol, fontsize=8.8, weight='bold', color=col, va='center')
        ax.text(2.4, y_start, f"[{mag}]", fontsize=7.6, weight='bold', color='#333333', va='center')
        ax.text(4.2, y_start, desc, fontsize=7.2, color='#455a64', va='center')
        y_start -= 0.92
    warn_rect = patches.FancyBboxPatch((1.0, 0.9), 8.0, 0.8, boxstyle="round,pad=0.15", edgecolor="#d32f2f", facecolor="#ffebee", lw=0.8)
    ax.add_patch(warn_rect)
    ax.text(5.0, 1.3, "CRITICAL: Unshielded spacecraft DC currents (50–500 µT) can exceed\nEarth GMF, inadvertently masking true lunar hypomagnetic exposure!",
            fontsize=6.8, weight='bold', ha='center', va='center', color='#b71c1c')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig1d_superposition_box.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2 Subpanels
# ---------------------------------------------------------------------------
def export_fig2_subpanels():
    print("Exporting Figure 2 subpanels...")
    df_kin = pd.read_csv(DATA_DIR / 'seedling_kinetics_summary.csv')

    # Fig 2a: Developmental Timeline
    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    bar_bg = patches.Rectangle((5, 52), 90, 8, facecolor='#e0e0e0', edgecolor='#9e9e9e', lw=1.0)
    ax.add_patch(bar_bg)
    phases = [
        ("Phase I\nImbibition", 5, 22, "#bbdefb", "#1976d2", "0–12 h", "Rapid water uptake;\nmembrane reorganization"),
        ("Phase II\nPeroxisomal Catabolism", 22, 45, "#ffe082", "#f57c00", "12–48 h", "Lipid mobilization (β-ox);\nglyoxylate bypass; ROS burst"),
        ("Phase III\nRadicle Emergence", 45, 68, "#c8e6c9", "#388e3c", "48–72 h", "Testa rupture; cell elongation;\nRAM division initiation"),
        ("Phase IV\nDe-Etiolation & Autotrophy", 68, 95, "#d1c4e9", "#512da8", "72–120 h", "Light perceived; CRY1/HY5;\nchlorophyll & thylakoid biogenesis")
    ]
    for name, x_start, x_end, bg_col, edge_col, time_str, desc in phases:
        w = x_end - x_start
        p_rect = patches.FancyBboxPatch((x_start, 62), w, 28, boxstyle="round,pad=0.2", facecolor=bg_col, edgecolor=edge_col, lw=1.2)
        ax.add_patch(p_rect)
        ax.text(x_start + w/2, 83, name, ha='center', va='center', weight='bold', fontsize=7.5, color='#212121')
        ax.text(x_start + w/2, 73, time_str, ha='center', va='center', weight='bold', fontsize=7.0, color=edge_col)
        ax.text(x_start + w/2, 65, desc, ha='center', va='center', fontsize=6.2, color='#424242')
    vulnerabilities = [
        ("Water imbibition\nlag observed", 13.5, "#d32f2f"),
        ("Impaired glyoxysome\nrespiration; ROS delay", 33.5, "#d32f2f"),
        ("Testa rupture delayed\n(t50 lag 12–36 h)", 56.5, "#d32f2f"),
        ("Downregulated HEMA1/POR;\nsevere seedling chlorosis", 81.5, "#d32f2f")
    ]
    for v_text, x_mid, col in vulnerabilities:
        v_box = patches.FancyBboxPatch((x_mid - 9, 14), 18, 26, boxstyle="round,pad=0.2", facecolor="#ffebee", edgecolor=col, lw=1.0)
        ax.add_patch(v_box)
        ax.text(x_mid, 34, "NNMF IMPACT", ha='center', va='center', weight='bold', fontsize=6.5, color=col)
        ax.text(x_mid, 23, v_text, ha='center', va='center', fontsize=6.2, color='#b71c1c')
        ax.annotate('', xy=(x_mid, 52), xytext=(x_mid, 40),
                    arrowprops=dict(facecolor=col, edgecolor=col, width=1.0, headwidth=4, headlength=4))
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig2a_5day_timeline.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 2b: Germination Kinetics
    fig, ax = plt.subplots(figsize=(5.4, 4.2), dpi=300)
    time_pts = np.linspace(0, 120, 200)
    # GMF Sigmoidal: Max 95%, t50 = 36 h, slope = 0.12
    germ_gmf = 95.0 / (1.0 + np.exp(-0.12 * (time_pts - 36.0)))
    # NNMF Sigmoidal: Max 76%, t50 = 60 h, slope = 0.08
    germ_nnmf = 76.0 / (1.0 + np.exp(-0.08 * (time_pts - 60.0)))
    ax.plot(time_pts, germ_gmf, color='#1565c0', lw=2.2, label='GMF Control (45 µT)')
    ax.plot(time_pts, germ_nnmf, color='#c62828', lw=2.2, linestyle='--', label='Near-Null Field (<10 nT)')
    ax.axhline(95.0, color='#1565c0', linestyle=':', alpha=0.6)
    ax.axhline(76.0, color='#c62828', linestyle=':', alpha=0.6)
    ax.scatter([36.0], [47.5], color='#1565c0', s=45, zorder=5)
    ax.scatter([60.0], [38.0], color='#c62828', s=45, zorder=5)
    ax.annotate(r'$t_{50} = 36\ \mathrm{h}$', xy=(36, 47.5), xytext=(12, 58),
                arrowprops=dict(arrowstyle="->", color='#1565c0', lw=1.0), fontsize=7.5, color='#1565c0', weight='bold')
    ax.annotate(r'$t_{50} = 60\ \mathrm{h}$ ($\Delta = +24\ \mathrm{h}$)', xy=(60, 38), xytext=(68, 25),
                arrowprops=dict(arrowstyle="->", color='#c62828', lw=1.0), fontsize=7.5, color='#c62828', weight='bold')
    ax.annotate('Final Capacity Drop:\n-19% viable seedlings', xy=(110, 85), xytext=(72, 85),
                arrowprops=dict(arrowstyle="->", color='#c62828', lw=1.0), fontsize=7.5, color='#c62828', weight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffebee', edgecolor='#c62828'))
    ax.set_xlabel('Time Post-Imbibition (hours)')
    ax.set_ylabel('Cumulative Germination (%)')
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 105)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig2b_germination_kinetics.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 2c: Seedling Biomass & Elongation
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=300)
    categories = ['Radicle Length\n(Day 3, mm)', 'Hypocotyl Height\n(Day 5, mm)', 'Fresh Weight\n(Day 5, mg/plant)', 'Dry Biomass Yield\n(Day 5, % control)']
    gmf_vals = [18.5, 14.2, 8.6, 100.0]
    nnmf_vals = [12.4, 9.8, 6.1, 71.5]
    x = np.arange(len(categories))
    w = 0.35
    ax.bar(x - w/2, gmf_vals, w, label='GMF (45 µT)', color='#1976d2', edgecolor='black', lw=0.6)
    ax.bar(x + w/2, nnmf_vals, w, label='NNMF (<10 nT)', color='#d32f2f', edgecolor='black', lw=0.6)
    for i in range(len(categories)):
        drop = (nnmf_vals[i] - gmf_vals[i]) / gmf_vals[i] * 100
        y_max = max(gmf_vals[i], nnmf_vals[i])
        ax.text(x[i], y_max * 1.05, f"{drop:.1f}%", ha='center', fontsize=7.2, color='#b71c1c', weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=7.2)
    ax.set_ylabel('Seedling Metric Value')
    ax.set_ylim(0, 118)
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.text(0.04, 0.70, 'Day 5 Vegetative Penalty:\n• Radicle length: -33.0%\n• Hypocotyl height: -31.0%\n• Fresh weight: -29.1%\n• Harvestable yield: -28.5%',
            transform=ax.transAxes, fontsize=7.2, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#fffde7', edgecolor='#fbc02d', alpha=0.95))
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig2c_biomass_yield.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 2d: Pigment Pathways
    fig, ax = plt.subplots(figsize=(5.4, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.text(5.0, 9.5, "Blue Light (450 nm) & Cryptochrome Signaling", ha='center', weight='bold', fontsize=8.2, color='#1565c0')
    cry_box = patches.FancyBboxPatch((1.5, 7.8), 7.0, 1.2, boxstyle="round,pad=0.2", facecolor="#e3f2fd", edgecolor="#1565c0", lw=1.2)
    ax.add_patch(cry_box)
    ax.text(5.0, 8.4, r"CRY1 / CRY2 Radical Pair $[\mathrm{FAD}^{\bullet-} \cdots \mathrm{TrpH}^{\bullet+}]$", ha='center', weight='bold', fontsize=7.8, color='#0d47a1')
    ax.annotate('', xy=(5.0, 6.8), xytext=(5.0, 7.8), arrowprops=dict(arrowstyle="->", color='#1565c0', lw=1.5))
    hy5_box = patches.FancyBboxPatch((2.0, 5.6), 6.0, 1.2, boxstyle="round,pad=0.2", facecolor="#fff9c4", edgecolor="#fbc02d", lw=1.2)
    ax.add_patch(hy5_box)
    ax.text(5.0, 6.2, "COP1 / SPA1 Dissociation & HY5 Stabilization", ha='center', weight='bold', fontsize=7.5, color='#f57f17')
    ax.annotate('NNMF:\nAttenuates\nHY5 accumulation!', xy=(6.5, 6.2), xytext=(8.0, 6.2),
                arrowprops=dict(arrowstyle="->", color='#c62828', lw=1.0), fontsize=6.5, color='#c62828', weight='bold', ha='center', va='center')
    ax.annotate('', xy=(3.0, 4.6), xytext=(4.0, 5.6), arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=1.3))
    ax.annotate('', xy=(7.0, 4.6), xytext=(6.0, 5.6), arrowprops=dict(arrowstyle="->", color='#6a1b9a', lw=1.3))
    chl_box = patches.FancyBboxPatch((0.5, 1.4), 4.2, 3.2, boxstyle="round,pad=0.2", facecolor="#e8f5e9", edgecolor="#2e7d32", lw=1.2)
    ax.add_patch(chl_box)
    ax.text(2.6, 4.1, "Chlorophyll Biosynthesis", ha='center', weight='bold', fontsize=7.5, color='#1b5e20')
    chl_genes = ["HEMA1 (Glutamyl-tRNA red.)", "CHLH (Mg-chelatase)", "PORA/B/C (Protochloroph.)", "Downregulated in NNMF!"]
    y_g = 3.4
    for g in chl_genes:
        col = '#c62828' if 'Downregulated' in g else '#2e7d32'
        ax.text(2.6, y_g, g, ha='center', fontsize=6.5, color=col, weight='bold' if 'Downregulated' in g else 'normal')
        y_g -= 0.6
    ant_box = patches.FancyBboxPatch((5.3, 1.4), 4.2, 3.2, boxstyle="round,pad=0.2", facecolor="#f3e5f5", edgecolor="#6a1b9a", lw=1.2)
    ax.add_patch(ant_box)
    ax.text(7.4, 4.1, "Anthocyanin Biosynthesis", ha='center', weight='bold', fontsize=7.5, color='#4a148c')
    ant_genes = ["CHS (Chalcone synthase)", "CHI (Chalcone isomerase)", "F3H (Flavanone 3-hydr.)", "Repressed in NNMF!"]
    y_a = 3.4
    for a in ant_genes:
        col = '#c62828' if 'Repressed' in a else '#4a148c'
        ax.text(7.4, y_a, a, ha='center', fontsize=6.5, color=col, weight='bold' if 'Repressed' in a else 'normal')
        y_a -= 0.6
    alert_box = patches.FancyBboxPatch((0.5, 0.2), 9.0, 0.9, boxstyle="round,pad=0.1", facecolor="#ffebee", edgecolor="#c62828", lw=0.8)
    ax.add_patch(alert_box)
    ax.text(5.0, 0.65, "PHENOTYPE: Severe seedling chlorosis, impaired photoprotection & delayed autotrophic greening",
            ha='center', va='center', weight='bold', fontsize=6.5, color='#b71c1c')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig2d_pigment_pathway.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 3 Subpanels
# ---------------------------------------------------------------------------
def export_fig3_subpanels():
    print("Exporting Figure 3 subpanels...")
    # Fig 3a: QBM-06 Pathway
    fig, ax = plt.subplots(figsize=(11.0, 4.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    p_box = patches.FancyBboxPatch((2, 10), 28, 80, boxstyle="round,pad=0.3", edgecolor="#f57c00", facecolor="#fff3e0", lw=1.5)
    ax.add_patch(p_box)
    ax.text(16, 85, "PEROXISOME / GLYOXYSOME", weight='bold', fontsize=8.5, ha='center', color="#e65100")
    ax.text(16, 76, "Triacylglycerol (TAG) Storage Lipids", fontsize=7.5, ha='center', color="#333")
    ax.annotate('', xy=(16, 64), xytext=(16, 72), arrowprops=dict(arrowstyle="->", color="#e65100", lw=1.5))
    ax.text(16, 60, "Fatty Acids → Acyl-CoA Pool", fontsize=7.5, ha='center', color="#333")
    ax.annotate('', xy=(16, 48), xytext=(16, 56), arrowprops=dict(arrowstyle="->", color="#e65100", lw=1.5))
    ax.text(16, 44, r"β-Oxidation Cycle ($\mathrm{H}_2\mathrm{O}_2$ by ACX)", fontsize=7.2, weight='bold', ha='center', color="#d32f2f")
    ax.text(16, 38, "[Primary Reactive Oxygen Source]", fontsize=6.8, ha='center', color="#b71c1c")
    ax.annotate('', xy=(16, 26), xytext=(16, 34), arrowprops=dict(arrowstyle="->", color="#e65100", lw=1.5))
    ax.text(16, 22, "Succinate Export (via Glyoxylate)", fontsize=7.5, ha='center', color="#333")
    ax.annotate('', xy=(38, 50), xytext=(30, 22), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color="#1565c0", lw=2.0))
    ax.text(34, 40, "Succinate\nTransport", fontsize=7.0, ha='center', color="#1565c0", weight='bold')

    m_box = patches.FancyBboxPatch((40, 10), 58, 80, boxstyle="round,pad=0.3", edgecolor="#1565c0", facecolor="#e3f2fd", lw=1.5)
    ax.add_patch(m_box)
    ax.text(69, 85, "MITOCHONDRION (RESPIRATORY ETC)", weight='bold', fontsize=8.5, ha='center', color="#0d47a1")
    ax.text(69, 76, "TCA Cycle Entry → Ubiquinone (UQ) Pool Reduction", fontsize=7.8, ha='center', color="#333")
    cmplx = [("Complex I\n(NADH)", 45), ("Complex II\n(Succinate)", 57), ("UQ Pool\n[Electron Hub]", 69), ("Complex III\n(Cyt c)", 81), ("Complex IV\n(COX)", 93)]
    for name, xc in cmplx:
        c_rect = patches.FancyBboxPatch((xc - 4.5, 45), 9, 22, boxstyle="round,pad=0.15",
                                        edgecolor="#0d47a1" if "UQ" not in name else "#e65100",
                                        facecolor="#ffffff" if "UQ" not in name else "#ffe0b2", lw=1.2)
        ax.add_patch(c_rect)
        ax.text(xc, 56, name, ha='center', va='center', fontsize=6.8, weight='bold')
    aox_box = patches.FancyBboxPatch((63, 16), 24, 18, boxstyle="round,pad=0.2", edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.4)
    ax.add_patch(aox_box)
    ax.text(75, 29, "Alternative Oxidase (AOX1D)", weight='bold', fontsize=7.8, ha='center', color="#1b5e20")
    ax.text(75, 21, "Direct UQ Oxidation: Excess e- → O2 (Safety Valve)\nPrevents Complex I/III Superoxide (O2•-) Burst",
            fontsize=6.8, ha='center', color="#2e7d32")
    ax.annotate('', xy=(69, 34), xytext=(69, 45), arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=2.0))
    ax.text(72, 38, "Bypass", fontsize=7.0, color="#2e7d32", weight='bold')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig3a_qbm06_pathway.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 3b: Evidentiary Tiers
    fig, ax = plt.subplots(figsize=(6.0, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    tiers = [
        ("Tier 1: Demonstrated Quantum Biology", "Cryptochrome FAD•- ... TrpH•+ radical pairs;\nZeeman resonance; in vitro magnetic sensitivity", "#000000", "#e0e0e0"),
        ("Tier 2: Plausible Quantum Biology", "Peroxisomal ROS radical pairs; flavin-dependent\noxidase modulation; singlet-triplet spin crossing", "#0072B2", "#e1f5fe"),
        ("Tier 3: Speculative Extrapolation", "Mitochondrial ETC tunnelling modulation;\nDNA magnetoreception; quantum coherence in enzymes", "#D55E00", "#fbe9e7"),
        ("Tier 4: General Context / Analogy", "Avian navigation paradigms applied to plant roots;\nmacroscopic geomagnetic alignment claims", "#999999", "#f5f5f5")
    ]
    y_t = 8.5
    for t_title, t_desc, col, bg in tiers:
        t_box = patches.FancyBboxPatch((0.5, y_t - 1.8), 9.0, 1.9, boxstyle="round,pad=0.2", edgecolor=col, facecolor=bg, lw=1.4)
        ax.add_patch(t_box)
        ax.text(0.8, y_t - 0.4, t_title, weight='bold', fontsize=7.8, color=col)
        ax.text(0.8, y_t - 1.2, t_desc, fontsize=6.8, color="#333333")
        y_t -= 2.2
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig3b_evidentiary_tiers.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 3c: Organellar ETC Hubs
    fig, ax = plt.subplots(figsize=(5.4, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.text(5.0, 9.4, "Dual Organellar Bioenergetic Engines", ha='center', weight='bold', fontsize=8.2, color="#1565c0")
    c_card = patches.FancyBboxPatch((0.6, 5.0), 8.8, 3.8, boxstyle="round,pad=0.2", edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.2)
    ax.add_patch(c_card)
    ax.text(5.0, 8.2, "Chloroplast Thylakoid PETC (Days 3–5)", ha='center', weight='bold', fontsize=7.5, color="#1b5e20")
    ax.text(5.0, 7.3, "PSII (P680) → Plastoquinone (PQ) → Cytochrome b6f → PSI (P700)", ha='center', fontsize=6.8, color="#333")
    ax.text(5.0, 6.2, "NNMF Stress: Attenuated chlorophyll synthesis starves reaction centers;\nExcess excitation energy leaks to Singlet Oxygen (1O2)", ha='center', fontsize=6.5, color="#c62828", weight='bold')

    m_card = patches.FancyBboxPatch((0.6, 0.6), 8.8, 3.8, boxstyle="round,pad=0.2", edgecolor="#1565c0", facecolor="#e3f2fd", lw=1.2)
    ax.add_patch(m_card)
    ax.text(5.0, 3.8, "Mitochondrial Inner Membrane ETC (Days 0–5)", ha='center', weight='bold', fontsize=7.5, color="#0d47a1")
    ax.text(5.0, 2.9, "Complex I/II → Ubiquinone (UQ) → Complex III → Cyt c → Complex IV (COX)", ha='center', fontsize=6.8, color="#333")
    ax.text(5.0, 1.8, "NNMF Stress: Electron over-reduction at UQ pool triggers Superoxide (O2•-);\nAlternative Oxidase (AOX1D) bypasses Complex III/IV to vent electrons", ha='center', fontsize=6.5, color="#1565c0", weight='bold')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig3c_organellar_etc.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 4 Subpanels
# ---------------------------------------------------------------------------
def export_fig4_subpanels():
    print("Exporting Figure 4 subpanels...")
    # Fig 4a: Stressor Space
    fig, ax = plt.subplots(figsize=(5.6, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    stressors = [
        ("Exploration Atmosphere", "56.5 kPa / 8.2 psia, 34% O2\nElevated CO2 (1200–3000 ppm)\nSuppress RuBisCO oxygenation", "#bbdefb", "#1565c0"),
        ("Lunar Hypomagnetic Field", "<0.8 nT ambient South Pole\nSpin-chemical radical pair shift\nDelayed t50 & pigment repression", "#ffebee", "#c62828"),
        ("Space Radiation (GCR / SPE)", "0.5–1.0 mGy/day chronic dose\nDirect DNA DSBs & radiolysis\nMitochondrial membrane oxidation", "#fff3e0", "#e65100")
    ]
    y_pos = 75
    for name, desc, bg, edge in stressors:
        box = patches.FancyBboxPatch((5, y_pos - 18), 90, 20, boxstyle="round,pad=0.3", edgecolor=edge, facecolor=bg, lw=1.2)
        ax.add_patch(box)
        ax.text(10, y_pos - 5, name, weight='bold', fontsize=7.8, color=edge)
        ax.text(10, y_pos - 13, desc, fontsize=6.8, color='#333333')
        y_pos -= 26
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig4a_multistressor_space.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 4b: Bioenergetic Engine
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    hub_rect = patches.FancyBboxPatch((1.5, 3.0), 7.0, 4.5, boxstyle="round,pad=0.3", edgecolor="#37474f", facecolor="#eceff1", lw=1.5)
    ax.add_patch(hub_rect)
    ax.text(5.0, 6.8, r"Mitochondrial $\mathrm{CO}_2 \leftrightarrow \mathrm{O}_2 \leftrightarrow \mathrm{ROS}$ Engine", weight='bold', fontsize=8.0, ha='center', color="#263238")
    ax.text(5.0, 5.8, "Elevated CO2 suppresses photorespiratory H2O2 in peroxisomes\n↓\nMetabolic burden shifts to Mitochondrial ETC\n↓\nUQ Pool over-reduction generates Superoxide (O2•-)",
            ha='center', fontsize=7.0, color="#37474f")
    aox_tag = patches.FancyBboxPatch((2.2, 3.4), 5.6, 1.2, boxstyle="round,pad=0.2", edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.2)
    ax.add_patch(aox_tag)
    ax.text(5.0, 4.0, "AOX1D Emergency Relief Valve: Vents Excess Electrons to O2", ha='center', weight='bold', fontsize=6.8, color="#1b5e20")
    ax.annotate('Exploration Atmosphere\n(High CO2, 56.5 kPa)', xy=(5.0, 7.5), xytext=(5.0, 9.0),
                ha='center', arrowprops=dict(arrowstyle="->", color="#1565c0", lw=1.3), fontsize=7.0, color="#1565c0", weight='bold')
    ax.annotate('Near-Null Field\n(<0.8 nT)', xy=(1.5, 5.2), xytext=(0.1, 5.2),
                arrowprops=dict(arrowstyle="->", color="#c62828", lw=1.3), fontsize=7.0, color="#c62828", weight='bold', va='center')
    ax.annotate('GCR Radiation\n(0.5–1 mGy/d)', xy=(8.5, 5.2), xytext=(8.6, 5.2),
                arrowprops=dict(arrowstyle="->", color="#e65100", lw=1.3), fontsize=7.0, color="#e65100", weight='bold', va='center')
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig4b_bioenergetic_engine.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 4c: Multi-Omics Empirical Overlap
    fig, ax = plt.subplots(figsize=(5.6, 4.4), dpi=300)
    overlap_genes = [("AOX1D", 2.45, 1.88, "Alternative Oxidase 1D"),
                     ("CAT3", 1.92, 1.45, "Catalase 3 (Peroxisomal)"),
                     ("APX1", 1.65, 1.32, "Ascorbate Peroxidase 1"),
                     ("PRXQ", 1.48, 1.25, "Peroxiredoxin Q"),
                     ("HEMA1", -1.85, -2.10, "Glutamyl-tRNA Reductase"),
                     ("PORA", -1.62, -1.95, "Protochlorophyllide Red.")]
    genes = [g[0] for g in overlap_genes]
    rad_lfc = [g[1] for g in overlap_genes]
    nnmf_lfc = [g[2] for g in overlap_genes]
    y = np.arange(len(genes))
    h = 0.35
    ax.barh(y + h/2, rad_lfc, h, label='Ionizing Rad (OSD-782, 1 Gy)', color='#f57c00', edgecolor='black', lw=0.6)
    ax.barh(y - h/2, nnmf_lfc, h, label='Near-Null Field (Parmagnani 2022)', color='#1976d2', edgecolor='black', lw=0.6)
    ax.axvline(0, color='black', lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(genes, fontsize=7.5, weight='bold')
    ax.set_xlabel('Log2 Fold Change vs. Control')
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=7.2)
    ax.grid(axis='x', linestyle=':', alpha=0.6)
    ax.set_xlim(-2.8, 3.2)
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig4c_multiomics_overlap.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 4d: Cross-Kingdom Astronaut Parallels
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    p_card = patches.FancyBboxPatch((0.5, 5.2), 9.0, 4.2, boxstyle="round,pad=0.2", edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.2)
    ax.add_patch(p_card)
    ax.text(5.0, 8.8, "PLANT PHENOTYPE (BLSS CROPS)", ha='center', weight='bold', fontsize=7.8, color="#1b5e20")
    ax.text(5.0, 7.8, "• Excessive mitochondrial electron leakage at Complexes I & III\n• Induction of Alternative Oxidase (AOX1D) and Catalase (CAT3)\n• Chlorophyll synthesis repression; reduced antioxidant reserves\n• 20–30% vegetative biomass deficit on Day 5",
            ha='center', fontsize=6.8, color="#2e7d32")
    h_card = patches.FancyBboxPatch((0.5, 0.6), 9.0, 4.2, boxstyle="round,pad=0.2", edgecolor="#c62828", facecolor="#ffebee", lw=1.2)
    ax.add_patch(h_card)
    ax.text(5.0, 4.2, "HUMAN ASTRONAUT PHENOTYPE (NASA TWINS / AFSHINNEKOO 2020)", ha='center', weight='bold', fontsize=7.8, color="#b71c1c")
    ax.text(5.0, 3.2, "• Conserved mitochondrial bioenergetic dysfunction in spaceflight\n• Elevated cell-free mitochondrial DNA (cf-mtDNA) & systemic inflammation\n• Shift from oxidative phosphorylation to glycolysis\n• Increased oxidative stress; vision, cardiovascular, & muscle decline",
            ha='center', fontsize=6.8, color="#c62828")
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig4d_crosskingdom_astronaut.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 5 Subpanels
# ---------------------------------------------------------------------------
def export_fig5_subpanels():
    print("Exporting Figure 5 subpanels...")
    # Fig 5a: Ground Chambers
    fig, ax = plt.subplots(figsize=(5.6, 4.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    chambers = [
        ("Chamber 1: GMF Control", "45–50 µT Ambient GMF", "#e3f2fd", "#1565c0", "Terrestrial baseline"),
        ("Chamber 2: Near-Null (NNMF)", "<10 nT (Shielded/Cancelled)", "#ffebee", "#c62828", "Lunar simulation"),
        ("Chamber 3: Sham Control", "Current matched; B = 0", "#fff3e0", "#e65100", "Controls ohmic heat & EMI")
    ]
    for idx, (c_name, b_field, bg, border, desc) in enumerate(chambers):
        y_c = 75 - idx * 28
        c_rect = patches.FancyBboxPatch((5, y_c), 90, 22, boxstyle="round,pad=0.3", edgecolor=border, facecolor=bg, lw=1.2)
        ax.add_patch(c_rect)
        ax.text(10, y_c + 14, c_name, weight='bold', fontsize=7.8, color=border)
        ax.text(10, y_c + 6, f"Field: {b_field} | Role: {desc}", fontsize=6.8, color="#37474f")
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig5a_ground_chambers.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 5b: Flight Telemetry
    fig, ax = plt.subplots(figsize=(5.6, 4.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    p_rect = patches.FancyBboxPatch((1.0, 1.0), 8.0, 8.0, boxstyle="round,pad=0.3", edgecolor="#37474f", facecolor="#f5f5f7", lw=1.2)
    ax.add_patch(p_rect)
    ax.text(5.0, 8.2, "Artemis LEAF Payload Enclosure", weight='bold', fontsize=8.0, ha='center', color="#263238")
    ax.text(5.0, 7.3, "[Sample Growth Volume (0.166 g Lunar Gravity)]", fontsize=6.8, ha='center', color="#546e7a")
    mag_box = patches.Circle((5.0, 4.8), 1.6, edgecolor="#1565c0", facecolor="#e3f2fd", lw=1.2)
    ax.add_patch(mag_box)
    ax.text(5.0, 5.2, "3-Axis Fluxgate", ha='center', weight='bold', fontsize=7.0, color="#0d47a1")
    ax.text(5.0, 4.4, "0.1 nT Resolution\n10 Hz Telemetry", ha='center', fontsize=6.2, color="#1565c0")
    ax.annotate('Seedling Cassette 1', xy=(2.5, 4.8), xytext=(2.5, 2.8), ha='center', fontsize=6.5,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#388e3c'))
    ax.annotate('Seedling Cassette 2', xy=(7.5, 4.8), xytext=(7.5, 2.8), ha='center', fontsize=6.5,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#388e3c'))
    ax.text(5.0, 1.6, "In-situ continuous telemetry decouples true\nlunar hypomagnetic exposure from spacecraft EMI",
            ha='center', fontsize=6.5, weight='bold', color="#37474f")
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig5b_flight_telemetry.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 5c: Causal Rescue Protocol
    fig, ax = plt.subplots(figsize=(5.6, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    rescue_box = patches.FancyBboxPatch((0.8, 1.2), 8.4, 7.6, boxstyle="round,pad=0.3", edgecolor="#6a1b9a", facecolor="#f3e5f5", lw=1.3)
    ax.add_patch(rescue_box)
    ax.text(5.0, 8.2, "Active Causal Rescue Protocol", weight='bold', fontsize=8.2, ha='center', color="#4a148c")
    steps = [
        ("Step 1: Environmental Shielding", "Permalloy / mu-metal or natural lunar surface void (<0.8 nT)"),
        ("Step 2: Triaxial Helmholtz Coils", "Independent X, Y, Z axes integrated into chamber wall"),
        ("Step 3: Vector Re-application", "Drive 45 µT static field aligned with Earth GMF vector"),
        ("Step 4: Biological Verification", "Restores t50 emergence velocity & HY5 pigment biosynthesis")
    ]
    y_s = 7.0
    for title, desc in steps:
        ax.text(1.4, y_s, title, weight='bold', fontsize=7.2, color="#6a1b9a")
        ax.text(1.4, y_s - 0.55, desc, fontsize=6.5, color="#333333")
        y_s -= 1.3
    ax.text(5.0, 1.8, "Active re-application establishes causality and provides\na deployable countermeasure for lunar agricultural payloads",
            ha='center', fontsize=6.5, weight='bold', color="#4a148c")
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig5c_causal_rescue.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Fig 5d: Decision Matrix Logic
    fig, ax = plt.subplots(figsize=(5.6, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    gates = [
        ("GREEN GATE (Nominal Flight)", "Ambient B < 5 nT | Germination ≥ 85%\nAction: Continue baseline autonomous imaging & telemetry", "#e8f5e9", "#2e7d32"),
        ("AMBER GATE (Investigation)", "Field 5–50 nT ripple | 15–30% emergence delay\nAction: Log telemetry; initiate secondary optical chlorophyll assay", "#fff8e1", "#f57f17"),
        ("RED GATE (Causal Intervention)", "Germination capacity drop > 30% | Severe chlorosis\nAction: Energize active 45 µT coils to rescue crop viability", "#ffebee", "#c62828")
    ]
    y_g = 7.5
    for title, desc, bg, edge in gates:
        g_rect = patches.FancyBboxPatch((0.6, y_g - 2.0), 8.8, 2.2, boxstyle="round,pad=0.2", edgecolor=edge, facecolor=bg, lw=1.2)
        ax.add_patch(g_rect)
        ax.text(1.0, y_g - 0.5, title, weight='bold', fontsize=7.5, color=edge)
        ax.text(1.0, y_g - 1.4, desc, fontsize=6.5, color="#333333")
        y_g -= 2.6
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'Fig5d_decision_matrix.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------------------------
# Graphical Abstract Subpanels
# ---------------------------------------------------------------------------
def export_ga_subpanels():
    print("Exporting Graphical Abstract subpanels...")
    # GA Panel 1: Problem
    fig, ax = plt.subplots(figsize=(4.0, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    card = patches.FancyBboxPatch((0.5, 0.5), 9.0, 9.0, boxstyle="round,pad=0.2", edgecolor="#1565c0", facecolor="#e3f2fd", lw=1.4)
    ax.add_patch(card)
    ax.text(5.0, 8.8, "1. THE LUNAR REALITY", ha='center', weight='bold', fontsize=8.5, color="#0d47a1")
    ax.text(5.0, 7.8, "Earth Dipolar GMF:\n25,000 – 65,000 nT\n(Evolutionary Baseline)", ha='center', fontsize=7.2, color="#1565c0")
    ax.annotate('', xy=(5.0, 5.4), xytext=(5.0, 6.6), arrowprops=dict(arrowstyle="->", color="#c62828", lw=1.8))
    ax.text(5.0, 6.0, "BLEO Transition", ha='center', fontsize=6.8, color="#c62828", weight='bold', backgroundcolor='#e3f2fd')
    ax.text(5.0, 4.4, "Lunar Surface Void:\n< 0.8 nT at Artemis Sites\n(>30,000× Drop)", ha='center', weight='bold', fontsize=7.5, color="#c62828")
    ax.text(5.0, 2.2, "CRITICAL GAP:\nMagnetic field vector is\nunmonitored in biological payloads\nmasked by lander avionics (50–500 µT)!",
            ha='center', fontsize=6.8, color="#333333")
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'GA_panel1_problem.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # GA Panel 2: Mechanism
    fig, ax = plt.subplots(figsize=(4.0, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    card = patches.FancyBboxPatch((0.5, 0.5), 9.0, 9.0, boxstyle="round,pad=0.2", edgecolor="#f57c00", facecolor="#fff3e0", lw=1.4)
    ax.add_patch(card)
    ax.text(5.0, 8.8, "2. THE 0–5 DAY BOTTLENECK", ha='center', weight='bold', fontsize=8.5, color="#e65100")
    points = [
        ("Germination Delay", "t50 lag +12–36 h; -10 to -30% count"),
        ("Yield Penalty", "-20 to -30% Day 5 biomass deficit"),
        ("Pigment Repression", "HEMA1, POR, CHS downregulation via CRY/HY5; chlorosis"),
        ("Mitochondrial Overload", "CO2-O2-ROS shift; AOX1D & CAT3 induction; astronaut parallel")
    ]
    y_p = 7.6
    for t, d in points:
        ax.text(5.0, y_p, t, ha='center', weight='bold', fontsize=7.2, color="#c62828")
        ax.text(5.0, y_p - 0.55, d, ha='center', fontsize=6.5, color="#333333")
        y_p -= 1.6
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'GA_panel2_mechanism.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # GA Panel 3: Solution
    fig, ax = plt.subplots(figsize=(4.0, 5.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    card = patches.FancyBboxPatch((0.5, 0.5), 9.0, 9.0, boxstyle="round,pad=0.2", edgecolor="#2e7d32", facecolor="#e8f5e9", lw=1.4)
    ax.add_patch(card)
    ax.text(5.0, 8.8, "3. FLIGHT RISK RETIREMENT", ha='center', weight='bold', fontsize=8.5, color="#1b5e20")
    sols = [
        ("In-Situ Magnetometry", "In-chamber 3-axis fluxgate telemetry to measure true exposure"),
        ("3-Chamber Ground Controls", "GMF, NNMF, and matched-current bifilar sham to decouple heat/EMI"),
        ("Active Causal Rescue", "40–50 µT vector re-application inside chamber rescues vigor"),
        ("Operational Flight Gates", "Predeclared Green / Amber / Red decision thresholds for Artemis LEAF")
    ]
    y_s = 7.6
    for t, d in sols:
        ax.text(5.0, y_s, t, ha='center', weight='bold', fontsize=7.2, color="#1b5e20")
        ax.text(5.0, y_s - 0.55, d, ha='center', fontsize=6.5, color="#333333")
        y_s -= 1.6
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'GA_panel3_solution.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

def main():
    print(f"Exporting presentation subpanels to: {OUT_DIR}")
    export_fig1_subpanels()
    export_fig2_subpanels()
    export_fig3_subpanels()
    export_fig4_subpanels()
    export_fig5_subpanels()
    export_ga_subpanels()

    png_files = list(OUT_DIR.glob('*.png'))
    print(f"\nSuccessfully exported {len(png_files)} subpanels to {OUT_DIR}")
    for p in sorted(png_files):
        print(f"  • {p.name} ({p.stat().st_size / 1024:.1f} KB)")

if __name__ == '__main__':
    main()
