"""
core.py
Handles: resume text extraction (PDF/DOCX), schema definition,
prompt + LLM chain setup, and chain execution.
Returns a single MatchResult object to the UI layer.
"""

import os
import tempfile
from typing import List
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ── 1. Output Schema ─────────────────────────────────────────────
class MatchResult(BaseModel):
    match_score: int = Field(description="Overall match score 0-100")
    matched_keywords: List[str] = Field(description="Key skills/terms present in both JD and resume")
    missing_keywords: List[str] = Field(description="Important JD keywords/skills absent from resume")
    improvement_areas: List[str] = Field(description="Specific, actionable suggestions to improve the resume for this JD")
    summary: str = Field(description="2-3 sentence overall assessment")


# ── 2. Resume Text Extraction ────────────────────────────────────
#PDF
#↓
#PyPDFLoader
#↓
#loader.load()
#↓
#docs
#↓
#page_content
#↓
#Complete resume text

def extract_resume_text(uploaded_file) -> str:      #extract_resume_text
    """Takes a Streamlit UploadedFile object, returns plain text."""
    suffix = os.path.splitext(uploaded_file.name)[1].lower()

#create a temporary file to store the uploaded resume for processing

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
        elif suffix == ".docx":
            loader = Docx2txtLoader(tmp_path)
        else:
            raise ValueError("Unsupported file type. Please upload PDF or DOCX.")

        docs = loader.load()
        return "\n".join(d.page_content for d in docs)  # Concatenate all page contents into a single string
    finally:
        os.unlink(tmp_path)     # Clean up the temporary file after extraction


# ── 3. LLM + Prompt + Chain Setup ────────────────────────────────
def _build_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(MatchResult)

    prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and ATS (Applicant Tracking System) analyst.

Compare the RESUME against the JOB DESCRIPTION below. Be precise and specific.

Rules:
- match_score should reflect skills, experience level, and role alignment — not just keyword overlap.
- missing_keywords should only include terms that meaningfully matter for this role (skip generic filler).
- improvement_areas should be concrete and actionable (e.g. "Quantify impact of the X project with metrics" not "improve resume").
- Only reference skills/terms that literally appear in the JD or resume text — do not invent or assume skills.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}
""")

    return prompt | structured_llm


# ── 4. Public Entry Point: Run Extraction + Chain, Return Result ─
def analyze_resume(jd_text: str, uploaded_file) -> MatchResult:
    """
    Full pipeline in one call:
    uploaded_file -> extracted text -> chain execution -> MatchResult
    """
    resume_text = extract_resume_text(uploaded_file)
    chain = _build_chain()
    result = chain.invoke({"jd_text": jd_text, "resume_text": resume_text})
    return result