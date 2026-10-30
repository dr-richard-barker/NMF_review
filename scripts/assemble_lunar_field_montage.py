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
    ax_map.set_title('Global Lunar Crustal Magnetic Field & Landing Sites (|B| at 30 km)', weight='bold', fontsize=8.8, pad=10)
    ax_map.text(-0.04, 1.03, 'a', transform=ax_map.transAxes, fontsize=11, weight='bold', va='bottom', ha='right')
    
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
    
    # Clean compact display names for South Pole sites to eliminate label collisions
    name_map = {
        'Malapert Massif': 'Malapert',
        'Leibnitz Beta Plateau': 'Leibnitz Beta',
        'Nobile Rim 1': 'Nobile 1',
        'Nobile Rim 2': 'Nobile 2',
        'Faustini Rim A': 'Faustini A',
        'Amundsen Rim': 'Amundsen',
        'Connecting Ridge': 'Conn. Ridge',
        'Connecting Ridge Extension': 'Conn. Ridge Ext.',
        'Peak Near Shackleton': 'Shackleton',
        'de Gerlache-Kocher Massif': 'de Gerl.-Kocher',
        'de Gerlache Rim 1': 'de Gerlache 1',
        'de Gerlache Rim 2': 'de Gerlache 2',
        'Haworth': 'Haworth',
    }

    # Verified zero-collision offsets and directional arrows for each Artemis South Pole site: (dx, dy, ha, va)
    site_offsets = {
        'Malapert Massif': (12, 14, 'left', 'bottom'),
        'Leibnitz Beta Plateau': (0, 32, 'center', 'bottom'),
        'Nobile Rim 1': (0, -32, 'center', 'top'),
        'Nobile Rim 2': (22, 0, 'left', 'center'),
        'Faustini Rim A': (12, -32, 'left', 'top'),
        'Amundsen Rim': (18, 28, 'left', 'bottom'),
        'Connecting Ridge': (15, 32, 'left', 'bottom'),
        'Connecting Ridge Extension': (0, -30, 'center', 'top'),
        'Peak Near Shackleton': (15, 110, 'left', 'bottom'),
        'de Gerlache-Kocher Massif': (14, 26, 'left', 'bottom'),
        'de Gerlache Rim 1': (14, -26, 'left', 'top'),
        'de Gerlache Rim 2': (18, 0, 'left', 'center'),
        'Haworth': (-14, 16, 'right', 'bottom'),
    }

    for _, row in artemis_sites.iterrows():
        s_name = name_map.get(row['name'], row['name'])
        dx, dy, ha_align, va_align = site_offsets.get(row['name'], (20, 12, 'left', 'bottom'))
        ax_polar.annotate(f"{s_name}\n({row['Bmag']:.2f} nT)", (row['lon'], row['lat']),
                          fontsize=6.5, ha=ha_align, va=va_align, xytext=(dx, dy), textcoords='offset points',
                          arrowprops=dict(arrowstyle="->", color="#37474f", lw=0.75, shrinkA=2, shrinkB=4),
                          bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.92, edgecolor='#757575', lw=0.45))
        
    ax_polar.set_xlim(-25, 385)
    ax_polar.set_ylim(-91.2, -82.4)
    ax_polar.set_xlabel('Longitude (°E)')
    ax_polar.set_ylabel('Latitude (°N)')
    ax_polar.set_title('Candidate Artemis Regions (|B| at 30 km Proxy)', weight='bold', pad=10, fontsize=8.8)
    ax_polar.text(-0.04, 1.03, 'b', transform=ax_polar.transAxes, fontsize=11, weight='bold', va='bottom', ha='right')
    ax_polar.grid(True, linestyle=':', alpha=0.6)
    
    cbar_pol = plt.colorbar(scatter, ax=ax_polar, orientation='vertical', fraction=0.035, pad=0.02)
    cbar_pol.set_label('$|\\mathbf{B}_{\\mathrm{crust}}|$ at 30 km (nT)', fontsize=7.8)
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
    ax_bar.axhline(1.0, color='#f57c00', linestyle='--', linewidth=1.0, label='Near-Null Boundary (1 nT; E_Z << a_hf)')
    ax_bar.axhline(5.0, color='#d32f2f', linestyle=':', linewidth=1.0, label='Moderate Crustal Swirl (5 nT)')
    
    ax_bar.set_xticks(x_pos)
    ax_bar.set_xticklabels(df_sorted['name'], rotation=55, ha='right', fontsize=7.0)
    ax_bar.set_ylabel('Crustal Field $|\\mathbf{B}|$ at 30 km (nT)')
    ax_bar.set_title('Crustal Field at Candidate Regions & Historical Sites', weight='bold', fontsize=8.8, pad=10)
    ax_bar.text(-0.04, 1.03, 'c', transform=ax_bar.transAxes, fontsize=11, weight='bold', va='bottom', ha='right')
    ax_bar.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=6.8)
    ax_bar.set_ylim(0, 5.5)
    ax_bar.grid(axis='y', linestyle=':', alpha=0.6)
    
    # Text annotation comparing to Earth GMF and Crustal Anomalies
    ax_bar.text(0.03, 0.72, 'Earth Geomagnetic Field: 25,000–65,000 nT\nExample Artemis Sites: 0.40–0.82 nT (30 km proxy)\nSurface enhancement bounded to <3–5 nT\nCrustal Swirls (Reiner Gamma): 1 to 100s of nT',
                transform=ax_bar.transAxes, fontsize=6.8, verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1976d2', alpha=0.95))

    # -------------------------------------------------------------
    # Panel (d): Superposition Equation & Biological Volume Schematic
    # -------------------------------------------------------------
    ax_sch = fig.add_subplot(gs[1, 1])
    ax_sch.axis('off')
    
    # Draw conceptual schematic
    ax_sch.set_xlim(0, 10.5)
    ax_sch.set_ylim(0, 11.2)
    ax_sch.set_title('Field Superposition at the Biological Volume', weight='bold', pad=10, fontsize=8.8)
    ax_sch.text(-0.02, 1.03, 'd', transform=ax_sch.transAxes, fontsize=11, weight='bold', va='bottom', ha='right')
    
    # 1. Equation banner (BLUE box) - widened with generous internal margins
    eq_rect = patches.FancyBboxPatch((0.20, 9.05), 10.10, 1.95, boxstyle="round,pad=0.1,rounding_size=0.25",
                                     edgecolor="#0288d1", facecolor="#e1f5fe", lw=1.2)
    ax_sch.add_patch(eq_rect)
    ax_sch.text(5.25, 10.20, r"$\mathbf{B}_{\mathrm{surface}}(t, \mathbf{x}) = \mathbf{B}_{\mathrm{crust}} + \mathbf{B}_{\mathrm{ext}} + \mathbf{B}_{\mathrm{lander}} + \mathbf{B}_{\mathrm{payload}} + \mathbf{B}_{\mathrm{control}}$",
                fontsize=8.0, weight='bold', ha='center', va='center', color='#01579b')
    ax_sch.text(5.25, 9.45, "Net Vector Sum Governs Primary Spin-Chemical Biomarkers",
                fontsize=7.2, ha='center', va='center', color='#0277bd', style='italic')

    # 2. Chamber box (GREY box) - widened to encompass all components comfortably
    cham_rect = patches.FancyBboxPatch((0.20, 0.35), 10.10, 8.40, boxstyle="round,pad=0.1,rounding_size=0.25",
                                       edgecolor="#37474f", facecolor="#eceff1", lw=1.5)
    ax_sch.add_patch(cham_rect)
    ax_sch.text(5.25, 8.40, "Lunar Plant Growth Enclosure (e.g., LEAF / BLSS)", 
                weight='bold', fontsize=8.2, ha='center', va='center', color='#263238')
    ax_sch.plot([0.60, 9.90], [8.05, 8.05], color='#b0bec5', lw=0.8, linestyle='--')

    # Vector contributions table / callouts
    contributions = [
        (r"$\mathbf{B}_{\mathrm{crust}}$", "0.40–0.82 nT", r"Lunar South Pole proxy (surface bound <3–5 nT; $|\nabla B| \ll 10^{-4}$ nT/cm)", "#1565c0"),
        (r"$\mathbf{B}_{\mathrm{ext}}$", "1 – 10 nT", "Dynamic solar wind IMF & magnetotail plasma sheet", "#2e7d32"),
        (r"$\mathbf{B}_{\mathrm{lander}}$", "50 – 500 µT", "Lander avionics, DC power buses & batteries at 1–3 m standoff", "#c62828"),
        (r"$\mathbf{B}_{\mathrm{payload}}$", "Static: 2–48 µT", "Internal wiring & drivers | AC PWM ripple: 15–50 nT_RMS", "#e65100"),
        (r"$\mathbf{B}_{\mathrm{control}}$", "40 – 50 µT", "Active 3-axis compensation / causal rescue coils", "#6a1b9a"),
    ]
    
    y_pos = [7.45, 6.70, 5.95, 5.20, 4.45]
    for (symbol, mag, desc, col), y_val in zip(contributions, y_pos):
        ax_sch.text(0.50, y_val, symbol, fontsize=8.4, weight='bold', color=col, va='center')
        ax_sch.text(1.75, y_val, f"[{mag}]", fontsize=7.1, weight='bold', color='#212121', va='center')
        ax_sch.text(4.00, y_val, desc, fontsize=6.6, color='#455a64', va='center')

    # 3. Warning notice (RED box) - widened with deep margins so text easily fits inside
    warn_rect = patches.FancyBboxPatch((0.45, 0.60), 9.60, 3.40, boxstyle="round,pad=0.15,rounding_size=0.2",
                                       edgecolor="#d32f2f", facecolor="#ffebee", lw=1.1)
    ax_sch.add_patch(warn_rect)
    ax_sch.text(5.25, 3.55, "CRITICAL: HARNESS ARTIFACTS & WITHIN-CASSETTE GRADIENTS",
                fontsize=7.4, weight='bold', ha='center', va='center', color='#b71c1c')
    ax_sch.text(5.25, 2.15, r"Unshielded payload DC currents (2–48 $\mu$T) generate steep gradients" + "\n" +
                r"($|\nabla B| \sim 1\mathrm{--}50$ nT/cm across 10 cm), swamping the regional near-null void." + "\n" +
                r"Bifilar twisted wiring and multi-point canopy magnetometry (<1 W, 50 g)" + "\n" +
                "are mandatory to measure and verify true biological exposures.",
                fontsize=6.6, ha='center', va='center', color='#c62828', linespacing=1.28)

    plt.tight_layout()
    out_pdf = OUT_DIR / 'Fig1_lunar_magnetic_environment_montage.pdf'
    out_png = OUT_DIR / 'Fig1_lunar_magnetic_environment_montage.png'
    fig.savefig(out_pdf, bbox_inches='tight')
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 1 successfully created at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    main()
