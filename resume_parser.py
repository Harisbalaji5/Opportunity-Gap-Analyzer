

from utils import SKILL_DATABASE
import PyPDF2
import docx

MAX_PDF_PAGES = 5
MAX_RESUME_CHARS = 20000

# ---------- Extract Text From PDF ----------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages[:MAX_PDF_PAGES]:
        page_text = page.extract_text() or ""
        text += page_text
        if len(text) >= MAX_RESUME_CHARS:
            break

    return text[:MAX_RESUME_CHARS]


# ---------- Extract Text From DOCX ----------
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"
        if len(text) >= MAX_RESUME_CHARS:
            break

    return text[:MAX_RESUME_CHARS]


# ---------- Extract Skills ----------
def extract_skills_from_resume(resume_text):
    found_skills = []

    resume_text = resume_text.lower()

    for skill in SKILL_DATABASE:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills
