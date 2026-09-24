"""
Compile DNA Storage Testbed Experimental Report to PDF
======================================================
Uses Playwright and Microsoft Edge to compile `dna_storage_experimental_report.html`
into `DNA_Storage_Experimental_Report.pdf` with MathJax vector SVG typography.
"""

import os
import shutil
from playwright.sync_api import sync_playwright

def compile_dna_report():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    html_path = os.path.join(script_dir, "dna_storage_experimental_report.html")
    pdf_path_docs = os.path.join(script_dir, "DNA_Storage_Experimental_Report.pdf")
    
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
        
        # Give an extra moment for images and styles to settle
        page.wait_for_timeout(2000)
        
        page.pdf(
            path=pdf_path_docs,
            format="Letter",
            print_background=True,
            margin={"top": "10mm", "bottom": "12mm", "left": "12mm", "right": "12mm"}
        )
        browser.close()
    
    # Mirror to papers directory for centralized archival access
    papers_dir = os.path.join(root_dir, "papers")
    if os.path.exists(papers_dir):
        shutil.copy2(pdf_path_docs, os.path.join(papers_dir, "DNA_Storage_Experimental_Report.pdf"))
    file_size_kb = os.path.getsize(pdf_path_docs) / 1024
    print(f"SUCCESS: Generated {pdf_path_docs} and mirrored to papers/ ({file_size_kb:.1f} KB)")

if __name__ == "__main__":
    compile_dna_report()
