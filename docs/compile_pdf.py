"""
Compile IEEE Research Paper to Publication-Grade PDF
=====================================================
Uses Playwright and Microsoft Edge to compile `paper_ieee.html` into `paper_publication.pdf`
with full CSS two-column formatting, KaTeX equations, and high-res vector SVGs.
"""

import os
import shutil
from playwright.sync_api import sync_playwright

def build_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    html_path = os.path.join(script_dir, "paper_ieee.html")
    pdf_path_docs = os.path.join(script_dir, "paper_publication.pdf")
    
    edge_executable = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    print(f"Compiling {html_path} -> {pdf_path_docs}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=edge_executable)
        page = browser.new_page()
        page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        page.pdf(
            path=pdf_path_docs,
            format="Letter",
            print_background=True,
            margin={"top": "15mm", "bottom": "18mm", "left": "14mm", "right": "14mm"}
        )
        browser.close()
    
    # Mirror to papers directory
    papers_dir = os.path.join(root_dir, "papers")
    if os.path.exists(papers_dir):
        shutil.copy2(pdf_path_docs, os.path.join(papers_dir, "paper_publication.pdf"))
    print("SUCCESS: Generated paper_publication.pdf and mirrored to papers/.")

if __name__ == "__main__":
    build_pdf()
