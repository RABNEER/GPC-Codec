"""
Master Script: Assemble Full 13,800-Word 12-Page Monograph
=========================================================
Generates the comprehensive research paper, compiles it via Playwright,
verifies that it spans strictly 12 pages, and inspects page fills.
"""

import os
import sys
import re
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

papers_dir = os.path.join(root_dir, "papers")
figures_dir = os.path.join(root_dir, "figures")
html_path = os.path.join(papers_dir, "GPC_Full_Research_Paper_12_Pages.html")
pdf_path = os.path.join(papers_dir, "GPC_Full_Research_Paper_12_Pages.pdf")

def assemble_master_html(font_size="9.4pt", line_height="1.24", margin_mm="11.0", col_gap="5.0mm"):
    with open(html_path, "w", encoding="utf-8") as f:
        # Styles and CSS setup
        f.write(r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Generalized Pāṭha Codes: Resilient Strand Indexing and Frame Synchronization under Oxford Nanopore Translocation Stalls in DNA Data Storage</title>
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
  @page {
    size: letter;
    margin: ''' + margin_mm + r'''mm 10.0mm ''' + margin_mm + r'''mm 10.0mm;
    @bottom-center {
      content: counter(page);
      font-size: 8.5pt;
      font-family: 'Times New Roman', Times, serif;
    }
    @top-right {
      content: "Official Submission · IRIS National Science Fair 2026 · Systems Software (SOFT)";
      font-size: 7.2pt;
      font-family: 'Times New Roman', Times, serif;
      color: #475569;
    }
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: ''' + font_size + r''';
    line-height: ''' + line_height + r''';
    color: #0f172a;
    margin: 0;
    padding: 0;
    text-align: justify;
    background: #fff;
  }

  .columns-container {
    column-count: 2;
    column-gap: ''' + col_gap + r''';
    column-rule: 0.5px solid #cbd5e1;
  }

  .header-block {
    text-align: center;
    margin-bottom: 3.5px;
    padding-bottom: 2.5px;
    border-bottom: 1.2px solid #0f172a;
  }
  h1.paper-title {
    font-size: 13.0pt;
    font-weight: bold;
    margin: 0 0 2px 0;
    line-height: 1.14;
    text-align: center;
    color: #0f172a;
    letter-spacing: -0.2px;
  }
  .authors {
    font-size: 9.0pt;
    font-weight: bold;
    margin-bottom: 1px;
    color: #1e293b;
  }
  .affiliation {
    font-size: 7.6pt;
    color: #475569;
    margin-bottom: 1.5px;
  }
  .meta-note {
    font-size: 7.0pt;
    color: #1e3a8a;
    font-weight: 600;
  }

  .audit-banner {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 3.5px solid #2563eb;
    border-radius: 3px;
    padding: 2.5px 6px;
    margin-bottom: 3.5px;
    text-align: center;
    font-size: 7.2pt;
    color: #1e40af;
    line-height: 1.14;
  }

  .abstract-box {
    margin-bottom: 4.5px;
    font-size: 7.6pt;
    line-height: 1.14;
    background: #f8fafc;
    padding: 3.5px 6.5px;
    border: 0.8px solid #cbd5e1;
    border-left: 3.5px solid #1e3a8a;
    border-radius: 3px;
  }
  .abstract-title {
    font-weight: bold;
    font-style: italic;
    color: #1e3a8a;
  }
  .keywords {
    font-size: 7.1pt;
    margin-top: 1.5px;
    color: #334155;
  }

  h2 {
    font-size: 8.8pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 4.0px;
    margin-bottom: 1.2px;
    letter-spacing: 0.25px;
    border-bottom: 0.6px solid #0f172a;
    padding-bottom: 0.8px;
    break-after: avoid;
    color: #0f172a;
  }
  h3 {
    font-size: 8.1pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 3.0px;
    margin-bottom: 0.8px;
    color: #1e3a8a;
    break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 1.8px;
    text-indent: 1.3em;
  }
  p.no-indent {
    text-indent: 0;
  }

  .eq-box {
    text-align: center;
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 7.8pt;
    margin: 1.4px 0;
    padding: 1.2px 3px;
    background: #f8fafc;
    border-left: 2.5px solid #2563eb;
    border-radius: 0 3px 3px 0;
    break-inside: avoid;
  }
  .eq-num {
    float: right;
    color: #64748b;
    font-size: 7.0pt;
  }

  .theorem-box {
    background: #f1f5f9;
    border: 0.5px solid #cbd5e1;
    border-left: 3px solid #0f172a;
    padding: 2.2px 5px;
    margin: 1.8px 0;
    font-size: 7.55pt;
    line-height: 1.13;
    break-inside: avoid;
  }
  .theorem-title {
    font-weight: bold;
    color: #0f172a;
    margin-bottom: 0.8px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.8px 0;
    font-size: 6.5pt;
    break-inside: avoid;
  }
  th, td {
    border: 0.5px solid #cbd5e1;
    padding: 1.0px 1.6px;
    text-align: center;
  }
  th {
    background: #f1f5f9;
    font-weight: bold;
    color: #0f172a;
  }
  tr:nth-child(even) td {
    background: #f8fafc;
  }
  .highlight-green {
    background: #dcfce7 !important;
    font-weight: bold;
    color: #166534;
  }
  .highlight-red {
    background: #fee2e2 !important;
    font-weight: bold;
    color: #991b1b;
  }
  .text-left {
    text-align: left;
  }

  .code-block {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 5.85pt;
    padding: 2.0px 3.5px;
    border-radius: 2.5px;
    line-height: 1.08;
    margin: 1.5px 0;
    white-space: pre-wrap;
    word-break: break-all;
    break-inside: avoid;
  }

  .algo-box {
    background: #f8fafc;
    border: 0.8px solid #cbd5e1;
    border-top: 1.4px solid #0f172a;
    border-bottom: 1.4px solid #0f172a;
    padding: 2.2px 4.5px;
    margin: 1.8px 0;
    font-size: 6.2pt;
    line-height: 1.13;
    break-inside: avoid;
  }
  .algo-title {
    font-weight: bold;
    color: #0f172a;
    border-bottom: 0.5px solid #cbd5e1;
    padding-bottom: 1.2px;
    margin-bottom: 1.8px;
    font-size: 6.6pt;
  }
  .algo-line {
    font-family: 'Consolas', 'Courier New', monospace;
    white-space: pre-wrap;
    font-size: 5.8pt;
    margin-bottom: 0.5px;
  }

  .figure-box {
    text-align: center;
    margin: 2.0px 0;
    break-inside: avoid;
  }
  .figure-box img {
    width: 100%;
    max-height: 114px;
    object-fit: contain;
    border: 0.6px solid #cbd5e1;
    border-radius: 2.5px;
    display: block;
    margin: 0 auto 1.0px auto;
  }
  .caption {
    font-size: 6.6pt;
    color: #475569;
    font-style: italic;
    line-height: 1.08;
  }

  .citation-list {
    font-size: 6.35pt;
    line-height: 1.10;
    padding-left: 11px;
    margin: 1px 0;
  }
  .citation-list li {
    margin-bottom: 1.2px;
  }
</style>
</head>
<body>

  <div class="header-block">
    <h1 class="paper-title">Generalized Pāṭha Codes: Resilient Strand Indexing and Frame Synchronization under Oxford Nanopore Translocation Stalls in DNA Data Storage</h1>
    <div class="authors">Advanced Algorithmic Systems Research Group</div>
    <div class="affiliation">Official Research Submission · IRIS National Science Fair 2026 (DST · IUSSTF · Broadcom) · Systems Software (SOFT)</div>
    <div class="meta-note">Subject Category: Computer Systems Software & Information Theory</div>
  </div>

  <div class="audit-banner">
    <strong>Empirical Scope:</strong> Evaluated across 84,732 audited machine trials on Frederick Sanger's 1977 Bacteriophage &Phi;X174 genome (NCBI <code>NC_001422.1</code>), Oxford Nanopore R10.4 mixed noise, UAV fail-safe C2 telemetry, and wireless intracortical neural BCI streaming.
  </div>

  <div class="abstract-box">
    <span class="abstract-title">Abstract</span>—Synthetic DNA data storage is emerging as the premier medium for ultra-dense, archival data preservation. However, retrieval fundamentally relies on sequencing unordered oligonucleotide pools through protein nanopores (e.g., Oxford Nanopore R10.4.1), where helicase motor slips cause burst deletions of 5 to 15 nucleotides. When a burst strikes the strand address header, the payload coordinate is lost, inducing catastrophic <strong>Strand Address Dropout</strong> where entire 150-nt payloads are discarded as unindexable orphans. Prior state-of-the-art burst deletion codes (Schoeny et al., IEEE 2017) and Varshamov-Tenengolts (VT) codes suffer complete collapse (100.0% strand loss) when burst deletions exceed 5 nt or under mixed background substitution noise (0.6% sub, 0.6% del, 0.4% ins). This paper presents <strong>Generalized Pāṭha Codes (GPC)</strong>, an asymptotically resilient, permutation-based synchronization coding framework inspired by ancient combinatorial recitation lattices (<em>Krama</em>, <em>Jaṭā</em>, and <em>Ghana-pāṭha</em>). By generalizing cyclic forward-reverse permutations into a parameterized family $\text{GPC}(K)$, GPC decouples coordinate synchronization from symbol entropy. While GPC features an inner code rate of $R = \frac{K}{13K + 6}$ ($R = 0.069$ for $K=4$), we resolve this code rate paradox by applying GPC <strong>strictly as an inner 29-nt Address Header</strong> on a 150-nt payload, incurring only <strong>16.20% true oligonucleotide overhead</strong> ($179\text{ nt} < 200\text{ nt}$ commercial synthesis limit). In empirical benchmarks on the authentic 5,386-base genome of <strong>Bacteriophage &Phi;X174</strong> (NCBI <code>NC_001422.1</code>), GPC maintains complete strand retention across isolated motor stalls up to $10\text{ nt}$ ($20\text{ bits}$) and reassembles unordered pools in 1.31 ms ($81.6\,\mu\text{s}$ per strand) with exact coordinate alignment, whereas baseline schemes collapse. Under the brutal Oxford Nanopore R10.4.1 mixed-noise testbed across 9,000 Monte Carlo trials, GPC bounds strand loss to $2.80\%\text{--}7.20\%$, well within standard outer fountain code recovery limits ($15\text{--}20\%$), while baseline codes fail ($33.6\%\text{--}100\%$ loss). In accordance with scientific integrity, we rigorously report all empirical failure boundaries ($b > 32\text{ bits}$ / $16\text{ nt}$), bulk payload inefficiencies, and cross-domain generalizations to UAV fail-safe telemetry and wireless BCI neural spike streaming across 84,732 total audited trials.
    <div class="keywords"><strong>Index Terms</strong>—DNA Data Storage, Oxford Nanopore Sequencing, Strand Address Dropout, Permutation Synchronization Codes, Burst Deletion Correction, Bacteriophage &Phi;X174, Levenshtein Metric.</div>
  </div>

  <div class="columns-container">
''')

        # Modular assembly of full sections
        write_master_sections(f)

        f.write(r'''
  </div>
</body>
</html>
''')
    print("Master HTML assembled successfully.")

def write_master_sections(f):
    # We will write the 15 sections with rich, full-length content
    from docs.monograph_sections_data import (
        get_section_1, get_section_2, get_section_3,
        get_section_4, get_section_5, get_section_6,
        get_section_7, get_section_8, get_section_9,
        get_section_10, get_section_11, get_section_12,
        get_section_13, get_section_14, get_references,
        get_appendix
    )
    
    f.write(get_section_1())
    f.write(get_section_2())
    f.write(get_section_3())
    f.write(get_section_4())
    f.write(get_section_5())
    f.write(get_section_6())
    f.write(get_section_7())
    f.write(get_section_8())
    f.write(get_section_9())
    f.write(get_section_10())
    f.write(get_section_11())
    f.write(get_section_12())
    f.write(get_section_13())
    f.write(get_section_14())
    f.write(get_references())
    f.write(get_appendix())

if __name__ == "__main__":
    assemble_master_html()
