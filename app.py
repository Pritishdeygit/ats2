from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --------------------- Helper Functions ---------------------

def get_gemini_response(input_text, pdf_text, prompt):
    """
    Calls Google Gemini API with the provided text, PDF content, and prompt.
    """
    if not pdf_text:
        return "PDF content not available."

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([input_text, pdf_text, prompt])
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

def extract_pdf_text(uploaded_file):
    """
    Extracts text from the uploaded PDF file using PyPDF2.
    """
    if uploaded_file is None:
        st.error("No file uploaded. Please upload a PDF.")
        return ""

    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        if not text.strip():
            st.warning("PDF has no readable text. Please upload a text-based PDF.")
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# --------------------- Streamlit App ---------------------

st.set_page_config(page_title="ATS RESUME EXPERT")
st.header("ATS Tracking System")

# Input job description
input_text = st.text_area("Job Description:", key="input")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])
if uploaded_file:
    st.success("PDF uploaded successfully!")

# Buttons
submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage match")

# Prompts
input_prompt1 = """
You are an experienced HR with Tech Experience in Data Science, Full Stack web development,
Big Data Engineering, DEVOPS, Data Analyst. Review the provided resume against the job description.
Highlight strengths and weaknesses, simply list the points.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with deep understanding of Data Science,
Full Stack web development, Big Data Engineering, DEVOPS, Data Analyst. Evaluate the resume
against the Job Description. Give percentage match first, then missing keywords, then final thoughts.
"""

# --------------------- Button Actions ---------------------

if submit1:
    if uploaded_file:
        pdf_text = extract_pdf_text(uploaded_file)
        if pdf_text:
            response = get_gemini_response(input_text, pdf_text, input_prompt1)
            st.subheader("Evaluation Response")
            st.write(response)
    else:
        st.warning("Please upload a resume.")

elif submit3:
    if uploaded_file:
        pdf_text = extract_pdf_text(uploaded_file)
        if pdf_text:
            response = get_gemini_response(input_text, pdf_text, input_prompt3)
            st.subheader("Percentage Match Response")
            st.write(response)
    else:
        st.warning("Please upload a resume.")
