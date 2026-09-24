"""
Compile Comprehensive Research Paper to Archival IEEE PDF
=========================================================
Uses Playwright and Microsoft Edge to compile `GPC_Comprehensive_Research_Paper.html`
into `GPC_Comprehensive_Research_Paper.pdf` with MathJax vector SVG typography.
"""

import os
import shutil
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

def compile_paper():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    html_path = os.path.join(script_dir, "GPC_Comprehensive_Research_Paper.html")
    pdf_path_docs = os.path.join(script_dir, "GPC_Comprehensive_Research_Paper.pdf")
    pdf_path_root = os.path.join(root_dir, "GPC_Comprehensive_Research_Paper.pdf")
    
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
        page.wait_for_timeout(3000)
        
        page.pdf(
            path=pdf_path_docs,
            format="Letter",
            print_background=True,
            margin={"top": "9mm", "bottom": "9mm", "left": "10mm", "right": "10mm"}
        )
        browser.close()
    
    # Mirror to root directory and papers directory for easy access
    shutil.copy2(pdf_path_docs, pdf_path_root)
    papers_dir = os.path.join(root_dir, "papers")
    if os.path.exists(papers_dir):
        shutil.copy2(pdf_path_docs, os.path.join(papers_dir, "GPC_Comprehensive_Research_Paper.pdf"))
    file_size_kb = os.path.getsize(pdf_path_docs) / 1024
    
    # Audit page count with pypdf
    reader = PdfReader(pdf_path_docs)
    num_pages = len(reader.pages)
    print(f"SUCCESS: Generated {pdf_path_docs} and mirrored to root ({file_size_kb:.1f} KB)")
    print(f"Total Pages: {num_pages}")
    
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"  Page {idx + 1}: {len(text)} characters extracted")

if __name__ == "__main__":
    compile_paper()
