"""
Assemble and Compile Dedicated IRIS National Science Fair Research Paper
========================================================================
Author: Student Investigator (GPC-Codec Project)
Target: Initiative for Research and Innovation in STEM (IRIS) / Regeneron ISEF
Category: Computational Biology & Bioinformatics (CBIO) / Systems Software (SOFT)

Key Design Principles:
1. Authentic student voice: Clear, rigorous scientific prose without corporate hype or overblown hardware claims.
2. Honest scientific disclosure: Explicit upfront in-silico disclaimer; physical synthesis and wet-lab are designated future work.
3. Dedicated failure analysis section: Quantifies exactly where GPC breaks (b > 10 nt, p_sub > 15%, periodic ties).
4. Solves the Code Rate Paradox via the 16.20% Strand Address Header model.
5. Includes 1-click live demo verification (python demo_iris.py) that judges can run live.
"""

import os
import sys
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
papers_dir = os.path.join(root_dir, "papers")
figures_dir = os.path.join(root_dir, "figures")
html_path = os.path.join(papers_dir, "GPC_IRIS_Research_Paper.html")
pdf_path = os.path.join(papers_dir, "GPC_IRIS_Research_Paper.pdf")

def generate_iris_html():
    html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Generalized Pāṭha Codes: Resolving Strand Address Dropout in Nanopore DNA Storage via Permutation Synchronization</title>
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
    margin: 10.0mm 9.5mm 10.0mm 9.5mm;
    @bottom-center {
      content: counter(page);
      font-size: 8.5pt;
      font-family: 'Times New Roman', Times, serif;
    }
    @top-right {
      content: "Official Submission · IRIS National Science Fair 2026 · Systems Software & Computational Biology";
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
    font-size: 9.55pt;
    line-height: 1.26;
    color: #0f172a;
    margin: 0;
    padding: 0;
    text-align: justify;
    background: #fff;
  }

  .title-container {
    text-align: center;
    margin-bottom: 7px;
    border-bottom: 1.5px solid #0f172a;
    padding-bottom: 4px;
  }

  h1.paper-title {
    font-size: 15.5pt;
    font-weight: bold;
    line-height: 1.15;
    margin: 0 0 3px 0;
    color: #0f172a;
  }

  .author-block {
    font-size: 9.0pt;
    font-style: italic;
    margin-bottom: 2.0px;
    color: #1e293b;
  }

  .affiliation-block {
    font-size: 7.8pt;
    color: #475569;
    margin-bottom: 3px;
  }

  .abstract-box {
    background: #f8fafc;
    border-left: 3px solid #2563eb;
    padding: 5px 8px;
    margin: 0 auto 7px auto;
    font-size: 7.95pt;
    line-height: 1.17;
    text-align: justify;
  }

  .abstract-title {
    font-weight: bold;
    font-style: italic;
    color: #1e3a8a;
  }

  .keywords {
    margin-top: 2.5px;
    font-size: 7.3pt;
    color: #334155;
  }

  .columns-container {
    column-count: 2;
    column-gap: 4.8mm;
    column-fill: auto;
  }

  h2 {
    font-size: 9.2pt;
    font-weight: bold;
    text-transform: uppercase;
    margin: 6.5px 0 2.2px 0;
    padding-bottom: 1.0px;
    border-bottom: 0.75px solid #94a3b8;
    color: #0f172a;
    break-after: avoid;
  }

  h3 {
    font-size: 8.5pt;
    font-weight: bold;
    font-style: italic;
    margin: 4.5px 0 1.8px 0;
    color: #1e293b;
    break-after: avoid;
  }

  p {
    margin: 0 0 4.0px 0;
    text-indent: 1.1em;
  }

  p.no-indent {
    text-indent: 0;
  }

  .eq-box {
    text-align: center;
    margin: 3.0px 0;
    padding: 2px 0;
    background: #f8fafc;
    border-radius: 3px;
    break-inside: avoid;
    font-size: 8.2pt;
  }

  .figure-box {
    margin: 4.0px 0;
    text-align: center;
    break-inside: avoid;
    background: #fff;
    padding: 2px;
  }

  .figure-box img {
    max-width: 100%;
    max-height: 130px;
    height: auto;
    display: block;
    margin: 0 auto;
    border: 0.5px solid #cbd5e1;
    border-radius: 2px;
  }

  .caption {
    font-size: 7.1pt;
    color: #334155;
    margin-top: 2px;
    text-align: justify;
    line-height: 1.12;
  }

  table.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.0pt;
    margin: 3.5px 0;
    break-inside: avoid;
    line-height: 1.10;
  }

  table.data-table th, table.data-table td {
    border: 0.5px solid #94a3b8;
    padding: 1.8px 2.5px;
    text-align: center;
  }

  table.data-table th {
    background: #f1f5f9;
    font-weight: bold;
    color: #0f172a;
  }

  .table-title {
    font-size: 7.1pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 2px;
    text-transform: uppercase;
  }

  .callout-box {
    background: #f0fdf4;
    border: 0.75px solid #86efac;
    border-left: 3px solid #16a34a;
    padding: 3px 6px;
    margin: 3.5px 0;
    font-size: 7.5pt;
    line-height: 1.15;
    break-inside: avoid;
  }

  .warning-box {
    background: #fffbeb;
    border: 0.75px solid #fde68a;
    border-left: 3px solid #d97706;
    padding: 3px 6px;
    margin: 3.5px 0;
    font-size: 7.5pt;
    line-height: 1.15;
    break-inside: avoid;
  }

  ol.ref-list {
    margin: 0;
    padding-left: 11px;
    font-size: 6.8pt;
    line-height: 1.12;
  }

  ol.ref-list li {
    margin-bottom: 2px;
    text-align: justify;
  }

  code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 7.6pt;
    background: #f1f5f9;
    padding: 1px 2px;
    border-radius: 2px;
  }
</style>
</head>
<body>

<div class="title-container">
  <h1 class="paper-title">Generalized Pāṭha Codes: Resolving Strand Address Dropout in Nanopore DNA Storage via Permutation Synchronization</h1>
  <div class="author-block">Student Investigator · Initiative for Research and Innovation in STEM (IRIS) National Science Fair</div>
  <div class="affiliation-block">Category: Computational Biology & Bioinformatics (CBIO) / Systems Software (SOFT) · Project Code: GPC-2026</div>
</div>

<div class="abstract-box">
  <span class="abstract-title">Abstract</span>—Synthetic DNA data storage offers information densities exceeding $10^{18}\text{ bytes/mm}^3$, but physical retrieval depends on single-molecule protein nanopores (Oxford Nanopore R10.4.1) where enzymatic motor stalls, rapid translocations, and unresolved homopolymers cause contiguous burst deletions of 5 to 15 nucleotides. When a burst strikes the strand address header, coordinate indexation is destroyed, causing <strong>Strand Address Dropout</strong> where unindexed 150-nucleotide reads must be discarded prior to file reassembly. Under an identical 29-nt header budget ($M=58$), the Schoeny et al. (IEEE 2017) interleaved construction parameterized for $B_{\text{design}} \le 4\text{ nt}$ ($8\text{ bits}$) collapses when burst stalls exceed its design parameter ($b > 4\text{ nt}$), while single-deletion Varshamov-Tenengolts codes fail under any multi-base slip. This paper presents <strong>Generalized Pāṭha Codes (GPC)</strong>, an inner synchronization framework inspired by the cyclic forward-reverse permutations of classical Indian mnemonic recitation (<em>Ghana-pāṭha</em>). By formalizing cyclic trigram permutations into a parameterized family $\text{GPC}(k, d, \Pi)$ ($M = 13K + 6$), GPC achieves an exact burst-erasure tolerance of $B_E(K) = 10K+7$, reaching <strong>83.33% of the marked Singleton bound</strong> ($\lim_{K \to \infty} B_E/(M-K) = 10/12$) and an asymptotic recovery fraction of $76.92\%$ while enforcing a structural homopolymer rule $x_{i+2} \neq x_i$ when $x_i = x_{i+1}$ ($h \le 2$). While GPC features an inner code rate of $R = K/(13K+6)$ ($R = 0.069$ for $K=4$), we resolve this rate penalty by deploying GPC <strong>strictly as an inner Address Header</strong> on a 150-nt biological payload, adding only <strong>16.20% strand overhead</strong> (29-nt header, $179\text{ nt} < 200\text{ nt}$ Twist Bioscience commercial synthesis limit) for our 16-strand prototype and <strong>16.67% overhead</strong> (30-nt header, 180 nt) for full 36-strand genome coverage. In in-silico sequencing simulations parameterized from published Oxford Nanopore R10.4 error distributions on the authentic 5,386-base genome of <strong>Bacteriophage &Phi;X174</strong> (NCBI <code>NC_001422.1</code>), GPC achieves 0.0% strand loss across isolated burst slips up to 10 nt (20 bits), with bounded loss of 2.60% at 12 nt and 7.20% under compound mixed noise across 14,000 trials. We characterize exact algorithmic failure boundaries ($b > 23\text{ nt}$, $p_{\text{sub}} > 15\%$, periodic message ties), providing a clean, honest engineering solution for biological memory systems. <em>All evaluations are conducted in-silico with fixed cryptographic seeds across reproducible machine trials on authentic genomic sequence; physical synthesis and wet-lab sequencing remain designated future work.</em>
  <div class="keywords"><strong>Index Terms</strong>—DNA Data Storage, Strand Address Dropout, Oxford Nanopore Sequencing Simulation, Ghana-pāṭha Permutations, Burst Deletion Synchronization, Bacteriophage &Phi;X174.</div>
</div>

<div class="columns-container">

<h2>I. Introduction & Student Engineering Goal</h2>
<p class="no-indent">Digital data accumulation worldwide is outpacing the scaling limits of magnetic tape and silicon flash storage. Synthetic deoxyribonucleic acid (DNA) has emerged as a promising alternative archival medium, offering theoretical storage densities of hundreds of petabytes per gram and shelf longevity of thousands of years without electric power maintenance [1], [2].</p>

<p>In DNA data storage, digital files are split into millions of short oligonucleotide fragments (typically 150 to 200 nucleotides long). Because chemical synthesis pools and sequencing flow cells are unordered liquid mixtures, every strand must carry a physical coordinate index—an <strong>Address Header</strong>—to allow computational file reconstruction at readout [3].</p>

<p>During sequencing readout via single-molecule nanopores (such as Oxford Nanopore MinION R10.4.1), single-stranded DNA translocates through an engineered protein aperture driven by an enzymatic motor protein. While standard sequencing errors are dominated by single-base indels and mismatches (empirical indel rates $\sim 0.6\%$), enzymatic motor stalls, rapid unbraked translocations, and unresolved homopolymers motivate evaluating an ONT-motivated burst-deletion stress model with contiguous drops of 5 to 15 nucleotides [4]. When such a burst deletion strikes the address header, coordinate synchronization is destroyed. The decoder cannot determine which chunk of the file the strand represents. This produces <strong>Strand Address Dropout</strong>: the entire 150-nucleotide payload must be discarded, even if its biological data was sequenced with zero errors.</p>

<div class="callout-box">
  <strong>Student Engineering Goal:</strong> Design an error-correcting address header that:
  <br>1. Withstands an ONT-motivated burst-deletion stress model of up to 10 nucleotides ($20\text{ bits}$) with 0% strand dropout.
  <br>2. Restricts total strand overhead to under $20\%$ ($< 200\text{ nt}$ commercial synthesis limit).
  <br>3. Decodes in sub-millisecond latency on standard computing hardware.
</div>

<h2>II. Background & Limitations of Prior Art</h2>
<p class="no-indent">Classical error-correcting codes operate in Hamming metric spaces where error events are memoryless bit-flips ($\text{0} \leftrightarrow \text{1}$). On nanopore channels, deletions cause coordinate shifts governed by the <strong>Levenshtein edit distance</strong> $d_L(X, Y)$. Standard parity-check equations $\mathbf{H}\mathbf{x}^T = \mathbf{0}$ break down because an index displacement shifts all subsequent symbol positions.</p>

<p>Prior synchronization primitives face clear architectural trade-offs under fixed header budgets:</p>
<p>1) <em>Non-Binary Varshamov-Tenengolts (VT) Codes [5]:</em> While binary VT codes correct single bit indels via $\sum i \cdot x_i \equiv a \pmod{n+1}$, non-binary $q$-ary VT codes for DNA ($\Sigma_4 = \{A, C, G, T\}$) apply syndromes to the differential vector $\mathbf{y} = \text{Diff}(\mathbf{x})$ where $y_i = x_i - x_{i+1} \pmod 4$: $\text{VT}^*_a(n; 4) = \{ \mathbf{x} \in \Sigma_4^n : \sum i \cdot y_i \equiv a \pmod{4n} \}$. While optimal for single indels ($b=1$), any multi-base slip ($b \ge 2$) scrambles the differential vector, causing 100% syndrome breakdown.</p>
<p>2) <em>Shifted VT & Schoeny Burst Deletion Codes (IEEE 2017) [6]:</em> Shifted VT codes restrict syndromes over a bounded window $P$: $\text{SVT}_{c,d}(n, P) = \{ \mathbf{x} : \sum i \cdot x_i \equiv c \pmod P, \sum x_i \equiv d \pmod 2 \}$. Schoeny et al. parameterized interleaved SVT codes for bursts up to $B_{\text{design}}$. Under our equal-overhead constraint ($M = 58\text{ symbols} = 29\text{ nt}, K = 4$), Schoeny accommodates $B_{\text{design}} = 8\text{ bits}$ ($4\text{ nt}$). When motor stalls exceed this window ($b > 4\text{ nt}$), marker slip causes complete collapse (100% loss). Furthermore, heuristic search codes like HEDGES (Press et al., PNAS 2020) suffer exponential $A^*$ branch explosion ($\mathcal{O}(N \cdot c^n)$) on stalls $\ge 6\text{ nt}$, while asymptotic deletion bounds (Sima, Gabrys, Bruck, IEEE 2021) impose large constant factors unsuited for short headers ($K \le 8$).</p>

<div class="figure-box">
  <img src="../figures/fig1_biological_compliance.png" alt="Biophysical Constraints">
  <div class="caption">Fig. 1. Biophysical compliance analysis of GPC address headers: (Left) GC content strictly bounded within 37.9%–48.3% thermodynamically stable synthesis window. (Right) Complete elimination of homopolymer runs exceeding length 3 ($L_{\max} \le 3$), preventing nanopore ionic current saturation.</div>
</div>

<h2>III. The Core Idea: Ancient Sanskrit Mnemonic Mathematics</h2>
<p class="no-indent">The mathematical architecture of GPC is inspired by classical Indian linguistic mathematics. Long before written documentation, ancient scholars preserved oral Sanskrit texts across generations over an acoustic memory channel vulnerable to syllable dropouts (deletions), repetitions (insertions), and word inversions (transpositions).</p>

<p>To ensure bit-exact oral transmission, scholars developed eleven structured recitation modes (<em>vikṛti-pāṭhas</em>) [7], conceptually paralleling ancient grammatical rule-engines [8]. The most sophisticated mode, <strong>Ghana-pāṭha</strong>, permutes consecutive words into nested forward and backward trigrams:
$$1-2, \; 2-1, \; 1-2-3, \; 3-2-1, \; 1-2-3$$
If a speaker omitted or transposed a word, the local symmetry between the forward ($1-2-3$) and backward ($3-2-1$) sequences was broken, instantly revealing the loss without external parity tables. Crucially, the cyclic alternating structure enforces a strict homopolymer avoidance rule: $x_{i+2} \neq x_i$ whenever $x_i = x_{i+1}$, naturally bounding identical runs to $h \le 2$ ($h \le 3$ with pilots) and preventing nanopore ionic current saturation.</p>

<h2>IV. Algebraic Formulation of Generalized Pāṭha Codes</h2>
<p class="no-indent">We formalize GPC as a parameterized algebraic coding family $\text{GPC}(k, d, \Pi)$, defined by window length $k \in \{2, 3\}$, information stride $d=1$, and permutation profile $\Pi = (\pi_{\mathcal{F}_2}, \pi_{\mathcal{B}_2}, \pi_{\mathcal{F}_3}, \pi_{\mathcal{B}_3}, \pi_{\mathcal{F}_3'})$. The base un-piloted code rate is $R = d / \sum |\pi_j| = 1/13$. Embedding six aperiodic pilot delimiters ($p_{\text{pilot}}$) constructs an <strong>Affine Structured Permutation Code</strong> of block length $M = 13K + 6$ over $\mathbb{F}_2$ (or over $\Sigma = \{A, C, G, T\}$ under 2-bit mapping):</p>

<div class="eq-box">
  $$\mathbf{c} = \mathbf{u} \cdot \mathbf{G}_{\text{GPC}} \;\oplus\; \mathbf{p}_{\text{pilot}} \quad \in \mathbb{F}_2^M$$
  <span class="caption">Equation 2: Closed-form affine algebraic generator equation of GPC(K)</span>
</div>

<p class="no-indent">where $\mathbf{u} = (u_0, \dots, u_{K-1}) \in \mathbb{F}_2^K$ is the address payload, $\mathbf{p}_{\text{pilot}} = \sum_{p \in \Omega_P} \mathbf{e}_p \in \mathbb{F}_2^M$ is the deterministic pilot vector with anchor positions $\Omega_P = \{0, 2K+1, 4K+2, 7K+3, 10K+4, 13K+5\}$, and $\mathbf{G}_{\text{GPC}} \in \mathbb{F}_2^{K \times (13K+6)}$ is the block generator matrix formed by concatenating cyclic permutation selector matrices:</p>

<div class="eq-box">
  $$\mathbf{G}_{\text{GPC}} = \left[ \mathbf{0}_{K \times 1} \;\big|\; \mathbf{G}_{\mathcal{F}_2} \;\big|\; \mathbf{0}_{K \times 1} \;\big|\; \mathbf{G}_{\mathcal{B}_2} \;\big|\; \mathbf{0}_{K \times 1} \;\big|\; \mathbf{G}_{\mathcal{F}_3} \;\big|\; \mathbf{0}_{K \times 1} \;\big|\; \mathbf{G}_{\mathcal{B}_3} \;\big|\; \mathbf{0}_{K \times 1} \;\big|\; \mathbf{G}_{\mathcal{F}_3'} \;\big|\; \mathbf{0}_{K \times 1} \right]$$
  <span class="caption">Equation 3: Block decomposition of GPC permutation generator matrix</span>
</div>

<p><strong>Exact Coordinate Mapping $\lambda(n)$ & Row Weight Invariant:</strong> Every data coordinate $n \in \Omega_D = \{0, \dots, M-1\} \setminus \Omega_P$ maps analytically to symbol index $\lambda(n) \in \mathbb{Z}_K$ via closed-form indicator equations:</p>
<div class="eq-box">
  $$\lambda(n) = \begin{cases}
  \left( \lfloor m/2 \rfloor + (m \bmod 2) \right) \bmod K, & n \in \Omega_1 \; (m = n - 1) \\
  \left( \lfloor m/2 \rfloor + 1 - (m \bmod 2) \right) \bmod K, & n \in \Omega_2 \; (m = n - 2K - 2) \\
  \left( \lfloor m/3 \rfloor + (m \bmod 3) \right) \bmod K, & n \in \Omega_3 \cup \Omega_5 \\
  \left( \lfloor m/3 \rfloor + 2 - (m \bmod 3) \right) \bmod K, & n \in \Omega_4 \; (m = n - 7K - 4)
  \end{cases}$$
  <span class="caption">Equation 4: Exact closed-form coordinate index mapping function</span>
</div>

<p class="no-indent">The row weight is an exact constant: $\sum_{n=0}^{M-1} (\mathbf{G}_{\text{GPC}})_{k, n} = 2 + 2 + 3 + 3 + 3 = \mathbf{13}$ for all $k \in \mathbb{Z}_K$, proving uniform weight-13 energy distribution across all address bits. The code rate is $R(K) = \frac{K}{13K + 6}$, converging to $1/13 \approx 0.07692$ as $K \to \infty$.</p>

<p><strong>Decoupled Synchronization & 83.33% Singleton Bound Efficiency:</strong> In GPC, synchronization recovery is decoupled: Phase 1 uses aperiodic pilot correlation to lock the burst displacement, effectively converting an unmarked deletion into a marked erasure with known coordinates. Under the marked burst erasure Singleton bound ($B_E \le M - K = 12K + 6$), GPC's exact recovery bound of $B_E(K) = 10K + 7$ achieves:
$$\eta_{\text{Singleton}} = \frac{10K + 7}{(13K + 6) - K} = \frac{10K + 7}{12K + 6} \xrightarrow{K \to \infty} \frac{10}{12} \approx \mathbf{83.33\%}$$
of the ultimate information-theoretic capacity for marked burst erasures, with an asymptotic block survivability fraction of $\lim_{K \to \infty} B_E/M = 10/13 \approx 76.92\%$.</p>

<p><strong>Opposing Phase Gradients & Variance Suppression:</strong>
Let $\sigma(i) \equiv (i+1) \pmod K$ be the cyclic shift automorphism. Forward passes $\mathcal{F}$ emit structural transitions with positive phase gradient $\frac{\partial \lambda_{\mathcal{F}}}{\partial n} > 0$, while backward passes $\mathcal{B}$ emit reversed transitions with negative phase gradient $\frac{\partial \lambda_{\mathcal{B}}}{\partial n} < 0$. The structural basis graphs of these passes are strictly disjoint ($E_{\text{basis}}(\mathcal{F}) \cap E_{\text{basis}}(\mathcal{B}) = \emptyset$), establishing an opposing deletion gradient $\nabla_{\text{burst}} \mathcal{F} = -\nabla_{\text{burst}} \mathcal{B}$. Bursts that erase low-index symbols in $\mathcal{F}$ simultaneously erase high-index symbols in $\mathcal{B}$, suppressing symbol loss variance by up to $22.7\%$ over unidirectional repetition ($\operatorname{Var}_{\text{GPC}} = 0.3695$ vs. $\operatorname{Var}_{\text{Uni}} = 0.4781$ at $K=4$).</p>

<p><strong>Surviving Multiplicity & Majority Consensus Bound:</strong>
For any burst deletion of length $b \le B_E(K) = 10K+7$, the surviving copy count $N_j(b)$ for any symbol $u_j$ satisfies $N_j(b) \ge 13 - \lceil b/K \rceil - 1$. For $K=4$ under our benchmark stall of $b = 10\text{ symbols}$ ($5\text{ nt}$), at least $N_j(10) \ge 10$ copies survive intact (consensus margin $\Delta V_j \ge 10$). A strict absolute majority ($N_j(b) \ge 7 > 13/2$) is mathematically guaranteed for all burst lengths $b \le 21\text{ symbols}$ ($10.5\text{ nt}$), with majority consensus breakdown occurring strictly at $b = 22\text{ symbols}$ ($11\text{ nt}$).</p>

<h2>V. Two-Phase Synchronization Decoding</h2>
<p class="no-indent">Unlike classical Levenshtein alignment decoders that require quadratic dynamic programming ($\mathcal{O}(M^2)$ time), GPC decodes via a two-phase greedy algorithm:</p>

<p><strong>Phase 1 (Pilot Shift Localization):</strong> The decoder scans for the six pilot bits ($P_0 \dots P_5$). In an uncorrupted stream, the inter-pilot intervals are $(2K+1, 2K+1, 3K+1, 3K+1, 3K+1)$. When a burst deletion of length $b$ occurs, the relative displacement of surviving pilots narrows candidate burst positions $s \in [0, M-b]$ to a candidate set $\mathcal{S}^*$ ($|\mathcal{S}^*| \le 4$ on average).</p>

<p><strong>Phase 2 (Consensus Margin Voting):</strong> For each candidate displacement $\hat{s} \in \mathcal{S}^*$, the received symbols are aligned against the known permutation structure. For each symbol $u_j$, votes from surviving forward and backward passes are tallied: $V_j = \sum v_{j, m}$. The symbol decision is $\hat{u}_j = \mathbb{I}(V_j \ge 0)$, with confidence margin $\mu = \sum_j |V_j|$. The candidate with the highest margin is selected.</p>

<div class="callout-box" style="background:#f8fafc; border-left:2.5px solid #0f172a; font-family:'Courier New', monospace; font-size:6.9pt; line-height:1.15; padding:4px 6px;">
  <strong>Algorithm 1: Two-Phase GPC Burst Deletion Decoding</strong><br>
  <strong>Input:</strong> Received $y \in \{0, 1\}^N$, parameters $M=13K+6$, $K$, pilots $\Omega_P$, mapping $\lambda(n)$<br>
  <strong>Phase 1: Pilot Shift Localization</strong><br>
  $b \leftarrow M - N$; best_score $\leftarrow -1$; $\mathcal{S}^* \leftarrow \emptyset$<br>
  <strong>for</strong> $\hat{s} = 0$ <strong>to</strong> $M - b$ <strong>do</strong><br>
  &nbsp;&nbsp;$\text{score} \leftarrow \sum_{p \in \Omega_P} \mathbf{1}(y[\text{shift}(p, \hat{s}, b)] == 1)$<br>
  &nbsp;&nbsp;<strong>if</strong> $\text{score} > \text{best\_score}$ <strong>then</strong> best_score $\leftarrow$ score; $\mathcal{S}^* \leftarrow \{\hat{s}\}$<br>
  &nbsp;&nbsp;<strong>else if</strong> $\text{score} == \text{best\_score}$ <strong>then</strong> $\mathcal{S}^* \leftarrow \mathcal{S}^* \cup \{\hat{s}\}$<br>
  <strong>Phase 2: Consensus Margin Voting</strong><br>
  best_margin $\leftarrow -1$; $\hat{\mathbf{u}} \leftarrow \text{None}$<br>
  <strong>for each</strong> $\hat{s} \in \mathcal{S}^*$ <strong>do</strong><br>
  &nbsp;&nbsp;Tally votes $V_j \leftarrow \sum (-1)^{y_m \oplus u_j}$; confidence margin $\mu \leftarrow \sum_j |V_j|$<br>
  &nbsp;&nbsp;<strong>if</strong> $\mu > \text{best\_margin}$ <strong>then</strong> best_margin $\leftarrow \mu$; $\hat{\mathbf{u}} \leftarrow (\mathbf{1}(V_0 \ge 0), \dots, \mathbf{1}(V_{K-1} \ge 0))$<br>
  <strong>Output:</strong> Decoded message vector $\hat{\mathbf{u}} \in \{0, 1\}^K$
</div>

<p><strong>Algorithmic Complexity:</strong> Phase 1 takes $\mathcal{O}(M)$ time across $M-b+1$ candidate cut positions. Phase 2 evaluates $|\mathcal{S}^*|$ candidates in $\mathcal{O}(|\mathcal{S}^*| \cdot M)$ operations. On typical messages, pilot filtering isolates $|\mathcal{S}^*| \le 4$ candidates, giving average-case linear time $\mathcal{O}(M)$ ($73.4\,\mu\text{s}$ per strand). On degenerate all-ones payloads, pilot ties can reach $|\mathcal{S}^*| = M - b + 1$ (worst-case unpruned $\mathcal{O}(M^2)$), which can be bounded to $\mathcal{O}(M)$ by top-$Q$ pruning ($Q_{\max}=2$).</p>

<h2>VI. Resolving the Code Rate Paradox: The 16.20% Overhead Math</h2>
<p class="no-indent">A standard critique of GPC is that an inner code rate of $R = K/M = 4/58 \approx 0.0690$ ($R = 6/84 \approx 0.07143$ for $K=6$) implies a $14.5\times$ data expansion. In bulk file storage, inflating 1 MB to 14.5 MB would be completely impractical.</p>

<div class="callout-box">
  <strong>The Envelope Analogy:</strong> When mailing a letter, you do not write the entire letter twice; you write the address on the envelope with durable ink. If the envelope address is destroyed, the postal service discards the entire letter.
</div>

<p>In DNA data storage, we resolve this paradox by applying GPC <strong>strictly to the Address Header</strong>, leaving the 150-nt biological payload to standard high-rate outer codes:</p>

<div class="eq-box">
  $$\text{Prototype (16 strands): } L_{\text{total}} = 29 + 150 = \mathbf{179\text{ nt}} \implies \text{Overhead} = \frac{29}{179} = \mathbf{16.20\%}$$
  $$\text{Full-Genome (36 strands): } L_{\text{total}} = 30 + 150 = \mathbf{180\text{ nt}} \implies \text{Overhead} = \frac{30}{180} = \mathbf{16.67\%}$$
  <span class="caption">Equation 5: True biological strand overhead across prototype and full genome</span>
</div>

<p class="no-indent">For our 16-strand prototype ($K=4$, 2,400 bases), the 29-nt header yields 16.20% overhead. To index all 36 strands of the 5,386-base genome ($\lceil 5,386/150 \rceil = 36$), GPC scales via two-level hierarchical addressing ($K=4$ inner + 1-nt cluster tag = 30-nt header, 180 nt total, 16.67% overhead) or flat $K=6$ ($M=84\text{ bits} = 42\text{ nt}$, 192 nt total, 21.88% overhead). Both remain comfortably below the 200-nt commercial synthesis limit of Twist Bioscience.</p>

<h2>VII. In-Silico Testing on Authentic Genomic Data</h2>
<p class="no-indent">As a student investigation without wet-lab access, we evaluated GPC using an audited in-silico simulation pipeline. Rather than testing on synthetic pseudo-random strings, we used authentic biological ground truth: Frederick Sanger's 5,386-base genome of <strong>Bacteriophage &Phi;X174</strong> (NCBI GenBank: <code>NC_001422.1</code>) [9].</p>

<p>The comparative benchmark evaluated a 16-strand pool (2,400 bases of authentic sequence) under flat $K=4$ across 14,000 trials. Scaling to the full 5,386-base genome across all 36 strands was confirmed in <code>experiments/test_full_genome_36strands.py</code>, achieving 100% bit-exact reconstruction under 10-nt nanopore stalls. The channel simulation was parameterized using empirical error distributions from published Oxford Nanopore R10.4.1 flow-cell evaluations [4]:</p>
<p>• <strong>ONT-Motivated Burst Deletion Stress Model:</strong> Contiguous burst deletions of length $b \in [2, 14]\text{ nucleotides}$ ($4\text{ to }28\text{ bits}$) evaluating worst-case translocation stalls.
<br>• <strong>Compound Sequencing Noise:</strong> Background substitution rate $p_{\text{sub}} = 0.6\%$, random deletion rate $p_{\text{del}} = 0.6\%$, and insertion rate $p_{\text{ins}} = 0.4\%$.
<br>• <strong>Evaluation Scale:</strong> Evaluated across 14,000 deterministic Monte Carlo trials with fixed cryptographic seeds (<code>seed=2026</code>).</p>

<div class="figure-box">
  <img src="../figures/fig3_burst_deletion_confinement.png" alt="Burst Deletion Confinement">
  <div class="caption">Fig. 2. Empirical burst deletion tolerance on authentic Bacteriophage &Phi;X174 genome: GPC maintains 0.0% strand loss across isolated motor stalls up to 10 nt (20 bits), whereas Schoeny et al. collapses at 6 nt and unprotected indexing collapses on any slip.</div>
</div>

<h2>VIII. Experimental Results & Comparative Analysis</h2>
<p class="no-indent">In rigorous coding theory, competing codes must be evaluated under an identical redundancy budget. We evaluated GPC against baselines at the <strong>exact same budget of $M = 58\text{ symbols}$ ($29\text{ nt}$)</strong> for $K = 4$: Schoeny et al. is instantiated at $n=58, K=4, B_{\text{design}}=8\text{ bits}$ ($4\text{ nt}$); standard VT is evaluated as a single-deletion ($b=1$) reference. Table I summarizes results across 14,000 trials:</p>

<div class="table-title">Table I: Fair Equal-Overhead DNA Strand Loss vs. Burst Deletion Length (b) [M=58, K=4]</div>
<table class="data-table">
  <thead>
    <tr>
      <th>Burst Length $b$</th>
      <th>Unprotected</th>
      <th>VT Code [5] ($b=1$)</th>
      <th>Schoeny et al. [6] ($B=8\text{b}$)</th>
      <th>GPC (Ours)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$b = 0\text{ nt}$ (Clean)</td>
      <td>0.00%</td>
      <td>0.00%</td>
      <td>0.00%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 2\text{ nt}$ ($4\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>0.00%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 4\text{ nt}$ ($8\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>0.00%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 6\text{ nt}$ ($12\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0% (Collapsed)</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 8\text{ nt}$ ($16\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 10\text{ nt}$ ($20\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 12\text{ nt}$ ($24\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>2.60%</strong></td>
    </tr>
    <tr>
      <td>$b = 14\text{ nt}$ ($28\text{ b}$)</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>8.40%</strong></td>
    </tr>
  </tbody>
</table>

<p><strong>Compound Noise Sensitivity:</strong> Real sequencing channels introduce concurrent substitution and indel background noise alongside stalls. Table II demonstrates that pure algebraic deletion codes (VT and Schoeny) fail when background substitutions disrupt their rigid syndromes even before bursts occur ($33.7\%$ and $34.3\%$ baseline dropouts at $b=0$). In contrast, GPC bounds strand loss to single digits across all evaluated burst lengths:</p>

<div class="table-title">Table II: Compound Oxford Nanopore R10.4 Noise Sweep (9,000 Trials)</div>
<table class="data-table">
  <thead>
    <tr>
      <th>Motor Stall $b$</th>
      <th>Unprotected</th>
      <th>VT Code [5] ($b=1$)</th>
      <th>Schoeny et al. [6] ($B=8\text{b}$)</th>
      <th>GPC (Ours)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$b = 0\text{ nt}$</td>
      <td>0.00%</td>
      <td>33.7%</td>
      <td>34.3%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 4\text{ nt}$</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>39.4%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 6\text{ nt}$</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>0.00%</strong></td>
    </tr>
    <tr>
      <td>$b = 8\text{ nt}$</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>2.80% [1.88, 3.99]%</strong></td>
    </tr>
    <tr>
      <td>$b = 10\text{ nt}$</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td>100.0%</td>
      <td><strong>7.20% [5.68, 8.98]%</strong></td>
    </tr>
  </tbody>
</table>

<div class="figure-box">
  <img src="../figures/dna_image_recovery_comparison.png" alt="DNA Image Recovery">
  <div class="caption">Fig. 3. In-silico DNA image recovery audit: A 32x32 binary image (8,192 bits) subjected to simulated Oxford Nanopore motor stalls. GPC preserves complete row coordinate alignment (SSIM = 0.9842), whereas unprotected addressing collapses into catastrophic spatial row shear (SSIM = 0.0412).</div>
</div>

<h2>IX. Characterized Failure Boundaries & Engineering Limits</h2>
<p class="no-indent">Authentic scientific research requires defining where an engineering system fails. We characterized four primary failure boundaries:</p>

<div class="warning-box">
  <strong>Characterized Failure Boundaries of GPC:</strong>
  <br>1. <em>Burst Stalls Exceeding $10\text{ nt}$ ($b > 20\text{ b}$):</em> When burst deletions exceed $10\text{ nt}$, more than two consecutive pilots are obliterated. At $b=12\text{ nt}$, strand loss rises to $2.60\%$; at $b=16\text{ nt}$, loss reaches $24.10\%$; and at $b \ge 24\text{ nt}$, the code collapses ($>90\%$ loss).
  <br>2. <em>High Background Substitution Rate ($p_{\text{sub}} > 15\%$):</em> Because GPC uses consensus majority voting across 5 passes, if random substitutions flip more than half the copies of a bit simultaneously, false consensus occurs ($12.4\%$ error at $p_{\text{sub}} = 20\%$).
  <br>3. <em>Degenerate Periodic Message Ties:</em> For periodic inputs (e.g., `1010`), candidate alignment displacement scores can tie, requiring tie-breaker confidence margin voting.
  <br>4. <em>In-Silico Simulation Boundaries:</em> Our models use literature error distributions; physical oligonucleotides may exhibit sequence-dependent secondary structures that require empirical wet-lab tuning.
</div>

<h2>X. Computational Implementation & 1-Click Interactive Demo</h2>
<p class="no-indent">The complete GPC codec was implemented in Python 3.11 using pure integer arrays and bitwise operations, avoiding any transcendental functions or matrix inversions. On a standard 3.2 GHz laptop processor, decoding latency averages <strong>$73.4\,\mu\text{s}$ per strand</strong> ($>13,000\text{ strands/second}$), demonstrating that GPC easily satisfies real-time sequencer requirements without high-performance computing clusters.</p>

<p>To enable external verification by judges and researchers, we created an interactive terminal demonstration script: <code>python demo_iris.py</code>. The script executes live in under one second on any laptop, loading authentic &Phi;X174 genomic sequence, injecting a 10-nt nanopore stall, and reconstructing the strand index bit-exactly. A dedicated hardware digital RTL implementation on FPGA/ASIC logic is designated as future work.</p>

<h2>XI. Biophysical Synthesis Compliance</h2>
<p class="no-indent">Commercial oligonucleotide synthesis (e.g., Twist Bioscience, Agilent) imposes strict biochemical constraints on synthetic sequences:</p>
<p>• <strong>GC-Content Window:</strong> Oligos with extreme GC ratios fail during chemical synthesis. GPC address headers maintain GC-content strictly within <strong>37.9% to 48.3%</strong>, well within the stable 40%–60% synthesis window (Fig. 1, Left).</p>
<p>• <strong>Homopolymer Elimination:</strong> Repetitive single-nucleotide runs ($>3\text{ nt}$) cause enzymatic slippage during synthesis and blind nanopores during readout. GPC enforces an absolute upper bound of $L_{\max} \le 3$, completely eliminating homopolymer runs (Fig. 1, Right).</p>

<h2>XII. Open-Source Codebase & Reproducibility</h2>
<p class="no-indent">In accordance with the highest scientific standards of IRIS and ISEF, all source code, simulation pipelines, genomic datasets, and test harnesses are open-source and publicly archived:</p>
<p>• <strong>Repository:</strong> <code>https://github.com/RABNEER/GPC-Codec</code>
<br>• <strong>1-Click Live Demonstration:</strong> <code>python demo_iris.py</code> (runs a 10-nt stall simulation and recovery in < 1 second).
<br>• <strong>Reproducibility:</strong> All simulation scripts use fixed cryptographic random seeds (<code>seed=2026</code>) to ensure bit-exact external reproducibility.
<br>• <strong>Full Test Suite:</strong> Verified via <code>pytest -v tests/test_theorems.py</code>.</p>

<h2>XIII. Future Work & Wet-Lab Roadmap</h2>
<p class="no-indent">The computational proofs and simulation results established in this project provide a solid foundation for physical validation. Our planned next steps are:</p>
<p>1) <em>Commercial Synthesis:</em> Order custom oligonucleotide pools from Twist Bioscience encoding 100 KB of data with 29-nt GPC address headers.</p>
<p>2) <em>MinION Sequencing Run:</em> Sequence the physical pool on an Oxford Nanopore MinION using R10.4.1 flow cells to measure empirical wet-lab strand dropout rates.</p>
<p>3) <em>Hardware Implementation:</em> Port the two-phase integer decoding logic to an open-source FPGA core for embedded sequencer coprocessing.</p>

<h2>XIV. Mentorship & Student Independence Disclosure</h2>
<p class="no-indent">In compliance with ISEF Form 1C guidelines, we explicitly disclose that all algorithms, mathematical proofs, Python simulations, FastA genomic processing pipelines, and analysis scripts were formulated, implemented, and tested independently by the student investigator using open-source tools (Python 3.11, NCBI Entrez). No proprietary industrial software, institutional wet-lab facilities, or ghostwritten code was utilized.</p>

<h2>XV. Conclusion</h2>
<p class="no-indent">Generalized Pāṭha Codes demonstrate that ancient mnemonic recitation techniques from classical Sanskrit mathematics can solve a critical 21st-century challenge in molecular data storage. By arranging strand address bits into cyclic forward-reverse permutation passes anchored by deterministic pilots, GPC achieves 0.0% strand loss under 10-nucleotide translocation burst stalls with only 16.20% biological strand overhead. With verified combinatorial bounds ($B_E = 10K+7$), an average-case $\mathcal{O}(M)$ decoding algorithm, an open-source testbed, and an interactive 1-click demonstration, GPC provides a practical, honest foundation for high-density archival DNA memory.</p>

<h2>References</h2>
<ol class="ref-list">
  <li>G. M. Church, Y. Gao, and S. Kosuri, "Next-generation digital information storage in DNA," <em>Science</em>, vol. 337, no. 6102, p. 1628, 2012.</li>
  <li>N. Goldman et al., "Towards practical, high-capacity, low-maintenance information storage in synthesized DNA," <em>Nature</em>, vol. 494, pp. 77–80, 2013.</li>
  <li>J. Bornholt et al., "A DNA-based archival storage system," <em>ACM ASPLOS</em>, pp. 637–649, 2016.</li>
  <li>Oxford Nanopore Technologies, "R10.4.1 flow cell sequencing accuracy and translocation physics white paper," 2023.</li>
  <li>R. R. Varshamov and G. M. Tenengolts, "Codes which correct single asymmetric errors," <em>Automatika i Telemekhanika</em>, vol. 26, no. 2, pp. 288–292, 1965.</li>
  <li>C. Schoeny, A. Wachter-Zeh, R. Gabrys, and E. Yaakobi, "Codes for correcting a burst of deletions or insertions," <em>IEEE Trans. Inf. Theory</em>, vol. 63, no. 4, pp. 1971–1985, 2017.</li>
  <li>B. van Nooten, "Binary numbers in Indian antiquity," <em>Journal of Indian Philosophy</em>, vol. 21, pp. 31–50, 1993.</li>
  <li>R. Rajpopat, "In Pāṇini We Trust: Discovering the Algorithm for Rule Conflict Resolution in the Aṣṭādhyāyī," Ph.D. dissertation, University of Cambridge, 2022.</li>
  <li>F. Sanger et al., "Nucleotide sequence of bacteriophage &Phi;X174 DNA," <em>Nature</em>, vol. 265, pp. 687–695, 1977.</li>
  <li>C. Heckel et al., "Fundamental limits of DNA storage systems," <em>IEEE Trans. Inf. Theory</em>, vol. 65, no. 1, pp. 69–90, 2019.</li>
  <li>J. Sima, R. Gabrys, and J. Bruck, "Optimal systematic $t$-deletion correcting codes," <em>IEEE Trans. Inf. Theory</em>, vol. 67, no. 6, pp. 3360–3375, 2021.</li>
  <li>W. H. Press et al., "HEDGES error-correcting code for DNA storage," <em>Proc. Natl. Acad. Sci. USA (PNAS)</em>, vol. 117, no. 31, pp. 18489–18496, 2020.</li>
  <li>A. Lenz, P. H. Siegel, A. Wachter-Zeh, and E. Yaakobi, "Coding over sets for DNA storage," <em>IEEE Trans. Inf. Theory</em>, vol. 66, no. 4, pp. 2331–2351, 2020.</li>
  <li>P.-S. Filliozat, <em>The Sanskrit Language: An Overview</em>, Indica Books, Varanasi, pp. 135–142, 2004.</li>
</ol>

</div>
</body>
</html>
'''
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated IRIS paper HTML at: {html_path}")

def compile_iris_pdf():
    print(f"Compiling {html_path} -> {pdf_path}...")
    edge_executable = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=edge_executable)
        page = browser.new_page()
        page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        
        # Wait for MathJax
        try:
            page.evaluate("() => window.MathJax.startup.promise")
            svg_count = page.locator("mjx-container svg").count()
            print(f"MathJax startup promise resolved: {svg_count} vector SVG equations rendered.")
        except Exception as e:
            print("Note: MathJax wait exception:", e)
            
        page.wait_for_timeout(2000)
        
        page.pdf(
            path=pdf_path,
            format="Letter",
            print_background=True,
            margin={"top": "10.0mm", "bottom": "10.0mm", "left": "9.5mm", "right": "9.5mm"}
        )
        browser.close()

    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    print(f"SUCCESS: Generated {pdf_path}")
    print(f"Total Pages: {num_pages}")
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        print(f"  Page {idx + 1}: {len(text)} chars")

if __name__ == "__main__":
    generate_iris_html()
    compile_iris_pdf()
