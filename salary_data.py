salary_data = {
    "Data Scientist": {
        "Junior/Entry Level": "$95,000 - $125,000",
        "Mid Level": "$130,000 - $165,000",
        "Senior Level": "$170,000 - $210,000",
        "Lead/Principal": "$220,000+"
    },
    "Software Engineer": {
        "Junior/Entry Level": "$90,000 - $120,000",
        "Mid Level": "$135,000 - $170,000",
        "Senior Level": "$175,000 - $220,000",
        "Lead/Principal": "$230,000+"
    },
    "Machine Learning Engineer": {
        "Junior/Entry Level": "$100,000 - $135,000",
        "Mid Level": "$145,000 - $185,000",
        "Senior Level": "$190,000 - $240,000",
        "Lead/Principal": "$250,000+"
    },
    "AI Research Scientist": {
        "Junior/Entry Level": "$130,000 - $160,000",
        "Mid Level": "$170,000 - $220,000",
        "Senior Level": "$230,000 - $300,000",
        "Lead/Principal": "$320,000+"
    },
    "Data Analyst": {
        "Junior/Entry Level": "$70,000 - $90,000",
        "Mid Level": "$95,000 - $120,000",
        "Senior Level": "$125,000 - $150,000",
        "Lead/Principal": "$160,000+"
    },
    "Product Manager": {
        "Junior/Entry Level": "$85,000 - $115,000",
        "Mid Level": "$125,000 - $160,000",
        "Senior Level": "$170,000 - $210,000",
        "Lead/Principal": "$220,000+"
    },
    "DevOps Engineer": {
        "Junior/Entry Level": "$95,000 - $120,000",
        "Mid Level": "$130,000 - $160,000",
        "Senior Level": "$170,000 - $200,000",
        "Lead/Principal": "$210,000+"
    },
    "Full Stack Developer": {
        "Junior/Entry Level": "$85,000 - $115,000",
        "Mid Level": "$125,000 - $155,000",
        "Senior Level": "$165,000 - $200,000",
        "Lead/Principal": "$210,000+"
    },
    "Mobile App Developer": {
        "Junior/Entry Level": "$80,000 - $110,000",
        "Mid Level": "$120,000 - $150,000",
        "Senior Level": "$160,000 - $190,000",
        "Lead/Principal": "$200,000+"
    },
    "Cybersecurity Analyst": {
        "Junior/Entry Level": "$85,000 - $110,000",
        "Mid Level": "$115,000 - $145,000",
        "Senior Level": "$150,000 - $180,000",
        "Lead/Principal": "$190,000+"
    },
    "Cloud Architect": {
        "Junior/Entry Level": "$100,000 - $130,000",
        "Mid Level": "$140,000 - $175,000",
        "Senior Level": "$180,000 - $230,000",
        "Lead/Principal": "$240,000+"
    }
}

def get_salary_range(role, level):
    """Retrieves salary range for a given role and experience level."""
    role_data = salary_data.get(role, {})
    
    # Normalize level string to match keys
    if "Senior" in level:
        key = "Senior Level"
    elif "Mid" in level:
        key = "Mid Level"
    elif "Lead" in level or "Principal" in level:
        key = "Lead/Principal"
    else:
        key = "Junior/Entry Level"
        
    return role_data.get(key, "Salary data not available")
