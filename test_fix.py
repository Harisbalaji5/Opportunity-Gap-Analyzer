from gap_engine import generate_learning_roadmap

print("Testing AI Roadmap Generation...")
roadmap = generate_learning_roadmap(["Python", "Machine Learning"], "Data Scientist")
if roadmap and "Week 1" in roadmap:
    print("SUCCESS: Roadmap Generated!")
    print(roadmap[:200] + "...")
else:
    print("FAILURE: Roadmap generation failed or returned unexpected format.")
    print(f"Output: {roadmap}")
