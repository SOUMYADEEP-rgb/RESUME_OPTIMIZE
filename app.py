import streamlit as st
import openai
import pdfplumber
from utils import preprocess_text, compute_similarity, extract_keywords, find_missing_keywords

st.title("📄 AI Resume & LinkedIn Optimizer")

resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])
job_description = st.text_area("Paste the Job Description")

if resume_file and job_description:
    # Extract text from PDF
    if resume_file.name.endswith(".pdf"):
        with pdfplumber.open(resume_file) as pdf:
            resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    else:
        resume_text = resume_file.read().decode("utf-8")

    # Process
    resume_clean = preprocess_text(resume_text)
    jd_clean = preprocess_text(job_description)

    score = compute_similarity(resume_clean, jd_clean)
    resume_keywords = extract_keywords(resume_clean)
    jd_keywords = extract_keywords(jd_clean)
    missing_keywords = find_missing_keywords(resume_keywords, jd_keywords)

    # Results
    st.metric("✅ Match Score", f"{score}%")
    st.write("🔍 Missing Keywords:")
    st.write(", ".join(missing_keywords))
    st.subheader("💼 LinkedIn Summary Generator")

    if st.button("Generate LinkedIn Summary"):
        # Simple heuristic: take first 2-3 lines from resume summary + top skills from job description
        resume_lines = resume_text.strip().split('\n')
        summary_lines = []
        for line in resume_lines:
            if line.strip():
                summary_lines.append(line.strip())
            if len(summary_lines) >= 3:
                break
        summary_text = " ".join(summary_lines)

        jd_words = job_description.lower().split()
        common_skills = ['python', 'sql', 'tableau', 'power bi', 'statistics', 'data analysis', 'machine learning']
        skills_found = [skill for skill in common_skills if skill in jd_words]

        linkedin_summary = f"{summary_text}. Skilled in {', '.join(skills_found)}. Passionate about leveraging data to drive business decisions."

        st.success("✅ Generated LinkedIn Summary:")
        st.write(linkedin_summary)