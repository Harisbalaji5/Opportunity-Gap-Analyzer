from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills_from_resume
from github_analyzer import analyze_github_profile
from gap_engine import analyze_skill_gap
from utils import get_skills_for_role

app = FastAPI()

@app.post("/analyze")
async def analyze(
    request: Request,
    job_role: str | None = Form(None),
    github_username: str | None = Form(None),
    resume: UploadFile | None = File(None)
):
    content_type = (request.headers.get("content-type") or "").lower()
    resume_text = ""

    if "application/json" in content_type:
        payload = await request.json()
        job_role = (payload.get("job_role") or "").strip()
        github_username = (payload.get("github_username") or "").strip()
        resume_text = (payload.get("resume_text") or "").strip()
    else:
        job_role = (job_role or "").strip()
        github_username = (github_username or "").strip()

        if not resume:
            raise HTTPException(status_code=400, detail="Missing resume file in form-data.")

        filename = (resume.filename or "").lower()
        try:
            if filename.endswith(".pdf"):
                resume_text = extract_text_from_pdf(resume.file)
            elif filename.endswith(".docx"):
                resume_text = extract_text_from_docx(resume.file)
            else:
                raise HTTPException(status_code=400, detail="Unsupported resume type. Use PDF or DOCX.")
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Failed to parse resume file: {exc}") from exc

    if not job_role:
        raise HTTPException(status_code=400, detail="job_role is required.")
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume content is empty or missing.")

    user_skills = extract_skills_from_resume(resume_text)
    job_skills = get_skills_for_role(job_role)

    if not job_skills:
        raise HTTPException(status_code=400, detail=f"Unsupported job_role: {job_role}")

    matched, missing, score = analyze_skill_gap(user_skills, job_skills)

    github_data = analyze_github_profile(github_username) if github_username else None

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "score": score,
        "github": github_data
    }
