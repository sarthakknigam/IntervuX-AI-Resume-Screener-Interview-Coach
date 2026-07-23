import os
import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from agents.parser import parse_resume
from agents.ats_matcher import ats_match
from agents.interview_agent import generate_interview_questions
from agents.interview_scorer import generate_interview_score
from audio_recorder_streamlit import audio_recorder
from utils.speech_to_text import speech_to_text


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="IntervuX | AI Resume Screener & Interview Coach",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL STYLES — dark charcoal theme, emerald / amber accents
# ============================================================
def load_custom_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', 'Segoe UI', sans-serif;
            }

            .stApp {
                background: linear-gradient(160deg, #0c1310 0%, #0a0f0d 45%, #0a0d10 100%);
            }

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            .block-container {
                padding-top: 1.3rem;
                padding-bottom: 2.6rem;
                max-width: 1120px;
            }

            /* ---------- Hero ---------- */
            .hero-wrapper {
                background: linear-gradient(135deg, #132019 0%, #16241d 50%, #1b2a20 100%);
                border: 1px solid rgba(16,185,129,0.18);
                border-radius: 18px;
                padding: 2.1rem 2.3rem;
                margin-bottom: 1.4rem;
                box-shadow: 0 10px 34px rgba(0,0,0,0.35);
                position: relative;
                overflow: hidden;
            }

            .hero-wrapper::before {
                content: "";
                position: absolute;
                top: -70px;
                right: -70px;
                width: 240px;
                height: 240px;
                background: radial-gradient(circle, rgba(245,158,11,0.16) 0%, rgba(245,158,11,0) 70%);
                border-radius: 50%;
            }

            .hero-brand {
                display: flex;
                align-items: center;
                gap: 0.65rem;
                margin-bottom: 0.55rem;
            }

            .hero-mark {
                width: 36px;
                height: 36px;
                border-radius: 10px;
                background: linear-gradient(135deg, #10b981, #f59e0b);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 1.05rem;
                color: #0a0f0d;
            }

            .hero-title {
                font-size: 2.05rem;
                font-weight: 800;
                color: #f2f7f4;
                letter-spacing: -0.4px;
            }

            .hero-tagline {
                font-size: 1rem;
                color: #9fb3a8;
                max-width: 680px;
                line-height: 1.5;
            }

            .hero-divider {
                height: 1px;
                background: rgba(16,185,129,0.16);
                margin: 1.1rem 0 1rem 0;
            }

            .hero-stats {
                display: flex;
                gap: 2.2rem;
                flex-wrap: wrap;
            }

            .hero-stat-label {
                font-size: 0.71rem;
                text-transform: uppercase;
                letter-spacing: 0.07em;
                color: #6fae8e;
                font-weight: 700;
            }

            .hero-stat-value {
                font-size: 0.92rem;
                color: #d8e6de;
                font-weight: 500;
                margin-top: 0.1rem;
            }

            /* ---------- Section headers ---------- */
            .section-header {
                margin: 1.5rem 0 0.7rem 0;
                padding-bottom: 0.4rem;
                border-bottom: 1px solid rgba(16,185,129,0.14);
            }

            .section-header h2 {
                font-size: 1.12rem;
                font-weight: 700;
                color: #e9f3ee;
                margin: 0;
                letter-spacing: -0.2px;
            }

            /* ---------- Cards ---------- */
            .panel {
                background: rgba(255,255,255,0.025);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px;
                padding: 1.2rem 1.4rem;
                margin-bottom: 0.75rem;
            }

            /* ---------- Candidate header ---------- */
            .profile-row {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1.1rem;
            }

            .avatar-circle {
                width: 54px;
                height: 54px;
                min-width: 54px;
                border-radius: 50%;
                background: linear-gradient(135deg, #10b981, #f59e0b);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #0a0f0d;
                font-weight: 800;
                font-size: 1.2rem;
            }

            .profile-name {
                font-size: 1.2rem;
                font-weight: 800;
                color: #f2f7f4;
            }

            .profile-contact {
                font-size: 0.85rem;
                color: #8ea79b;
            }

            .info-label {
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.07em;
                color: #6fae8e;
                font-weight: 700;
                margin: 0.75rem 0 0.3rem 0;
            }

            .info-label:first-of-type {
                margin-top: 0;
            }

            .skill-chip {
                display: inline-block;
                background: rgba(16,185,129,0.1);
                border: 1px solid rgba(16,185,129,0.35);
                color: #6ee7b7;
                padding: 0.27rem 0.78rem;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 500;
                margin: 0 6px 6px 0;
            }

            .list-item {
                font-size: 0.92rem;
                color: #cdddd4;
                padding: 0.3rem 0;
                border-bottom: 1px dashed rgba(255,255,255,0.06);
            }

            .list-item:last-child {
                border-bottom: none;
            }

            /* ---------- Score ring ---------- */
            .score-wrap {
                display: flex;
                align-items: center;
                gap: 1.6rem;
                flex-wrap: wrap;
            }

            .score-ring {
                width: 118px;
                height: 118px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: conic-gradient(#10b981 calc(var(--pct) * 1%), rgba(255,255,255,0.07) 0);
                position: relative;
            }

            .score-ring::before {
                content: "";
                position: absolute;
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background: #0e1613;
            }

            .score-ring-value {
                position: relative;
                font-size: 1.45rem;
                font-weight: 800;
                color: #f2f7f4;
            }

            .decision-badge {
                display: inline-block;
                padding: 0.38rem 0.95rem;
                border-radius: 9px;
                font-weight: 700;
                font-size: 0.9rem;
                background: rgba(245,158,11,0.12);
                color: #fbbf24;
                border: 1px solid rgba(245,158,11,0.35);
            }

            .tag-good {
                display: inline-block;
                background: rgba(16,185,129,0.1);
                border: 1px solid rgba(16,185,129,0.35);
                color: #6ee7b7;
                padding: 0.25rem 0.72rem;
                border-radius: 999px;
                font-size: 0.81rem;
                margin: 0 6px 6px 0;
            }

            .tag-bad {
                display: inline-block;
                background: rgba(244,63,94,0.1);
                border: 1px solid rgba(244,63,94,0.32);
                color: #fb7185;
                padding: 0.25rem 0.72rem;
                border-radius: 999px;
                font-size: 0.81rem;
                margin: 0 6px 6px 0;
            }

            .callout {
                background: rgba(245,158,11,0.06);
                border-left: 3px solid #f59e0b;
                border-radius: 8px;
                padding: 0.6rem 0.85rem;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                color: #e4dcc9;
            }

            .summary-box {
                background: rgba(255,255,255,0.03);
                border-radius: 10px;
                padding: 1rem 1.15rem;
                font-size: 0.92rem;
                color: #cdddd4;
                line-height: 1.55;
                border: 1px solid rgba(255,255,255,0.06);
            }

            /* ---------- Buttons ---------- */
            div.stButton > button {
                background: linear-gradient(135deg, #10b981, #059669);
                color: #06120d;
                border: none;
                border-radius: 9px;
                padding: 0.55rem 1.3rem;
                font-weight: 700;
                box-shadow: 0 3px 12px rgba(16,185,129,0.28);
                transition: all 0.15s ease;
            }

            div.stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 5px 18px rgba(16,185,129,0.4);
            }

            div.stButton > button:disabled {
                background: rgba(255,255,255,0.07);
                color: #6b7d74;
                box-shadow: none;
            }

            /* ---------- Metric / expander ---------- */
            div[data-testid="stMetric"] {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px;
                padding: 0.6rem 0.9rem;
            }

            details {
                background: rgba(255,255,255,0.025);
                border: 1px solid rgba(255,255,255,0.06) !important;
                border-radius: 10px !important;
            }

            hr {
                border-color: rgba(255,255,255,0.06);
                margin: 0.9rem 0 !important;
            }

            /* ---------- Question stepper ---------- */
            .stepper-track {
                display: flex;
                gap: 4px;
                margin-bottom: 0.9rem;
            }

            .stepper-seg {
                flex: 1;
                height: 5px;
                border-radius: 3px;
                background: rgba(255,255,255,0.08);
            }

            .stepper-seg.done {
                background: #10b981;
            }

            .stepper-label {
                font-size: 0.78rem;
                color: #8ea79b;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }

            .question-card {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 10px;
                padding: 0.85rem 1.05rem;
                font-size: 0.98rem;
                color: #eef6f1;
                margin-bottom: 0.55rem;
            }

            .category-title {
                display: inline-block;
                background: rgba(245,158,11,0.1);
                border: 1px solid rgba(245,158,11,0.3);
                color: #fbbf24;
                padding: 0.18rem 0.65rem;
                border-radius: 999px;
                font-size: 0.71rem;
                font-weight: 700;
                letter-spacing: 0.05em;
                margin: 0.9rem 0 0.5rem 0;
            }

            .category-title:first-child {
                margin-top: 0;
            }

            /* Reduce default vertical gaps between Streamlit elements */
            div[data-testid="stVerticalBlock"] > div {
                gap: 0.4rem;
            }

            textarea, input {
                font-size: 0.92rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initials(name: str) -> str:
    parts = [p for p in name.strip().split(" ") if p]
    if not parts:
        return "NA"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def hero_header():
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-brand">
                <div class="hero-mark">IX</div>
                <div class="hero-title">IntervuX</div>
            </div>
            <div class="hero-tagline">Your End-to-End AI Interview Platform.</div>
            <div class="hero-divider"></div>
            <div class="hero-stats">
                <div>
                    <div class="hero-stat-label">Resume Analysis</div>
                    <div class="hero-stat-value">Automated parsing & ATS scoring</div>
                </div>
                <div>
                    <div class="hero-stat-label">Interview Simulation</div>
                    <div class="hero-stat-value">Voice-based mock interviews</div>
                </div>
                <div>
                    <div class="hero-stat-label">Feedback</div>
                    <div class="hero-stat-value">Detailed, question-level scoring</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str):
    st.markdown(
        f"""
        <div class="section-header">
            <h2>{title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_start():
    st.markdown('<div class="panel">', unsafe_allow_html=True)


def panel_end():
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# APP INIT
# ============================================================
load_custom_css()

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "questions" not in st.session_state:
    st.session_state.questions = None

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = []

if "interview_score" not in st.session_state:
    st.session_state.interview_score = None

hero_header()

# ============================================================
# UPLOAD SECTION
# ============================================================
section_header("Upload Your Resume")

panel_start()
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    label_visibility="collapsed",
)
panel_end()

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume_text = extract_text_from_pdf(file_path)

    with st.expander("View Extracted Resume Text"):
        st.text_area("", resume_text, height=350)

    section_header("Job Description")

    panel_start()
    job_description = st.text_area(
        "Paste the Job Description",
        height=220,
        placeholder="Paste the job description here...",
        label_visibility="collapsed",
    )
    panel_end()

    if st.button("Analyze Resume"):

        if not job_description.strip():
            st.warning("Please paste a Job Description.")
            st.stop()

        with st.spinner("Analyzing Resume..."):

            resume = parse_resume(resume_text)
            ats = ats_match(resume_text, job_description)

        with st.spinner("Generating interview questions..."):
            questions = generate_interview_questions(
                resume_text,
                job_description
            )

        st.session_state.analysis_done = True
        st.session_state.resume_data = resume.model_dump()
        st.session_state.ats = ats
        st.session_state.questions = questions

    if st.session_state.analysis_done:

        data = st.session_state.resume_data
        ats = st.session_state.ats
        questions = st.session_state.questions

        st.success("Analysis Complete")

        # ------------------------------------------------------
        section_header("Candidate Details")

        panel_start()

        name = data.get("name", "Not Found")

        st.markdown(
            f"""
            <div class="profile-row">
                <div class="avatar-circle">{initials(name) if name != "Not Found" else "NA"}</div>
                <div>
                    <div class="profile-name">{name}</div>
                    <div class="profile-contact">{data.get("email", "Not Found")} &nbsp;•&nbsp; {data.get("phone", "Not Found")}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="info-label">Skills</div>', unsafe_allow_html=True)
        if data.get("skills"):
            badges = "".join(
                [f'<span class="skill-chip">{skill}</span>' for skill in data["skills"]]
            )
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.write("No skills found.")

        panel_end()

        panel_start()

        st.markdown('<div class="info-label">Education</div>', unsafe_allow_html=True)
        if data.get("education"):
            for edu in data["education"]:
                st.markdown(f'<div class="list-item">{edu}</div>', unsafe_allow_html=True)
        else:
            st.write("No education details found.")

        st.markdown('<div class="info-label">Projects</div>', unsafe_allow_html=True)
        if data.get("projects"):
            for project in data["projects"]:
                st.markdown(f'<div class="list-item">{project}</div>', unsafe_allow_html=True)
        else:
            st.write("No projects found.")

        st.markdown('<div class="info-label">Experience</div>', unsafe_allow_html=True)
        if data.get("experience"):
            for exp in data["experience"]:
                st.markdown(f'<div class="list-item">{exp}</div>', unsafe_allow_html=True)
        else:
            st.write("No experience found.")

        panel_end()

        # ------------------------------------------------------
        section_header("ATS Analysis")

        panel_start()

        st.markdown(
            f"""
            <div class="score-wrap">
                <div class="score-ring" style="--pct:{ats.ats_score};">
                    <div class="score-ring-value">{ats.ats_score}%</div>
                </div>
                <div>
                    <div class="info-label">Hiring Decision</div>
                    <span class="decision-badge">{ats.hiring_decision}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="info-label">Matching Skills</div>', unsafe_allow_html=True)
            if ats.matching_skills:
                tags = "".join([f'<span class="tag-good">{s}</span>' for s in ats.matching_skills])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.write("No matching skills found.")

        with col2:
            st.markdown('<div class="info-label">Missing Skills</div>', unsafe_allow_html=True)
            if ats.missing_skills:
                tags = "".join([f'<span class="tag-bad">{s}</span>' for s in ats.missing_skills])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.write("No missing skills.")

        st.markdown('<div class="info-label">Strengths</div>', unsafe_allow_html=True)
        for strength in ats.strengths:
            st.markdown(f'<div class="list-item">{strength}</div>', unsafe_allow_html=True)

        st.markdown('<div class="info-label">Weaknesses</div>', unsafe_allow_html=True)
        for weakness in ats.weaknesses:
            st.markdown(f'<div class="list-item">{weakness}</div>', unsafe_allow_html=True)

        st.markdown('<div class="info-label">Suggestions</div>', unsafe_allow_html=True)
        for suggestion in ats.suggestions:
            st.markdown(f'<div class="callout">{suggestion}</div>', unsafe_allow_html=True)

        st.markdown('<div class="info-label">Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-box">{ats.summary}</div>', unsafe_allow_html=True)

        panel_end()

        # ------------------------------------------------------
        section_header("AI Interview Questions")

        if questions:

            panel_start()

            st.markdown('<span class="category-title">TECHNICAL</span>', unsafe_allow_html=True)
            if questions.Technical_Questions:
                for i, question in enumerate(questions.Technical_Questions, start=1):
                    st.markdown(f'<div class="question-card">Q{i}. {question}</div>', unsafe_allow_html=True)
            else:
                st.info("No technical questions generated.")

            st.markdown('<span class="category-title">PROJECT</span>', unsafe_allow_html=True)
            if questions.Project_Questions:
                for i, question in enumerate(questions.Project_Questions, start=1):
                    st.markdown(f'<div class="question-card">Q{i}. {question}</div>', unsafe_allow_html=True)
            else:
                st.info("No project questions generated.")

            st.markdown('<span class="category-title">HR</span>', unsafe_allow_html=True)
            if questions.HR_Questions:
                for i, question in enumerate(questions.HR_Questions, start=1):
                    st.markdown(f'<div class="question-card">Q{i}. {question}</div>', unsafe_allow_html=True)
            else:
                st.info("No HR questions generated.")

            panel_end()

        # ------------------------------------------------------
        section_header("AI Mock Interview")

        if questions:

            if "mock_started" not in st.session_state:
                st.session_state.mock_started = False

            if "current_question" not in st.session_state:
                st.session_state.current_question = 0

            panel_start()

            if st.button("Start Mock Interview"):
                st.session_state.mock_started = True
                st.session_state.current_question = 0
                st.session_state.interview_answers = []
                st.session_state.interview_score = None

            if st.session_state.mock_started:

                all_questions = (
                    questions.Technical_Questions
                    + questions.Project_Questions
                    + questions.HR_Questions
                )

                if st.session_state.current_question < len(all_questions):

                    current_question = all_questions[
                        st.session_state.current_question
                    ]

                    total = len(all_questions)
                    done = st.session_state.current_question

                    segs = "".join(
                        f'<div class="stepper-seg{" done" if i < done else ""}"></div>'
                        for i in range(total)
                    )
                    st.markdown(
                        f'<div class="stepper-label">Question {done + 1} of {total}</div>'
                        f'<div class="stepper-track">{segs}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(f'<div class="question-card">{current_question}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="info-label">Record Your Answer</div>', unsafe_allow_html=True)

                    audio_bytes = audio_recorder(
                        text="Click to Record",
                        recording_color="#e74c3c",
                        neutral_color="#10b981",
                        icon_name="microphone",
                        icon_size="2x",
                        key=f"audio_recorder_{st.session_state.current_question}",
                        pause_threshold=10.0,
                    )

                    if audio_bytes:

                        with open("answer.webm", "wb") as f:

                            f.write(audio_bytes)

                        st.success("Audio Recorded")
                        st.audio(audio_bytes)

                        with st.spinner("Transcribing..."):
                            st.session_state.answer = speech_to_text("answer.webm")

                    st.markdown('<div class="info-label">Your Answer</div>', unsafe_allow_html=True)
                    st.write(st.session_state.answer)

                    has_answer = bool(st.session_state.answer.strip())

                    if not has_answer:
                        st.warning("Please record an answer before proceeding, or click 'Skip this question'.")

                    col_next, col_skip = st.columns(2)

                    with col_next:
                        if st.button("Next Question", disabled=not has_answer):
                            st.session_state.interview_answers.append({
                                "question": current_question,
                                "answer": st.session_state.answer,
                                "skipped": False,
                            })
                            st.session_state.current_question += 1
                            st.session_state.answer = ""
                            st.rerun()

                    with col_skip:
                        if st.button("Skip this question"):
                            st.session_state.interview_answers.append({
                                "question": current_question,
                                "answer": "",
                                "skipped": True,
                            })
                            st.session_state.current_question += 1
                            st.session_state.answer = ""
                            st.rerun()
                else:

                    st.success("Mock Interview Completed")

                    section_header("Interview Score")

                    if st.button("Get Interview Score"):
                        with st.spinner("Evaluating your answers..."):
                            st.session_state.interview_score = generate_interview_score(
                                st.session_state.interview_answers,
                                job_description
                            )

                    score = st.session_state.interview_score

                    if score:

                        st.markdown(
                            f"""
                            <div class="score-wrap">
                                <div class="score-ring" style="--pct:{score.overall_score};">
                                    <div class="score-ring-value">{score.overall_score}%</div>
                                </div>
                                <div>
                                    <div class="info-label">Overall Feedback</div>
                                    <div class="summary-box" style="max-width:480px;">{score.overall_feedback}</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown('<div class="info-label" style="margin-top:1.1rem;">Question-wise Breakdown</div>', unsafe_allow_html=True)

                        for qs in score.question_scores:
                            with st.expander(f"Q: {qs.question}"):
                                if qs.skipped:
                                    st.warning("Skipped")
                                else:
                                    st.write(f"**Score:** {qs.score}/10")
                                    st.write(f"**Feedback:** {qs.feedback}")

            panel_end()

        else:
            st.error("Failed to generate interview questions.")
