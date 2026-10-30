#!/usr/bin/env python3
"""
generate_latex_tables.py
Generates clean, booktabs-formatted LaTeX table fragments in latex/tables/
"""

import pandas as pd
from pathlib import Path

OUT_DIR = Path('latex/tables')
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_table1():
    df = pd.read_csv('tables/Table1_site_magnetic_values.csv')
    path = OUT_DIR / 'table1_sites.tex'
    with open(path, 'w') as f:
        f.write(r"""\begin{table*}[t]
\caption{Crustal magnetic field magnitude and vector components at candidate Artemis landing regions and historical lunar surface landing sites derived from orbital magnetometer models at 30~km altitude.}\label{tab:sites}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}llcccccc@{}}
\toprule
Landing Site / Region & Mission & Lat ($^\circ$N) & Lon ($^\circ$E) & $|B|$ (nT) & $B_r$ (nT) & $B_\theta$ (nT) & $B_\phi$ (nT) \\
\midrule
""")
        for _, r in df.iterrows():
            name = str(r['landing_site']).replace(' (Example Candidate)', '')
            f.write(f"{name} & {r['mission']} & {r['latitude']:.2f} & {r['longitude']:.2f} & {r['b_mag_30km_nt']:.2f} & {r['br_nt']:.2f} & {r['btheta_nt']:.2f} & {r['bphi_nt']:.2f} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Sources: NASA Artemis Candidate Regions (2022, 2024); Hood et al. (2022); Mitchell et al. (2008); Tsunakawa et al. (2015); Purucker \& Nicholas (2010). Coordinates are given in degrees north and east.
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

def generate_table2():
    df = pd.read_csv('tables/Table2_database_search_strategies.csv')
    path = OUT_DIR / 'table2_search_strategies.tex'
    with open(path, 'w') as f:
        f.write(r"""\begin{table*}[t]
\caption{Database-specific search strategies, Boolean syntax, and retrieval metrics used in this integrative review.}\label{tab:search}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}p{2.6cm}p{9.4cm}ccc@{}}
\toprule
Database / Source & Exact Search Syntax \& Boolean Operators & Coverage & Retrieved & Screened \\
\midrule
""")
        for _, r in df.iterrows():
            db = str(r['Database / Repository']).replace('&', r'\&')
            syntax = str(r['Exact Search Syntax & Boolean Operators']).replace('&', r'\&').replace('_', r'\_').replace('"', "''")
            cov = str(r['Coverage Window']).replace('–', '--')
            ret = str(r['Raw Records Retrieved'])
            scr = str(r['Screened Records'])
            f.write(f"{db} & \\raggedright\\footnotesize {syntax} & {cov} & {ret} & {scr} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Systematic evidence identification across 6 indexed databases and public archives following SANRA and PRISMA guidelines.
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

def generate_table3():
    df = pd.read_csv('tables/Table3_biology_literature.csv')
    path = OUT_DIR / 'table3_biology_literature.tex'
    with open(path, 'w') as f:
        f.write(r"""\begin{table*}[t]
\caption{Empirical biological penalties, developmental phenotypes, and molecular mechanisms documented in near-null magnetic fields across plant and cellular systems.}\label{tab:biology}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}p{2.8cm}p{2.2cm}p{3.8cm}p{4.2cm}p{1.2cm}p{2.4cm}@{}}
\toprule
Organism & Field Regime & Biological Phenotype & Proposed Mechanism & Tier & Key Source \\
\midrule
""")
        for _, r in df.iterrows():
            org = str(r['organism']).replace('&', r'\&')
            cond = str(r['condition']).replace('<', '$<$').replace('~', r'$\sim$').replace('uT', r'$\upmu$T')
            eff = str(r['biological_effect']).replace('&', r'\&').replace('–', '--')
            mech = str(r['molecular_mechanism']).replace('&', r'\&').replace('–', '--').replace('+', '$^+$')
            tier = str(r['evidence_tier'])
            ref = str(r['key_reference']).replace('&', r'\&')
            f.write(f"\\raggedright\\footnotesize {org} & \\raggedright\\footnotesize {cond} & \\raggedright\\footnotesize {eff} & \\raggedright\\footnotesize {mech} & \\footnotesize {tier} & \\raggedright\\footnotesize {ref} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Evidentiary hierarchy: Tier 1 (Demonstrated field effect on target biomolecule), Tier 2 (Demonstrated in pathway/cellular phenotype), Tier 3 (Physically plausible quantum/spin hypothesis).
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

def generate_table4():
    df = pd.read_csv('tables/Table4_flight_decision_matrix.csv')
    path = OUT_DIR / 'table4_decision_matrix.tex'
    with open(path, 'w') as f:
        f.write(r"""\begin{table*}[t]
\caption{Phenotypic risk disambiguation matrix for lunar spaceflight plant biology: distinguishing near-null magnetic field effects from partial gravity and ionizing radiation confounders.}\label{tab:matrix}
\begin{tabular*}{\textwidth}{@{\extracolsep\fill}p{2.4cm}p{2.8cm}p{3.0cm}p{3.0cm}p{2.6cm}p{3.0cm}@{}}
\toprule
Stressor & Cellular Target & Emergence & Greening / Pigments & Diagnostic Markers & Disambiguation Strategy \\
\midrule
""")
        for _, r in df.iterrows():
            st = str(r['environmental_stressor']).replace('&', r'\&').replace('<', '$<$')
            targ = str(r['primary_cellular_target']).replace('&', r'\&').replace('•-', r'$^{\bullet -}$').replace('•+', r'$^{\bullet +}$')
            em = str(r['emergence_kinetics_phenotype']).replace('&', r'\&').replace('Δ', r'$\Delta$').replace('t50', r'$t_{50}$').replace('%', r'\%')
            green = str(r['photosynthetic_greening_pigments']).replace('&', r'\&').replace('–', '--')
            diag = str(r['diagnostic_biomarkers']).replace('&', r'\&').replace('gamma-H2AX', r'$\gamma$-H2AX')
            strat = str(r['ground_flight_disambiguation_strategy']).replace('&', r'\&').replace('µT', r'$\upmu$T')
            f.write(f"\\raggedright\\scriptsize \\textbf{{{st}}} & \\raggedright\\scriptsize {targ} & \\raggedright\\scriptsize {em} & \\raggedright\\scriptsize {green} & \\raggedright\\scriptsize {diag} & \\raggedright\\scriptsize {strat} \\\\\n")
        f.write(r"""\bottomrule
\end{tabular*}
\begin{tablenotes}
\item Methodological framework for resolving confounding environmental factors in lunar surface payloads such as Artemis missions' LEAF.
\end{tablenotes}
\end{table*}
""")
    print(f"Generated {path}")

if __name__ == '__main__':
    generate_table1()
    generate_table2()
    generate_table3()
    generate_table4()
