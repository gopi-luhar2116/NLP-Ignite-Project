from modules.pdf_reader import extract_text_from_pdf
from modules.preprocess import preprocess_text
from modules.skill_extractor import extract_skills
from modules.matcher import compare_skills
from modules.ats_score import calculate_ats_score
from modules.suggestions import generate_suggestions
import streamlit as st

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

def metric_card(title, value, color="#FFFFFF"):
    st.markdown(f"""
    <div style="
        background:#1E293B;
        padding:20px;
        border-radius:15px;
        border:1px solid #334155;
        text-align:center;
        min-height:120px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">

        <div style="
            color:#94A3B8;
            font-size:16px;
            font-weight:500;
            margin-bottom:10px;
        ">
            {title}
        </div>

        <div style="
            color:{color};
            font-size:36px;
            font-weight:700;
        ">
            {value}
        </div>

    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='padding:25px 10px 10px 10px;'>

<h1 style='margin-bottom:5px;
font-size:48px;
font-weight:700;
color:white;'>

Resume Matcher & ATS Optimizer

</h1>

<p style='font-size:18px;
color:#94A3B8;
margin-top:0;'>

NLP-powered resume analysis that evaluates compatibility with a job description and provides actionable ATS recommendations.

</p>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,1], gap="large")

with col1:

    st.markdown("### Resume")

    uploaded_file = st.file_uploader(
         "",
        type=["pdf"]
    )

with col2:

    st.markdown("### Job Description")

    job_description = st.text_area(
        "",
        height=240,
        placeholder="Paste the complete job description..."
    )

analyze = st.button("Analyze Resume", use_container_width=True)
    
if analyze:

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

            st.divider()

            st.markdown("## Analysis Overview")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                metric_card("Compatibility", f"{ats_score:.0f}%", "#3B82F6")

            with col2:
                metric_card("Resume Skills", len(resume_skills), "#22C55E")

            with col3:
                metric_card("Missing Skills", len(missing_skills), "#EF4444")

            with col4:
                metric_card("Matched Skills", len(matched_skills), "#FACC15")

            st.markdown("<br>", unsafe_allow_html=True)

            if ats_score >= 80:
                st.success("Excellent Compatibility")

            elif ats_score >= 60:
                st.warning("Good Compatibility")

            else:
                st.error("Needs Improvement")

        else:

            resume_text = uploaded_file.read().decode("utf-8")
            processed_resume = preprocess_text(resume_text)
            #resume_skills = extract_skills(processed_resume)

        with st.expander("⚙ Developer View (NLP Processing)"):

            st.subheader("Original Resume")

            st.write(resume_text)

            st.subheader("Processed Tokens")

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

        st.header("📈 Resume vs Job Comparison")

        comparison = []

        for skill in sorted(set(job_skills)):

            comparison.append({
            "Job Requirement": skill,
            "Found in Resume": "✅" if skill.lower() in [s.lower() for s in resume_skills] else "❌"
        })

        st.table(comparison)

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
