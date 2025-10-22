from dotenv import load_dotenv
load_dotenv()

import io
import streamlit as st
import base64
import os
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text 

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open PDF with PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = doc.load_page(0)  # first page
        pix = page.get_pixmap()
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(img_byte_arr, format='JPEG')
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

## Streamlit App
st.set_page_config(page_title="ATS RESUME EXPERT")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage match")

input_prompt1 = """ You are an experienced HR with Tech Experience in the field of Data Science, Full Stack
web development, Big Data Engineering, DEVOPS, Data Analyst, your task is to review the provided
resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job role.
simply list out the points"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack
web development, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality.
Your task is to evaluate the resume against the provided Job Description. Give me the percentage match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final
thoughts. Simply give me the percentage and then list the missing keywords.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is ")
        st.write(response)
    else:
        st.write("Please upload a resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is ")
        st.write(response)
    else:
        st.write("Please upload the resume")
