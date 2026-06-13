"""Convert rapport-synthetique.md to PDF using WeasyPrint."""
import markdown
from weasyprint import HTML
import os

REPORTS_DIR = "/home/ubuntu/MYP/PhishGuard/reports"
MD_PATH = os.path.join(REPORTS_DIR, "rapport-synthetique.md")
PDF_PATH = os.path.join(REPORTS_DIR, "rapport-synthetique.pdf")

# Read markdown
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert to HTML
html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code", "toc"])

# Wrap in styled HTML document
html_doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>PhishGuard — Rapport Synthétique</title>
<style>
    @page {{
        size: A4;
        margin: 2cm 2.5cm;
        @bottom-center {{
            content: counter(page);
            font-size: 10px;
            color: #666;
        }}
    }}
    body {{
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #1a1a1a;
        max-width: 100%;
    }}
    h1 {{
        font-size: 22pt;
        color: #0f172a;
        border-bottom: 3px solid #0ea5e9;
        padding-bottom: 8px;
        margin-top: 30px;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 16pt;
        color: #1e293b;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 4px;
        margin-top: 24px;
        page-break-after: avoid;
    }}
    h3 {{
        font-size: 13pt;
        color: #334155;
        margin-top: 18px;
        page-break-after: avoid;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 10pt;
    }}
    th {{
        background: #0f172a;
        color: white;
        padding: 8px 10px;
        text-align: left;
        font-weight: 600;
    }}
    td {{
        padding: 6px 10px;
        border-bottom: 1px solid #e2e8f0;
    }}
    tr:nth-child(even) td {{
        background: #f8fafc;
    }}
    tr:hover td {{
        background: #e0f2fe;
    }}
    code {{
        background: #f1f5f9;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 9pt;
        font-family: 'Consolas', 'Monaco', monospace;
    }}
    pre {{
        background: #1e293b;
        color: #e2e8f0;
        padding: 14px;
        border-radius: 6px;
        font-size: 9pt;
        overflow-x: auto;
        line-height: 1.4;
    }}
    pre code {{
        background: transparent;
        padding: 0;
        color: inherit;
    }}
    blockquote {{
        border-left: 4px solid #0ea5e9;
        margin: 12px 0;
        padding: 8px 16px;
        background: #f0f9ff;
        font-style: italic;
    }}
    ul, ol {{
        padding-left: 24px;
    }}
    li {{
        margin: 4px 0;
    }}
    strong {{
        color: #0f172a;
    }}
    hr {{
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 20px 0;
    }}
    .title-page {{
        text-align: center;
        padding-top: 120px;
    }}
    .title-page h1 {{
        font-size: 28pt;
        border-bottom: none;
        color: #0f172a;
    }}
    .title-page .subtitle {{
        font-size: 14pt;
        color: #64748b;
        margin-top: 8px;
    }}
    .title-page .author {{
        font-size: 12pt;
        color: #94a3b8;
        margin-top: 40px;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

# Generate PDF
HTML(string=html_doc, base_url=REPORTS_DIR).write_pdf(PDF_PATH)
print(f"✅ PDF generated: {PDF_PATH}")
print(f"   Size: {os.path.getsize(PDF_PATH) / 1024:.0f} KB")
