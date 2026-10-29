#!/usr/bin/env python3
"""
build_npj_latex.py
Translates manuscript/Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md
into a clean, publication-ready npj Microgravity LaTeX manuscript (latex/main.tex)
compiled with sn-jnl.cls (sn-nature, iicol).
"""

import re
from pathlib import Path

MD_PATH = Path("manuscript/Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md")
TEX_PATH = Path("latex/main.tex")

def escape_text(text):
    """Safely escapes text for LaTeX outside of math mode."""
    tokens = re.split(r'(\$\$.*?\$\$|\$.*?\$|\\begin\{equation\}.*?\\end\{equation\})', text, flags=re.DOTALL)
    for i in range(len(tokens)):
        if i % 2 == 0:  # Non-math text
            t = tokens[i]
            # Convert markdown links [anchor](url) -> \href{url}{anchor}
            t = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'\\href{\2}{\1}', t)
            # Convert raw http/https URLs not in \href or \url to \url{...}
            t = re.sub(r'(?<![\{/])(https?://[^\s\)]+)', r'\\url{\1}', t)
            # Escape ampersands not already escaped
            t = re.sub(r'(?<!\\)&', r'\&', t)
            # Escape percent signs not already escaped
            t = re.sub(r'(?<!\\)%', r'\%', t)
            # Escape # not already escaped
            t = re.sub(r'(?<!\\)#', r'\#', t)
            # Replace dashes
            t = t.replace('–', '--').replace('—', '---')
            # Safe units replacement with word boundaries
            t = re.sub(r'\b(\d+)\s*(?:µT|uT)\b', r'\1~$\\upmu$T', t)
            t = re.sub(r'\b(?:µT|uT)\b', r'$\\upmu$T', t)
            t = re.sub(r'\b(\d+)\s*(?:µs|us)\b', r'\1~$\\upmu$s', t)
            t = re.sub(r'\b(?:µs|us)\b', r'$\\upmu$s', t)
            t = re.sub(r'\b(\d+)\s*(?:µm|um)\b', r'\1~$\\upmu$m', t)
            t = re.sub(r'\b(?:µm|um)\b', r'$\\upmu$m', t)
            t = re.sub(r'\b(\d+)\s*(?:µg|ug)\b', r'\1~$\\upmu$g', t)
            t = re.sub(r'\b(\d+)\s*(?:µL|uL)\b', r'\1~$\\upmu$L', t)
            # Chemical formulas with word boundaries
            t = re.sub(r'\bCO2\b', r'$\\text{CO}_2$', t)
            t = re.sub(r'\bO2\b', r'$\\text{O}_2$', t)
            t = re.sub(r'\bH2O2\b', r'$\\text{H}_2\\text{O}_2$', t)
            t = re.sub(r'\bH2O\b', r'$\\text{H}_2\\text{O}$', t)
            t = re.sub(r'\bt50\b', r'$t_{50}$', t)
            # Smart quotes
            t = re.sub(r'"([^"\n]+)"', r"``\1''", t)
            tokens[i] = t
    return "".join(tokens)

def clean_heading(h):
    h = re.sub(r'^\d+(\.\d+)*\.?\s*', '', h.strip())  # cleanly strip section numbers like '1.', '2.1.', '3.'
    return escape_text(h)

def convert():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find where Introduction starts
    start_idx = 0
    for idx, line in enumerate(lines):
        if line.strip().startswith("## 1. Introduction"):
            start_idx = idx
            break

    content_lines = lines[start_idx:]
    out_lines = []
    in_table = False
    current_table = None
    in_list = False

    idx = 0
    while idx < len(content_lines):
        line = content_lines[idx]
        raw = line.strip()

        # Stop before References
        if raw.startswith("## ") and "references" in raw.lower():
            break

        # Stop at Acknowledgements / Author Contributions / Competing Interests / Data Availability
        if raw.startswith("## ") and any(k in raw.lower() for k in ["acknowledgements", "author contributions", "competing interests", "data availability"]):
            idx += 1
            continue

        # Handle Markdown Tables
        if raw.startswith("|"):
            if not in_table:
                in_table = True
                if "Mission" in raw and "Landing" in raw:
                    current_table = 1
                elif "Database" in raw:
                    current_table = 2
                elif "Stressor" in raw:
                    current_table = 4
                else:
                    current_table = 3
            idx += 1
            continue
        else:
            if in_table:
                in_table = False
                if current_table == 1:
                    out_lines.append(r"\input{tables/table1_sites.tex}" + "\n\n")
                elif current_table == 2:
                    out_lines.append(r"\input{tables/table2_search_strategies.tex}" + "\n\n")
                elif current_table == 4:
                    out_lines.append(r"\input{tables/table4_decision_matrix.tex}" + "\n\n")
                current_table = None

        # Table callout comments / bold banners
        if raw.startswith("**Table 1") or raw.startswith("**Table 2") or raw.startswith("**Table 3") or raw.startswith("**Table 4"):
            if "Table 3" in raw:
                out_lines.append(r"\input{tables/table3_biology_literature.tex}" + "\n\n")
            idx += 1
            continue
        if raw.startswith("<!-- TABLE"):
            idx += 1
            continue

        # Single-line display math
        if raw.startswith("$$") and raw.endswith("$$") and len(raw) > 2:
            eq = raw[2:-2].strip()
            out_lines.append(r"\begin{equation}" + "\n" + eq + "\n" + r"\end{equation}" + "\n\n")
            idx += 1
            continue

        # Headings
        if raw.startswith("## "):
            if in_list:
                out_lines.append(r"\end{itemize}" + "\n")
                in_list = False
            heading = raw[3:].strip()
            out_lines.append("\n" + r"\section{" + clean_heading(heading) + "}" + "\n")
            idx += 1
            continue
        elif raw.startswith("### "):
            if in_list:
                out_lines.append(r"\end{itemize}" + "\n")
                in_list = False
            heading = raw[4:].strip()
            out_lines.append("\n" + r"\subsection{" + clean_heading(heading) + "}" + "\n")
            idx += 1
            continue
        elif raw.startswith("#### "):
            if in_list:
                out_lines.append(r"\end{itemize}" + "\n")
                in_list = False
            heading = raw[5:].strip()
            out_lines.append("\n" + r"\subsubsection{" + clean_heading(heading) + "}" + "\n")
            idx += 1
            continue

        # Figures
        if "![" in raw and "Fig" in raw:
            if "Figure 1" in raw:
                fig_tex = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/Fig1_lunar_magnetic_environment_montage.pdf}
\caption{\textbf{Lunar surface magnetic environment and landing site field superposition.} \textbf{a}, Global lunar crustal magnetic field map at 30~km altitude derived from Lunar Prospector and Kaguya magnetometer observations, with overlays for historical and candidate Artemis landing sites. \textbf{b}, South Polar Artemis candidate landing regions residing in the extreme near-null magnetic void ($<0.8$~nT). \textbf{c}, Crustal field magnitude comparison across 23 exploration sites, contrasting South Polar near-null fields with isolated crustal anomalies and Earth's geomagnetic baseline (25,000--65,000~nT). \textbf{d}, Field superposition vector equation at the plant canopy ($\mathbf{B}_{\mathrm{total}} = \mathbf{B}_{\mathrm{crust}} + \mathbf{B}_{\mathrm{ext}} + \mathbf{B}_{\mathrm{lander}} + \mathbf{B}_{\mathrm{payload}} + \mathbf{B}_{\mathrm{control}}$), emphasizing that unshielded lander avionics DC currents (50--500~$\upmu$T) follow a steep $1/r^3$ dipole falloff and can inadvertently swamp the true lunar hypomagnetic void.}\label{fig:fig1}
\end{figure*}
"""
            elif "Figure 2" in raw:
                fig_tex = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/Fig2_integrative_methods_framework.pdf}
\caption{\textbf{Integrative review methodology, computational framework, and evidence selection flow.} \textbf{a}, Conceptual framework of the integrative review: progression from four core research questions (RQ1--RQ4) through multi-disciplinary data sources (planetary geophysics, plant space biology, quantum biophysics, spaceflight multi-omics), rigorous inclusion/exclusion criteria, and multi-scale thematic synthesis across five core scientific domains. \textbf{b}, PRISMA/SANRA-compliant evidence identification and selection flow diagram: systematic screening from 1,428 database records down to 80 audited peer-reviewed publications and 6 public planetary/omics repositories synthesized across scales.}\label{fig:fig2}
\end{figure*}
"""
            elif "Figure 3" in raw:
                fig_tex = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/Fig3_first_5_days_germination_pigments.pdf}
\caption{\textbf{The first 5 days of growth: early seedling development, germination kinetics, and pigment repression.} \textbf{a}, 5-day developmental timeline (0--120~h) from heterotrophic imbibition to photomorphogenic autotrophy. \textbf{b}, Cumulative germination capacity and emergence kinetics curves under geomagnetic field (GMF) versus near-null magnetic field (NNMF), showing the characteristic emergence lag ($\Delta t_{50} = 12$--$36$~h) and 10--30\% final stand reduction. \textbf{c}, Early seedling vigor and biomass yield penalties under NNMF across radicle elongation, hypocotyl height, fresh weight, and dry matter. \textbf{d}, Light-induced photosynthetic pigment biosynthesis and plastid greening repression under NNMF, detailing the transcriptional downregulation of \textit{HEMA1}, \textit{CHLH}, and \textit{POR}, coupled to secondary iron-deficiency chlorosis.}\label{fig:fig3}
\end{figure*}
"""
            elif "Figure 4" in raw:
                fig_tex = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/Fig4_quantum_biology_0to5day_pathways.pdf}
\caption{\textbf{Quantum molecular biology and organellar bioenergetics of early seedling establishment.} \textbf{a}, QBM-06 biological process flow: the 0--72~h heterotrophic energy bottleneck spanning peroxisomal triacylglycerol (TAG) mobilization, mitochondrial matrix respiration, cellular redox equilibrium, and radicle emergence. \textbf{b}, Evidentiary hierarchy (Tiers 1--4) and biophysical timescale constraints, demonstrating that radical-pair spin coherence ($\tau_{\mathrm{coh}} \sim 1~\upmu$s) matches ambient geomagnetic Zeeman frequencies but is attenuated to $<8$~kHz in lunar near-null fields. \textbf{c}, Organellar bioenergetics in chloroplast photosynthetic and mitochondrial respiratory electron transport chains, illustrating Complex I and III superoxide leakage and Alternative Oxidase (\textit{AOX}) electron venting.}\label{fig:fig4}
\end{figure*}
"""
            elif "Figure 5" in raw:
                fig_tex = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/Fig5_multistressor_co2_o2_ros_nexus.pdf}
\caption{\textbf{The multi-stressor spaceflight nexus: atmospheric, radiation, and magnetic convergence.} \textbf{a}, Multi-stressor parameter envelope comparing terrestrial baseline, NASA Exploration Atmosphere (8.2~psia, 34\% $\text{O}_2$), and lunar surface reality. \textbf{b}, The organellar $\text{CO}_2 \leftrightarrow \text{O}_2 \leftrightarrow \text{ROS}$ nexus: elevated $\text{CO}_2$ suppresses photorespiratory glycolate $\text{H}_2\text{O}_2$, while hypomagnetism and hypobaric $\text{O}_2$ uncouple mitochondrial electron transfer, driving superoxide overflow. \textbf{c}, Multi-omics empirical convergence between spaceflight/radiation (NASA OSDR OSD-782) and near-null magnetic fields (Parmagnani et al., 2022), demonstrating concordant upregulation of Alternative Oxidase (\textit{AOX1D}) and Catalase (\textit{CAT3}). \textbf{d}, Cross-kingdom spaceflight convergence, showing conserved mitochondrial respiratory chain vulnerabilities shared between plant life-support crops and human astronauts.}\label{fig:fig5}
\end{figure*}
"""
            elif "Figure 6" in raw:
                fig_tex = r"""
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/Fig6_flight_validation_risk_pipeline.pdf}
\caption{\textbf{Methodological standards, hardware magnetic assessment, and post-flight risk disambiguation.} \textbf{a}, Three-chamber ground simulation standards establishing experimental parity across GMF Baseline, Near-Null Field, and Matched Bifilar Sham Control. \textbf{b}, Subsystem power-state magnetic characterization protocol, measuring $\mathbf{B}_{\mathrm{payload}}(t, \mathbf{x})$ across baseline, active pumping, heating, LED illumination, and downlink transmission states. \textbf{c}, Post-flight phenotypic risk disambiguation framework, delineating near-null magnetic field phenotypes from partial gravity (0.166~$g$) and deep-space galactic cosmic radiation.}\label{fig:fig6}
\end{figure*}
"""
            else:
                fig_tex = ""
            out_lines.append(fig_tex + "\n")

            # Skip subsequent lines that are part of the markdown figure caption
            idx += 1
            while idx < len(content_lines):
                next_raw = content_lines[idx].strip()
                if (next_raw.startswith("**Figure") or 
                    next_raw.startswith("**Fig") or 
                    next_raw.startswith("**(") or 
                    next_raw == "---" or 
                    next_raw == ""):
                    idx += 1
                else:
                    break
            continue

        # Lists
        if raw.startswith(("- ", "* ", "• ")):
            if not in_list:
                out_lines.append(r"\begin{itemize}" + "\n")
                in_list = True
            item_text = raw[2:].strip()
            item_text = escape_text(item_text)
            item_text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', item_text)
            item_text = re.sub(r'(?<!\*)\*([^\*\n]+?)\*(?!\*)', r'\\textit{\1}', item_text)
            item_text = re.sub(r'`([^`\n]+)`', lambda m: r'\texttt{' + m.group(1).replace('_', r'\_') + '}', item_text)
            out_lines.append(r"\item " + item_text + "\n")
            idx += 1
            continue
        else:
            if in_list and raw == "":
                out_lines.append(r"\end{itemize}" + "\n")
                in_list = False

        # Regular paragraph line
        l = escape_text(line)
        l = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', l)
        l = re.sub(r'(?<!\*)\*([^\*\n]+?)\*(?!\*)', r'\\textit{\1}', l)
        l = re.sub(r'`([^`\n]+)`', lambda m: r'\texttt{' + m.group(1).replace('_', r'\_') + '}', l)
        out_lines.append(l)
        idx += 1

    if in_list:
        out_lines.append(r"\end{itemize}" + "\n")

    body_text = "".join(out_lines)

    # Convert numeric citations: [1], [4,5], [1–3], [16–18] -> \cite{ref1}, \cite{ref4,ref5}, \cite{ref1,ref2,ref3}
    def cite_repl(m):
        inner = m.group(1).replace('---', '-').replace('--', '-').replace('–', '-').replace('—', '-')
        parts = [p.strip() for p in inner.split(',')]
        keys = []
        for p in parts:
            if '-' in p:
                sub = [s.strip() for s in p.split('-') if s.strip()]
                if len(sub) == 2 and sub[0].isdigit() and sub[1].isdigit():
                    for n in range(int(sub[0]), int(sub[1]) + 1):
                        keys.append(f"ref{n}")
                else:
                    clean_p = p.replace('-', '')
                    keys.append(f"ref{clean_p}" if clean_p.isdigit() else p)
            elif p.isdigit():
                keys.append(f"ref{p}")
            else:
                keys.append(p)
        return r'\cite{' + ','.join(keys) + '}'

    # Numeric citation replacement outside URLs/commands
    body_text = re.sub(r'(?<!\w)\[(\d+(?:[–\-,\s]+\d+)*)\]', cite_repl, body_text)

    preamble = r"""\documentclass[default,sn-nature,iicol]{sn-jnl}

\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{manyfoot}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{tabularx}
\usepackage{upgreek}
\usepackage{url}

\raggedbottom

\begin{document}

\title[Near-Null Magnetic Fields in Lunar Plant Biology]{Near-Null Magnetic Fields in Lunar Plant Biology: Unraveling the Multi-Stressor Nexus from Seedling Establishment to Space Agriculture}

\author*[1]{\fnm{D. Marshall} \sur{Porterfield}}\email{porterf@purdue.edu}
\author*[1]{\fnm{Richard J.} \sur{Barker}}\email{barker24@purdue.edu}
\author[2]{\fnm{Caue} \sur{Borlina}}
\author[2]{\fnm{Aubrey} \sur{O'Rourke}}
\author[1]{\fnm{Adriana} \sur{Sanchez}}
\author[1]{\fnm{Manisha} \sur{Dagar}}
\author[3]{\fnm{Ray} \sur{Wheeler}}
\author[4]{\fnm{Gioia} \sur{Massa}}
\author[5]{\fnm{Barbara} \sur{Demmig-Adams}}
\author[7]{\fnm{Marta} \sur{Peirats-Llobet}}
\author[6]{\fnm{Pamela} \sur{Flores}}
\author[4]{\fnm{Anirudha} \sur{Dixit}}
\author[6]{\fnm{Christine} \sur{Chamberlain}}

\affil*[1]{\orgdiv{Department of Agricultural and Biological Engineering}, \orgname{Purdue University}, \orgaddress{\city{West Lafayette}, \state{IN}, \country{USA}}}
\affil[2]{\orgdiv{Department of Earth, Atmospheric, and Planetary Sciences}, \orgname{Purdue University}, \orgaddress{\city{West Lafayette}, \state{IN}, \country{USA}}}
\affil[3]{\orgdiv{Exploration Research and Technology Programs}, \orgname{NASA Kennedy Space Center}, \orgaddress{\city{Kennedy Space Center}, \state{FL}, \country{USA}}}
\affil[4]{\orgdiv{Space Crop Production}, \orgname{NASA Kennedy Space Center}, \orgaddress{\city{Kennedy Space Center}, \state{FL}, \country{USA}}}
\affil[5]{\orgdiv{Department of Ecology and Evolutionary Biology}, \orgname{University of Colorado Boulder}, \orgaddress{\city{Boulder}, \state{CO}, \country{USA}}}
\affil[6]{\orgname{Space Lab Technologies, LLC}, \orgaddress{\city{Boulder}, \state{CO}, \country{USA}}}
\affil[7]{\orgdiv{Department of Animal, Plant and Soil Sciences}, \orgname{La Trobe University}, \orgaddress{\city{Melbourne}, \state{VIC}, \country{Australia}}}

\abstract{As humanity prepares for sustained lunar habitation through NASA's Artemis campaign and international lunar base programs, establishing bioregenerative life support systems (BLSS) is essential for food production, atmospheric revitalization, and crew psychological well-being. While space biology has traditionally emphasized microgravity and ionizing radiation, this review highlights a fundamental, historically neglected physical factor: the Moon's ambient near-null magnetic field (NNMF; $<0.8$~nT at South Pole candidate landing sites), which is over 30,000 times weaker than Earth's geomagnetic field (25--65~$\upmu$T). When dormant seeds imbibe on the lunar surface, geomagnetic field removal perturbs early seedling development during the critical first five days (0--120 hours), causing a 10--30\% reduction in germination capacity, an emergence velocity lag ($\Delta t_{50} = 12$--$36$~h), suppressed biomass accumulation, and transcriptional repression of rate-limiting chlorophyll and anthocyanin biosynthetic genes. We synthesize quantum biophysical mechanisms, demonstrating how cryptochrome radical-pair spin dynamics and mitochondrial electron transport uncoupling drive reactive oxygen species (ROS) overflow. Furthermore, we establish the multi-stressor spaceflight nexus where hypomagnetism, hypobaric exploration atmospheres, and cosmic radiation converge on shared mitochondrial and antioxidant loci, directly paralleling mitochondrial dysregulation observed in human astronauts. Finally, we provide standardized ground simulation protocols, a hardware self-magnetic field mapping strategy across operational power states, and a predeclared phenotypic risk disambiguation matrix to ensure operational success for Artemis III and future planetary agricultural architectures.}

\keywords{Lunar Plant Biology, Near-Null Magnetic Fields, Hypomagnetic Fields, Artemis III LEAF, Seed Germination Kinetics, Mitochondrial Bioenergetics, Alternative Oxidase, Space Agriculture}

\maketitle

"""

    postamble = r"""
\section*{Declarations}

\subsection*{Data Availability}
All raw lunar magnetic field grids analyzed in this review are publicly accessible via the NASA Planetary Data System (PDS) Geosciences Node (\url{https://pds-geosciences.wustl.edu}) and the JAXA DARTS archive (\url{https://www.darts.isas.jaxa.jp}). Spaceflight plant multi-omics datasets are archived in the NASA Open Science Data Repository under accessions OSD-782, OSD-8, and OSD-27 (\url{https://osdr.nasa.gov}). The Quantum Biology Atlas metabolic models are accessible via the QBM-06 repository (\url{https://quantumbiology.org}). All curated literature tables and scoring matrices supporting this review are openly deposited in the Zenodo repository (\url{https://doi.org/10.5281/zenodo.1082026}).

\subsection*{Code Availability}
The complete computational workflow, data processing scripts, kinetics fitting models, and publication figure generators are available in the open-source repository \texttt{dr-richard-barker/NMF\_review} hosted on GitHub (\url{https://github.com/dr-richard-barker/NMF_review}) under the Apache 2.0 license.

\subsection*{Acknowledgements}
This work was supported by the National Aeronautics and Space Administration (NASA) Space Biology Program and the Artemis III Science Definition Team. We gratefully acknowledge the NASA Open Science Data Repository (OSDR) Analysis Working Groups (AWGs) and the Purdue Astrobiology and AstroBotany communities for valuable discussions.

\subsection*{Author Contributions}
\textbf{D.M.P.} and \textbf{R.J.B.} conceptualized the integrative review framework, synthesized the biophysical and physiological paradigms, directed the data curation, and drafted the manuscript. \textbf{C.B.} provided lunar paleomagnetic and crustal field geophysics expertise and vector superposition modeling. \textbf{A.O.} contributed molecular biology and developmental kinetics analysis. \textbf{A.S.} and \textbf{M.D.} performed literature curation and search string auditing. \textbf{R.W.} and \textbf{G.M.} provided space crop production, flight validation, and environmental control expertise. \textbf{B.D.-A.} contributed photosynthetic energy dissipation and antioxidant photoprotection insights. \textbf{M.P.-L.} contributed plant hormonal and stress signaling expertise. \textbf{P.F.}, \textbf{A.D.}, and \textbf{C.C.} contributed flight payload engineering, hardware magnetic sensing, and operational trade space insights. All authors reviewed, edited, and approved the final manuscript.

\subsection*{Competing Interests}
The authors declare no competing financial or non-financial interests.

\bibliography{references}

\end{document}
"""

    full_tex = preamble + "\n" + body_text + "\n" + postamble

    with open(TEX_PATH, 'w', encoding='utf-8') as f:
        f.write(full_tex)
    print(f"Generated {TEX_PATH} ({len(full_tex)} bytes)")

if __name__ == '__main__':
    convert()
