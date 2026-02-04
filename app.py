from utils import get_skills_for_role

role = input("Enter job role: ")

skills = get_skills_for_role(role)

print("Required Skills:")
for skill in skills:
    print("-", skill)
