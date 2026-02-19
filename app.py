import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import requests
import time

from github_analyzer import analyze_github_profile, analyze_github_with_ai
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills_from_resume
from utils import get_skills_for_role, calculate_github_score
from gap_engine import (
    analyze_skill_gap, 
    calculate_career_readiness, 
    generate_recommendations, 
    calculate_resume_quality, 
    calculate_experience_level,
    calculate_ai_proficiency,
    analyze_resume_impact,
    get_detailed_recommendations,
    ai_resume_audit,
    generate_learning_roadmap
)
from job_roles_data import job_roles

# Page Config
st.set_page_config(page_title="AI Opportunity Gap Analyzer", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

# --- MODERN PROFESSIONAL UI (STRIPE-LIKE) ---
st.markdown("""
    <style>
    /* Global Font & Colors */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');
    
    :root {
        --primary-color: #4F46E5; /* Indigo 600 */
        --secondary-color: #10B981; /* Emerald 500 */
        --background-color: #F8FAFC; /* Slate 50 */
        --card-bg: #FFFFFF;
        --text-color: #1E293B; /* Slate 800 */
        --text-muted: #64748B; /* Slate 500 */
        --border-color: #E2E8F0; /* Slate 200 */
    }

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        color: var(--text-color);
        background-color: var(--background-color);
    }
    
    /* Main Container */
    .stApp {
        background-color: var(--background-color);
        background-image: radial-gradient(#E2E8F0 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Headings */
    h1, h2, h3 {
        font-family: 'Sora', sans-serif;
        color: var(--text-color);
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    h1 {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Cards */
    .feature-card {
        background-color: var(--card-bg);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 1rem;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: var(--primary-color);
    }
    
    /* Metric Typography */
    .metric-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        display: block;
    }
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-color);
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    .metric-sub {
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    /* Custom Button */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.5);
        transform: translateY(-1px);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }
    
    /* Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: white !important;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        color: var(--text-color) !important;
    }
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    .upload-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.35rem;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: #1E293B !important;
    }

    /* Force Text Colors */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p,
    .stTextInput label, .stSelectbox label, .stFileUploader label,
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li {
        color: var(--text-color) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background-color: transparent;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        color: var(--text-muted);
        border: 1px solid transparent;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary-color);
        background-color: rgba(79, 70, 229, 0.05);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #EEF2FF;
        color: var(--primary-color);
        border-color: #C7D2FE;
        font-weight: 600;
    }
    .hero-shell {
        background: linear-gradient(140deg, #EEF2FF 0%, #FFFFFF 55%, #ECFDF5 100%);
        border: 1px solid #DDE5F2;
        border-radius: 18px;
        padding: 2rem;
        margin-top: 0.75rem;
        box-shadow: 0 14px 24px -20px rgba(15, 23, 42, 0.35);
    }
    .hero-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.9rem;
        font-weight: 800;
        color: #0B1320 !important;
        text-shadow: none;
        margin: 0;
    }
    .hero-copy {
        font-size: 1rem;
        color: #475569;
        margin-top: 0.6rem;
        margin-bottom: 1rem;
        max-width: 760px;
    }
    .hero-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #D2DAE8;
        color: #334155;
        border-radius: 999px;
        padding: 0.4rem 0.8rem;
        font-size: 0.82rem;
        font-weight: 600;
    }    </style>
""", unsafe_allow_html=True)

# --- CACHED FUNCTIONS ---
@st.cache_data(ttl=3600)
def cached_extract_pdf(file):
    return extract_text_from_pdf(file)

@st.cache_data(ttl=3600)
def cached_extract_docx(file):
    return extract_text_from_docx(file)

@st.cache_data(ttl=600)
def cached_analyze_skills(user_skills, job_skills):
    return analyze_skill_gap(user_skills, job_skills)

@st.cache_data(ttl=3600)
def cached_github_analysis(username):
    return analyze_github_profile(username)

@st.cache_data(ttl=3600)
def cached_github_ai_feedback(username, data):
    return analyze_github_with_ai(username, data)

@st.cache_data(ttl=3600)
def cached_ai_resume_audit(text, role):
    return ai_resume_audit(text, role)

@st.cache_data(ttl=3600)
def cached_ai_recommendations(missing, role):
    from gap_engine import generate_recommendations
    return generate_recommendations(missing, role)

@st.cache_data(ttl=3600)
def cached_ai_roadmap(missing, role):
    return generate_learning_roadmap(missing, role)

# --- HELPER UI FUNCTIONS ---
def metric_card_html(label, value, subtext="", color="var(--primary-color)"):
    return f"""
    <div class="feature-card" style="border-top: 4px solid {color};">
        <span class="metric-label">{label}</span>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtext}</div>
    </div>
    """

def skill_chip(skill, type="neutral"):
    colors = {
        "neutral": ("#F3F4F6", "#374151"),
        "success": ("#D1FAE5", "#065F46"),
        "missing": ("#FEE2E2", "#991B1B"),
        "highlight": ("#E0E7FF", "#4338CA")
    }
    bg, text = colors.get(type, colors["neutral"])
    return f"""
    <span style="
        background-color: {bg}; 
        color: {text}; 
        padding: 0.25rem 0.75rem; 
        border-radius: 9999px; 
        font-size: 0.85rem; 
        font-weight: 500; 
        margin-right: 0.5rem; 
        margin-bottom: 0.5rem; 
        display: inline-block;
        border: 1px solid rgba(0,0,0,0.05);
    ">{skill}</span>
    """

def generate_report(role, career_score, missing_skills, recommendations):
    report = f"""
    AI CAREER ANALYSIS REPORT
    -------------------------
    Target Role: {role}
    Date: {datetime.now().strftime("%Y-%m-%d")}
    
    OVERALL READINESS: {career_score}%
    
    MISSING SKILLS:
    {', '.join(missing_skills) if missing_skills else "None - Great job!"}
    
    RECOMMENDATIONS:
    """
    for rec in recommendations:
        report += f"- {rec}\n"
        
    return report


def merge_recommendations(primary, fallback, min_items=6):
    """Merge AI and fallback recommendations and deduplicate."""
    primary = primary or []
    fallback = fallback or []
    merged = []
    seen = set()
    for rec in primary + fallback:
        key = rec.strip().lower()
        if key and key not in seen:
            seen.add(key)
            merged.append(rec)
    return merged[: max(min_items, len(merged))]

# --- SIDEBAR ---
with st.sidebar:
    role = st.selectbox("Job Role", list(job_roles.keys()))
    st.markdown('<div class="upload-title">Resume (PDF/DOCX)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf", "docx"], label_visibility="collapsed")
    github_username = st.text_input("GitHub Username")
    
    st.markdown("---")
    analyze_btn = st.button("Run Analysis", type="primary")
    
    st.markdown("""
        <div style="margin-top:2rem; font-size:0.8rem; color:#9CA3AF;">
        v3.0 | Modern Pro Edition
        </div>
    """, unsafe_allow_html=True)

    # Check Local AI Status
    try:
        if requests.get("http://localhost:11434/api/tags", timeout=1).status_code == 200:
            st.success("🟢 Local AI Active")
        else:
            st.warning("⚫ Local AI Offline")
    except:
        st.warning("⚫ Local AI Offline")

# --- MAIN CONTENT ---
# --- SESSION STATE INITIALIZATION ---
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# --- MAIN CONTENT ---
if not st.session_state.analysis_complete:
    st.markdown("""
        <div class="hero-shell">
            <h2 class="hero-title">Optimize Your Career Path</h2>
            <p class="hero-copy">
                Upload your resume and role to get a clean, actionable analysis across readiness, skill gaps, and growth roadmap.
            </p>
            <div class="hero-row">
                <span class="hero-pill">Resume Analysis</span>
                <span class="hero-pill">Role-Based Matching</span>
                <span class="hero-pill">GitHub Insights</span>
                <span class="hero-pill">AI Recommendations</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
# Processing Logic
if analyze_btn and uploaded_file:
    try:
        with st.spinner("Processing Profile..."):
            # Extraction
            if uploaded_file.type == "application/pdf":
                resume_text = cached_extract_pdf(uploaded_file)
            else:
                resume_text = cached_extract_docx(uploaded_file)
                
            # Analysis
            user_skills = extract_skills_from_resume(resume_text)
            job_skills = get_skills_for_role(role)
            # Hard bypass of cached_analyze_skills: deterministic fast lexical match.
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
            score = (len(matched) / len(job_skills)) * 100 if job_skills else 0
            
            resume_quality_score, resume_feedback = calculate_resume_quality(resume_text)
            experience_level = calculate_experience_level(resume_text)
            ai_level, ai_level_desc = calculate_ai_proficiency(user_skills)
            impact_score, impact_feedback = analyze_resume_impact(resume_text)
            
            github_data = None
            github_score = 0
            github_feedback = None
            
            github_username = github_username.strip()
            if github_username:
                github_data = cached_github_analysis(github_username)
                if github_data:
                    github_score = calculate_github_score(github_data)

            career_score = calculate_career_readiness(score, github_score)

            # Fast path: avoid long AI generation during initial processing.
            ai_recs = merge_recommendations([], get_detailed_recommendations(missing), min_items=8)
            ai_roadmap = None
            ai_audit = None
            github_feedback = None
            
            # Save to Session State
            st.session_state.analysis_complete = True
            st.session_state.role = role
            st.session_state.career_score = career_score
            st.session_state.matched = matched
            st.session_state.missing = missing
            st.session_state.score = score
            st.session_state.resume_quality_score = resume_quality_score
            st.session_state.resume_feedback = resume_feedback
            st.session_state.experience_level = experience_level
            st.session_state.ai_level = ai_level
            st.session_state.ai_level_desc = ai_level_desc
            st.session_state.impact_score = impact_score
            st.session_state.impact_feedback = impact_feedback
            st.session_state.github_score = github_score
            st.session_state.ai_recs = ai_recs
            st.session_state.ai_roadmap = ai_roadmap
            st.session_state.ai_audit = ai_audit
            st.session_state.github_data_exists = bool(github_data)
            st.session_state.github_data = github_data
            st.session_state.github_feedback = github_feedback
            st.session_state.github_username = github_username
            st.session_state.resume_text = resume_text
    except Exception as exc:
        st.session_state.analysis_complete = False
        st.error(f"Processing failed: {exc}")

# Render Results if Analysis Complete
if st.session_state.analysis_complete:
    # Retrieve from Session State
    role = st.session_state.role
    career_score = st.session_state.career_score
    matched = st.session_state.matched
    missing = st.session_state.missing
    score = st.session_state.score
    resume_quality_score = st.session_state.resume_quality_score
    resume_feedback = st.session_state.resume_feedback
    experience_level = st.session_state.experience_level
    ai_level = st.session_state.ai_level
    ai_level_desc = st.session_state.ai_level_desc
    impact_score = st.session_state.impact_score
    impact_feedback = st.session_state.impact_feedback
    github_score = st.session_state.github_score
    ai_recs = st.session_state.ai_recs
    ai_audit = st.session_state.ai_audit
    github_data_exists = st.session_state.github_data_exists
    
    # --- DASHBOARD ---
    st.markdown(f"## Analysis for **{role}**")
    
    # Top Metrics
    ai_level_parts = ai_level.split(maxsplit=1)
    ai_level_main = ai_level_parts[0] if ai_level_parts else ai_level
    ai_level_sub = ai_level_parts[1] if len(ai_level_parts) > 1 else ""
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(metric_card_html("Readiness", f"{career_score}%", "Overall Score", "#2563EB"), unsafe_allow_html=True)
    with c2: st.markdown(metric_card_html("AI Proficiency", ai_level_main, ai_level_sub, "#7C3AED"), unsafe_allow_html=True)
    with c3: st.markdown(metric_card_html("GitHub Impact", str(github_score), "Code Quality", "#D97706"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs(["📊 Overview", "🧠 Skills & Gaps", "📄 Resume", "🗺️ Roadmap", "📥 Report"] )
    
    # Tab 1: Overview
    with tabs[0]:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Career Trajectory")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = career_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#4F46E5"},
                    'bar': {'color': "#4F46E5"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#E2E8F0",
                    'steps': [
                        {'range': [0, 50], 'color': "#F1F5F9"},
                        {'range': [50, 80], 'color': "#E2E8F0"}
                    ],
                }
            ))
            fig.update_layout(
                height=300, 
                margin=dict(t=0,b=0,l=0,r=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'family': "Outfit, sans-serif"}
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Career Level")
            st.info(f"**{experience_level}**")
            st.markdown(f"*{ai_level_desc}*")

        if st.session_state.get("github_feedback"):
            st.markdown("---")
            st.markdown("### 🤖 Senior Recruiter Feedback (AI)")
            st.info(st.session_state.github_feedback)

    # Tab 2: Skills
    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ✅ Matched Skills")
            html = "".join([skill_chip(s, "success") for s in matched])
            st.markdown(html, unsafe_allow_html=True)
            
        with c2:
            st.markdown("#### ⚠️ Missing Skills")
            html = "".join([skill_chip(s, "missing") for s in missing])
            st.markdown(html, unsafe_allow_html=True)
        st.markdown("<br>#### Recommended Projects", unsafe_allow_html=True)
        if st.button("Generate Rich AI Recommendations", key="gen_rich_recs"):
            with st.spinner("Generating expanded recommendations..."):
                ai_primary = cached_ai_recommendations(missing, role)
                ai_fallback = get_detailed_recommendations(missing)
                st.session_state.ai_recs = merge_recommendations(ai_primary, ai_fallback, min_items=8)
        if st.session_state.get("ai_recs"):
            for rec in st.session_state.ai_recs:
                st.info(rec)

    # Tab 3: Resume
    with tabs[2]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Quality Audit")
            st.metric("Structure Score", f"{resume_quality_score}/100")
            for f in resume_feedback: st.warning(f)
        with c2:
            st.markdown("#### Impact Analysis")
            st.metric("Impact Score", f"{impact_score}/100")
            st.progress(impact_score)
            for f in impact_feedback: st.info(f)
        if st.button("Run Deep AI Resume Analysis", key="gen_deep_audit"):
            with st.spinner("Running deep AI analysis..."):
                st.session_state.ai_audit = cached_ai_resume_audit(
                    st.session_state.get("resume_text", ""),
                    role
                )

        if st.session_state.get("ai_audit"):
            st.markdown("---")
            st.markdown("### Deep Dive Audit (AI)")
            st.warning(st.session_state.ai_audit)

        # Tab 4: Roadmap
    with tabs[3]:
        st.markdown("### AI Learning Roadmap")
        if st.button("Generate AI Roadmap", key="gen_ai_roadmap"):
            with st.spinner("Building roadmap..."):
                st.session_state.ai_roadmap = cached_ai_roadmap(missing, role)
        if st.session_state.get("ai_roadmap"):
            st.markdown(st.session_state.ai_roadmap)
        else:
            st.info("No roadmap generated yet.")

    # Tab 5: Export
    with tabs[4]:
        st.markdown("### 📥 Download Report")
        report_txt = generate_report(role, career_score, missing, ai_recs)
        st.download_button("Download PDF/Text Report", report_txt, file_name="career_report.txt")
elif analyze_btn and not uploaded_file:
    st.warning("Please upload a resume to begin.")






