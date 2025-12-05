# ATS Resume Expert

ATS Resume Expert is a web application that helps evaluate resumes against job descriptions using advanced AI. It leverages **Google Gemini API** to provide insights about strengths, weaknesses, and keyword matches to optimize resumes for Applicant Tracking Systems (ATS).

---

## Features

- Upload a resume in **PDF format**.
- Input a **Job Description** for analysis.
- Evaluate the resume to highlight **strengths and weaknesses**.
- Get **percentage match** and missing keywords compared to the job description.
- Uses **AI-powered analysis** via Google Gemini API.
- Built with **Streamlit** for a user-friendly web interface.

---

## Technologies Used

- **Python**
- **Streamlit**
- **Google Gemini API**
- **pdf2image** (for PDF to image conversion)
- **PIL (Pillow)**
- **dotenv** (for managing API keys)
- **base64** (for image encoding)

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/ats-resume-expert.git
cd ats-resume-expert

**Create a virtual environment (recommended):**

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


##Install dependencies:

pip install -r requirements.txt


Add your Google API key in a .env file:

GOOGLE_API_KEY=your_google_api_key_here

##Usage

Run the Streamlit app:

streamlit run app.py


##Open the app in your browser (usually opens automatically at http://localhost:8501).

Steps in the app:

Enter the job description.

Upload your resume PDF.

Click “Tell me about the resume” to get strengths and weaknesses.

Click “Percentage match” to get ATS score and missing keywords.

Screenshots


Upload resume and input job description.


AI-generated evaluation of resume.

##Notes

Ensure Poppler is installed if running locally for PDF processing (pdf2image dependency).

Compatible with Streamlit Cloud, which includes Poppler by default.

##Author

Pritish Dey

Email: pritish.dey2003@gmail.com

LinkedIn: linkedin.com/in/pritishdey

Location: Guwahati, Assam, India



