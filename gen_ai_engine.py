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
    if not check_ollama_status():
        return None

    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        
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
        return "You are all set! No specific roadmap needed."
        
    roadmap = f"""
### Week 1: Foundation
- **Mon-Wed**: Basics of {missing_skills[0] if len(missing_skills) > 0 else 'Core Concepts'}
- **Thu-Fri**: Hands-on exercises
- **Weekend**: Mini-project

### Week 2: Deep Dive
- **Mon-Wed**: Advanced concepts of {missing_skills[1] if len(missing_skills) > 1 else 'Advanced Topics'}
- **Thu-Fri**: Integration with other tools
- **Weekend**: Build a POC

### Week 3: Application
- **Mon-Wed**: Real-world use cases
- **Thu-Fri**: Debugging and optimization
- **Weekend**: Contribute to Open Source

### Week 4: Mastery
- **Mon-Wed**: System Design implications
- **Thu-Fri**: Mock Interviews
- **Weekend**: Final Capstone Project
"""
    return roadmap

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
    Create a 4-week learning roadmap for a {role} to learn: {', '.join(missing_skills)}.
    Format safely as Markdown.
    """
    
    response = query_ollama(prompt)
    if response:
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

