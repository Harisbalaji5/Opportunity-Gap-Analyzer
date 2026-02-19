from job_roles_data import job_roles

def get_skills_for_role(role):
    for job_role in job_roles:
        if job_role.lower() == role.lower():
            return job_roles[job_role]
    return []


SKILL_DATABASE = [
    # Programming Languages
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Ruby", "PHP", "Swift", "Kotlin", "Go", "Rust", "R", "Scala", "Dart",
    
    # Data Science & AI
    "Machine Learning", "Deep Learning", "Data Science", "Statistics", "Pandas", "NumPy", "Scikit-learn", "Keras",
    "TensorFlow", "PyTorch", "NLP", "Computer Vision", "OpenCV", "Reinforcement Learning", "Generative AI", "LLM",
    "Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI", "Excel", "Data Visualization",

    # Web Development
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot", 
    "ASP.NET", "Ruby on Rails", "Laravel", "Tailwind CSS", "Bootstrap", "SASS", "GraphQL", "REST APIs",
    
    # Database
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "NoSQL", "Redis", "Cassandra", "Oracle", "SQLite", "Firebase",

    # DevOps & Cloud
    "Git", "GitHub", "GitLab", "Docker", "Kubernetes", "Jenkins", "Travis CI", "CircleCI", "Ansible", "Terraform",
    "AWS", "Azure", "Google Cloud", "Linux", "Unix", "Bash", "Shell Scripting", "Nginx", "Apache",

    # Mobile Development
    "Android", "iOS", "Flutter", "React Native", "SwiftUI", "Jetpack Compose",
    
    # Cybersecurity
    "Network Security", "Penetration Testing", "Ethical Hacking", "Cryptography", "Firewalls", "Wireshark", "Metasploit", "SIEM",
    
    # Other
    "Agile", "Scrum", "JIRA", "Trello", "Slack", "Communication", "Leadership", "Problem Solving", "Critical Thinking"
]

def calculate_github_score(github_data):
    if not github_data:
        return 0

    score = 0

    # Repo contribution
    score += min(github_data["total_repos"] * 5, 40)

    # Stars contribution
    score += min(github_data["total_stars"] * 2, 30)

    # Language diversity
    score += min(len(github_data["languages"]) * 5, 30)

    return min(score, 100)
