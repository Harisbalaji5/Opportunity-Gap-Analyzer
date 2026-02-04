import matplotlib.pyplot as plt
import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills_from_resume
from utils import get_skills_for_role
from gap_engine import analyze_skill_gap
from job_roles_data import job_roles

st.title("AI Opportunity Gap Analyzer")

# Job role dropdown
role = st.selectbox("Select Target Job Role", list(job_roles.keys()))

# Resume input
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if st.button("Analyze", key="analyze_button"):

    if uploaded_file is not None:

        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)

        else:
            st.error("Unsupported file format")
            st.stop()

        user_skills = extract_skills_from_resume(resume_text)
        job_skills = get_skills_for_role(role)

        matched, missing, score = analyze_skill_gap(user_skills, job_skills)

        st.success("Analysis Completed")

        st.divider()
        st.metric(label="Career Readiness Score", value=f"{round(score,2)}%")

        st.subheader("Match Score")
        st.write(f"{round(score,2)}%")

        st.subheader("Matched Skills")
        st.write(matched)

        st.subheader("Missing Skills")
        st.write(missing)

        st.subheader("Skill Gap Overview")

        labels = ["Matched Skills", "Missing Skills"]
        values = [len(matched), len(missing)]

        fig = plt.figure()
        plt.bar(labels, values)
        plt.title("Skill Gap Analysis")
        plt.ylabel("Number of Skills")

        st.pyplot(fig)

    else:
        st.warning("Please upload resume")
