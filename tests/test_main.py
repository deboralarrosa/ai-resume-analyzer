"""
Unit tests for AI Resume & Job Description Analyzer using pytest.
"""

from main import build_analysis_prompt, clean_extracted_text, find_missing_keywords


def test_clean_extracted_text() -> None:
    """Verify that multiple spaces, tabs, and newlines are normalized."""
    raw = "Python   Developer\n\n   with   SQL\tand   Git"
    assert clean_extracted_text(raw) == "Python Developer with SQL and Git"


def test_find_missing_keywords() -> None:
    """Verify case-insensitive detection of missing job keywords."""
    resume = "Experienced in Python, SQL, and Docker containerization."
    target_skills = ["python", "Docker", "FastAPI", "Kubernetes"]
    missing = find_missing_keywords(resume, target_skills)
    assert missing == ["FastAPI", "Kubernetes"]


def test_build_analysis_prompt() -> None:
    """Verify that both the resume text and job description are included in the prompt."""
    resume = "Jane Doe - Data Analyst skilled in Python and Pandas."
    job = "Looking for a Data Analyst with Python, Pandas, and Tableau."
    prompt = build_analysis_prompt(resume_text=resume, job_description=job)

    assert "Jane Doe - Data Analyst" in prompt
    assert "Tableau" in prompt
    assert "Missing Keywords" in prompt
