#!/usr/bin/env python3
"""
build_lssr_docx.py

Builds the final publication-ready Microsoft Word document (.docx)
for Life Sciences in Space Research from the master markdown manuscript
and embeds all high-resolution figures.
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path('/Users/drb_laptop/Documents/NMF_review')
MD_FILE = BASE_DIR / 'manuscript' / 'Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md'
OUT_DOCX = BASE_DIR / 'Near_Null_Magnetic_Fields_Lunar_Plant_Biology_LSSR_Review.docx'

def main():
    print(f"Reading manuscript from {MD_FILE}...")
    content = MD_FILE.read_text(encoding='utf-8')
    
    # Replace file:// URI with absolute filesystem paths so pandoc embeds the images
    content_clean = content.replace('file:///Users/drb_laptop/Documents/NMF_review/figures/', 
                                    '/Users/drb_laptop/Documents/NMF_review/figures/')
    
    tmp_md = BASE_DIR / 'manuscript' / '_temp_for_docx.md'
    tmp_md.write_text(content_clean, encoding='utf-8')
    
    cmd = [
        '/opt/homebrew/bin/pandoc',
        str(tmp_md),
        '-o', str(OUT_DOCX),
        '--toc',
        '--toc-depth=2'
    ]
    
    print(f"Running pandoc to create {OUT_DOCX}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if tmp_md.exists():
        tmp_md.unlink()
        
    if res.returncode == 0 and OUT_DOCX.exists():
        size_mb = OUT_DOCX.stat().st_size / (1024 * 1024)
        print(f"SUCCESS: Generated {OUT_DOCX} ({size_mb:.2f} MB)")
    else:
        print(f"ERROR: Pandoc failed with return code {res.returncode}")
        print("STDERR:", res.stderr)
        print("STDOUT:", res.stdout)

if __name__ == '__main__':
    main()
