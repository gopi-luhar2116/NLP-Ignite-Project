print("RUNNING APP_NEW")
import streamlit as st

from modules.pdf_reader import extract_text_from_pdf
from modules.preprocess import preprocess_text
from modules.skill_extractor import extract_skills
from modules.matcher import compare_skills
from modules.ats_score import calculate_ats_score
from modules.suggestions import generate_suggestions

st.title("THIS IS APP_NEW")

st.set_page_config(
    page_title="Resume Matcher & ATS Optimizer",
    page_icon="📄",
    layout="wide"
)

st.title("Resume Matcher & ATS Optimizer")

st.caption(
    "NLP-powered resume analysis that evaluates compatibility "
    "between your resume and a job description."
)

st.divider()

left, right = st.columns(2)
with left:

    st.subheader("Resume")

    uploaded_file = st.file_uploader(
        "Upload a PDF resume",
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

if analyze:
        resume_text = extract_text_from_pdf(uploaded_file)

    processed_resume = preprocess_text(resume_text)
    processed_job = preprocess_text(job_description)

    resume_skills = extract_skills(processed_resume)
    job_skills = extract_skills(processed_job)

    matched_skills, missing_skills = compare_skills(
        resume_skills,
        job_skills
    )

    ats_score = calculate_ats_score(
        matched_skills,
        job_skills
    )

    recommendations = generate_suggestions(
        missing_skills,
        ats_score
    )
        
    st.divider()
    st.subheader("Analysis Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "ATS Score",
        f"{ats_score}%"
    )

    c2.metric(
        "Resume Skills",
        len(resume_skills)
    )

    c3.metric(
        "Matched Skills",
        len(matched_skills)
    )

    c4.metric(
        "Missing Skills",
        len(missing_skills)
    )

    st.write("")

    if ats_score >= 80:
        st.success("Excellent Compatibility")

    elif ats_score >= 60:
        st.warning("Good Compatibility")

    else:
        st.error("Needs Improvement") 

        st.subheader("Skill Comparison")

    table = []

    for skill in sorted(job_skills):

        if skill in matched_skills:
            status = "✅ Found"

        else:
            status = "❌ Missing"

        table.append({
            "Required Skill": skill,
            "Status": status
        })

    st.table(table)       

    if uploaded_file is None:
        st.warning("Please upload a resume.")
        st.stop()

    if job_description.strip() == "":
        st.warning("Please paste a job description.")
        st.stop()