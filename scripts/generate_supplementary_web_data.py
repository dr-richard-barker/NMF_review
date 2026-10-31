#!/usr/bin/env python3
"""
generate_supplementary_web_data.py
Sanitizes Table S1 (80 papers) and Table S2 (6 datasets) from manuscript and bib sources,
outputs clean CSVs to tables/ and docs/assets/, and produces docs/cose/supplementary-tables.js
with embedded JSON datasets and interactive client-side logic.
"""

import re
import csv
import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MD_PATH = BASE_DIR / "manuscript" / "Hypomagnetic_Lunar_Plant_Biology_LSSR_Review.md"
RAW_S1_CSV = BASE_DIR / "tables" / "Table_S1_literature_corpus.csv"
OUT_S1_CSV = BASE_DIR / "tables" / "Table_S1_literature_corpus.csv"
DOCS_ASSETS_S1 = BASE_DIR / "docs" / "assets" / "Table_S1_literature_corpus.csv"
S2_CSV = BASE_DIR / "tables" / "Table_S2_public_datasets.csv"
DOCS_ASSETS_S2 = BASE_DIR / "docs" / "assets" / "Table_S2_public_datasets.csv"
OUT_JS = BASE_DIR / "docs" / "cose" / "supplementary-tables.js"

CATEGORIES = [
    "Hypomagnetic Biology & Quantum Biophysics",
    "Plant Growth & Photomorphogenesis",
    "Spaceflight Plant Physiology & BLSS",
    "Mitochondrial Bioenergetics & Cellular Stress",
    "Planetary Magnetism & Exploration Environment",
    "Space Radiation & Multi-Stressor Synergy"
]

def load_categories_map():
    cat_map = {}
    if RAW_S1_CSV.exists():
        with open(RAW_S1_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row:
                    continue
                ref_id = row[0].strip()
                for c in row:
                    c_clean = c.strip()
                    if c_clean in CATEGORIES:
                        cat_map[ref_id] = c_clean
                        break
    return cat_map

def parse_markdown_references():
    cat_map = load_categories_map()
    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_refs = False
    records = []

    for line in lines:
        if line.strip().startswith("## References"):
            in_refs = True
            continue
        if not in_refs:
            continue
        l = line.strip()
        if not l:
            continue
        m = re.match(r"^(\d+)\.\s+(.*)", l)
        if not m:
            continue
        num = int(m.group(1))
        if num > 80:
            continue  # Corpus comprises 80 papers (Table S1)

        raw_line = m.group(2).strip()

        # Extract URL or DOI
        url_m = re.search(r"https?://[^\s]+", raw_line)
        url = url_m.group(0).rstrip(".") if url_m else ""
        
        # Remove URL from raw text
        if url_m:
            text = raw_line[:url_m.start()] + raw_line[url_m.end():]
        else:
            text = raw_line

        text = re.sub(r"\s+", " ", text).strip().rstrip(".")

        # Extract trailing journal / volume / year
        # Matches: . *Journal* **Vol**, pages (Year)
        # or . *Journal* (Year)
        m_end = re.search(r"\.\s+\*([^*]+)\*\s*(?:\*\*([^*]+)\*\*,?\s*([0-9–\-a-zA-Z]+)?)?,?\s*(?:ICES-[0-9\-]+,?\s*)?\(([^)]+)\)$", text)
        if not m_end:
            # Fallback journal without asterisks or in-press formats
            m_end = re.search(r"\.\s+([A-Z][a-zA-Z\s\.,&]+)\s*(?:\*\*([^*]+)\*\*,?\s*([0-9–\-a-zA-Z]+)?)?,?\s*\(([^)]+)\)$", text)

        if m_end:
            pre_j = text[:m_end.start()].strip()
            journal_str = text[m_end.start():].strip().lstrip(".").strip()
        else:
            ym = re.search(r"\.\s+([^.]+)\s*\(([^)]+)\)$", text)
            if ym:
                pre_j = text[:ym.start()].strip()
                journal_str = text[ym.start():].strip().lstrip(".").strip()
            else:
                pre_j = text
                journal_str = ""

        # Parse Authors vs Title in pre_j
        if " et al." in pre_j:
            idx = pre_j.find(" et al.") + len(" et al.")
            authors = pre_j[:idx].strip()
            title = pre_j[idx:].strip().lstrip(".").strip()
        elif " & " in pre_j:
            amp_idx = pre_j.rfind(" & ")
            sub = pre_j[amp_idx:]
            m_init = re.search(r"&\s+[A-Za-z\u00C0-\u024F\-\'\s]+,\s*([A-Z]\.?\s*)+\.\s+", sub)
            if m_init:
                split_pos = amp_idx + m_init.end()
                authors = pre_j[:split_pos].strip().rstrip(".")
                title = pre_j[split_pos:].strip()
            else:
                m_dot = re.search(r"(\.\s+)(?=[A-Z][a-z])", sub)
                if m_dot:
                    split_pos = amp_idx + m_dot.start() + 1
                    authors = pre_j[:split_pos].strip().rstrip(".")
                    title = pre_j[split_pos:].strip()
                else:
                    authors = pre_j
                    title = ""
        elif pre_j.startswith("NASA."):
            authors = "NASA"
            title = pre_j[len("NASA."):].strip()
        elif pre_j.startswith("Space Lab Tech."):
            authors = "Space Lab Tech"
            title = pre_j[len("Space Lab Tech."):].strip()
        else:
            m_init = re.search(r"^[A-Za-z\u00C0-\u024F\-\'\s]+,\s*([A-Z]\.?\s*)+\.\s+", pre_j)
            if m_init:
                authors = pre_j[:m_init.end()].strip().rstrip(".")
                title = pre_j[m_init.end():].strip()
            else:
                splits = pre_j.split(". ")
                authors = splits[0]
                title = ". ".join(splits[1:])

        # Clean title & journal formatting for plain text CSV
        clean_title = re.sub(r"[\*]", "", title).strip()
        clean_journal = re.sub(r"[\*]", "", journal_str).strip()

        # Clean year
        year_m = re.search(r"\(.*?(\d{4})[a-z]?\)", journal_str)
        year = year_m.group(1) if year_m else ""

        ref_id = f"REF-{num:02d}"
        category = cat_map.get(ref_id, "Hypomagnetic Biology & Quantum Biophysics")

        # Full citation for copy action
        full_cite = f"{authors}. {clean_title}. {clean_journal}."
        if url:
            full_cite += f" {url}"

        records.append({
            "Reference_ID": ref_id,
            "Citation_Number": num,
            "Authors": authors,
            "Title": clean_title,
            "Journal_Or_Source": clean_journal,
            "Thematic_Category": category,
            "DOI_Or_URL": url,
            "Year": year,
            "Full_Citation": full_cite
        })

    return records

def load_table_s2():
    records = []
    with open(S2_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "Dataset_ID": row["Dataset_ID"],
                "Repository": row["Repository"],
                "Accession": row["Accession"],
                "Target_System": row["Target_System"],
                "Platform_Or_Mission": row["Platform_Or_Mission"],
                "Assay_Types": row["Assay_Types"],
                "Description": row["Description"],
                "DOI_Or_URL": row["DOI_Or_URL"]
            })
    return records

def write_clean_csv(s1_records):
    fields = ["Reference_ID", "Citation_Number", "Authors", "Title", "Journal_Or_Source", "Thematic_Category", "DOI_Or_URL"]
    for out_path in [OUT_S1_CSV, DOCS_ASSETS_S1]:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for r in s1_records:
                writer.writerow(r)
    print(f"Wrote clean Table S1 CSV with {len(s1_records)} rows to {OUT_S1_CSV} and {DOCS_ASSETS_S1}")

    # Ensure S2 is copied to docs/assets
    DOCS_ASSETS_S2.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(S2_CSV, DOCS_ASSETS_S2)
    print(f"Copied Table S2 CSV to {DOCS_ASSETS_S2}")

def generate_js(s1_records, s2_records):
    OUT_JS.parent.mkdir(parents=True, exist_ok=True)

    s1_json = json.dumps(s1_records, indent=2, ensure_ascii=False)
    s2_json = json.dumps(s2_records, indent=2, ensure_ascii=False)

    js_content = f"""/**
 * supplementary-tables.js
 * Interactive In-Browser Supplementary Table Explorer
 * Near-Null Magnetic Fields in Lunar Plant Biology (npj Microgravity / LSSR)
 * Supports Table S1 (80 audited papers) & Table S2 (6 public multi-omics datasets)
 */

(function () {{
  "use strict";

  const TABLE_S1_DATA = {s1_json};
  const TABLE_S2_DATA = {s2_json};

  // State Management
  const state = {{
    activeTab: "s1", // "s1" | "s2"
    searchQuery: "",
    categoryFilter: "All",
    sortColumn: "Citation_Number",
    sortAsc: true,
    currentPage: 1,
    pageSize: 10,
    s2View: "cards" // "cards" | "table"
  }};

  function getCategoryBadgeClass(category) {{
    switch (category) {{
      case "Hypomagnetic Biology & Quantum Biophysics":
        return "cat-purple";
      case "Plant Growth & Photomorphogenesis":
        return "cat-green";
      case "Spaceflight Plant Physiology & BLSS":
        return "cat-blue";
      case "Mitochondrial Bioenergetics & Cellular Stress":
        return "cat-amber";
      case "Planetary Magnetism & Exploration Environment":
        return "cat-cyan";
      case "Space Radiation & Multi-Stressor Synergy":
        return "cat-rose";
      default:
        return "cat-default";
    }}
  }}

  function getRepositoryBadgeClass(repo) {{
    if (repo.includes("OSDR")) return "repo-osdr";
    if (repo.includes("PDS") || repo.includes("JAXA")) return "repo-pds";
    if (repo.includes("Cell")) return "repo-cell";
    return "repo-github";
  }}

  function showToast(message) {{
    let toast = document.getElementById("supp-toast");
    if (!toast) {{{{
      toast = document.createElement("div");
      toast.id = "supp-toast";
      toast.className = "supp-toast";
      document.body.appendChild(toast);
    }}}}
    toast.textContent = message;
    toast.classList.add("visible");
    setTimeout(() => {{{{
      toast.classList.remove("visible");
    }}}}, 2500);
  }}

  function copyToClipboard(text, confirmationMsg) {{
    if (navigator.clipboard && window.isSecureContext) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(confirmationMsg || "Citation copied to clipboard!");
      }}).catch(() => {{
        fallbackCopy(text, confirmationMsg);
      }});
    }} else {{
      fallbackCopy(text, confirmationMsg);
    }}
  }}

  function fallbackCopy(text, confirmationMsg) {{
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try {{
      document.execCommand("copy");
      showToast(confirmationMsg || "Citation copied to clipboard!");
    }} catch (err) {{
      prompt("Copy to clipboard:", text);
    }}
    document.body.removeChild(ta);
  }}

  function filterAndSortS1() {{
    let items = TABLE_S1_DATA.slice();

    // 1. Category Filter
    if (state.categoryFilter !== "All") {{
      items = items.filter(r => r.Thematic_Category === state.categoryFilter);
    }}

    // 2. Search Query
    if (state.searchQuery.trim() !== "") {{
      const q = state.searchQuery.toLowerCase();
      items = items.filter(r => {{
        return (
          r.Reference_ID.toLowerCase().includes(q) ||
          r.Citation_Number.toString().includes(q) ||
          r.Authors.toLowerCase().includes(q) ||
          r.Title.toLowerCase().includes(q) ||
          r.Journal_Or_Source.toLowerCase().includes(q) ||
          r.Thematic_Category.toLowerCase().includes(q) ||
          (r.Year && r.Year.includes(q))
        );
      }});
    }}

    // 3. Sorting
    items.sort((a, b) => {{
      let valA = a[state.sortColumn];
      let valB = b[state.sortColumn];

      if (state.sortColumn === "Citation_Number") {{
        return state.sortAsc ? valA - valB : valB - valA;
      }}

      valA = (valA || "").toString().toLowerCase();
      valB = (valB || "").toString().toLowerCase();
      if (valA < valB) return state.sortAsc ? -1 : 1;
      if (valA > valB) return state.sortAsc ? 1 : -1;
      return 0;
    }});

    return items;
  }}

  function renderS1Table() {{
    const filtered = filterAndSortS1();
    const total = filtered.length;

    // Pagination calculations
    const pageSize = state.pageSize === "All" ? total : parseInt(state.pageSize, 10);
    const totalPages = pageSize === 0 ? 1 : Math.ceil(total / pageSize);
    if (state.currentPage > totalPages) state.currentPage = Math.max(1, totalPages);

    const startIdx = (state.currentPage - 1) * pageSize;
    const endIdx = state.pageSize === "All" ? total : Math.min(startIdx + pageSize, total);
    const pageItems = filtered.slice(startIdx, endIdx);

    // Summary Text
    const summaryEl = document.getElementById("supp-s1-summary");
    if (summaryEl) {{
      if (total === 0) {{
        summaryEl.textContent = "No publications matched your search criteria.";
      }} else {{
        const rangeText = state.pageSize === "All" ? `All ${{total}}` : `${{startIdx + 1}}–${{endIdx}} of ${{total}}`;
        summaryEl.innerHTML = `Showing <strong>${{rangeText}}</strong> audited publications (filtered from 80 corpus total)`;
      }}
    }}

    // Table Body
    const tbody = document.getElementById("supp-s1-tbody");
    if (!tbody) return;

    if (pageItems.length === 0) {{
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:30px; color:var(--muted, #64748b);">No publications found matching "<em>${{escapeHtml(state.searchQuery)}}</em>"</td></tr>`;
      renderPagination(totalPages, total);
      return;
    }}

    let rowsHtml = "";
    for (const item of pageItems) {{
      const badgeCls = getCategoryBadgeClass(item.Thematic_Category);
      const linkHtml = item.DOI_Or_URL
        ? `<a class="supp-link-btn" href="${{item.DOI_Or_URL}}" target="_blank" rel="noopener" title="Open source publication">
             ${{item.DOI_Or_URL.includes("doi.org") ? "DOI ↗" : "URL ↗"}}
           </a>`
        : `<span class="supp-no-link" title="Print / Archived Reference">—</span>`;

      rowsHtml += `
        <tr>
          <td class="col-num">
            <span class="ref-badge" title="${{item.Reference_ID}}">[${{item.Citation_Number}}]</span>
          </td>
          <td class="col-authors">
            <strong>${{escapeHtml(item.Authors)}}</strong>
          </td>
          <td class="col-details">
            <div class="pub-title">${{escapeHtml(item.Title)}}</div>
            <div class="pub-journal"><em>${{escapeHtml(item.Journal_Or_Source)}}</em></div>
          </td>
          <td class="col-cat">
            <span class="cat-pill ${{badgeCls}}">${{escapeHtml(item.Thematic_Category)}}</span>
          </td>
          <td class="col-actions">
            ${{linkHtml}}
            <button class="supp-copy-btn" data-cite="${{escapeAttr(item.Full_Citation)}}" title="Copy full citation to clipboard">
              📋 Cite
            </button>
          </td>
        </tr>
      `;
    }}
    tbody.innerHTML = rowsHtml;

    // Attach cite click listeners
    const copyBtns = tbody.querySelectorAll(".supp-copy-btn");
    copyBtns.forEach(btn => {{
      btn.addEventListener("click", function() {{
        const citeText = this.getAttribute("data-cite");
        copyToClipboard(citeText, "Citation copied to clipboard!");
      }});
    }});

    renderPagination(totalPages, total);
  }}

  function renderPagination(totalPages, totalItems) {{
    const container = document.getElementById("supp-pagination");
    if (!container) return;

    if (state.pageSize === "All" || totalPages <= 1) {{
      container.innerHTML = "";
      return;
    }}

    let html = `<div class="pagination-wrap">`;
    html += `<button class="page-btn nav-btn" data-page="${{state.currentPage - 1}}" ${{state.currentPage === 1 ? "disabled" : ""}}>‹ Previous</button>`;

    // Windowed page numbers
    let startPage = Math.max(1, state.currentPage - 2);
    let endPage = Math.min(totalPages, startPage + 4);
    if (endPage - startPage < 4) {{
      startPage = Math.max(1, endPage - 4);
    }}

    if (startPage > 1) {{
      html += `<button class="page-btn" data-page="1">1</button>`;
      if (startPage > 2) html += `<span class="page-ellipsis">…</span>`;
    }}

    for (let p = startPage; p <= endPage; p++) {{
      html += `<button class="page-btn ${{p === state.currentPage ? "active" : ""}}" data-page="${{p}}">${{p}}</button>`;
    }}

    if (endPage < totalPages) {{
      if (endPage < totalPages - 1) html += `<span class="page-ellipsis">…</span>`;
      html += `<button class="page-btn" data-page="${{totalPages}}">${{totalPages}}</button>`;
    }}

    html += `<button class="page-btn nav-btn" data-page="${{state.currentPage + 1}}" ${{state.currentPage === totalPages ? "disabled" : ""}}>Next ›</button>`;
    html += `</div>`;

    container.innerHTML = html;

    const pageButtons = container.querySelectorAll(".page-btn:not([disabled])");
    pageButtons.forEach(btn => {{
      btn.addEventListener("click", function() {{
        const targetPage = parseInt(this.getAttribute("data-page"), 10);
        if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalPages) {{
          state.currentPage = targetPage;
          renderS1Table();
          // Scroll gently to top of table
          const section = document.getElementById("supplementary-tables");
          if (section) section.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }}
      }});
    }});
  }}

  function renderS2Cards() {{
    const container = document.getElementById("supp-s2-content");
    if (!container) return;

    let html = `
      <div class="s2-header-desc">
        <p>Six curated public spaceflight, planetary magnetometer, and computational systems biology repositories synthesizing multi-omics and vector geophysical archives across Apollo, Lunar Prospector, Kaguya, ISS, and Artemis analog missions.</p>
      </div>
      <div class="s2-cards-grid">
    `;

    for (const ds of TABLE_S2_DATA) {{
      const repoCls = getRepositoryBadgeClass(ds.Repository);
      html += `
        <div class="s2-card">
          <div class="s2-card-top">
            <span class="repo-badge ${{repoCls}}">${{escapeHtml(ds.Repository)}}</span>
            <span class="accession-tag">${{escapeHtml(ds.Accession)}}</span>
          </div>
          <h4 class="s2-target">${{escapeHtml(ds.Target_System)}}</h4>
          <div class="s2-platform">
            <strong>Platform / Mission:</strong> ${{escapeHtml(ds.Platform_Or_Mission)}}
          </div>
          <div class="s2-assays">
            <strong>Assay Types:</strong> <span class="assay-pill">${{escapeHtml(ds.Assay_Types)}}</span>
          </div>
          <p class="s2-desc">${{escapeHtml(ds.Description)}}</p>
          <div class="s2-action">
            <a class="btn primary s2-btn" href="${{ds.DOI_Or_URL}}" target="_blank" rel="noopener">
              Explore Repository (${{escapeHtml(ds.Dataset_ID)}}) ↗
            </a>
          </div>
        </div>
      `;
    }}

    html += `</div>`;
    container.innerHTML = html;
  }}

  function escapeHtml(str) {{
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }}

  function escapeAttr(str) {{
    if (!str) return "";
    return str.replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }}

  function setupEventListeners() {{
    // Tab switching
    const tabS1 = document.getElementById("tab-btn-s1");
    const tabS2 = document.getElementById("tab-btn-s2");
    const s1Container = document.getElementById("supp-s1-container");
    const s2Container = document.getElementById("supp-s2-container");

    if (tabS1 && tabS2) {{
      tabS1.addEventListener("click", () => {{
        state.activeTab = "s1";
        tabS1.classList.add("active");
        tabS2.classList.remove("active");
        if (s1Container) s1Container.style.display = "block";
        if (s2Container) s2Container.style.display = "none";
      }});

      tabS2.addEventListener("click", () => {{
        state.activeTab = "s2";
        tabS2.classList.add("active");
        tabS1.classList.remove("active");
        if (s1Container) s1Container.style.display = "none";
        if (s2Container) s2Container.style.display = "block";
        renderS2Cards();
      }});
    }}

    // Search Input
    const searchInput = document.getElementById("supp-search-input");
    const searchClear = document.getElementById("supp-search-clear");
    if (searchInput) {{
      searchInput.addEventListener("input", (e) => {{
        state.searchQuery = e.target.value;
        state.currentPage = 1;
        if (searchClear) {{
          searchClear.style.display = state.searchQuery ? "inline-block" : "none";
        }}
        renderS1Table();
      }});

      if (searchClear) {{
        searchClear.addEventListener("click", () => {{
          searchInput.value = "";
          state.searchQuery = "";
          searchClear.style.display = "none";
          state.currentPage = 1;
          renderS1Table();
          searchInput.focus();
        }});
      }}
    }}

    // Category Filter Dropdown
    const catSelect = document.getElementById("supp-category-select");
    if (catSelect) {{
      catSelect.addEventListener("change", (e) => {{
        state.categoryFilter = e.target.value;
        state.currentPage = 1;
        renderS1Table();
      }});
    }}

    // Page Size Selector
    const pageSizeSelect = document.getElementById("supp-page-size");
    if (pageSizeSelect) {{
      pageSizeSelect.addEventListener("change", (e) => {{
        state.pageSize = e.target.value;
        state.currentPage = 1;
        renderS1Table();
      }});
    }}

    // Sort Headers
    const sortHeaders = document.querySelectorAll(".supp-table th.sortable");
    sortHeaders.forEach(th => {{
      th.addEventListener("click", function() {{
        const col = this.getAttribute("data-sort");
        if (state.sortColumn === col) {{
          state.sortAsc = !state.sortAsc;
        }} else {{
          state.sortColumn = col;
          state.sortAsc = true;
        }}

        // Update UI sort arrows
        sortHeaders.forEach(h => {{
          h.classList.remove("sort-asc", "sort-desc");
        }});
        this.classList.add(state.sortAsc ? "sort-asc" : "sort-desc");

        renderS1Table();
      }});
    }});
  }}

  // Initialize on DOM ready
  document.addEventListener("DOMContentLoaded", () => {{
    setupEventListeners();
    renderS1Table();
  }});

}})();
"""

    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Generated {OUT_JS} with embedded JSON and logic engine.")

def main():
    print("Beginning Supplementary Web Data generation...")
    s1_records = parse_markdown_references()
    print(f"Successfully extracted {len(s1_records)} Table S1 records.")
    s2_records = load_table_s2()
    print(f"Successfully loaded {len(s2_records)} Table S2 records.")
    write_clean_csv(s1_records)
    generate_js(s1_records, s2_records)
    print("Done!")

if __name__ == "__main__":
    main()
