from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --------------------- Helper Functions ---------------------

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def get_gemini_response(input_text, pdf_text, prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([input_text, pdf_text, prompt])
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

# --------------------- Streamlit App ---------------------

st.set_page_config(page_title="ATS RESUME EXPERT")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with Tech Experience in Data Science, Full Stack web development,
Big Data Engineering, DEVOPS, Data Analyst. Review the resume against the job description.
Highlight strengths and weaknesses, simply list the points.
"""

input_prompt3 = """
You are a skilled ATS scanner with deep understanding of Data Science,
Full Stack web development, Big Data Engineering, DEVOPS, Data Analyst. Evaluate the resume
against the Job Description. Give percentage match first, then missing keywords, then final thoughts.
"""

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
else:
    pdf_text = None

if submit1:
    if pdf_text:
        response = get_gemini_response(input_text, pdf_text, input_prompt1)
        st.subheader("Evaluation Response")
        st.write(response)
    else:
        st.warning("Please upload a resume.")

elif submit3:
    if pdf_text:
        response = get_gemini_response(input_text, pdf_text, input_prompt3)
        st.subheader("Percentage Match Response")
        st.write(response)
    else:
        st.warning("Please upload a resume.")
