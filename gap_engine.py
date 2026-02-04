def analyze_skill_gap(user_skills, job_skills):
    matched = []
    missing = []

    if not job_skills:
        return matched, missing, 0

    for skill in job_skills:
        if skill in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    match_score = (len(matched) / len(job_skills)) * 100

    return matched, missing, match_score

def calculate_career_readiness(resume_score, github_score):
    return round((resume_score * 0.6) + (github_score * 0.4), 2)

def generate_recommendations(missing_skills, github_score):
    recommendations = []

    if missing_skills:
        recommendations.append(
            f"Focus on learning these missing skills: {', '.join(missing_skills)}"
        )

    if github_score < 40:
        recommendations.append(
            "Improve GitHub activity by building projects and pushing code regularly."
        )

    if not recommendations:
        recommendations.append(
            "Great profile! You are well-aligned with your target role."
        )

    return recommendations

