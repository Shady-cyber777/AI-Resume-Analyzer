import streamlit as st
import pypdf
import ollama

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("AI Resume Analyzer")
st.write("Upload your resume and paste a job description to get an AI resume match analysis.")

resume_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
job_description = st.text_area("Paste the job description here")

def extract_text_from_pdf(file):
    reader = pypdf.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

if st.button("Analyze Resume"):
    if resume_file is None:
        st.error("Please upload a resume PDF.")
    elif job_description.strip() == "":
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing resume with local Ollama AI..."):
            resume_text = extract_text_from_pdf(resume_file)

            prompt = f"""
You are an AI resume analyzer.

Compare the resume to the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Give me:
1. Match score out of 100
2. Skills that match
3. Missing skills
4. Resume improvement suggestions
5. Interview questions to prepare for
"""

            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.subheader("AI Resume Analysis")
            st.write(response["message"]["content"])