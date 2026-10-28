#!/usr/bin/env python3
"""
scripts/prepare_zenodo.py

Generates MANIFEST.tsv and CHECKSUMS.sha256 for Zenodo deposition.
Computes SHA-256 checksums and file sizes for all tracked, public repository
deliverables in accordance with FAIR and ABAI reproducible science standards.

Usage:
    python3 scripts/prepare_zenodo.py
"""

import os
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    ".abai",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
}

EXCLUDE_FILES = {
    ".DS_Store",
    "MANIFEST.tsv",
    "CHECKSUMS.sha256",
    "_temp_for_docx.md",
}

def get_file_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_description(rel_path: str) -> str:
    p = rel_path
    if p.startswith("manuscript/"):
        if p.endswith(".bib"):
            return "BibTeX library (audited and CrossRef-verified DOIs)"
        elif p.endswith(".md"):
            return "Complete review manuscript text in Markdown format"
    elif p.endswith(".docx"):
        if "Near_Null" in p:
            return "Pandoc-compiled Word submission manuscript with 300 DPI embedded figures"
        elif "LEAF Perspective" in p:
            return "Original working draft manuscript (archive reference)"
    elif p.endswith(".pptx"):
        return "Editable 16:9 widescreen PowerPoint presentation deck with separable subpanels and presenter notes"
    elif p.startswith("presentation/assets/subpanels/"):
        return "Standalone high-resolution (300 DPI) subpanel component for editable figure montages"
    elif p.startswith("figures/"):
        if p.endswith(".png"):
            return "High-resolution (300 DPI) publication raster figure"
        elif p.endswith(".pdf"):
            return "Publication-quality vector PDF figure"
    elif p.startswith("data/"):
        return "Processed empirical CSV dataset supporting figures and analyses"
    elif p.startswith("tables/"):
        return "Manuscript reference table in structured CSV format"
    elif p.startswith("scripts/"):
        return "Reproducible Python analysis, visualization, or QC audit script"
    elif p.startswith("docs/assets/"):
        return "Web display figure asset for GitHub Pages"
    elif p.startswith("docs/cose/"):
        return "Collaborative Science Environment (CoSE) portal asset"
    elif p == "docs/index.html":
        return "Interactive GitHub Pages showcase single-page web portal"
    elif p == "README.md":
        return "Repository documentation and reproduction guide"
    elif p == "LICENSE":
        return "Dual open-access license agreement (CC-BY-4.0 & MIT)"
    elif p == "CITATION.cff":
        return "Citation File Format v1.2.0 metadata"
    elif p == ".zenodo.json":
        return "Zenodo deposit metadata schema"
    elif p == "Makefile":
        return "Automation Makefile for pipeline reproduction"
    elif p == ".gitignore":
        return "Git ignore specifications"
    return "Repository deliverable"

def main():
    records = []
    print(f"Scanning repository at: {REPO_ROOT}")

    for root, dirs, files in os.walk(REPO_ROOT):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in sorted(files):
            if file in EXCLUDE_FILES or file.startswith("~$") or file.endswith(".tmp"):
                continue

            file_path = Path(root) / file
            rel_path = file_path.relative_to(REPO_ROOT).as_posix()

            sha256 = get_file_sha256(file_path)
            size = file_path.stat().st_size
            desc = get_description(rel_path)

            records.append((rel_path, size, sha256, desc))

    records.sort(key=lambda x: x[0])

    manifest_path = REPO_ROOT / "MANIFEST.tsv"
    checksums_path = REPO_ROOT / "CHECKSUMS.sha256"

    # Write MANIFEST.tsv
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("filepath\tsize_bytes\tsha256\tdescription\n")
        for rel_path, size, sha256, desc in records:
            f.write(f"{rel_path}\t{size}\t{sha256}\t{desc}\n")

    # Write CHECKSUMS.sha256 (standard format: `<sha256>  <filepath>`)
    with open(checksums_path, "w", encoding="utf-8") as f:
        for rel_path, size, sha256, desc in records:
            f.write(f"{sha256}  {rel_path}\n")

    total_bytes = sum(r[1] for r in records)
    total_mb = total_bytes / (1024 * 1024)

    print(f"Generated {manifest_path.name} and {checksums_path.name}")
    print(f"Total tracked items: {len(records)}")
    print(f"Total payload size:  {total_mb:.2f} MB ({total_bytes:,} bytes)")

if __name__ == "__main__":
    main()
