# Research Papers & Technical Reports Dossier

This directory archives all formal academic publications, technical monographs, and experimental reports for **Generalized Patha Codes (GPC)**.

---

## 📑 Master Publications Index

| File | Type | Pages | Description |
|---|---|:---:|---|
| **[`GPC_Comprehensive_Research_Paper.pdf`](GPC_Comprehensive_Research_Paper.pdf)** | **Primary Journal Paper** | **4** | **Master IRIS National Science Fair 2026 Submission Manuscript.** Contains full theoretical theorems, SOTA benchmark comparisons, 161k+ audited machine trials, and physical domain testbeds. |
| **[`GPC_Comprehensive_Research_Paper.md`](GPC_Comprehensive_Research_Paper.md)** | Full Markdown Source | - | Complete textual manuscript formatted with GitHub Flavored Markdown and KaTeX math. |
| **[`GPC_Comprehensive_Research_Paper.html`](GPC_Comprehensive_Research_Paper.html)** | Master IEEE HTML Source | - | High-density IEEE 2-column production template with vector SVG MathJax equations. |
| **[`GPC_Mathematical_Formulas_and_Execution_Blueprint.pdf`](GPC_Mathematical_Formulas_and_Execution_Blueprint.pdf)** | Technical Monograph | 4 | Complete mathematical derivations, coordinate span calculations, and execution architecture blueprint. |
| **[`DNA_Storage_Experimental_Report.pdf`](DNA_Storage_Experimental_Report.pdf)** | Domain Testbed Report | 4 | In silico synthetic DNA storage testbed with Goldman (Nature 2013) base-3 encoding and Nanopore indel simulations. |
| **[`Swarm_Telemetry_Experimental_Report.pdf`](Swarm_Telemetry_Experimental_Report.pdf)** | Domain Testbed Report | 4 | 8-UAV quadcopter swarm 3D kinematic telemetry simulation under RF jamming blackouts. |
| **[`paper_publication.pdf`](paper_publication.pdf)** | IEEE Conference Paper | 3 | Concise 3-page preliminary IEEE conference format paper. |

---

## 🔬 Compilation Instructions
All PDFs can be rebuilt from their respective HTML templates using the headless compiler scripts located in `docs/`:

```bash
# Compile Master 4-Page Journal Paper:
python docs/compile_comprehensive_paper_pdf.py

# Compile Mathematical Blueprint:
python docs/compile_blueprint_pdf.py

# Compile DNA Storage Testbed Report:
python docs/compile_dna_report_pdf.py

# Compile Swarm Telemetry Testbed Report:
python docs/compile_swarm_report_pdf.py
```
