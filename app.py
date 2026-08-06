import streamlit as st

from modules.pdf_reader import extract_text_from_pdf
from modules.preprocess import preprocess_text
from modules.skill_extractor import extract_skills
from modules.matcher import compare_skills, calculate_semantic_similarity
from modules.ats_score import calculate_ats_score
from modules.suggestions import generate_suggestions

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Resume Matcher & ATS Optimizer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CSS ---------------- #

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# ---------------- HEADER ---------------- #

st.markdown("""
<h1 style='margin-bottom:0px;'>
Resume Matcher & ATS Optimizer
</h1>

<p style='color:gray;font-size:18px;'>
Analyze your resume against a job description using NLP
to evaluate ATS compatibility and identify missing skills.
</p>
""", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT SECTION ---------------- #

left, right = st.columns(2)

with left:
    st.subheader("Resume")
    uploaded_file = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"]
    )

with right:
    st.subheader("Job Description")
    job_description = st.text_area(
        "",
        height=250,
        placeholder="Paste the complete job description here..."
    )

st.write("")

analyze = st.button(
    "Analyze Resume",
    use_container_width=True
)

# ---------------- ANALYSIS & RESULTS ---------------- #

if analyze:

    if uploaded_file is None:
        st.error("Please upload a resume.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        # Extract Resume
        resume_text = extract_text_from_pdf(uploaded_file)

        # Preprocess
        processed_resume = preprocess_text(resume_text)
        processed_job = preprocess_text(job_description)

        # Extract Skills
        resume_skills = extract_skills(processed_resume)
        job_skills = extract_skills(processed_job)

        # Compare Skills
        matched_skills, missing_skills = compare_skills(
            resume_skills,
            job_skills
        )

        # Recommendations
        recommendations = generate_suggestions(
            missing_skills,
            0
        )

    # ---------------- DUAL SCORING LOGIC ---------------- #
    raw_resume_str = " ".join(processed_resume)
    raw_job_str = " ".join(processed_job)
    
    # Calculate Semantic Cosine Similarity via TF-IDF
    semantic_score = calculate_semantic_similarity(raw_resume_str, raw_job_str)
    
    # Hybrid Final ATS Score (60% Skill Match + 40% Semantic Similarity)
    keyword_score = calculate_ats_score(matched_skills, job_skills)
    final_score = round((keyword_score * 0.6) + (semantic_score * 0.4))

    st.markdown("---")
    st.markdown("## 📊 Hybrid ATS Analysis")

    st.progress(int(final_score))

    if final_score >= 80:
        st.success(f"🚀 High Match Potential • {final_score}% Overall Score")
    elif final_score >= 60:
        st.info(f"📈 Moderate Match • {final_score}% Overall Score")
    else:
        st.error(f"⚠️ Low Match • {final_score}% Overall Score")

    st.write("")

    # ---------------- METRIC CARDS ---------------- #
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{final_score}%</div>
            <div class="metric-label">Overall Match</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #a78bfa;">{semantic_score}%</div>
            <div class="metric-label">Semantic Similarity</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #4ade80;">{len(matched_skills)}</div>
            <div class="metric-label">Matched Skills</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f87171;">{len(missing_skills)}</div>
            <div class="metric-label">Missing Skills</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- SKILL GAP ANALYSIS ---------------- #
    st.divider()
    st.header("🎯 Skill Gap Breakdown")

    s_left, s_right = st.columns(2)

    with s_left:
        st.subheader("✅ Matched Keywords")
        if matched_skills:
            matched_html = "".join([
                f"<span style='background-color: #064e3b; color: #6ee7b7; border: 1px solid #047857; "
                f"padding: 6px 14px; border-radius: 20px; margin: 4px; display: inline-block; "
                f"font-size: 14px; font-weight: 500;'>{s.title()}</span>"
                for s in matched_skills
            ])
            st.markdown(matched_html, unsafe_allow_html=True)
        else:
            st.info("No explicit skills matched.")

    with s_right:
        st.subheader("🚨 Priority Missing Keywords")
        if missing_skills:
            missing_html = "".join([
                f"<span style='background-color: #7f1d1d; color: #fca5a5; border: 1px solid #b91c1c; "
                f"padding: 6px 14px; border-radius: 20px; margin: 4px; display: inline-block; "
                f"font-size: 14px; font-weight: 500;'>{s.title()}</span>"
                for s in missing_skills
            ])
            st.markdown(missing_html, unsafe_allow_html=True)
        else:
            st.success("All required skills found in resume!")

    # ---------------- ACTIONABLE RECOMMENDATIONS ---------------- #
    st.divider()
    st.header("💡 Actionable Recommendations")

    if missing_skills:
        st.markdown(f"""
        <div class="suggestion-card">
            <b>🔑 High Impact Addition:</b> Add top missing keywords like <b>{', '.join([s.title() for s in missing_skills[:3]])}</b> to your skill list or project bullet points.
        </div>
        <div class="suggestion-card">
            <b>📝 Contextual Alignment:</b> Incorporate these technical terms naturally in your experience section rather than just listing them in a skills block.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("Your resume aligns exceptionally well with the target job description.")

    # ---------------- DEBUG / PROCESSED TEXT ---------------- #
    st.write("")
    with st.expander("🔍 View Processed Text Tokens"):
        st.write("**Processed Resume Tokens:**")
        st.caption(" ".join(processed_resume))
        st.write("**Processed Job Description Tokens:**")
        st.caption(" ".join(processed_job))