from dotenv import load_dotenv
load_dotenv()

import io
import streamlit as st 
import base64
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure Google API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to convert uploaded PDF to images (works on Streamlit Cloud)
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to images (Poppler installed via apt.txt on Streamlit Cloud)
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode image to base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Streamlit App
st.set_page_config(page_title="ATS RESUME EXPERT")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with Tech Experience in Data Science, Full Stack Web Development,
Big Data Engineering, DEVOPS, Data Analyst roles. Review the provided resume against the job description
and share your professional evaluation. Highlight strengths and weaknesses.
Simply list the points.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with deep understanding of
Data Science, Full Stack Web Development, Big Data Engineering, DEVOPS, Data Analyst.
Evaluate the resume against the job description. Give the percentage match first,
then list missing keywords, and finally provide overall thoughts.
"""

# Handle "Tell me about the resume"
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload a resume.")

# Handle "Percentage match"
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please upload a resume.")
