import json
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Progress Tracking | CareerPath AI",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PROFILE_FILE = DATA_DIR / "profile.json"
PROGRESS_FILE = DATA_DIR / "progress.json"


# =========================================================
# LOAD PROFILE
# =========================================================

def load_profile():
    if not PROFILE_FILE.exists():
        return {}

    try:
        with open(
            PROFILE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)
    except Exception:
        return {}


# =========================================================
# LOAD PROGRESS
# =========================================================

def load_progress():
    if not PROGRESS_FILE.exists():
        return {}

    try:
        with open(
            PROGRESS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)
    except Exception:
        return {}


# =========================================================
# SAVE PROGRESS
# =========================================================

def save_progress(progress):
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            progress,
            file,
            indent=4
        )


# =========================================================
# PROFILE
# =========================================================

profile = load_profile()

if not profile:
    st.warning(
        "Please complete your Career Profile first."
    )
    st.stop()


name = profile.get(
    "name",
    profile.get(
        "full_name",
        "Student"
    )
)

domain = profile.get(
    "domain",
    profile.get(
        "preferred_domain",
        "Not specified"
    )
)

skills = profile.get(
    "skills",
    []
)

if isinstance(skills, str):
    skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]


interests = profile.get(
    "interests",
    []
)

if isinstance(interests, str):
    interests = [
        interest.strip()
        for interest in interests.split(",")
        if interest.strip()
    ]


# =========================================================
# PAGE HEADER
# =========================================================

st.title("📊 Progress Tracking")

st.caption(
    "CareerPath AI • Track your learning, projects, interviews and career readiness"
)

st.success(
    f"Progress tracking personalized for {name}."
)


# =========================================================
# PROFILE SUMMARY
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Preferred Domain",
        domain
    )

with c2:
    st.metric(
        "Current Skills",
        len(skills)
    )

with c3:
    st.metric(
        "Interests",
        len(interests)
    )


st.divider()


# =========================================================
# LOAD SAVED PROGRESS
# =========================================================

saved_progress = load_progress()


# =========================================================
# CAREER DEVELOPMENT
# =========================================================

st.subheader("🎯 Career Development Progress")

career_items = [
    "Completed my Career Profile",
    "Reviewed my Career Recommendations",
    "Reviewed my Career Roadmap",
    "Completed my Learning Roadmap"
]

career_values = []

for index, item in enumerate(career_items):

    key = f"career_{index}"

    default_value = saved_progress.get(
        key,
        False
    )

    value = st.checkbox(
        item,
        value=default_value,
        key=key
    )

    career_values.append(value)


career_progress = (
    sum(career_values) /
    len(career_values)
) * 100


st.progress(
    career_progress / 100
)

st.write(
    f"Career Development: **{career_progress:.0f}%**"
)


st.divider()


# =========================================================
# SKILL DEVELOPMENT
# =========================================================

st.subheader("🧠 Skill Development")

skill_items = [
    "Learned a new technical skill",
    "Practiced my existing skills",
    "Completed practical exercises",
    "Improved problem-solving skills",
    "Improved communication skills"
]

skill_values = []

for index, item in enumerate(skill_items):

    key = f"skill_{index}"

    default_value = saved_progress.get(
        key,
        False
    )

    value = st.checkbox(
        item,
        value=default_value,
        key=key
    )

    skill_values.append(value)


skill_progress = (
    sum(skill_values) /
    len(skill_values)
) * 100


st.progress(
    skill_progress / 100
)

st.write(
    f"Skill Development: **{skill_progress:.0f}%**"
)


st.divider()


# =========================================================
# PROJECT PROGRESS
# =========================================================

st.subheader("🚀 Project Progress")

project_items = [
    "Completed a beginner project",
    "Completed an intermediate project",
    "Completed my major project",
    "Documented my projects",
    "Uploaded projects to GitHub",
    "Added important projects to my resume"
]

project_values = []

for index, item in enumerate(project_items):

    key = f"project_{index}"

    default_value = saved_progress.get(
        key,
        False
    )

    value = st.checkbox(
        item,
        value=default_value,
        key=key
    )

    project_values.append(value)


project_progress = (
    sum(project_values) /
    len(project_values)
) * 100


st.progress(
    project_progress / 100
)

st.write(
    f"Project Development: **{project_progress:.0f}%**"
)


st.divider()


# =========================================================
# INTERVIEW PREPARATION
# =========================================================

st.subheader("🎤 Interview Preparation")

interview_items = [
    "Practiced technical questions",
    "Practiced career-specific questions",
    "Practiced HR questions",
    "Prepared my self-introduction",
    "Prepared my project explanation",
    "Prepared questions for the interviewer"
]

interview_values = []

for index, item in enumerate(interview_items):

    key = f"interview_{index}"

    default_value = saved_progress.get(
        key,
        False
    )

    value = st.checkbox(
        item,
        value=default_value,
        key=key
    )

    interview_values.append(value)


interview_progress = (
    sum(interview_values) /
    len(interview_values)
) * 100


st.progress(
    interview_progress / 100
)

st.write(
    f"Interview Preparation: **{interview_progress:.0f}%**"
)


st.divider()


# =========================================================
# RESUME & JOB READINESS
# =========================================================

st.subheader("💼 Job Readiness")

job_items = [
    "Resume is updated",
    "Resume improvement suggestions completed",
    "GitHub profile is ready",
    "Professional portfolio is ready",
    "Technical interview preparation completed",
    "HR interview preparation completed"
]

job_values = []

for index, item in enumerate(job_items):

    key = f"job_{index}"

    default_value = saved_progress.get(
        key,
        False
    )

    value = st.checkbox(
        item,
        value=default_value,
        key=key
    )

    job_values.append(value)


job_progress = (
    sum(job_values) /
    len(job_values)
) * 100


st.progress(
    job_progress / 100
)

st.write(
    f"Job Readiness: **{job_progress:.0f}%**"
)


st.divider()


# =========================================================
# OVERALL PROGRESS
# =========================================================

st.subheader("🏆 Overall Career Readiness")

all_progress = [
    career_progress,
    skill_progress,
    project_progress,
    interview_progress,
    job_progress
]

overall_progress = (
    sum(all_progress) /
    len(all_progress)
)


st.metric(
    "Overall Career Readiness",
    f"{overall_progress:.0f}%"
)

st.progress(
    overall_progress / 100
)


if overall_progress < 30:

    st.info(
        "🌱 You are at the beginning of your career preparation. "
        "Start with your fundamental skills and learning roadmap."
    )

elif overall_progress < 60:

    st.info(
        "📚 Good progress. Continue developing your skills "
        "and building practical projects."
    )

elif overall_progress < 80:

    st.info(
        "🚀 You are making strong progress. "
        "Focus on projects, interviews and job preparation."
    )

else:

    st.success(
        "🎉 Excellent progress. Continue maintaining your skills, "
        "portfolio and interview readiness."
    )


st.divider()


# =========================================================
# SAVE BUTTON
# =========================================================

st.subheader("💾 Save Your Progress")

if st.button(
    "Save Progress",
    type="primary",
    use_container_width=True
):

    progress_data = {}

    for index, value in enumerate(career_values):
        progress_data[
            f"career_{index}"
        ] = value

    for index, value in enumerate(skill_values):
        progress_data[
            f"skill_{index}"
        ] = value

    for index, value in enumerate(project_values):
        progress_data[
            f"project_{index}"
        ] = value

    for index, value in enumerate(interview_values):
        progress_data[
            f"interview_{index}"
        ] = value

    for index, value in enumerate(job_values):
        progress_data[
            f"job_{index}"
        ] = value

    progress_data["overall_progress"] = overall_progress

    save_progress(
        progress_data
    )

    st.success(
        "✅ Your progress has been saved successfully."
    )


# =========================================================
# FINAL MESSAGE
# =========================================================

st.info(
    "Keep updating your checklist as you learn, practice, "
    "build projects and prepare for your career."
)