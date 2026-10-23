# AI Resume & Job Description Analyzer

A streamlined web application built with **Streamlit** and the **Google Gemini API** that extracts text from PDF resumes, compares candidate qualifications against a target job description, and identifies missing keywords and high-impact improvements.

## Why This Project?

Tailoring a resume for every job application is tedious. This tool combines PDF parsing (`pdfplumber`), structured LLM prompting, and a pure-Python interactive web interface (`Streamlit`) to give instant, actionable feedback.

## Key Features

- **Clean Web Interface**: Built in pure Python with `Streamlit`—no HTML, CSS, or JavaScript required.
- **Accurate PDF Text Extraction**: Uses `pdfplumber` to extract and normalize multi-page resume text.
- **Structured AI Evaluation**: Sends a carefully engineered prompt to the Gemini LLM API to return a match score, missing technical keywords, and 3 concrete improvements.
- **Type-Safe & Unit Tested**: Full Python static Type Hints and unit tests powered by `pytest`.
- **Docker Support**: Ready to run anywhere with the included `Dockerfile`.

## Architecture Workflow

```
+------------------+      +---------------------+      +----------------------+      +--------------------+
|   User Inputs    | ---> |   PDF Text Parser   | ---> |  Structured Prompt   | ---> |   Streamlit UI     |
| (PDF + Job Post) |      |    (pdfplumber)     |      |  (Google Gemini API) |      | (Missing Keywords) |
+------------------+      +---------------------+      +----------------------+      +--------------------+
```

## Project Structure

```
ai-resume-analyzer/
├── main.py              # Streamlit UI, PDF extraction, and LLM API integration
├── requirements.txt     # Project dependencies
├── .env.example         # Template for API key configuration
├── Dockerfile           # Container definition for Streamlit deployment
├── README.md            # Project documentation
└── tests/
    └── test_main.py     # Unit tests with pytest
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Your API Key

Copy `.env.example` to `.env` and add your Google Gemini API key:

```bash
cp .env.example .env
```

Edit `.env`:

```ini
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 4. Launch the Web App

```bash
streamlit run main.py
```

Open your browser at `http://localhost:8501`.

## Running Unit Tests

Validate the text extraction, keyword matching, and prompt builder logic using `pytest`:

```bash
pytest
```

## Running with Docker

```bash
docker build -t ai-resume-analyzer .
docker run -p 8501:8501 --env-file .env ai-resume-analyzer
```
