from modules.pdf_reader import extract_text_from_pdf
from modules.preprocess import preprocess_text
from modules.skill_extractor import extract_skills
from modules.matcher import compare_skills
from modules.ats_score import calculate_ats_score
from modules.suggestions import generate_suggestions
import streamlit as st

st.title("📄 Resume Matcher & ATS Optimizer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf","txt"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload a resume.")

    else:

        if uploaded_file.type == "application/pdf":

            resume_text = extract_text_from_pdf(uploaded_file)
            processed_resume = preprocess_text(resume_text)
            resume_skills = extract_skills(processed_resume)
            processed_job = preprocess_text(job_description)
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

        else:

            resume_text = uploaded_file.read().decode("utf-8")
            processed_resume = preprocess_text(resume_text)
            #resume_skills = extract_skills(processed_resume)

        st.subheader("Extracted Resume Text")

        with st.expander("View Original Resume Text"):
            st.write(resume_text)

        with st.expander("View Processed Resume Tokens"):
    # Change ", ".join(...) to " ".join(...) for clean text output
            st.write(" ".join(processed_resume))

        st.subheader("🎯 Skills Detected")

        cols = st.columns(3)

        for i, skill in enumerate(resume_skills):
            cols[i % 3].success(skill)

        st.subheader("💼 Job Skills Required")

        if job_skills:
            cols = st.columns(3)

            for i, skill in enumerate(job_skills):
                cols[i % 3].success(skill)

        else:
            st.warning("No job skills detected.")

        st.subheader("✅ Matching Skills")

        if matched_skills:

            cols = st.columns(3)

            for i, skill in enumerate(matched_skills):
                cols[i % 3].success(skill.title())

        else:
            st.warning("No matching skills.")

        st.subheader("❌ Missing Skills")

        if missing_skills:

            cols = st.columns(3)

            for i, skill in enumerate(missing_skills):
                cols[i % 3].error(skill.title())

        else:
            st.success("No missing skills.")

        st.subheader("🎯 ATS Match Score")

        st.progress(int(ats_score))

        if ats_score >= 80:
            st.success(f"🎯 ATS Score : {ats_score}%")

        elif ats_score >= 60:
            st.warning(f"🎯 ATS Score : {ats_score}%")

        else:
            st.error(f"🎯 ATS Score : {ats_score}%")

        st.subheader("💡 ATS Recommendations")

        for suggestion in recommendations:
            st.info(suggestion)

        st.subheader("📊 Analysis Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Resume Skills", len(resume_skills))

        col2.metric("Required Skills", len(job_skills))

        col3.metric("Matched Skills", len(matched_skills))
