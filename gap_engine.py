import re
import json
from gen_ai_engine import (
    query_ollama, 
    generate_learning_roadmap as gen_roadmap_ai,
    ai_resume_audit as gen_audit_ai
)

def analyze_skill_gap(user_skills, job_skills):
    if not job_skills:
        return [], [], 0

    # Fast lexical matcher to guarantee responsive processing.
    user_lower = [s.lower().strip() for s in user_skills]
    matched = []
    for js in job_skills:
        j = js.lower().strip()
        if any(
            j == u
            or j in u
            or u in j
            or bool(set(j.split()) & set(u.split()))
            for u in user_lower
        ):
            matched.append(js)

    missing = [skill for skill in job_skills if skill not in matched]

    match_score = (len(matched) / len(job_skills)) * 100

    return matched, missing, match_score

def calculate_career_readiness(resume_score, github_score):
    return round((resume_score * 0.6) + (github_score * 0.4), 2)

def calculate_resume_quality(resume_text):
    score = 0
    feedback = []
    
    # Check length
    word_count = len(resume_text.split())
    if 300 <= word_count <= 1000:
        score += 20
    elif word_count < 300:
        feedback.append("Resume might be too short.")
    else:
        feedback.append("Resume might be too long.")

    # Check for sections
    sections = ["experience", "education", "skills", "projects", "summary", "objective"]
    found_sections = [s for s in sections if s in resume_text.lower()]
    score += (len(found_sections) / len(sections)) * 40
    if len(found_sections) < 3:
        feedback.append(f"Consider adding more sections like: {', '.join([s for s in sections if s not in found_sections])}")

    # Check for email
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    if re.search(email_pattern, resume_text):
        score += 20
    else:
        feedback.append("No email address found or format incorrect.")
        
    # Check for phone
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    if re.search(phone_pattern, resume_text):
        score += 20
    else:
        feedback.append("Phone number check failed (might be just formatting).")

    return int(min(score, 100)), feedback

def calculate_experience_level(resume_text):
    text = resume_text.lower()
    if any(keyword in text for keyword in ["senior", "lead", "manager", "principal", "architect", "5+ years", "6+ years", "7+ years", "8+ years", "9+ years", "10+ years"]):
        return "Senior Level"
    elif any(keyword in text for keyword in ["mid-level", "mid level", "intermediate", "3+ years", "4+ years", "2+ years"]):
        return "Mid Level"
    elif any(keyword in text for keyword in ["junior", "associate", "intern", "fresher", "entry level", "graduate", "0-1 years"]):
        return "Junior/Entry Level"
    else:
        return "Entry Level (Estimated)"

# --- NEW ADVANCED INSIGHTS ---

def calculate_ai_proficiency(user_skills):
    tiers = {
        "Foundation": ["python", "sql", "pandas", "numpy", "matplotlib", "excel"],
        "Intermediate": ["scikit-learn", "tensorflow", "keras", "pytorch", "nlp", "opencv", "flask", "django"],
        "Advanced": ["transformers", "llm", "generative ai", "reinforcement learning", "mlops", "docker", "kubernetes", "aws", "azure"]
    }
    
    score = 0
    
    user_skills_lower = [s.lower() for s in user_skills]
    
    # Check Foundation
    foundation_count = sum(1 for s in tiers["Foundation"] if s in user_skills_lower)
    if foundation_count >= 2:
        score += 1
        
    # Check Intermediate
    intermediate_count = sum(1 for s in tiers["Intermediate"] if s in user_skills_lower)
    if intermediate_count >= 1:
        score += 2
        
    # Check Advanced
    advanced_count = sum(1 for s in tiers["Advanced"] if s in user_skills_lower)
    if advanced_count >= 1:
        score += 3
        
    # Simply sum tiered scores? Or max tier achieved?
    # Logic: If you have advanced, you are likely advanced.
    if advanced_count > 0:
        return "AI Expert 🧠", "You demonstrate advanced AI capabilities (LLMs, MLOps, Cloud)."
    elif intermediate_count > 0:
        return "AI Practitioner 🛠️", "You can build and deploy standard AI models."
    elif foundation_count > 0:
        return "AI Enthusiast 🎓", "You have the data science foundations."
    else:
        return "Aspiring AI Developer 🌱", "Start with Python and Data Basics."

def analyze_resume_impact(resume_text):
    text = resume_text.lower()
    
    # 1. Action Verbs
    action_verbs = ["achieved", "developed", "led", "managed", "created", "designed", "implemented", "optimized", "increased", "decreased", "saved", "generated"]
    verb_count = sum(1 for verb in action_verbs if verb in text)
    
    # 2. Quantifiable Metrics (simplified regex for numbers/%)
    metrics_count = len(re.findall(r'\d+%|\$\d+|\d+ users|\d+ years', text))
    
    impact_score = min((verb_count * 5) + (metrics_count * 10), 100)
    
    feedback = []
    if verb_count < 3:
        feedback.append("Use more strong action verbs (e.g., Led, Developed, Optimized).")
    if metrics_count < 2:
        feedback.append("Quantify your achievements! (e.g., 'Increased efficiency by 20%').")
        
    return int(impact_score), feedback

def get_detailed_recommendations(missing_skills):
    # Mapping skills to actionable advice
    rec_db = {
        "python": "Build a web scraper or data analysis tool. Course: generic Python bootcamp.",
        "sql": "Practice complex queries on LeetCode/HackerRank.",
        "machine learning": "Course: Andrew Ng's ML Specialization on Coursera.",
        "deep learning": "Project: Build a digit recognizer using MNIST.",
        "nlp": "Project: Create a sentiment analysis bot for Twitter/Reddit.",
        "computer vision": "Project: Build a face mask detector using OpenCV.",
        "tensorflow": "Practice: Reimplement a paper from scratch.",
        "pytorch": "Course: Fast.ai Practical Deep Learning.",
        "docker": "Project: Containerize a simple Flask app.",
        "kubernetes": "Lab: Deploy a microservice cluster specifically for ML models.",
        "aws": "Cert: AWS Certified Machine Learning Specialty.",
        "azure": "Cert: Azure AI Engineer Associate."
    }
    
    recommendations = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in rec_db:
             recommendations.append(f"**{skill}**: {rec_db[skill_lower]}")
        else:
             # Fallback
             recommendations.append(f"**{skill}**: Build a small project to demonstrate this skill.")
             
    return recommendations


def generate_recommendations(missing_skills, role):
    if not missing_skills:
        return []
        
    prompt = f"""
    You are a Career Coach. The user wants to be a {role} but is missing these skills: {', '.join(missing_skills)}.
    
    Suggest 3 specific, hands-on projects they can build to learn these skills.
    
    Format:
    - [Project Name]: [Brief Description]
    """
    
    response = query_ollama(prompt)
    if response:
        # Split by newlines and clean up
        lines = [line.strip() for line in response.split('\n') if line.strip() and (line.strip().startswith('-') or line.strip().startswith('*') or line.strip()[0].isdigit())]
        return lines if lines else [response] 
        
    # Fallback to dictionary lookup
    return get_detailed_recommendations(missing_skills)

def ai_resume_audit(resume_text, role):
    return gen_audit_ai(resume_text, role)

def _build_structured_roadmap(missing_skills, role):
    skills = missing_skills[:]
    while len(skills) < 3:
        skills.append("Core Fundamentals")
    s1, s2, s3 = skills[0], skills[1], skills[2]
    skills_text = ", ".join(missing_skills) if missing_skills else "Core interview and project readiness"
    suggestions = get_detailed_recommendations(missing_skills)[:6]
    suggestion_line = suggestions[0] if suggestions else "Build one measurable project and document outcomes."

    return f"""## Career Timeline Roadmap ({role})

### Goal
Build a job-ready {role} profile with strong project proof and interview clarity.

### Step 1: Brief (Days 1-2)
- Define hiring-aligned goals and baseline your current level.
- Prioritize top gaps: {skills_text}.
- **Output:** 1-page action plan with time blocks and success metrics.

### Step 2: Sketch (Days 3-5)
- Design one capstone project mapped to {role} expectations.
- Split scope into modules for {s1}, {s2}, and {s3}.
- **Output:** System sketch + milestone backlog.

### Step 3: Solution Sprint (Week 2)
- Build core functionality around {s1}.
- Add validation, error handling, and a simple test flow.
- **Output:** Prototype v1 with runnable instructions.

### Step 4: Design and Depth (Week 3)
- Expand feature depth with {s2} and integrate {s3}.
- Improve performance, structure, and maintainability.
- **Output:** Capstone v2 with measurable improvements.

### Step 5: Presentation (Week 4 - Part 1)
- Prepare portfolio narrative focused on business impact.
- Create interview stories and a short project walkthrough.
- **Output:** Portfolio-ready case study and demo script.

### Step 6: Revision (Week 4 - Part 2)
- Run two mock interviews and refine weak areas.
- Finalize resume bullets and align to target role keywords.
- **Output:** Final resume + final capstone submission.

### Priority Recommendation
- {suggestion_line}
"""


def _roadmap_is_structured(text):
    if not text:
        return False
    timeline_tokens = ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "Output"]
    week_tokens = ["Week 1", "Week 2", "Week 3", "Week 4", "Deliverable", "Checkpoint"]
    return all(token in text for token in timeline_tokens) or all(token in text for token in week_tokens)


def generate_learning_roadmap(missing_skills, role):
    ai_roadmap = gen_roadmap_ai(missing_skills, role)
    if _roadmap_is_structured(ai_roadmap):
        return ai_roadmap
    return _build_structured_roadmap(missing_skills, role)
