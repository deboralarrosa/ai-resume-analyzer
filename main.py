"""
AI Resume & Job Description Analyzer
A clean Streamlit web app that extracts text from a PDF resume, compares it
against a job description using an LLM API (Google Gemini), and highlights
missing keywords and actionable improvements.
"""

import os
import re
from typing import BinaryIO

import pdfplumber
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()


def clean_extracted_text(raw_text: str) -> str:
    """Normalize whitespace and remove extra blank lines from extracted PDF text."""
    if not raw_text:
        return ""
    cleaned = re.sub(r"\s+", " ", raw_text)
    return cleaned.strip()


def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    """Extract and clean all text pages from an uploaded PDF file."""
    pages_text: list[str] = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_content = page.extract_text()
            if page_content:
                pages_text.append(page_content)
    return clean_extracted_text(" ".join(pages_text))


def find_missing_keywords(resume_text: str, required_keywords: list[str]) -> list[str]:
    """Identify which target keywords are missing from the resume (case-insensitive)."""
    resume_lower = resume_text.lower()
    missing: list[str] = []
    for keyword in required_keywords:
        cleaned_kw = keyword.strip()
        if cleaned_kw and cleaned_kw.lower() not in resume_lower:
            missing.append(cleaned_kw)
    return missing


def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    """Create a structured prompt for the LLM to evaluate the resume against the job post."""
    return (
        "You are an expert technical recruiter and career coach.\n"
        "Compare the following Resume against the Job Description and provide:\n"
        "1. **Match Score (0-100%)**: A realistic estimate of alignment.\n"
        "2. **Missing Keywords**: Specific technical skills or tools mentioned in the job "
        "description that are missing from the resume.\n"
        "3. **Top 3 Actionable Improvements**: Concrete bullet points the candidate can add.\n\n"
        f"--- JOB DESCRIPTION ---\n{job_description.strip()}\n\n"
        f"--- RESUME ---\n{resume_text.strip()}"
    )


def analyze_resume_with_ai(resume_text: str, job_description: str, api_key: str) -> str:
    """Send the structured prompt to the Gemini LLM API and return the analysis."""
    client = genai.Client(api_key=api_key)
    prompt = build_analysis_prompt(resume_text, job_description)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text or "No response generated."


def render_app() -> None:
    """Render the Streamlit user interface."""
    st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")
    st.title("📄 AI Resume & Job Match Analyzer")
    st.write("Upload your resume (PDF) and paste a job description to discover missing keywords.")

    uploaded_pdf = st.file_uploader("1. Upload your Resume (PDF)", type=["pdf"])
    job_description = st.text_area("2. Paste the Job Description", height=180)

    if st.button("Analyze Resume", type="primary"):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not uploaded_pdf or not job_description.strip():
            st.warning("Please upload a PDF resume and paste a job description first.")
            return
        if not api_key:
            st.error("Missing GEMINI_API_KEY in environment variables (.env).")
            return

        with st.spinner("Extracting PDF text and analyzing with AI..."):
            resume_text = extract_text_from_pdf(uploaded_pdf)
            result = analyze_resume_with_ai(resume_text, job_description, api_key)
            st.subheader("Analysis Results")
            st.markdown(result)


if __name__ == "__main__":
    render_app()
