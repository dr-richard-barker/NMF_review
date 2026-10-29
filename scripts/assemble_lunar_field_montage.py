#!/usr/bin/env python3
"""
assemble_lunar_field_montage.py

Generates Figure 1 for Life Sciences in Space Research:
Montage of the Lunar Surface Magnetic Environment & Landing Sites.
Panels:
(a) Global Crustal Field Map with Landing Site Overlays (Apollo, Chang'e, Chandrayaan, Artemis)
(b) Crustal Magnetic Field Magnitude Across Candidate and Historical Landing Sites
(c) Magnetic Field Superposition at the Biological Volume: B_total = B_crust + B_ext + B_lander + B_payload + B_control
(d) South Polar Artemis Exploration Footprint Magnetic Detail
"""

import os
import sys
from pathlib import Path

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_cache'

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Matplotlib configuration for LSSR / Elsevier publication standard
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

REPO_ROOT = Path(__file__).resolve().parent.parent
LUNAR_DATA_DIR = REPO_ROOT / 'data'
GRID_FILE = LUNAR_DATA_DIR / 'lunar_mag_field_grid.csv'
SITES_FILE = LUNAR_DATA_DIR / 'landing_sites_magnetic.csv'
OUT_DIR = REPO_ROOT / 'figures'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print(f"Loading data from {LUNAR_DATA_DIR}...")
    df_sites = pd.read_csv(SITES_FILE)
    df_grid = pd.read_csv(GRID_FILE)
    
    fig = plt.figure(figsize=(11.5, 9.2), dpi=300)
    
    # 4-panel layout:
    # Row 1: Global map (a) [left] and South Polar detail (b) [right]
    # Row 2: Landing site bar chart (c) [left] and Field Superposition Schematic (d) [right]
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1.0], width_ratios=[1.20, 1.0], hspace=0.34, wspace=0.36)
    
    # -------------------------------------------------------------
    # Panel (a): Global Crustal Magnetic Map with Landing Sites
    # -------------------------------------------------------------
    ax_map = fig.add_subplot(gs[0, 0])
    
    lons = np.sort(df_grid['lon'].unique())
    lats = np.sort(df_grid['lat'].unique())
    lon_mesh, lat_mesh = np.meshgrid(lons, lats)
    z_bmag = df_grid.pivot(index='lat', columns='lon', values='Bmag').values
    
    vmax = np.nanpercentile(z_bmag, 98)
    img = ax_map.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='viridis',
                            vmin=0, vmax=vmax, alpha=0.90, shading='auto')
    
    # Markers for missions
    markers = {'Artemis': '*', 'Apollo': 'o', "Chang'e": 's', 'Chandrayaan': '^'}
    colors = {'Artemis': '#ff1744', 'Apollo': '#ffffff', "Chang'e": '#ffea00', 'Chandrayaan': '#00e5ff'}
    
    for mission in ['Apollo', "Chang'e", 'Chandrayaan', 'Artemis']:
        sub = df_sites[df_sites['mission'] == mission]
        if not sub.empty:
            ax_map.scatter(sub['lon'], sub['lat'], marker=markers.get(mission, 'o'),
                           color=colors.get(mission, 'white'), edgecolor='black', linewidth=0.7,
                           s=75 if mission == 'Artemis' else 40, label=f"{mission} ({len(sub)})", zorder=5)
            
    ax_map.legend(loc='lower center', bbox_to_anchor=(0.5, -0.24), ncol=4, frameon=True, facecolor='white', framealpha=0.9)
    ax_map.set_xlabel('Longitude (°E)')
    ax_map.set_ylabel('Latitude (°N)')
    ax_map.set_xlim(0, 360)
    ax_map.set_ylim(-90, 65)
    ax_map.set_title('(a) Global Lunar Crustal Magnetic Field & Landing Sites (|B| at 30 km)', weight='bold')
    
    cbar = plt.colorbar(img, ax=ax_map, orientation='vertical', fraction=0.03, pad=0.015)
    cbar.set_label('$|\\mathbf{B}|$ at 30 km (nT)', fontsize=7.8)
    cbar.ax.tick_params(labelsize=6.8)
    
    # Highlight South Pole Artemis region
    rect = patches.Rectangle((0, -90), 360, 10, linewidth=1.2, edgecolor='#ff1744', facecolor='none', linestyle='--', zorder=6)
    ax_map.add_patch(rect)
    ax_map.text(180, -78, 'Example Artemis South Pole Regions (B < 1 nT)', color='#ff1744', weight='bold', ha='center', fontsize=7.2,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor='#ff1744'))

    # -------------------------------------------------------------
    # Panel (b): South Polar Detail (Artemis Exploration Footprint)
    # -------------------------------------------------------------
    ax_polar = fig.add_subplot(gs[0, 1])
    
    artemis_sites = df_sites[df_sites['mission'] == 'Artemis'].copy()
    artemis_sites = artemis_sites.sort_values('Bmag', ascending=True).reset_index(drop=True)
    
    # Polar scatter / scatter in lat-lon
    ax_polar.set_facecolor('#f5f5f7')
    scatter = ax_polar.scatter(artemis_sites['lon'], artemis_sites['lat'], 
                               c=artemis_sites['Bmag'], cmap='plasma', s=110,
                               edgecolor='black', linewidth=0.8, vmin=0.3, vmax=0.9, zorder=4)
    
    # Custom non-overlapping offsets for each Artemis South Pole site: (dx, dy, ha, va)
    site_offsets = {
        'Haworth': (-8, 10, 'right', 'bottom'),
        'Connecting Ridge': (-10, 6, 'right', 'bottom'),
        'Connecting Ridge Extension': (10, -10, 'left', 'top'),
        'de Gerlache Rim 1': (10, 8, 'left', 'bottom'),
        'de Gerlache Rim 2': (10, -10, 'left', 'top'),
        'de Gerlache-Kocher Massif': (-10, 6, 'right', 'bottom'),
        'Peak Near Shackleton': (10, 4, 'left', 'bottom'),
        'Faustini Rim A': (-10, 8, 'right', 'bottom'),
        'Nobile Rim 1': (10, 8, 'left', 'bottom'),
        'Nobile Rim 2': (10, -12, 'left', 'top'),
        'Leibnitz Beta Plateau': (-10, -12, 'right', 'top'),
        'Amundsen Rim': (10, -12, 'left', 'top'),
        'Malapert Massif': (10, 0, 'left', 'center'),
    }

    for _, row in artemis_sites.iterrows():
        s_name = row['name'].replace('Connecting Ridge Extension', 'Conn. Ridge Ext.').replace('de Gerlache-Kocher Massif', 'de Gerlache-Kocher')
        dx, dy, ha_align, va_align = site_offsets.get(row['name'], (8, 0, 'left', 'center'))
        ax_polar.annotate(f"{s_name}\n({row['Bmag']:.2f} nT)", (row['lon'], row['lat']),
                          fontsize=6.8, ha=ha_align, va=va_align, xytext=(dx, dy), textcoords='offset points',
                          bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.90, edgecolor='#757575', lw=0.4))
        
    ax_polar.set_xlim(-15, 385)
    ax_polar.set_ylim(-91.0, -82.6)
    ax_polar.set_xlabel('Longitude (°E)')
    ax_polar.set_ylabel('Latitude (°N)')
    ax_polar.set_title('(b) Example Candidate Artemis Regions (Near-Null Field)', weight='bold', pad=12)
    ax_polar.grid(True, linestyle=':', alpha=0.6)
    
    cbar_pol = plt.colorbar(scatter, ax=ax_polar, orientation='vertical', fraction=0.035, pad=0.02)
    cbar_pol.set_label('$|\\mathbf{B}_{\\mathrm{crust}}|$ (nT)', fontsize=7.8)
    cbar_pol.ax.tick_params(labelsize=6.8)

    # -------------------------------------------------------------
    # Panel (c): Landing Site Comparison Bar Chart
    # -------------------------------------------------------------
    ax_bar = fig.add_subplot(gs[1, 0])
    
    df_sorted = df_sites.sort_values(['mission', 'Bmag'], ascending=[True, False]).reset_index(drop=True)
    color_map = {'high-field': '#d32f2f', 'moderate': '#f57c00', 'low/null-field': '#1976d2'}
    bar_colors = [color_map.get(c, '#757575') for c in df_sorted['classification']]
    
    x_pos = np.arange(len(df_sorted))
    ax_bar.bar(x_pos, df_sorted['Bmag'], color=bar_colors, edgecolor='black', linewidth=0.5, alpha=0.9)
    
    # Reference thresholds
    ax_bar.axhline(1.0, color='#f57c00', linestyle='--', linewidth=1.0, label='Near-Null Boundary (1 nT)')
    ax_bar.axhline(5.0, color='#d32f2f', linestyle=':', linewidth=1.0, label='Moderate Crustal Swirl (5 nT)')
    
    ax_bar.set_xticks(x_pos)
    ax_bar.set_xticklabels(df_sorted['name'], rotation=55, ha='right', fontsize=7.0)
    ax_bar.set_ylabel('Crustal Field $|\\mathbf{B}|$ at 30 km (nT)')
    ax_bar.set_title('(c) Magnetic Field at Candidate Regions & Historical Sites', weight='bold')
    ax_bar.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=7.0)
    ax_bar.set_ylim(0, 5.5)
    ax_bar.grid(axis='y', linestyle=':', alpha=0.6)
    
    # Text annotation comparing to Earth GMF and Crustal Anomalies
    ax_bar.text(0.03, 0.72, 'Earth Geomagnetic Field: 25,000–65,000 nT\nExample Artemis Sites: 0.40–0.82 nT (>30,000× lower)\nCrustal Swirls (Reiner Gamma): 1 to 100s of nT',
                transform=ax_bar.transAxes, fontsize=7.2, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1976d2', alpha=0.95))

    # -------------------------------------------------------------
    # Panel (d): Superposition Equation & Biological Volume Schematic
    # -------------------------------------------------------------
    ax_sch = fig.add_subplot(gs[1, 1])
    ax_sch.axis('off')
    
    # Draw conceptual schematic
    ax_sch.set_xlim(0, 10)
    ax_sch.set_ylim(0, 10)
    ax_sch.set_title('(d) Field Superposition at the Biological Volume', weight='bold', pad=12)
    
    # 1. Equation banner (BLUE box)
    eq_rect = patches.FancyBboxPatch((0.5, 7.95), 9.0, 1.65, boxstyle="round,pad=0.1,rounding_size=0.25",
                                     edgecolor="#0288d1", facecolor="#e1f5fe", lw=1.2)
    ax_sch.add_patch(eq_rect)
    ax_sch.text(5.0, 8.95, r"$\mathbf{B}_{\mathrm{total}}(t, \mathbf{x}) = \mathbf{B}_{\mathrm{crust}} + \mathbf{B}_{\mathrm{ext}} + \mathbf{B}_{\mathrm{lander}} + \mathbf{B}_{\mathrm{payload}} + \mathbf{B}_{\mathrm{control}}$",
                fontsize=8.8, weight='bold', ha='center', va='center', color='#01579b')
    ax_sch.text(5.0, 8.35, "Net Vector Sum Governs Primary Spin-Chemical Biomarkers",
                fontsize=7.2, ha='center', va='center', color='#0277bd', style='italic')

    # 2. Chamber box (GREY box)
    cham_rect = patches.FancyBboxPatch((0.5, 0.40), 9.0, 7.25, boxstyle="round,pad=0.1,rounding_size=0.25",
                                       edgecolor="#37474f", facecolor="#eceff1", lw=1.5)
    ax_sch.add_patch(cham_rect)
    ax_sch.text(5.0, 7.25, "Lunar Plant Growth Enclosure (e.g., LEAF / BLSS)", 
                weight='bold', fontsize=8.2, ha='center', va='center', color='#263238')
    ax_sch.plot([1.0, 9.0], [6.95, 6.95], color='#b0bec5', lw=0.8, linestyle='--')

    # Vector contributions table / callouts
    contributions = [
        (r"$\mathbf{B}_{\mathrm{crust}}$", "0.4 – 0.8 nT", "Lunar South Pole paleomagnetic void", "#1565c0"),
        (r"$\mathbf{B}_{\mathrm{ext}}$", "1 – 5 nT", "Solar wind IMF / magnetotail shadow", "#2e7d32"),
        (r"$\mathbf{B}_{\mathrm{lander}}$", "50 – 500 µT", "Lander avionics, DC power buses & batteries [Confounder]", "#c62828"),
        (r"$\mathbf{B}_{\mathrm{payload}}$", "15 – 20 nT", "Payload fans, fluidic pumps, heaters, LEDs [Ripple]", "#e65100"),
        (r"$\mathbf{B}_{\mathrm{control}}$", "40 – 50 µT", "Active 3-axis compensation / causal rescue coils", "#6a1b9a"),
    ]
    
    y_pos = [6.45, 5.65, 4.85, 4.05, 3.25]
    for (symbol, mag, desc, col), y_val in zip(contributions, y_pos):
        ax_sch.text(1.00, y_val, symbol, fontsize=8.4, weight='bold', color=col, va='center')
        ax_sch.text(2.40, y_val, f"[{mag}]", fontsize=7.4, weight='bold', color='#212121', va='center')
        ax_sch.text(4.15, y_val, desc, fontsize=6.8, color='#455a64', va='center')

    # 3. Warning notice (RED box) - neatly positioned with generous padding
    warn_rect = patches.FancyBboxPatch((0.85, 0.65), 8.3, 1.85, boxstyle="round,pad=0.1,rounding_size=0.2",
                                       edgecolor="#d32f2f", facecolor="#ffebee", lw=1.0)
    ax_sch.add_patch(warn_rect)
    ax_sch.text(5.0, 2.15, "CRITICAL: LANDER AVIONICS ARTIFACT RISK",
                fontsize=7.2, weight='bold', ha='center', va='center', color='#b71c1c')
    ax_sch.text(5.0, 1.45, "Unshielded DC currents (50–500 µT) follow a steep 1/r³ falloff and can swamp\nthe ambient null field. Sample-level 3-axis canopy magnetometry (<1 W, 50 g)\nis essential to decouple true lunar hypomagnetic effects from avionics noise.",
                fontsize=6.5, ha='center', va='center', color='#b71c1c', linespacing=1.25)

    plt.tight_layout()
    out_pdf = OUT_DIR / 'Fig1_lunar_magnetic_environment_montage.pdf'
    out_png = OUT_DIR / 'Fig1_lunar_magnetic_environment_montage.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 1 successfully created at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    main()
