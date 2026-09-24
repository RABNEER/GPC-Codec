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
        
    print(f"Compiling {html_path} -> {pdf_path}...")
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
        page.wait_for_timeout(3500)
        
        page.pdf(
            path=pdf_path,
            format="Letter",
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
        )
        browser.close()
    
    file_size_kb = os.path.getsize(pdf_path) / 1024
    
    # Audit page count with pypdf
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    print(f"SUCCESS: Generated {pdf_path} ({file_size_kb:.1f} KB)")
    print(f"Total Pages: {num_pages}")
    
    if num_pages == 12:
        print("EXACT MATCH: The document is strictly 12 pages!")
    else:
        print(f"PAGE COUNT NOTICE: Document has {num_pages} pages (target: 12). Adjusting required.")

if __name__ == "__main__":
    compile_12page_paper()
