"""
app.py
Professional, full-screen Streamlit UI for the Resume <-> Job Description
matcher powered by core.py (analyze_resume / MatchResult).
"""

import json
import streamlit as st
from core import analyze_resume, MatchResult


# ──────────────────────────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Resume Parser Pro",
    page_icon="📄",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────────────────────────
# 2. GLOBAL CSS
# ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* ---- kill default Streamlit chrome ---- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}

    /* ---- true full-width layout ---- */
    .block-container {
        max-width: 100% !important;
        padding: 1.2rem 3rem 3rem 3rem !important;
    }

    /* ---- app background ---- */
    .stApp {
        background: #0f1420;
        color: #e6e9f0;
    }
    section[data-testid="stSidebar"] {
        background: #141a2b;
        border-right: 1px solid #232b42;
    }
    section[data-testid="stSidebar"] * {
        color: #e6e9f0;
    }

    /* ---- accent color ---- */
    :root {
        --accent: #6366f1;
        --accent-soft: rgba(99, 102, 241, 0.15);
        --card-bg: #171e30;
        --card-border: #262f47;
        --good: #22c55e;
        --warn: #f59e0b;
        --bad: #ef4444;
    }

    /* ---- hero ---- */
    .hero {
        background: linear-gradient(120deg, #1a2140 0%, #23295a 60%, #2d1b4e 100%);
        border: 1px solid var(--card-border);
        border-radius: 18px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }
    .hero h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #a5b4fc, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        margin: 0.4rem 0 0 0;
        color: #aab2c8;
        font-size: 1rem;
    }

    /* ---- generic card ---- */
    .card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.18);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(0,0,0,0.3);
    }
    .card h3 {
        margin-top: 0;
        font-size: 1.05rem;
        font-weight: 700;
        color: #d7dcec;
    }

    /* ---- pills / badges ---- */
    .pill {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        margin: 0.25rem 0.35rem 0.25rem 0;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .pill-good {
        background: rgba(34,197,94,0.15);
        color: #4ade80;
        border: 1px solid rgba(34,197,94,0.35);
    }
    .pill-bad {
        background: rgba(239,68,68,0.12);
        color: #f87171;
        border: 1px solid rgba(239,68,68,0.32);
    }

    /* ---- upload zone ---- */
    div[data-testid="stFileUploaderDropzone"] {
        background: var(--card-bg) !important;
        border: 2px dashed #3a4468 !important;
        border-radius: 14px !important;
    }

    /* ---- buttons ---- */
    .stButton > button {
        background: var(--accent);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.3rem;
        font-weight: 600;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        background: #4f46e5;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(99,102,241,0.35);
    }

    /* ---- metric cards ---- */
    div[data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 0.8rem 1rem;
    }

    /* ---- score ring text ---- */
    .score-big {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 0;
    }
    .score-label {
        text-align: center;
        color: #9aa3ba;
        font-size: 0.9rem;
        margin-top: -0.3rem;
    }

    /* ---- expander ---- */
    div[data-testid="stExpander"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────
# 3. HERO HEADER
# ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>📄 Resume Parser Pro</h1>
        <p>AI-powered resume ↔ job description matching — instant scoring, gap analysis, and actionable improvement tips.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────
# 4. SESSION STATE
# ──────────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None


# ──────────────────────────────────────────────────────────────────
# 5. SIDEBAR — inputs
# ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")

    jd_text = st.text_area(
        "Paste the Job Description",
        height=220,
        placeholder="Paste the full job description text here...",
    )

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF or DOCX)",
        type=["pdf", "docx"],
    )

    st.markdown("#### Analysis Options")
    show_matched = st.toggle("Show matched keywords", value=True)
    show_missing = st.toggle("Show missing keywords", value=True)
    show_improve = st.toggle("Show improvement suggestions", value=True)

    analyze_clicked = st.button("🔍 Analyze Resume", use_container_width=True)

    with st.expander("ℹ️ About this tool"):
        st.write(
            "Upload a resume and paste a job description. The app extracts the "
            "resume text, sends both to an LLM, and returns a structured match "
            "score, matched/missing keywords, and concrete improvement tips."
        )
        st.caption("Supported formats: PDF, DOCX. Powered by GPT-4o-mini via LangChain.")


# ──────────────────────────────────────────────────────────────────
# 6. RUN ANALYSIS
# ──────────────────────────────────────────────────────────────────
if analyze_clicked:
    st.session_state.result = None
    st.session_state.error = None

    if not uploaded_file:
        st.session_state.error = "Please upload a resume file (PDF or DOCX)."
    elif not jd_text or not jd_text.strip():
        st.session_state.error = "Please paste a job description."
    else:
        with st.spinner("Analyzing resume against job description..."):
            try:
                result: MatchResult = analyze_resume(jd_text, uploaded_file)
                st.session_state.result = result
            except Exception as e:
                st.session_state.error = f"Analysis failed: {e}"

if st.session_state.error:
    st.error(st.session_state.error)


# ──────────────────────────────────────────────────────────────────
# 7. MAIN CONTENT
# ──────────────────────────────────────────────────────────────────
result: MatchResult = st.session_state.result

if result is None and not st.session_state.error:
    st.markdown(
        """
        <div class="card" style="text-align:center; padding:3rem 2rem;">
            <h3>👋 Ready when you are</h3>
            <p style="color:#9aa3ba;">
                Paste a job description and upload a resume in the sidebar, then click
                <b>Analyze Resume</b> to see the match report here.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif result is not None:
    st.toast("Analysis complete!", icon="✅")

    left, right = st.columns([1, 2.2], gap="large")

    # ---- LEFT: score card ----
    with left:
        score = result.match_score
        color = "#22c55e" if score >= 75 else "#f59e0b" if score >= 50 else "#ef4444"
        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
                <h3>Match Score</h3>
                <p class="score-big" style="color:{color};">{score}</p>
                <p class="score-label">out of 100</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(max(score, 0), 100) / 100)

        c1, c2 = st.columns(2)
        c1.metric("Matched", len(result.matched_keywords))
        c2.metric("Missing", len(result.missing_keywords))

        st.markdown(
            f"""
            <div class="card">
                <h3>📝 Summary</h3>
                <p style="color:#c7cce0;">{result.summary}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- RIGHT: tabs ----
    with right:
        tab_names = []
        if show_matched:
            tab_names.append("✅ Matched Keywords")
        if show_missing:
            tab_names.append("⚠️ Missing Keywords")
        if show_improve:
            tab_names.append("🚀 Improvement Areas")
        tab_names.append("📦 Export")

        tabs = st.tabs(tab_names)
        idx = 0

        if show_matched:
            with tabs[idx]:
                if result.matched_keywords:
                    pills = "".join(
                        f'<span class="pill pill-good">{kw}</span>'
                        for kw in result.matched_keywords
                    )
                    st.markdown(f'<div class="card">{pills}</div>', unsafe_allow_html=True)
                else:
                    st.info("No matched keywords found.")
            idx += 1

        if show_missing:
            with tabs[idx]:
                if result.missing_keywords:
                    pills = "".join(
                        f'<span class="pill pill-bad">{kw}</span>'
                        for kw in result.missing_keywords
                    )
                    st.markdown(f'<div class="card">{pills}</div>', unsafe_allow_html=True)
                else:
                    st.success("No missing keywords — great coverage!")
            idx += 1

        if show_improve:
            with tabs[idx]:
                if result.improvement_areas:
                    for i, item in enumerate(result.improvement_areas, 1):
                        with st.expander(f"Suggestion {i}", expanded=(i == 1)):
                            st.write(item)
                else:
                    st.info("No specific improvement areas were flagged.")
            idx += 1

        with tabs[idx]:
            export_data = {
                "match_score": result.match_score,
                "matched_keywords": result.matched_keywords,
                "missing_keywords": result.missing_keywords,
                "improvement_areas": result.improvement_areas,
                "summary": result.summary,
            }
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("Download the full analysis as JSON.")
            st.download_button(
                "⬇️ Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name="resume_match_report.json",
                mime="application/json",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)