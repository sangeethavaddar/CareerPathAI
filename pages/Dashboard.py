import json
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Career Dashboard | CareerPath AI",
    page_icon="📊",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROFILE_FILE = DATA_DIR / "profile.json"
CAREERS_FILE = DATA_DIR / "careers.csv"


def load_profile():
    if not PROFILE_FILE.exists():
        return {}

    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


@st.cache_data
def load_careers():
    if not CAREERS_FILE.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(CAREERS_FILE)
    except Exception:
        return pd.DataFrame()


profile = load_profile()
careers = load_careers()


# ---------------------------------------------------------
# PROFILE DATA
# ---------------------------------------------------------

name = profile.get(
    "name",
    profile.get("full_name", "Student")
)

domain = profile.get(
    "domain",
    profile.get("preferred_domain", "Not specified")
)

education = profile.get(
    "education",
    profile.get("education_level", "Not specified")
)

course = profile.get(
    "course",
    profile.get("specialization", "Not specified")
)

skills = profile.get("skills", [])
interests = profile.get("interests", [])
experience = profile.get("experience", "")
projects = profile.get("projects", "")
career_goal = profile.get(
    "career_goal",
    profile.get("goal", "")
)


def convert_to_list(value):
    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


skills = convert_to_list(skills)
interests = convert_to_list(interests)


# ---------------------------------------------------------
# READINESS CALCULATION
# ---------------------------------------------------------

profile_items = [
    bool(name and name != "Student"),
    bool(domain and domain != "Not specified"),
    bool(education and education != "Not specified"),
    bool(course and course != "Not specified"),
    len(skills) > 0,
    len(interests) > 0,
    bool(experience),
    bool(projects),
    bool(career_goal)
]

profile_completion = round(
    sum(profile_items) / len(profile_items) * 100
)


skill_score = min(len(skills) * 10, 100)
interest_score = min(len(interests) * 20, 100)
project_score = 100 if projects else 0
experience_score = 100 if experience else 0
goal_score = 100 if career_goal else 0


overall_readiness = round(
    (
        profile_completion
        + skill_score
        + interest_score
        + project_score
        + experience_score
        + goal_score
    ) / 6
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("📊 CareerPath AI Dashboard")

st.caption(
    "Your personalized career discovery, learning and job-readiness dashboard"
)


if not profile:
    st.warning(
        "Complete your Career Profile first to generate your dashboard."
    )

    st.page_link(
        "app.py",
        label="➡️ Go to Career Profile"
    )

    st.stop()


st.success(
    f"Welcome back, {name}! Your CareerPath AI dashboard is ready."
)


# ---------------------------------------------------------
# PROFILE SUMMARY
# ---------------------------------------------------------

st.subheader("👤 Career Profile")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Preferred Domain",
        domain
    )

with c2:
    st.metric(
        "Education",
        education
    )

with c3:
    st.metric(
        "Skills",
        len(skills)
    )

with c4:
    st.metric(
        "Interests",
        len(interests)
    )


st.divider()


# ---------------------------------------------------------
# CAREER READINESS
# ---------------------------------------------------------

st.subheader("🎯 Career Readiness")

r1, r2, r3 = st.columns(3)

with r1:
    st.metric(
        "Overall Readiness",
        f"{overall_readiness}%"
    )

with r2:
    st.metric(
        "Profile Completion",
        f"{profile_completion}%"
    )

with r3:
    st.metric(
        "Skills Coverage",
        f"{skill_score}%"
    )


st.progress(
    overall_readiness / 100
)


if overall_readiness >= 80:
    st.success(
        "Your profile shows strong preparation progress. Continue improving your skills and projects."
    )
elif overall_readiness >= 50:
    st.info(
        "You have a good foundation. Focus on skill development, projects and interview preparation."
    )
else:
    st.warning(
        "Your preparation is still developing. Follow the learning roadmap step by step."
    )


st.divider()


# ---------------------------------------------------------
# PROFILE DETAILS
# ---------------------------------------------------------

st.subheader("📋 Profile Overview")

left, right = st.columns(2)

with left:

    st.write(f"**Name:** {name}")
    st.write(f"**Education:** {education}")
    st.write(f"**Specialization:** {course}")
    st.write(f"**Preferred Domain:** {domain}")

with right:

    st.write(
        f"**Experience:** "
        f"{experience if experience else 'Not added yet'}"
    )

    st.write(
        f"**Career Goal:** "
        f"{career_goal if career_goal else 'Not added yet'}"
    )


st.divider()


# ---------------------------------------------------------
# SKILLS
# ---------------------------------------------------------

st.subheader("🧠 Your Current Skills")

if skills:

    skill_columns = st.columns(3)

    for index, skill in enumerate(skills):

        with skill_columns[index % 3]:
            st.info(f"✓ {skill}")

else:

    st.warning(
        "No skills detected. Add your skills in Career Profile."
    )


st.divider()


# ---------------------------------------------------------
# INTERESTS
# ---------------------------------------------------------

st.subheader("❤️ Your Interests")

if interests:

    for interest in interests:
        st.write(f"• {interest}")

else:

    st.warning(
        "No interests detected."
    )


st.divider()


# ---------------------------------------------------------
# CAREER DATABASE
# ---------------------------------------------------------

st.subheader("💼 Career Opportunities")

if not careers.empty:

    total_careers = len(careers)

    if "domain" in careers.columns:

        domain_count = len(
            careers[
                careers["domain"].astype(str).str.lower()
                == str(domain).lower()
            ]
        )

    else:
        domain_count = 0

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Careers Available",
            total_careers
        )

    with c2:
        st.metric(
            "Careers in Your Domain",
            domain_count
        )

else:

    st.info(
        "Career database is currently unavailable."
    )


st.divider()


# ---------------------------------------------------------
# PROJECT AND EXPERIENCE STATUS
# ---------------------------------------------------------

st.subheader("🚀 Career Building Status")

p1, p2, p3 = st.columns(3)

with p1:

    if projects:
        st.success("Projects Added")
    else:
        st.warning("Projects Needed")

with p2:

    if experience:
        st.success("Experience Added")
    else:
        st.warning("Experience Needed")

with p3:

    if career_goal:
        st.success("Career Goal Set")
    else:
        st.warning("Career Goal Needed")


st.divider()


# ---------------------------------------------------------
# QUICK ACTIONS
# ---------------------------------------------------------

st.subheader("⚡ Quick Actions")

q1, q2, q3 = st.columns(3)

with q1:

    st.page_link(
        "pages/Learning_Roadmap.py",
        label="📚 Learning Roadmap"
    )

    st.page_link(
        "pages/Resume_Improvement.py",
        label="📄 Improve Resume"
    )

with q2:

    st.page_link(
        "pages/Interview_Preparation.py",
        label="🎤 Interview Preparation"
    )

    st.page_link(
        "pages/Job_Matching.py",
        label="💼 Job Matching"
    )

with q3:

    st.page_link(
        "pages/Progress_Tracking.py",
        label="📈 Track Progress"
    )

    st.page_link(
        "pages/Resume_Analyzer.py",
        label="🔍 Resume Analyzer"
    )


st.divider()


# ---------------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------------

st.info(
    "CareerPath AI brings your career profile, skills, learning, "
    "projects, resume, job matching and interview preparation together "
    "in one career development platform."
)