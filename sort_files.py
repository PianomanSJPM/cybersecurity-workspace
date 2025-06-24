import os
import shutil
from docx import Document
from pptx import Presentation

# Define keywords for each category
CATEGORIES = {
    "Portfolio": [
        "portfolio", "exemplar", "project", "work sample",
        "worksheet", "journal", "exercise", "response"
    ],
    "Glossaries": ["glossary", "terms", "definitions"],
    "Lessons": [
        "lesson", "module", "summary", "explained",
        "monitoring", "cicd", "ongoing", "training"
    ]
}

def get_category(filename, content):
    filename_lower = filename.lower()
    content_lower = content.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in filename_lower or kw in content_lower:
                return category
    return None

def read_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception:
        return ""

def read_pptx(file_path):
    try:
        prs = Presentation(file_path)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return "\n".join(text)
    except Exception:
        return ""

def main():
    folder = os.getcwd()
    files = [f for f in os.listdir(folder) if f.endswith(('.docx', '.pptx'))]
    for file in files:
        file_path = os.path.join(folder, file)
        content = ""
        if file.endswith('.docx'):
            content = read_docx(file_path)
        elif file.endswith('.pptx'):
            content = read_pptx(file_path)
        category = get_category(file, content)
        if category:
            dest_folder = os.path.join(folder, category)
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(dest_folder, file))
            print(f"Moved '{file}' to '{category}'")
        else:
            print(f"No category found for '{file}'. File left in place.")

if __name__ == "__main__":
    main()