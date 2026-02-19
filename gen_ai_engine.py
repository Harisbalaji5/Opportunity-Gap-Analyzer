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

def mock_roadmap(missing_skills, role="Target Role"):
    skill_a = missing_skills[0] if len(missing_skills) > 0 else "Core Fundamentals"
    skill_b = missing_skills[1] if len(missing_skills) > 1 else "Applied Practice"
    skill_c = missing_skills[2] if len(missing_skills) > 2 else "System Integration"
    skill_text = ", ".join(missing_skills) if missing_skills else "Foundational role skills"

    return f"""## Career Timeline Roadmap ({role})

### Goal
Transition to a job-ready {role} profile with visible project proof and interview readiness.

### Step 1: Brief (Days 1-2)
- Define target outcomes for {role} and baseline your current level.
- Prioritize top skill gaps: {skill_text}.
- **Output:** 1-page learning contract with weekly time blocks.

### Step 2: Sketch (Days 3-5)
- Design a capstone concept mapped to hiring expectations.
- Break it into modules covering {skill_a}, {skill_b}, and {skill_c}.
- **Output:** Architecture sketch + feature backlog.

### Step 3: Solution Sprint (Week 2)
- Build core module for {skill_a} and one practical use case.
- Add data flow, validation, and basic test checks.
- **Output:** Working prototype v1 with README.

### Step 4: Design and Depth (Week 3)
- Implement advanced module for {skill_b} and integrate {skill_c}.
- Improve reliability, code structure, and explainability.
- **Output:** Capstone v2 with metrics and screenshots.

### Step 5: Presentation (Week 4 - Part 1)
- Prepare portfolio narrative and STAR stories tied to outcomes.
- Create a 3-5 minute project walkthrough demo.
- **Output:** Portfolio page + interview-ready pitch deck.

### Step 6: Revision (Week 4 - Part 2)
- Run 2 mock interviews and patch weak answers.
- Refine resume bullets with measurable impact statements.
- **Output:** Final resume + finalized capstone + action checklist.
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
    Generates a timeline-style roadmap using AI with a fallback.
    """
    prompt = f"""
    You are a senior career coach.
    Create a strict, structured career timeline roadmap for a {role}.
    Missing skills: {', '.join(missing_skills)}.

    Return MARKDOWN using this exact section structure:
    1) ## Career Timeline Roadmap ({role})
    2) ### Goal
    3) ### Step 1: Brief (Days 1-2)
    4) ### Step 2: Sketch (Days 3-5)
    5) ### Step 3: Solution Sprint (Week 2)
    6) ### Step 4: Design and Depth (Week 3)
    7) ### Step 5: Presentation (Week 4 - Part 1)
    8) ### Step 6: Revision (Week 4 - Part 2)

    Requirements:
    - Each step must include:
      - 2 concise action bullets
      - 1 output line in format: **Output:** ...
    - Provide practical, role-specific tasks with measurable outputs.
    - Keep total response under 320 words.
    """
    
    response = query_ollama(prompt)
    if response and "Step 1" in response and "Step 6" in response and "**Output:**" in response:
        return response
        
    return mock_roadmap(missing_skills, role)

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

