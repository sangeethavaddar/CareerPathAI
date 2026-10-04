import json
from pathlib import Path

import pandas as pd
import streamlit as st

from engine.data_loader import load_careers
from engine.matcher import recommend_careers
from engine.ai_explainer import generate_career_explanation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #07152f, #123879, #07152f);
        color: white;
    }

    [data-testid="stSidebar"] {
        background: #081631;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    p, label {
        color: #f5f7ff !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(45, 105, 210, 0.35);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.12);
    }

    div[data-testid="stMetricLabel"] {
        color: #dce7ff !important;
    }

    div[data-testid="stMetricValue"] {
        color: white !important;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
PROFILE_FILE = DATA_DIR / "profile.json"
SKILLS_FILE = DATA_DIR / "skills.csv"


# ============================================================
# LOAD DATA
# ============================================================

careers = load_careers()


def load_profile():
    if PROFILE_FILE.exists():
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return {}

    return {}


def save_profile(data):
    DATA_DIR.mkdir(exist_ok=True)

    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


profile = load_profile()


# ============================================================
# LOAD SKILLS
# ============================================================

if SKILLS_FILE.exists():

    try:
        skills_df = pd.read_csv(SKILLS_FILE)

        all_skills = (
            skills_df["skill"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

    except Exception:

        all_skills = []

else:

    all_skills = []


all_skills = list(dict.fromkeys(all_skills))


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        values = value

    else:
        values = (
            str(value)
            .replace(";", ",")
            .replace("|", ",")
            .split(",")
        )

    return [
        str(item).strip()
        for item in values
        if str(item).strip()
    ]


def normalize_skill(value):

    return (
        str(value)
        .strip()
        .lower()
        .replace("_", " ")
    )


def calculate_skill_analysis(
    user_skills,
    required_skills
):

    user = []

    for skill in clean_list(user_skills):

        value = normalize_skill(skill)

        if value and value not in user:
            user.append(value)

    required = []

    for skill in clean_list(required_skills):

        value = normalize_skill(skill)

        if value and value not in required:
            required.append(value)

    matching = []

    for required_skill in required:

        for user_skill in user:

            if (
                required_skill == user_skill
                or required_skill in user_skill
                or user_skill in required_skill
            ):

                if required_skill not in matching:
                    matching.append(required_skill)

                break

    gaps = [
        skill
        for skill in required
        if skill not in matching
    ]

    if required:
        coverage = (
            len(matching) / len(required)
        ) * 100
    else:
        coverage = 0

    return (
        matching,
        gaps,
        round(coverage, 2)
    )


def get_career(career_name):

    rows = careers[
        careers["career"].astype(str)
        == str(career_name)
    ]

    if rows.empty:
        return None

    return rows.iloc[0].to_dict()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎯 CareerPath AI")

    st.write(
        "AI-powered career guidance and decision support"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "👤 Career Profile",
            "🎯 Career Recommendations",
            "🔍 Skill Analysis",
            "🗺️ Career Roadmap",
            "⚖️ Career Comparison"
        ]
    )

    st.divider()

    st.info(
        "CareerPath AI analyzes your profile and suggests "
        "career paths based on multiple factors."
    )


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.title("🎯 CareerPath AI")

    st.subheader(
        "AI-powered career guidance and decision support"
    )

    st.write(
        "Discover career paths based on your skills, "
        "interests, education, experience and goals."
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Career Paths",
            len(careers)
        )

    with c2:
        st.metric(
            "Professional Domains",
            careers["domain"].nunique()
        )

    with c3:
        st.metric(
            "Skills",
            len(all_skills)
        )

    with c4:
        st.metric(
            "AI Features",
            6
        )

    st.divider()

    st.subheader("✨ Main Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "🎯 Smart Career Matching\n\n"
            "Personalized career recommendations."
        )

    with c2:
        st.info(
            "🔍 Skill Analysis\n\n"
            "Find matching skills and skill gaps."
        )

    with c3:
        st.info(
            "🗺️ Career Roadmap\n\n"
            "Build a step-by-step career path."
        )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "⚖️ Career Comparison\n\n"
            "Compare different career paths."
        )

    with c2:
        st.info(
            "🤖 AI Career Explanation\n\n"
            "Understand why a career matches your profile."
        )

    with c3:
        st.info(
            "📊 Explainable Matching\n\n"
            "Understand the factors behind recommendations."
        )


# ============================================================
# CAREER PROFILE
# ============================================================

elif page == "👤 Career Profile":

    st.title("👤 Career Profile")

    st.write(
        "Enter your information to receive personalized recommendations."
    )

    with st.form("profile_form"):

        st.subheader("Personal Information")

        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input(
                "Full Name",
                value=profile.get("name", "")
            )

        with c2:
            age = st.number_input(
                "Age",
                min_value=10,
                max_value=100,
                value=int(profile.get("age", 21))
            )

        st.subheader("Education")

        education_options = [
            "10th / Secondary School",
            "12th / Higher Secondary",
            "Diploma",
            "Bachelor's Degree",
            "Master's Degree",
            "PhD"
        ]

        saved_education = profile.get(
            "education",
            "Bachelor's Degree"
        )

        if saved_education not in education_options:
            saved_education = "Bachelor's Degree"

        education = st.selectbox(
            "Highest Education",
            education_options,
            index=education_options.index(
                saved_education
            )
        )

        course = st.text_input(
            "Course / Specialization",
            value=profile.get("course", "")
        )

        st.subheader("Professional Preferences")

        domains = sorted(
            careers["domain"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        saved_domain = profile.get(
            "domain",
            domains[0] if domains else ""
        )

        if saved_domain not in domains and domains:
            saved_domain = domains[0]

        domain = st.selectbox(
            "Preferred Professional Domain",
            domains,
            index=(
                domains.index(saved_domain)
                if saved_domain in domains
                else 0
            )
        )

        interest_options = [
            "Technology",
            "Research",
            "Biology",
            "Medicine",
            "Anatomy",
            "Agriculture",
            "Food Safety",
            "Finance",
            "Business",
            "Marketing",
            "Communication",
            "Writing",
            "Creativity",
            "Social Media",
            "Design",
            "Law",
            "Education",
            "Environment",
            "Sports",
            "Hospitality"
        ]

        saved_interests = clean_list(
            profile.get("interests", [])
        )

        interests = st.multiselect(
            "Interests",
            interest_options,
            default=[
                item
                for item in saved_interests
                if item in interest_options
            ]
        )

        saved_skills = clean_list(
            profile.get("skills", [])
        )

        skills = st.multiselect(
            "Skills",
            all_skills,
            default=[
                item
                for item in saved_skills
                if item in all_skills
            ]
        )

        experience_options = [
            "No Experience",
            "Less than 1 year",
            "1-2 years",
            "3-5 years",
            "More than 5 years"
        ]

        saved_experience = profile.get(
            "experience",
            "No Experience"
        )

        if saved_experience not in experience_options:
            saved_experience = "No Experience"

        experience = st.selectbox(
            "Experience",
            experience_options,
            index=experience_options.index(
                saved_experience
            )
        )

        projects = st.text_area(
            "Projects",
            value=profile.get("projects", "")
        )

        career_goal = st.text_area(
            "Career Goal",
            value=profile.get("career_goal", "")
        )

        save_button = st.form_submit_button(
            "💾 Save Career Profile",
            use_container_width=True
        )

        if save_button:

            new_profile = {
                "name": name,
                "age": age,
                "education": education,
                "course": course,
                "domain": domain,
                "interests": interests,
                "skills": skills,
                "experience": experience,
                "projects": projects,
                "career_goal": career_goal
            }

            save_profile(new_profile)

            profile = new_profile

            st.success(
                "Career profile saved successfully!"
            )


# ============================================================
# CAREER RECOMMENDATIONS + AI EXPLANATION
# ============================================================

elif page == "🎯 Career Recommendations":

    st.title("🎯 Career Recommendations")

    st.write(
        "Personalized career recommendations based on your profile."
    )

    recommendations = recommend_careers(
        profile,
        careers,
        top_n=5
    )

    if not recommendations:

        st.warning(
            "Please complete your Career Profile first."
        )

    else:

        st.success(
            f"Found {len(recommendations)} personalized career recommendations."
        )

        for index, result in enumerate(
            recommendations,
            start=1
        ):

            career_name = result.get(
                "career",
                "Unknown Career"
            )

            career = get_career(
                career_name
            )

            if career is None:
                continue

            st.divider()

            st.header(
                f"#{index} {career_name}"
            )

            st.write(
                f"**Professional Domain:** "
                f"{career.get('domain', '')}"
            )

            st.metric(
                "Overall Profile Match",
                f"{float(result.get('match', 0)):.2f}%"
            )

            st.write(
                career.get(
                    "description",
                    ""
                )
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Skills",
                    f"{float(result.get('skills', 0)):.1f}%"
                )

            with c2:
                st.metric(
                    "Interests",
                    f"{float(result.get('interests', 0)):.1f}%"
                )

            with c3:
                st.metric(
                    "Education",
                    f"{float(result.get('education', 0)):.1f}%"
                )

            with c4:
                st.metric(
                    "Experience",
                    f"{float(result.get('experience', 0)):.1f}%"
                )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Domain Match",
                    f"{float(result.get('domain', 0)):.1f}%"
                )

            with c2:
                st.metric(
                    "Projects",
                    f"{float(result.get('projects', 0)):.1f}%"
                )

            with c3:
                st.metric(
                    "Career Goal",
                    f"{float(result.get('career_goal', 0)):.1f}%"
                )

            st.subheader("Matching Skills")

            matched = result.get(
                "matched_skills",
                []
            )

            if matched:
                st.success(
                    ", ".join(
                        str(x).title()
                        for x in matched
                    )
                )
            else:
                st.info(
                    "No direct skill matches found."
                )

            st.subheader("Skill Gaps")

            gaps = result.get(
                "skill_gaps",
                []
            )

            if gaps:
                st.warning(
                    ", ".join(
                        str(x).title()
                        for x in gaps
                    )
                )
            else:
                st.success(
                    "No major skill gaps identified."
                )

            st.subheader("Matching Interests")

            matched_interests = result.get(
                "matched_interests",
                []
            )

            if matched_interests:
                st.info(
                    ", ".join(
                        str(x).title()
                        for x in matched_interests
                    )
                )
            else:
                st.info(
                    "No direct interest matches found."
                )

            # ------------------------------------------------
            # AI EXPLANATION
            # ------------------------------------------------

            st.subheader(
                "🤖 AI Career Explanation"
            )

            explanation = generate_career_explanation(
                profile,
                career,
                result
            )

            st.info(
                explanation.get(
                    "summary",
                    ""
                )
            )

            st.markdown(
                "**Why this career may suit you:**"
            )

            for strength in explanation.get(
                "strengths",
                []
            ):
                st.write(
                    "• " + strength
                )

            st.markdown(
                "**What you should improve:**"
            )

            for improvement in explanation.get(
                "improvements",
                []
            ):
                st.write(
                    "• " + improvement
                )


# ============================================================
# SKILL ANALYSIS
# ============================================================

elif page == "🔍 Skill Analysis":

    st.title("🔍 Skill Analysis")

    st.write(
        "Compare your current skills with the skills required for a career."
    )

    career_names = (
        careers["career"]
        .dropna()
        .astype(str)
        .tolist()
    )

    selected_career = st.selectbox(
        "Choose a career",
        career_names
    )

    career = get_career(
        selected_career
    )

    if career is not None:

        required_skills = career.get(
            "skills",
            ""
        )

        user_skills = profile.get(
            "skills",
            []
        )

        matching_skills, skill_gaps, coverage = (
            calculate_skill_analysis(
                user_skills,
                required_skills
            )
        )

        st.subheader("Skill Coverage")

        st.metric(
            "Skill Coverage",
            f"{coverage:.1f}%"
        )

        st.divider()

        st.subheader("✅ Matching Skills")

        if matching_skills:

            st.success(
                ", ".join(
                    skill.title()
                    for skill in matching_skills
                )
            )

        else:

            st.info(
                "No direct skill matches found."
            )

        st.subheader("🧩 Skill Gaps")

        if skill_gaps:

            for skill in skill_gaps:
                st.warning(
                    skill.title()
                )

        else:

            st.success(
                "No skill gaps found."
            )

        st.divider()

        st.subheader("📊 Skill Analysis Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Required Skills",
                len(clean_list(required_skills))
            )

        with c2:
            st.metric(
                "Matching Skills",
                len(matching_skills)
            )

        with c3:
            st.metric(
                "Skill Gaps",
                len(skill_gaps)
            )


# ============================================================
# CAREER ROADMAP
# ============================================================

elif page == "🗺️ Career Roadmap":

    st.title("🗺️ Career Roadmap")

    st.write(
        "A structured development path based on your recommended careers."
    )

    recommendations = recommend_careers(
        profile,
        careers,
        top_n=3
    )

    if not recommendations:

        st.warning(
            "Please complete your Career Profile first."
        )

    else:

        for index, result in enumerate(
            recommendations,
            start=1
        ):

            career_name = result.get(
                "career",
                "Unknown Career"
            )

            career = get_career(
                career_name
            )

            if career is None:
                continue

            st.divider()

            st.header(
                f"#{index} {career_name}"
            )

            st.write(
                f"**Domain:** "
                f"{career.get('domain', '')}"
            )

            st.write(
                career.get(
                    "description",
                    ""
                )
            )

            st.subheader(
                "Step 1 — Strengthen Existing Skills"
            )

            matched = result.get(
                "matched_skills",
                []
            )

            if matched:

                st.write(
                    "Continue developing: "
                    + ", ".join(
                        str(x).lower()
                        for x in matched
                    )
                )

            else:

                st.write(
                    "Build the fundamental skills required for this career."
                )

            st.subheader(
                "Step 2 — Close Skill Gaps"
            )

            gaps = result.get(
                "skill_gaps",
                []
            )

            if gaps:

                st.write(
                    "Focus on: "
                    + ", ".join(
                        str(x).lower()
                        for x in gaps
                    )
                )

            else:

                st.write(
                    "No major skill gaps were identified."
                )

            st.subheader(
                "Step 3 — Build Practical Experience"
            )

            st.write(
                "Work on projects, internships, practical exercises "
                "or real-world activities related to this career."
            )

            st.subheader(
                "Step 4 — Prepare Professionally"
            )

            st.write(
                "Build your resume, portfolio and professional "
                "communication skills."
            )

            st.subheader(
                "Step 5 — Continue Learning"
            )

            st.write(
                "Follow relevant courses, certifications and "
                "industry developments."
            )


# ============================================================
# CAREER COMPARISON
# ============================================================

elif page == "⚖️ Career Comparison":

    st.title("⚖️ Career Comparison")

    st.write(
        "Compare two career paths using your current profile."
    )

    career_names = (
        careers["career"]
        .dropna()
        .astype(str)
        .tolist()
    )

    c1, c2 = st.columns(2)

    with c1:

        career_1 = st.selectbox(
            "Career 1",
            career_names,
            key="career_one"
        )

    with c2:

        career_2 = st.selectbox(
            "Career 2",
            career_names,
            index=1 if len(career_names) > 1 else 0,
            key="career_two"
        )

    first = get_career(
        career_1
    )

    second = get_career(
        career_2
    )

    if first is not None and second is not None:

        first_result = recommend_careers(
            profile,
            pd.DataFrame([first]),
            top_n=1
        )

        second_result = recommend_careers(
            profile,
            pd.DataFrame([second]),
            top_n=1
        )

        first_result = (
            first_result[0]
            if first_result
            else {"match": 0}
        )

        second_result = (
            second_result[0]
            if second_result
            else {"match": 0}
        )

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            st.subheader(
                career_1
            )

            st.metric(
                "Profile Match",
                f"{float(first_result.get('match', 0)):.2f}%"
            )

            st.write(
                first.get(
                    "description",
                    ""
                )
            )

        with c2:

            st.subheader(
                career_2
            )

            st.metric(
                "Profile Match",
                f"{float(second_result.get('match', 0)):.2f}%"
            )

            st.write(
                second.get(
                    "description",
                    ""
                )
            )

        st.subheader(
            "📊 Factor-by-Factor Comparison"
        )

        comparison = pd.DataFrame(
            {
                "Factor": [
                    "Skills",
                    "Interests",
                    "Education",
                    "Experience",
                    "Domain",
                    "Projects",
                    "Career Goal"
                ],
                career_1: [
                    first_result.get("skills", 0),
                    first_result.get("interests", 0),
                    first_result.get("education", 0),
                    first_result.get("experience", 0),
                    first_result.get("domain", 0),
                    first_result.get("projects", 0),
                    first_result.get("career_goal", 0)
                ],
                career_2: [
                    second_result.get("skills", 0),
                    second_result.get("interests", 0),
                    second_result.get("education", 0),
                    second_result.get("experience", 0),
                    second_result.get("domain", 0),
                    second_result.get("projects", 0),
                    second_result.get("career_goal", 0)
                ]
            }
        )

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "🧩 Matching Skills"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**{career_1}**"
            )

            skills = first_result.get(
                "matched_skills",
                []
            )

            st.write(
                ", ".join(
                    str(x).lower()
                    for x in skills
                )
                if skills
                else "No direct skill matches found."
            )

        with c2:

            st.write(
                f"**{career_2}**"
            )

            skills = second_result.get(
                "matched_skills",
                []
            )

            st.write(
                ", ".join(
                    str(x).lower()
                    for x in skills
                )
                if skills
                else "No direct skill matches found."
            )

        st.subheader(
            "🧩 Skill Gaps"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**{career_1}**"
            )

            gaps = first_result.get(
                "skill_gaps",
                []
            )

            st.write(
                ", ".join(
                    str(x).lower()
                    for x in gaps
                )
                if gaps
                else "No major skill gaps."
            )

        with c2:

            st.write(
                f"**{career_2}**"
            )

            gaps = second_result.get(
                "skill_gaps",
                []
            )

            st.write(
                ", ".join(
                    str(x).lower()
                    for x in gaps
                )
                if gaps
                else "No major skill gaps."
            )

        st.subheader(
            "🎓 Education Information"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**{career_1}**"
            )

            st.write(
                first.get(
                    "education",
                    "Information not available."
                )
            )

        with c2:

            st.write(
                f"**{career_2}**"
            )

            st.write(
                second.get(
                    "education",
                    "Information not available."
                )
            )