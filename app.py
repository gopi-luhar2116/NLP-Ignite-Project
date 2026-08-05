from modules.pdf_reader import extract_text_from_pdf
from modules.preprocess import preprocess_text
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

        else:

            resume_text = uploaded_file.read().decode("utf-8")

        st.subheader("Extracted Resume Text")

        with st.expander("View Extracted Resume Text"):
            st.write(resume_text)


#hello this 