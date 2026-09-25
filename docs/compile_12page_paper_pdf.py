"""
Compile 12-Page Master Research Paper to Publication-Grade PDF
===============================================================
Uses Playwright and Microsoft Edge to compile `papers/GPC_Full_Research_Paper_12_Pages.html`
into `papers/GPC_Full_Research_Paper_12_Pages.pdf` with MathJax vector SVG typography,
high-res figures, and precise 12-page budget verification.
"""

import os
import sys
import shutil
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

def compile_12page_paper():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    papers_dir = os.path.join(root_dir, "papers")
    
    html_path = os.path.join(papers_dir, "GPC_Full_Research_Paper_12_Pages.html")
    pdf_path = os.path.join(papers_dir, "GPC_Full_Research_Paper_12_Pages.pdf")
    
    edge_executable = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    if not os.path.exists(html_path):
        print(f"Error: HTML template not found at {html_path}")
        sys.exit(1)
        
    # Regenerate master HTML with golden 12-page parameters
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from docs.assemble_master_12page_monograph import assemble_master_html
    assemble_master_html()

    print(f"Compiling {html_path} -> {pdf_path}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=edge_executable)
        page = browser.new_page()
        page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        
        # Wait for MathJax to finish compiling equations into vector SVGs
        try:
            page.evaluate("() => window.MathJax.startup.promise")
            svg_count = page.locator("mjx-container svg").count()
            print(f"MathJax startup promise resolved: {svg_count} vector SVG equations rendered.")
        except Exception as e:
            print("Note: MathJax wait exception:", e)
        
        # Settle layout
        page.wait_for_timeout(2000)
        
        page.pdf(
            path=pdf_path,
            format="Letter",
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
        )
        browser.close()
    
    file_size_kb = os.path.getsize(pdf_path) / 1024
    
    # Audit page count with fitz
    import fitz
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    print(f"SUCCESS: Generated {pdf_path} ({file_size_kb:.1f} KB)")
    print(f"Total Pages: {num_pages}")
    for i, p in enumerate(doc):
        print(f"  Page {i+1}: {len(p.get_text())} chars")
    
    if num_pages == 12:
        print("EXACT MATCH: The document is strictly 12 pages!")
    else:
        print(f"PAGE COUNT NOTICE: Document has {num_pages} pages (target: 12). Adjusting required.")

if __name__ == "__main__":
    compile_12page_paper()
