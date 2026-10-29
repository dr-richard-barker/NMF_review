#!/usr/bin/env python3
"""
build_complete_bibtex.py
Parses the 83 references from manuscript/Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md
and produces latex/references.bib with keys ref1, ref2, ..., ref83.
"""

import re
from pathlib import Path

MD_PATH = Path("manuscript/Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md")
BIB_PATH = Path("latex/references.bib")

def clean_latex_accents(s):
    if not s:
        return s
    replacements = {
        'Ł': r'{\L}',
        'ł': r'{\l}',
        'ś': r"{\'s}",
        'Ś': r"{\'S}",
        'ü': r'{\"u}',
        'Ü': r'{\"U}',
        'ö': r'{\"o}',
        'Ö': r'{\"O}',
        'ä': r'{\"a}',
        'Ä': r'{\"A}',
        '—': '---',
        '–': '--',
        '’': "'",
        '‘': "'",
        '“': "``",
        '”': "''",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s

def parse_ref_line(line):
    # Example:
    # 50. Solov’yov, I. A., Chandler, D. E. & Schulten, K. Magnetic field effects in *Arabidopsis thaliana* cryptochrome-1. *Biophys. J.* **92**, 2711–2726 (2007). https://doi.org/10.1529/biophysj.106.097139
    m = re.match(r'^(\d+)\.\s+(.*)', line)
    if not m:
        return None
    ref_num = int(m.group(1))
    text = m.group(2).strip()

    # Extract URL / DOI if present
    doi = None
    url = None
    url_m = re.search(r'https?://[^\s]+', text)
    if url_m:
        raw_url = url_m.group(0).rstrip('.')
        if 'doi.org/' in raw_url:
            doi = raw_url.split('doi.org/')[-1]
        else:
            url = raw_url
        text = text[:url_m.start()].strip().rstrip('.')

    # Extract Year from (YYYY) or (26 March 2024)
    year_m = re.search(r'\(.*?(\d{4})[a-z]?\)', text)
    year = year_m.group(1) if year_m else "2026"
    if year_m:
        text = text[:year_m.start()].strip().rstrip('.')

    # Extract Volume and Pages if present
    vol = None
    pages = None
    vol_m = re.search(r'\*\*([^*]+)\*\*,\s*([0-9–\-a-zA-Z]+)', text)
    if vol_m:
        vol = vol_m.group(1)
        pages = vol_m.group(2).replace('–', '--')
        text = text[:vol_m.start()].strip().rstrip('.')
    else:
        vol_only_m = re.search(r'\*\*([^*]+)\*\*', text)
        if vol_only_m:
            vol = vol_only_m.group(1)
            text = text[:vol_only_m.start()].strip().rstrip('.')

    # Extract Journal from *...* at the end of the text
    journal = None
    j_m = re.search(r'\*([^*]+)\*\s*(?=\*\*[0-9]+|\([0-9]{4}\)|,\s*pp|\(ed|\(in press|\(26|,\s*ICES)', text)
    if not j_m:
        j_m = re.search(r'\*([^*]+)\*$', text)
    if j_m:
        journal = j_m.group(1).replace('*', '').strip()
        pre_j = text[:j_m.start()].strip().rstrip('.')
    else:
        pre_j = text

    # Remaining text in pre_j contains Authors and Title
    if ' et al.' in pre_j:
        idx = pre_j.find(' et al.') + len(' et al.')
        authors = pre_j[:idx].strip()
        title = pre_j[idx:].strip().lstrip('.').strip()
    else:
        splits = list(re.finditer(r'\.\s+(?=([A-Z][a-z]|[A-Z]{2,}))', pre_j))
        if splits:
            if ' & ' in pre_j:
                amp_idx = pre_j.rfind(' & ')
                valid_splits = [s for s in splits if s.start() > amp_idx]
                split_pt = valid_splits[0] if valid_splits else splits[-1]
            elif ' and ' in pre_j:
                and_idx = pre_j.rfind(' and ')
                valid_splits = [s for s in splits if s.start() > and_idx]
                split_pt = valid_splits[0] if valid_splits else splits[-1]
            else:
                split_pt = splits[0]

            authors = pre_j[:split_pt.start()+1].strip().rstrip('.')
            title = pre_j[split_pt.end():].strip().lstrip('.').strip()
        else:
            authors = pre_j
            title = "Near-Null Magnetic Fields in Lunar Plant Biology"

    # Clean authors for BibTeX:
    # Multiple authors must be separated by ' and ', NOT commas.
    authors = authors.replace(' & ', ' and ').replace(' et al.', ' and others')
    authors = re.sub(r'\.,\s+', '. and ', authors)
    authors = clean_latex_accents(authors)

    # Clean title (preserve LaTeX math like $bc_1$)
    title = clean_latex_accents(title.replace('*', '').strip().rstrip('.'))
    if journal:
        journal = clean_latex_accents(journal)

    key = f"ref{ref_num}"
    
    if journal:
        bib = f"@article{{{key},\n"
        bib += f"  author = {{{authors}}},\n"
        bib += f"  title = {{{{{title}}}}},\n"
        bib += f"  journal = {{{journal}}},\n"
        if vol:
            bib += f"  volume = {{{vol}}},\n"
        if pages:
            bib += f"  pages = {{{pages}}},\n"
        bib += f"  year = {{{year}}},\n"
        if doi:
            bib += f"  doi = {{{doi}}},\n"
        if url:
            bib += f"  url = {{{url}}},\n"
        bib += "}\n"
    else:
        bib = f"@misc{{{key},\n"
        bib += f"  author = {{{authors}}},\n"
        bib += f"  title = {{{{{title}}}}},\n"
        bib += f"  year = {{{year}}},\n"
        if url:
            bib += f"  url = {{{url}}},\n"
        bib += "}\n"

    return ref_num, bib

def build():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    recording = False
    entries = []
    for line in lines:
        if line.strip().startswith("## References"):
            recording = True
            continue
        if recording:
            l = line.strip()
            if l and l[0].isdigit() and '. ' in l[:5]:
                res = parse_ref_line(l)
                if res:
                    entries.append(res)

    entries.sort(key=lambda x: x[0])
    with open(BIB_PATH, 'w', encoding='utf-8') as f:
        for num, bib in entries:
            f.write(bib + "\n")
    print(f"Successfully generated {BIB_PATH} with {len(entries)} BibTeX entries!")

if __name__ == '__main__':
    build()
