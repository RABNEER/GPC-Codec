"""
Compile GPC Mathematical Formulas & Execution Blueprint to PDF
==============================================================
Uses Playwright and Microsoft Edge to compile `formulas_and_solutions_blueprint.html`
into `GPC_Mathematical_Formulas_and_Execution_Blueprint.pdf`.
"""

import os
import shutil
from playwright.sync_api import sync_playwright

def compile_blueprint():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    html_path = os.path.join(script_dir, "formulas_and_solutions_blueprint.html")
    pdf_path_docs = os.path.join(script_dir, "GPC_Mathematical_Formulas_and_Execution_Blueprint.pdf")
    pdf_path_root = os.path.join(root_dir, "GPC_Mathematical_Formulas_and_Execution_Blueprint.pdf")
    
    edge_executable = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    print(f"Compiling {html_path} -> {pdf_path_docs}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=edge_executable)
        page = browser.new_page()
        page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        # Wait for MathJax to finish compiling equations into vector SVGs
        try:
            page.wait_for_selector("mjx-container svg", timeout=15000)
            print("MathJax vector SVG equations detected and rendered.")
        except Exception as e:
            print("Note: MathJax selector wait timed out, proceeding...")
        page.wait_for_timeout(1500)
        page.pdf(
            path=pdf_path_docs,
            format="Letter",
            print_background=True,
            margin={"top": "10mm", "bottom": "12mm", "left": "12mm", "right": "12mm"}
        )
        browser.close()
    
    # Mirror to root directory for easy top-level access
    shutil.copy2(pdf_path_docs, pdf_path_root)
    file_size_kb = os.path.getsize(pdf_path_docs) / 1024
    print(f"SUCCESS: Generated {pdf_path_docs} and mirrored to root ({file_size_kb:.1f} KB)")

if __name__ == "__main__":
    compile_blueprint()
