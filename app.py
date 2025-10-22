from dotenv import load_dotenv
load_dotenv()

import io
import streamlit as st
import os
import pdf2image
import base64
import google.generativeai as genai
import fitz  # PyMuPDF for text extraction

# Configure the Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --------------------- Helper Functions ---------------------

def get_gemini_response(input_text, pdf_text, prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([input_text, pdf_text, prompt])
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text

def get_first_page_image(uploaded_file):
    uploaded_file.seek(0)  # reset file pointer after reading
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    pdf_image = base64.b64encode(img_bytes).decode()
    return pdf_image

# --------------------- Streamlit App ---------------------

st.set_page_config(page_title="ATS RESUME EXPERT")
st.header("ATS Tracking System")

# Input job description
input_text = st.text_area("Job Description:", key="input")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])
if uploaded_file is not None:
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

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)  # extract text for Gemini
    first_page_image = get_first_page_image(uploaded_file)  # optional for display
    st.image(base64.b64decode(first_page_image), use_column_width=True)

    if submit1:
        response = get_gemini_response(input_text, pdf_text, input_prompt1)
        st.subheader("Evaluation Response")
        st.write(response)

    elif submit3:
        response = get_gemini_response(input_text, pdf_text, input_prompt3)
        st.subheader("Percentage Match Response")
        st.write(response)
