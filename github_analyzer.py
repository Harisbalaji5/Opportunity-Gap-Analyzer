import requests
from gen_ai_engine import query_ollama

GITHUB_API_URL = "https://api.github.com/users/"

def analyze_github_profile(username):
    user_url = GITHUB_API_URL + username
    repos_url = user_url + "/repos"

    user_response = requests.get(user_url)
    repos_response = requests.get(repos_url)

    if user_response.status_code != 200:
        return None

    user_data = user_response.json()
    repos_data = repos_response.json()

    total_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)

    languages = {}
    total_stars = 0

    for repo in repos_data:
        lang = repo.get("language")
        stars = repo.get("stargazers_count", 0)

        total_stars += stars

        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    return {
        "total_repos": total_repos,
        "followers": followers,
        "languages": languages,
        "total_stars": total_stars
    }

def analyze_github_with_ai(username, profile_data):
    """
    Sends GitHub stats to Llama 3 for a qualitative recruiter review.
    """
    prompt = f"""
    You are a Senior Technical Recruiter. Review this GitHub profile summary for user '{username}':
    
    - Public Repos: {profile_data['total_repos']}
    - Followers: {profile_data['followers']}
    - Total Stars Earned: {profile_data['total_stars']}
    - Top Languages: {profile_data['languages']}
    
    Based ONLY on these stats, provide a honest, 3-sentence assessment of their engineering level (Junior/Mid/Senior/Expert).
    Then, give 2 specific tips to improve their profile visibility.
    
    Format:
    **Assessment:** [Your text]
    
    **Tips:**
    1. [Tip 1]
    2. [Tip 2]
    """
    
    response = query_ollama(prompt)
    if not response:
        return "Could not generate AI feedback at this time."
        
    return response
