from dotenv import load_dotenv
load_dotenv()

import io
import streamlit as st
import base64
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure the Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --------------------- Helper Functions ---------------------

def get_gemini_response(input_text, pdf_content, prompt):
    """
    Calls Google Gemini API with the provided text, PDF content, and prompt.
    """
    if pdf_content is None:
        return "PDF content not available."

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"


def input_pdf_setup(uploaded_file):
    """
    Converts the first page of an uploaded PDF into a base64-encoded image for Streamlit display.
    Compatible with Streamlit Cloud.
    """
    if uploaded_file is None:
        st.error("No file uploaded. Please upload a PDF file.")
        return None

    try:
        # Read the uploaded PDF into bytes
        pdf_bytes = uploaded_file.read()
        
        # Convert PDF to images (all pages)
        images = pdf2image.convert_from_bytes(pdf_bytes)
        
        if not images:
            st.error("Unable to process PDF. It may be empty or corrupted.")
            return None

        # Take the first page
        first_page = images[0]

        # Convert the first page to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()

        # Encode image to base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes).decode()
            }
        ]
        return pdf_parts

    except pdf2image.exceptions.PDFInfoNotInstalledError:
        st.error(
            "PDF processing failed because Poppler is not installed. "
            "Streamlit Cloud should have Poppler by default."
        )
        return None

    except Exception as e:
        st.error(f"An unexpected error occurred while processing the PDF: {e}")
        return None

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

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("Evaluation Response")
            st.write(response)
    else:
        st.warning("Please upload a resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("Percentage Match Response")
            st.write(response)
    else:
        st.warning("Please upload a resume.")
