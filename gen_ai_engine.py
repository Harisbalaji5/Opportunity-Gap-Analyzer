import requests
import json
import random
from datetime import date

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

def check_ollama_status():
    """Checks if Ollama is running and the model is available."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=1)
        if response.status_code == 200:
            return True
    except:
        return False
    return False

def query_ollama(prompt):
    """
    Queries the local Ollama instance. Returns None if it fails.
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }, timeout=25)
        
        if response.status_code == 200:
            return response.json().get("response", "")
        return None
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None


# --- MOCK GENERATORS (FALLBACKS) ---

def mock_cover_letter(user_name, company_name, role, matched_skills):
    return f"""
{user_name if user_name else "[Your Name]"}
{date.today().strftime("%B %d, %Y")}

Hiring Manager
{company_name if company_name else "[Company Name]"}

Dear Hiring Team,

I am writing to express my enthusiastic application for the {role} position at {company_name}. With a strong foundation in {', '.join(matched_skills[:3]) if matched_skills else 'relevant technologies'}, I am confident in my ability to contribute effectively to your team.

I have always admired {company_name}'s commitment to innovation. Throughout my career, I have focused on building scalable and efficient solutions, a value I know we share.

I am eager to bring my problem-solving skills and technical expertise to this role. Thank you for your time and consideration.

Sincerely,

{user_name if user_name else "[Your Name]"}
"""

def mock_interview_questions(role, missing_skills):
    questions = []
    
    # 1. Technical Gaps
    for skill in missing_skills[:2]:
        questions.append({
            "type": "Technical Gap",
            "skill": skill,
            "question": f"Can you explain a basic project where you would use {skill}?",
            "tip": f"Focus on the 'Why' and 'How' of {skill}. Even if you haven't used it, explain its purpose."
        })
        
    # 2. General Role
    questions.append({
        "type": "Behavioral",
        "question": "Tell me about a time you had to learn a new technology quickly.",
        "tip": "Use the STAR method (Situation, Task, Action, Result) to frame your answer."
    })
    
    return questions

def mock_roadmap(missing_skills):
    if not missing_skills:
        return """## 4-Week Career Roadmap

### Goal
Strengthen interview readiness and portfolio quality.

### Week 1: Baseline and Planning
- Audit your current projects and identify measurable gaps.
- Set a weekly schedule (8-10 focused hours).
- Define one capstone project scope and acceptance criteria.

### Week 2: Build and Iterate
- Implement core features for your capstone.
- Write concise documentation and usage notes.
- Add tests and basic quality checks.

### Week 3: Polish and Showcase
- Improve UX, error handling, and performance.
- Prepare a role-focused README and demo script.
- Publish progress updates and lessons learned.

### Week 4: Interview Readiness
- Run mock interviews (technical + behavioral).
- Refine project explanations using STAR format.
- Finalize portfolio links and resume bullets.
"""

    skill_a = missing_skills[0] if len(missing_skills) > 0 else "Core Fundamentals"
    skill_b = missing_skills[1] if len(missing_skills) > 1 else "Applied Practice"
    skill_c = missing_skills[2] if len(missing_skills) > 2 else "System Integration"
    all_skills = ", ".join(missing_skills)

    return f"""## 4-Week Structured Learning Roadmap

### Target Skills
{all_skills}

### Outcome by Week 4
- Deliver one portfolio-grade project mapped to the target role.
- Demonstrate hands-on capability in {skill_a}, {skill_b}, and {skill_c}.
- Prepare concise interview-ready explanations and measurable impact bullets.

### Week 1: Foundation Sprint ({skill_a})
**Focus**
- Build conceptual clarity and environment setup.
- Complete 2-3 focused labs on {skill_a}.

**Deliverable**
- One mini-project or notebook showing core workflows.

**Checkpoint**
- Explain key concepts of {skill_a} in under 3 minutes.

### Week 2: Applied Build ({skill_b})
**Focus**
- Implement role-relevant use cases with real or realistic data.
- Add validation, edge-case handling, and clean structure.

**Deliverable**
- Feature-complete module demonstrating {skill_b}.

**Checkpoint**
- Record a short demo and document decisions/tradeoffs.

### Week 3: Integration and Scale ({skill_c})
**Focus**
- Integrate prior modules into one coherent project.
- Improve reliability, performance, and maintainability.

**Deliverable**
- Integrated capstone v1 with README and architecture notes.

**Checkpoint**
- Pass self-review checklist: correctness, readability, reproducibility.

### Week 4: Portfolio and Interview Readiness
**Focus**
- Final polish: tests, docs, screenshots, and deployment/demo flow.
- Prepare interview stories tied to your capstone.

**Deliverable**
- Final capstone v2 + role-specific resume updates.

**Checkpoint**
- Complete 2 mock interviews and refine weak areas.

### Daily Cadence (Recommended)
- 60-90 min learning block
- 60-90 min implementation block
- 15 min reflection log (what worked, blockers, next step)

### Recommended Resources
- Official docs for each target skill first
- One high-quality course per skill (avoid course-hopping)
- Problem sets / labs for deliberate practice
"""

def mock_audit(role):
    return """
**Critical Issues:**
1. **Lack of Metrics**: Many bullet points list duties rather than achievements.
2. **Generic Summary**: The professional summary could apply to anyone. Tailor it to the specific role.
3. **Passive Voice**: Use stronger action verbs.

**Rewrite Example:**
[Original] "Responsible for managing the database."
[Improved] "Optimized database performance, reducing query time by 30%."
"""


# --- MAIN FUNCTIONS with FALLBACKS ---

def generate_cover_letter(user_name, company_name, role, matched_skills, missing_skills):
    """
    Generates a tailored cover letter using AI with a fallback.
    """
    prompt = f"""
    Write a professional cover letter for {user_name} applying for {role} at {company_name}.
    Highlight these skills: {', '.join(matched_skills)}.
    Mention learning these: {', '.join(missing_skills)}.
    Keep it under 300 words.
    """
    
    response = query_ollama(prompt)
    if response:
        return response
        
    return mock_cover_letter(user_name, company_name, role, matched_skills)

def generate_interview_questions(role, missing_skills):
    """
    Generates interview questions using AI with a fallback.
    """
    prompt = f"""
    Generate 3 interview questions for a {role}.
    Focus on: {', '.join(missing_skills)}.
    Return ONLY a raw JSON array (no markdown) with objects having 'type', 'question', 'tip'.
    """
    
    response = query_ollama(prompt)
    if response:
        try:
            # Clean possible markdown wrapping
            cleaned = response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except:
            pass
            
    return mock_interview_questions(role, missing_skills)

def generate_learning_roadmap(missing_skills, role):
    """
    Generates a 4-week roadmap using AI with a fallback.
    """
    prompt = f"""
    You are a senior career coach.
    Create a strict, structured 4-week roadmap for a {role}.
    Missing skills: {', '.join(missing_skills)}.

    Return MARKDOWN using this exact section structure:
    1) ## 4-Week Structured Learning Roadmap
    2) ### Target Skills
    3) ### Outcome by Week 4
    4) ### Week 1: Foundation Sprint
       - Focus
       - Deliverable
       - Checkpoint
    5) ### Week 2: Applied Build
       - Focus
       - Deliverable
       - Checkpoint
    6) ### Week 3: Integration and Scale
       - Focus
       - Deliverable
       - Checkpoint
    7) ### Week 4: Portfolio and Interview Readiness
       - Focus
       - Deliverable
       - Checkpoint
    8) ### Daily Cadence (Recommended)
    9) ### Recommended Resources

    Requirements:
    - Provide practical, role-specific tasks.
    - Include measurable outputs each week.
    - Keep total response under 350 words.
    """
    
    response = query_ollama(prompt)
    if response and "Week 1" in response and "Deliverable" in response:
        return response
        
    return mock_roadmap(missing_skills)

def ai_resume_audit(resume_text, role):
    """
    Audits the resume using AI with a fallback.
    """
    prompt = f"""
    Audit this resume for a {role}.
    Resume: "{resume_text[:1000]}..."
    Provide 3 critical issues and 1 rewrite.
    """
    
    response = query_ollama(prompt)
    if response:
        return response
        
    return mock_audit(role)

