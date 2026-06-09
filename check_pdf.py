import os
import PyPDF2
import re

# Find the first PDF file in the current directory and subdirectories
pdf_file = None
for root, dirs, files in os.walk('.'):
    # Skip .git directory
    if '.git' in root:
        continue
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_file = os.path.join(root, file)
            break
    if pdf_file:
        break

if not pdf_file:
    print("No PDF file found.")
    exit(1)

# Extract text from PDF
text = ""
with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        text += page.extract_text() + "\n"

# Preprocess text: get words (alphanumeric, length>=3) and lowercase
words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
words = [w.lower() for w in words]

# Define stop words (a small set)
stop_words = {'the', 'and', 'of', 'to', 'a', 'in', 'is', 'it', 'that', 'for', 'was', 'with', 'as', 'on', 'at', 'but', 'be', 'by', 'or', 'are', 'this', 'have', 'has', 'had', 'not', 'they', 'we', 'you', 'i', 'he', 'she', 'his', 'her', 'its', 'our', 'your', 'their', 'me', 'him', 'us', 'them'}

# Get unique keywords from PDF, excluding stop words
pdf_keywords = set([w for w in words if w not in stop_words])

# Now, walk the codebase to get words from code files
code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.kts', '.scala', '.clj', '.ex', '.exs'}
code_words = set()
for root, dirs, files in os.walk('.'):
    # Skip .git and any hidden directories? We'll skip .git for sure.
    if '.git' in root:
        continue
    for file in files:
        if any(file.endswith(ext) for ext in code_extensions):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Extract words similarly
                    words_in_file = re.findall(r'\b[a-zA-Z]{3,}\b', content)
                    words_in_file = [w.lower() for w in words_in_file]
                    code_words.update(words_in_file)
            except Exception as e:
                # Skip files that can't be read
                pass

# Now, check how many pdf_keywords are in code_words
found = pdf_keywords & code_words
missing = pdf_keywords - code_words
total = len(pdf_keywords)
found_count = len(found)
percentage = (found_count / total * 100) if total > 0 else 0

print(f"PDF file: {pdf_file}")
print(f"Total unique keywords (after stop words): {total}")
print(f"Found in code: {found_count}")
print(f"Percentage: {percentage:.2f}%")
if missing:
    print(f"Missing keywords (first 10): {list(missing)[:10]}")
else:
    print("No missing keywords.")