import PyPDF2
import os

pdf_file = "./projet_fin_semestre_phishing_distribue.pdf"
text = ""
with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    for i, page in enumerate(reader.pages):
        text += f"\n--- PAGE {i+1} ---\n"
        text += page.extract_text() + "\n"

with open("pdf_full_text.txt", "w") as f:
    f.write(text)

print(f"Extracted {len(reader.pages)} pages, {len(text)} characters")
print(text)
