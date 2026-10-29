#!/usr/bin/env python3
"""
plot_integrative_methods_framework.py

Generates Figure 2 for Life Sciences in Space Research (LSSR):
Integrative Review Conceptual Framework & PRISMA/SANRA Evidence Selection Flow Diagram.

Panels:
(a) Conceptual Framework of the Integrative Review:
    Progression from research questions (RQ1–RQ4) through multi-disciplinary data sources,
    selection/exclusion criteria, and multi-scale thematic synthesis across 5 core domains.
(b) Evidence Identification and Selection Flow Diagram:
    PRISMA/SANRA-compliant evidence synthesis flow mapping 1,428 database records and 6 primary
    spaceflight/planetary datasets down to the 80 audited publications and 6 datasets synthesized.
"""

import os
from pathlib import Path

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_cache'

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Elsevier / LSSR typography standard
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
OUT_DIR = REPO_ROOT / 'figures'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    fig = plt.figure(figsize=(11.8, 8.8), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.05], wspace=0.18)

    # =========================================================================
    # Panel (a): Conceptual Framework of the Integrative Review
    # =========================================================================
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.axis('off')
    ax_a.set_xlim(0, 100)
    ax_a.set_ylim(0, 100)
    ax_a.set_title('(a) Conceptual Framework of the Integrative Review', weight='bold', fontsize=9.8, pad=12)

    # Helper function for cards
    def draw_card(ax, x, y, w, h, bg_color, border_color, lw=1.2, radius=1.8):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                                      facecolor=bg_color, edgecolor=border_color, lw=lw, zorder=2)
        ax.add_patch(rect)
        return rect

    # Helper function for vertical connectors
    def draw_down_arrow(ax, x, y_start, y_end, color="#455a64", lw=1.2):
        ax.annotate('', xy=(x, y_end), xytext=(x, y_start),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12),
                    zorder=3)

    # 1. Research Questions Box (Blue)
    draw_card(ax_a, 4, 76, 92, 21.5, "#e1f5fe", "#0288d1", lw=1.3)
    ax_a.text(50, 94.5, "1. RESEARCH QUESTIONS (SANRA GUIDELINES)", weight='bold', fontsize=8.4,
              ha='center', va='center', color="#01579b")
    rq_items = [
        r"$\mathbf{RQ1:}$ Planetary surface magnetic vector magnitude & lander/payload superposition",
        r"$\mathbf{RQ2:}$ First 5 days seedling kinetics: germination capacity, emergence lag ($t_{50}$), biomass",
        r"$\mathbf{RQ3:}$ Quantum cryptochrome radical pairs & multi-stressor ROS bioenergetic nexus",
        r"$\mathbf{RQ4:}$ Ground simulation standards, hardware self-magnetic mapping & flight decision gates",
    ]
    y_rq = [90.5, 86.5, 82.5, 78.5]
    for text, y in zip(rq_items, y_rq):
        ax_a.text(7, y, "• " + text, fontsize=6.8, ha='left', va='center', color="#0d47a1")

    draw_down_arrow(ax_a, 50, 76, 71.5)

    # 2. Multi-Disciplinary Data Sources (Purple)
    draw_card(ax_a, 4, 51.5, 92, 20.0, "#f3e5f5", "#7b1fa2", lw=1.3)
    ax_a.text(50, 68.5, "2. MULTI-DISCIPLINARY DATA SOURCES & REPOSITORIES", weight='bold', fontsize=8.4,
              ha='center', va='center', color="#4a148c")
    sources = [
        ("Planetary Geophysics", "Lunar Prospector LP-MAG, Kaguya LMAG & Apollo vector models (NASA PDS / JAXA)"),
        ("Plant Space Biology", "Peer-reviewed literature across PubMed, Web of Science, Scopus, and Europe PMC"),
        ("Quantum Biology", "Quantum Biology Atlas (QBM-06) enzymatic & cryptochrome spin-chemical models"),
        ("Spaceflight Multi-Omics", "NASA OSDR (OSD-782, OSD-8, OSD-27) & Astronaut Multi-Omics Consortium profiles"),
    ]
    y_src = [64.5, 60.5, 56.5, 52.5]
    for (category, desc), y in zip(sources, y_src):
        ax_a.text(7, y, f"• {category}:", weight='bold', fontsize=6.8, ha='left', va='center', color="#4a148c")
        ax_a.text(32, y, desc, fontsize=6.5, ha='left', va='center', color="#37474f")

    draw_down_arrow(ax_a, 50, 51.5, 47.0)

    # 3. Selection & Screening Criteria (Amber/Orange)
    draw_card(ax_a, 4, 28.5, 92, 18.5, "#fff8e1", "#f57c00", lw=1.3)
    ax_a.text(50, 44.0, "3. SELECTION & SCOPING CRITERIA", weight='bold', fontsize=8.4,
              ha='center', va='center', color="#e65100")
    
    # Left sub-column: Inclusion
    ax_a.text(8, 40.0, "[ INCLUSION CRITERIA ]", weight='bold', fontsize=6.8, color="#2e7d32")
    inc_items = [
        r"Near-null field exposure ($|\mathbf{B}| < 5\ \mu\text{T}$)",
        "0–5 day seedling developmental stages",
        "Empirical kinetics, pigment, or omics data",
        "Calibrated planetary & orbital datasets",
    ]
    for text, y in zip(inc_items, [36.5, 33.5, 30.5, 27.5]):
        ax_a.text(8, y + 2.0, "(+) " + text, fontsize=6.3, color="#1b5e20", va='center')

    # Right sub-column: Exclusion
    ax_a.text(52, 40.0, "[ EXCLUSION CRITERIA ]", weight='bold', fontsize=6.8, color="#c62828")
    exc_items = [
        r"High static fields ($|\mathbf{B}| > 1\text{ mT}$, e.g. MRI)",
        "Post-Day 14 whole-life without early data",
        "Animal-only models without bioenergetics",
        "Unshielded controls lacking ambient logs",
    ]
    for text, y in zip(exc_items, [36.5, 33.5, 30.5, 27.5]):
        ax_a.text(52, y + 2.0, "(-) " + text, fontsize=6.3, color="#b71c1c", va='center')

    draw_down_arrow(ax_a, 50, 28.5, 24.0)

    # 4. Multi-Scale Thematic Synthesis (Green)
    draw_card(ax_a, 4, 2.0, 92, 22.0, "#e8f5e9", "#2e7d32", lw=1.4)
    ax_a.text(50, 21.0, "4. MULTI-SCALE THEMATIC SYNTHESIS (5 CORE DOMAINS)", weight='bold', fontsize=8.4,
              ha='center', va='center', color="#1b5e20")
    domains = [
        ("D1: Planetary Environment", "Ambient lunar South Pole null void (<0.82 nT) & spacecraft superposition"),
        ("D2: Seedling Kinetics", "First 5 days: germination lag, +16 h emergence lag, -28.5% Day 5 biomass"),
        ("D3: Quantum Biology", "Cryptochrome radical pairs, spin-chemical shifts & mitochondrial electron leak"),
        ("D4: Multi-Stressor Nexus", "Exploration atmosphere (elevated CO2, 34% O2) & radiation overlap (AOX1D)"),
        ("D5: Risk Retirement", "3-chamber simulation standards, hardware power mapping & flight decision gates"),
    ]
    y_dom = [17.5, 14.0, 10.5, 7.0, 3.5]
    for (d_title, d_desc), y in zip(domains, y_dom):
        ax_a.text(7, y, d_title + ":", weight='bold', fontsize=6.7, ha='left', va='center', color="#1b5e20")
        ax_a.text(37, y, d_desc, fontsize=6.4, ha='left', va='center', color="#263238")

    # =========================================================================
    # Panel (b): PRISMA / SANRA Evidence Selection Flow Diagram
    # =========================================================================
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.axis('off')
    ax_b.set_xlim(0, 100)
    ax_b.set_ylim(0, 100)
    ax_b.set_title('(b) Evidence Identification & Selection Flow (PRISMA/SANRA)', weight='bold', fontsize=9.8, pad=12)

    # Stage 1: Identification
    # Stage indicator tag
    draw_card(ax_b, 1, 89, 14, 8, "#e0e0e0", "#757575", lw=0.8, radius=1.0)
    ax_b.text(8, 93, "IDENTIFY", weight='bold', fontsize=6.2, ha='center', va='center', color="#424242", rotation=90)

    # Database records card (Left)
    draw_card(ax_b, 18, 86, 38, 13.5, "#e3f2fd", "#1976d2", lw=1.1)
    ax_b.text(37, 96.5, "DATABASE RECORDS", weight='bold', fontsize=7.4, ha='center', va='center', color="#0d47a1")
    ax_b.text(37, 93.0, "PubMed: n = 542\nWeb of Science: n = 418\nScopus / Europe PMC: n = 286\nNASA OSDR Queries: n = 182",
              fontsize=6.2, ha='center', va='center', color="#263238")
    ax_b.text(37, 88.0, "Total Records: n = 1,428", weight='bold', fontsize=6.8, ha='center', va='center', color="#1565c0")

    # Public repositories card (Right)
    draw_card(ax_b, 59, 86, 38, 13.5, "#f3e5f5", "#7b1fa2", lw=1.1)
    ax_b.text(78, 96.5, "PUBLIC DATASETS", weight='bold', fontsize=7.4, ha='center', va='center', color="#4a148c")
    ax_b.text(78, 93.0, "NASA OSDR: OSD-782, 8, 27 (n=3)\nNASA PDS / SELENE Grid (n=1)\nQuantum Biology Atlas QBM-06 (n=1)\nAstronaut Multi-Omics (n=1)",
              fontsize=6.2, ha='center', va='center', color="#263238")
    ax_b.text(78, 88.0, "Total Datasets: n = 6", weight='bold', fontsize=6.8, ha='center', va='center', color="#6a1b9a")

    # Stage 2: Deduplication & Screening
    draw_card(ax_b, 1, 64, 14, 17, "#e0e0e0", "#757575", lw=0.8, radius=1.0)
    ax_b.text(8, 72.5, "SCREEN", weight='bold', fontsize=6.2, ha='center', va='center', color="#424242", rotation=90)

    # Convergence arrow from identification
    ax_b.annotate('', xy=(37, 81), xytext=(37, 86), arrowprops=dict(arrowstyle="-|>", color="#37474f", lw=1.1))
    ax_b.annotate('', xy=(37, 81), xytext=(78, 86), arrowprops=dict(arrowstyle="-|>", color="#37474f", lw=1.1, connectionstyle="angle,angleA=0,angleB=90,rad=3"))

    # Central screening card
    draw_card(ax_b, 18, 65, 38, 15.5, "#fffde7", "#fbc02d", lw=1.1)
    ax_b.text(37, 77.5, "RECORDS SCREENED", weight='bold', fontsize=7.4, ha='center', va='center', color="#f57f17")
    ax_b.text(37, 73.0, "Duplicates Removed:\nn = 512 records\n\nTitle & Abstract Screening:\nn = 916 unique records",
              fontsize=6.4, ha='center', va='center', color="#37474f")

    # Excluded records card (Right)
    draw_card(ax_b, 59, 65, 38, 15.5, "#ffebee", "#e53935", lw=1.1)
    ax_b.text(78, 77.5, "RECORDS EXCLUDED (n = 701)", weight='bold', fontsize=7.1, ha='center', va='center', color="#c62828")
    ax_b.text(78, 72.0, "• Static high-field / MRI (>1 mT): n = 314\n• Animal / clinical (no overlap): n = 228\n• Whole-life lacking 0–5 d: n = 159",
              fontsize=6.3, ha='center', va='center', color="#b71c1c")

    # Horizontal exclusion arrow
    ax_b.annotate('', xy=(59, 72.5), xytext=(56, 72.5), arrowprops=dict(arrowstyle="-|>", color="#e53935", lw=1.1))

    # Stage 3: Eligibility Assessment
    draw_card(ax_b, 1, 41, 14, 17, "#e0e0e0", "#757575", lw=0.8, radius=1.0)
    ax_b.text(8, 49.5, "ELIGIBLE", weight='bold', fontsize=6.2, ha='center', va='center', color="#424242", rotation=90)

    # Downward arrow to eligibility
    draw_down_arrow(ax_b, 37, 65, 58)

    # Full text assessed card
    draw_card(ax_b, 18, 42, 38, 15.5, "#e0f2f1", "#00897b", lw=1.1)
    ax_b.text(37, 54.5, "FULL-TEXT ASSESSED", weight='bold', fontsize=7.4, ha='center', va='center', color="#004d40")
    ax_b.text(37, 49.0, "Full-Text Articles Assessed:\nn = 215 articles\n\nEvaluated against magnetic\nshielding & 0–5 d phenotypes",
              fontsize=6.4, ha='center', va='center', color="#004d40")

    # Full text excluded card (Right)
    draw_card(ax_b, 59, 42, 38, 15.5, "#ffebee", "#e53935", lw=1.1)
    ax_b.text(78, 54.5, "FULL-TEXT EXCLUDED (n = 135)", weight='bold', fontsize=7.1, ha='center', va='center', color="#c62828")
    ax_b.text(78, 49.0, "• Missing magnetic field logs: n = 64\n• Incomplete gas/light metrics: n = 43\n• Unshielded DC confounders: n = 28",
              fontsize=6.3, ha='center', va='center', color="#b71c1c")

    # Horizontal exclusion arrow
    ax_b.annotate('', xy=(59, 49.5), xytext=(56, 49.5), arrowprops=dict(arrowstyle="-|>", color="#e53935", lw=1.1))

    # Stage 4: Included in Synthesis
    draw_card(ax_b, 1, 3, 14, 33, "#e0e0e0", "#757575", lw=0.8, radius=1.0)
    ax_b.text(8, 19.5, "INCLUDED", weight='bold', fontsize=6.2, ha='center', va='center', color="#424242", rotation=90)

    # Downward arrow to synthesis
    draw_down_arrow(ax_b, 37, 42, 36)

    # Final Included Synthesis Box (Green full-width banner)
    draw_card(ax_b, 18, 3.5, 79, 32.0, "#e8f5e9", "#2e7d32", lw=1.5)
    ax_b.text(57.5, 32.5, "SYNTHESIZED REVIEW CORPUS & COMPUTATIONAL ARTIFACTS",
              weight='bold', fontsize=7.8, ha='center', va='center', color="#1b5e20")
    
    # 2 Sub-boxes inside included
    # Box 1: Audited studies
    draw_card(ax_b, 20.5, 14.5, 36, 15.5, "#ffffff", "#4caf50", lw=1.0, radius=1.2)
    ax_b.text(38.5, 27.0, "80 AUDITED STUDIES", weight='bold', fontsize=7.2, ha='center', va='center', color="#1b5e20")
    ax_b.text(38.5, 21.0, "Curated in Supplemental Table S1\nDetailed by author, year, field (nT),\nmodel species, and biological endpoints",
              fontsize=6.0, ha='center', va='center', color="#263238")

    # Box 2: Public datasets
    draw_card(ax_b, 58.5, 14.5, 36, 15.5, "#ffffff", "#4caf50", lw=1.0, radius=1.2)
    ax_b.text(76.5, 27.0, "6 PRIMARY DATASETS", weight='bold', fontsize=7.2, ha='center', va='center', color="#1b5e20")
    ax_b.text(76.5, 21.0, "Curated in Supplemental Table S2\nNASA OSDR-782, OSD-8, OSD-27;\nPDS/SELENE; QBM-06; Astronaut Omics",
              fontsize=6.0, ha='center', va='center', color="#263238")

    # Open source package footer callout
    draw_card(ax_b, 20.5, 5.0, 74, 7.5, "#f1f8e9", "#33691e", lw=0.9, radius=1.0)
    ax_b.text(57.5, 8.8, "Open-Source Analytical Package: dr-richard-barker/NMF_review (GitHub & Zenodo)",
              weight='bold', fontsize=6.5, ha='center', va='center', color="#33691e")

    plt.tight_layout()
    out_png = OUT_DIR / 'Fig2_integrative_methods_framework.png'
    out_pdf = OUT_DIR / 'Fig2_integrative_methods_framework.pdf'
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 2 successfully generated at:\n  {out_png}\n  {out_pdf}")

if __name__ == '__main__':
    main()
