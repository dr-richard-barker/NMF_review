#!/usr/bin/env python3
"""
generate_latex_tables.py
Generates clean, booktabs-formatted LaTeX table fragments in latex/tables/
optimized for Springer Nature [sn-nature, iicol] two-column layout.
"""

import re
import pandas as pd
from pathlib import Path

OUT_DIR = Path('latex/tables')
OUT_DIR.mkdir(parents=True, exist_ok=True)

def tex_escape(s):
    """Safely escapes text for inclusion in LaTeX table cells."""
    if pd.isna(s):
        return ""
    s = str(s).strip()
    
    # Mathematical and greek symbols
    s = s.replace('γ', r'$\gamma$')
    s = s.replace('κ', r'$\kappa$')
    s = s.replace('Δ', r'$\Delta$')
    s = s.replace('±', r'$\pm$')
    s = s.replace('≥', r'$\ge$')
    s = s.replace('≤', r'$\le$')
    s = s.replace('~', r'$\sim$')
    s = s.replace('•-', r'$^{\bullet -}$')
    s = s.replace('•+', r'$^{\bullet +}$')
    s = s.replace('•', r'$\bullet$')
    s = s.replace('²', r'$^2$')
    s = s.replace('°C', r'$^\circ$C')
    s = s.replace('°', r'$^\circ$')
    s = s.replace('–', '--').replace('—', '---')
    
    # Units and formulas
    s = re.sub(r'\bµT\b', r'$\\upmu$T', s)
    s = re.sub(r'\buT\b', r'$\\upmu$T', s)
    s = re.sub(r'\bµmol\b', r'$\\upmu$mol', s)
    s = re.sub(r'\bumol\b', r'$\\upmu$mol', s)
    s = re.sub(r'\bH2O2\b', r'$\\text{H}_2\\text{O}_2$', s)
    s = re.sub(r'\bFv/Fm\b', r'$F_v/F_m$', s)
    s = re.sub(r'\bH\+\b', r'H$^+$', s)
    s = re.sub(r'\bt50\b', r'$t_{50}$', s)
    
    # LaTeX special characters
    s = re.sub(r'(?<!\\)&', r'\&', s)
    s = re.sub(r'(?<!\\)%', r'\%', s)
    s = re.sub(r'(?<!\\)_', r'\_', s)
    s = re.sub(r'(?<!\\)#', r'\#', s)
    s = re.sub(r'<', r'$<$', s)
    s = re.sub(r'>', r'$>$', s)
    
    return s

def generate_table1():
    df = pd.read_csv('tables/Table1_site_magnetic_values.csv')
    path = OUT_DIR / 'table1_sites.tex'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(r"""\begin{table*}[t]
\caption{Crustal magnetic field magnitude and vector components at candidate Artemis landing regions and historical lunar surface landing sites derived from orbital magnetometer models at 30~km mapping altitude (crustal proxy).}\label{tab:sites}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}llcccccc@{}}
\toprule
Landing Site / Region & Mission & Lat ($^\circ$N) & Lon ($^\circ$E) & $|B|$ (nT) & $B_r$ (nT) & $B_\theta$ (nT) & $B_\phi$ (nT) \\
\midrule
""")
        for _, r in df.iterrows():
            name = tex_escape(str(r['landing_site']).replace(' (Example Candidate)', ''))
            f.write(f"\\raggedright\\footnotesize {name} & \\footnotesize {tex_escape(r['mission'])} & \\footnotesize {r['latitude']:.2f} & \\footnotesize {r['longitude']:.2f} & \\footnotesize {r['b_mag_30km_nt']:.2f} & \\footnotesize {r['br_nt']:.2f} & \\footnotesize {r['btheta_nt']:.2f} & \\footnotesize {r['bphi_nt']:.2f} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Note: Values represent regional crustal remnant fields at 30~km mapping altitude derived from Lunar Prospector and Kaguya magnetometer observations and spherical harmonic models (Hood et al., 2022; Tsunakawa et al., 2015; Purucker \& Nicholas, 2010), acting as a physical proxy for relative site ranking. Total in situ surface field inside a plant cassette encompasses downward-continued crustal field, dynamic interplanetary solar wind/IMF ($1$--$10$~nT), terrestrial magnetotail passage ($5$--$20$~nT), and spacecraft/payload self-magnetic fields ($\mathbf{B}_{\mathrm{surface}} = \mathbf{B}_{\mathrm{crust}} + \mathbf{B}_{\mathrm{ext}} + \mathbf{B}_{\mathrm{lander}} + \mathbf{B}_{\mathrm{payload}}$).
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

def generate_table2():
    df = pd.read_csv('tables/Table2_database_search_strategies.csv')
    path = OUT_DIR / 'table2_search_strategies.tex'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(r"""\begin{table*}[t]
\caption{Database-specific search strategies, Boolean syntax, and retrieval metrics used in this integrative review (date last searched: 15 October 2026).}\label{tab:search}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}p{2.0cm}p{7.0cm}p{1.6cm}p{1.3cm}p{1.3cm}p{3.0cm}@{}}
\toprule
Database & Exact Search Syntax \& Boolean Filters & Window & Retrieved & Screened & Screening Protocol \\
\midrule
""")
        for _, r in df.iterrows():
            db = tex_escape(r['Database / Repository'])
            syntax = tex_escape(r['Exact Search Syntax & Boolean Operators']).replace('"', "''")
            cov = tex_escape(r['Coverage Window'])
            ret = tex_escape(r['Raw Records Retrieved'])
            scr = tex_escape(r['Screened Records'])
            workflow = tex_escape(r['Screening Workflow'])
            f.write(f"\\raggedright\\scriptsize \\textbf{{{db}}} & \\raggedright\\scriptsize {syntax} & \\raggedright\\scriptsize {cov} & \\raggedright\\scriptsize {ret} & \\raggedright\\scriptsize {scr} & \\raggedright\\scriptsize {workflow} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Systematic evidence identification across 6 indexed databases and public archives following SANRA and PRISMA guidelines. Dual independent screening executed by A.S. and M.D. (Cohen's $\kappa = 0.88$ at title/abstract stage) with consensus adjudication by D.M.P. and R.J.B. Primary English peer-reviewed literature synthesized; historical non-English studies evaluated via authoritative translations/abstracts.
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

def generate_table3():
    df = pd.read_csv('tables/Table3_biology_literature.csv')
    path = OUT_DIR / 'table3_biology_literature.tex'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(r"""\begin{table*}[t]
\caption{Per-study empirical early seedling growth penalties, emergence velocity shifts, and experimental metadata synthesized across representative angiosperms under near-null and hypomagnetic fields.}\label{tab:biology}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}p{2.2cm}p{1.6cm}p{1.6cm}p{2.3cm}p{1.6cm}p{1.1cm}p{1.1cm}p{2.2cm}p{2.4cm}@{}}
\toprule
Species \& Cultivar & Residual $|B|$ & Method & Controls & Milestone & Cap. $\Delta$ & $\Delta t_{50}$ & Biomass / Vigor & Key Source \\
\midrule
""")
        for _, r in df.iterrows():
            sp = tex_escape(r['species'])
            cv = tex_escape(r['cultivar_or_ecotype'])
            res = tex_escape(r['residual_field_seed_plane'])
            meth = tex_escape(r['field_reduction_method'])
            ctrl = tex_escape(r['environmental_controls'])
            ms = tex_escape(r['scored_milestone'])
            cap = tex_escape(r['germination_capacity_delta'])
            dt = tex_escape(r['delta_t50_hours'])
            pen = tex_escape(r['biomass_elongation_penalty'])
            ref = tex_escape(r['key_reference'])
            
            f.write(f"\\raggedright\\scriptsize \\textbf{{{sp}}} ({cv}) & \\raggedright\\scriptsize {res} & \\raggedright\\scriptsize {meth} & \\raggedright\\scriptsize {ctrl} & \\raggedright\\scriptsize {ms} & \\raggedright\\scriptsize {cap} & \\raggedright\\scriptsize {dt} & \\raggedright\\scriptsize {pen} & \\raggedright\\scriptsize {ref} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Developmental Milestones: $M_1$ = Testa rupture and radicle protrusion ($\ge 1$--$2$~mm); $M_2$ = Hypocotyl/coleoptile emergence through substrate surface; $M_3$ = Cotyledon opening, photomorphogenic de-etiolation, and photosynthetic greening. Note: Figure~3b,c represents an illustrative composite schematic parameterized by mean literature values across these datasets rather than a formal meta-analysis.
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

def generate_table4():
    df = pd.read_csv('tables/Table4_flight_decision_matrix.csv')
    path = OUT_DIR / 'table4_decision_matrix.tex'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(r"""\begin{table*}[t]
\caption{Operational phenotypic risk disambiguation matrix for lunar plant biology: distinguishing near-null magnetic field effects from partial gravity and ionizing radiation across developmental tiers and measurement modalities.}\label{tab:matrix}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}p{2.0cm}p{1.1cm}p{1.3cm}p{2.3cm}p{2.3cm}p{2.3cm}p{2.4cm}p{2.4cm}@{}}
\toprule
Stressor & Tier & Window & Primary Cellular Target & Emergence \& Elongation & Pigments \& Bioenergetics & Diagnostic Markers & Flight Modality \& Strategy \\
\midrule
""")
        for _, r in df.iterrows():
            st = tex_escape(r['environmental_stressor'])
            tier = tex_escape(r['evidence_tier'])
            win = tex_escape(r['manifestation_time_window'])
            targ = tex_escape(r['primary_cellular_target'])
            em = tex_escape(r['emergence_kinetics_phenotype']) + ' ' + tex_escape(r['seedling_elongation_morphology'])
            green = tex_escape(r['photosynthetic_greening_pigments']) + ' ' + tex_escape(r['mitochondrial_ros_signature'])
            diag = tex_escape(r['diagnostic_biomarkers'])
            mod = tex_escape(r['measurement_modality_flight_feasibility']) + '. Causal: ' + tex_escape(r['ground_causal_validation'])
            
            f.write(f"\\raggedright\\scriptsize \\textbf{{{st}}} & \\raggedright\\scriptsize {tier} & \\raggedright\\scriptsize {win} & \\raggedright\\scriptsize {targ} & \\raggedright\\scriptsize {em} & \\raggedright\\scriptsize {green} & \\raggedright\\scriptsize {diag} & \\raggedright\\scriptsize {mod} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Methodological framework for resolving confounding environmental factors in lunar surface payloads such as Artemis missions' LEAF. Ground causal validation utilizes orthogonal $45~\upmu$T Helmholtz re-application or 1g centrifugation; flight diagnostic inference utilizes passive triaxial fluxgate logging, dosimeter telemetry, and post-flight returned sample multi-omics.
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

if __name__ == '__main__':
    generate_table1()
    generate_table2()
    generate_table3()
    generate_table4()
