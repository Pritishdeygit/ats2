# ATS Resume Expert

1. **Project Overview:**  
   ATS Resume Expert is a web application that helps evaluate resumes against job descriptions using advanced AI. It leverages **Google Gemini API** to provide insights about strengths, weaknesses, and keyword matches to optimize resumes for Applicant Tracking Systems (ATS).

2. **Features:**  
   - Upload a resume in **PDF format**.  
   - Input a **Job Description** for analysis.  
   - Evaluate the resume to highlight **strengths and weaknesses**.  
   - Get **percentage match** and missing keywords compared to the job description.  
   - Uses **AI-powered analysis** via Google Gemini API.  
   - Built with **Streamlit** for a user-friendly web interface.

3. **Technologies Used:**  
   - **Python**  
   - **Streamlit**  
   - **Google Gemini API**  
   - **pdf2image** (for PDF to image conversion)  
   - **PIL (Pillow)**  
   - **dotenv** (for managing API keys)  
   - **base64** (for image encoding)

4. **Installation:**  
   - **Clone the repository:**  
     ```bash
     git clone https://github.com/your-username/ats-resume-expert.git
     cd ats-resume-expert
     ```  
   - **Create a virtual environment (recommended):**  
     ```bash
     python -m venv venv
     # Linux/Mac
     source venv/bin/activate
     # Windows
     venv\Scripts\activate
     ```  
   - **Install dependencies:**  
     ```bash
     pip install -r requirements.txt
     ```  
   - **Add your Google API key** in a `.env` file:  
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

5. **Usage:**  
   - **Run the Streamlit app:**  
     ```bash
     streamlit run app.py
     ```  
   - **Open the app** in your browser (usually opens automatically at `http://localhost:8501`).  
   - **Steps in the app:**  
     - Enter the **job description**.  
     - Upload your **resume PDF**.  
     - Click **“Tell me about the resume”** to get strengths and weaknesses.  
     - Click **“Percentage match”** to get ATS score and missing keywords.

6. **Notes:**  
   - Ensure **Poppler** is installed if running locally for PDF processing (`pdf2image` dependency).  
   - Compatible with **Streamlit Cloud**, which includes Poppler by default.

7. **Author:**  
   **Pritish Dey**  
   - Email: pritish.dey2003@gmail.com  
   - LinkedIn: [linkedin.com/in/pritishdey](https://www.linkedin.com/in/pritishdey)  
   - Location: Guwahati, Assam, India
