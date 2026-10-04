import streamlit as st
import pandas as pd
import json
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Career Comparison",
    page_icon="⚖️",
    layout="wide"
)


# =========================================================
# FILE PATHS
# =========================================================

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

PROFILE_FILE = PROJECT_FOLDER / "data" / "profile.json"
CAREERS_FILE = PROJECT_FOLDER / "data" / "careers.csv"
COMPARISON_FILE = PROJECT_FOLDER / "data" / "comparison.json"


# =========================================================
# LOAD PROFILE
# =========================================================

def load_profile():

    default_profile = {
        "name": "",
        "age": "",
        "education": "Bachelor's Degree",
        "specialization": "",
        "experience": "No Experience",
        "career_goal": "",
        "preferred_domain": "Technology",
        "skills": [],
        "interests": [],
        "projects": []
    }

    try:
        if PROFILE_FILE.exists():

            with open(PROFILE_FILE, "r", encoding="utf-8") as file:
                saved_profile = json.load(file)

            if isinstance(saved_profile, dict):
                default_profile.update(saved_profile)

    except Exception:
        pass

    return default_profile


# =========================================================
# LOAD CAREERS
# =========================================================

def load_careers():

    try:
        return pd.read_csv(CAREERS_FILE)

    except Exception as error:
        st.error(f"Unable to load career database: {error}")
        return pd.DataFrame()


# =========================================================
# LOAD SAVED COMPARISON
# =========================================================

def load_comparison():

    default_data = {
        "selected_careers": []
    }

    try:

        if COMPARISON_FILE.exists():

            with open(COMPARISON_FILE, "r", encoding="utf-8") as file:
                saved_data = json.load(file)

            if isinstance(saved_data, dict):
                default_data.update(saved_data)

    except Exception:
        pass

    return default_data


# =========================================================
# SAVE COMPARISON
# =========================================================

def save_comparison(selected):

    COMPARISON_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "selected_careers": selected
    }

    with open(
        COMPARISON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# =========================================================
# DATA
# =========================================================

profile = load_profile()
careers = load_careers()
saved_comparison = load_comparison()


if careers.empty:
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("⚖️ Career Comparison")

st.write(
    "Compare different career paths using your current "
    "skills, interests, education, experience and projects."
)


# =========================================================
# PROFILE SUMMARY
# =========================================================

st.subheader("Your Current Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Education",
        str(profile.get("education", "Not specified"))
    )

with col2:
    st.metric(
        "Experience",
        str(profile.get("experience", "Not specified"))
    )

with col3:
    st.metric(
        "Domain",
        str(profile.get("preferred_domain", "Not specified"))
    )

with col4:
    st.metric(
        "Skills",
        len(profile.get("skills", []))
    )


# =========================================================
# CAREER SELECTION
# =========================================================

st.subheader("Select Careers to Compare")

career_names = careers["career"].dropna().tolist()

saved_selected = saved_comparison.get(
    "selected_careers",
    []
)

if not isinstance(saved_selected, list):
    saved_selected = []

# Keep only careers that still exist in careers.csv
saved_selected = [
    career
    for career in saved_selected
    if career in career_names
]


# Initialize session state only once
if "comparison_selected_careers" not in st.session_state:

    st.session_state.comparison_selected_careers = saved_selected


selected_careers = st.multiselect(
    "Choose 2 to 4 careers",
    career_names,
    key="comparison_selected_careers"
)


# =========================================================
# SAVE SELECTION AUTOMATICALLY
# =========================================================

if selected_careers != saved_selected:

    try:
        save_comparison(selected_careers)

    except Exception:
        pass


if len(selected_careers) < 2:

    st.info(
        "Select at least 2 careers to start the comparison."
    )

    st.stop()


if len(selected_careers) > 4:

    st.warning(
        "Please compare a maximum of 4 careers."
    )

    st.stop()


# =========================================================
# PROFILE DATA
# =========================================================

profile_skills = [
    str(skill).strip().lower()
    for skill in profile.get("skills", [])
]

profile_interests = [
    str(interest).strip().lower()
    for interest in profile.get("interests", [])
]

profile_projects = [
    str(project).strip().lower()
    for project in profile.get("projects", [])
]

profile_education = str(
    profile.get("education", "")
).lower()

profile_specialization = str(
    profile.get("specialization", "")
).lower()

profile_experience = str(
    profile.get("experience", "")
).lower()

profile_domain = str(
    profile.get("preferred_domain", "")
).lower()

profile_goal = str(
    profile.get("career_goal", "")
).lower()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def split_values(value):

    if pd.isna(value):
        return []

    return [
        item.strip().lower()
        for item in str(value).split(",")
        if item.strip()
    ]


def calculate_skill_score(row):

    required = split_values(row.get("skills", ""))

    if not required:
        return 0

    matched = 0

    for required_skill in required:

        for user_skill in profile_skills:

            if (
                required_skill in user_skill
                or user_skill in required_skill
            ):
                matched += 1
                break

    return round(
        (matched / len(required)) * 100,
        1
    )


def calculate_interest_score(row):

    required = split_values(row.get("interests", ""))

    if not required:
        return 0

    matched = 0

    for required_interest in required:

        for user_interest in profile_interests:

            if (
                required_interest in user_interest
                or user_interest in required_interest
            ):
                matched += 1
                break

    return round(
        (matched / len(required)) * 100,
        1
    )


def calculate_education_score(row):

    career = str(row.get("career", "")).lower()
    domain = str(row.get("domain", "")).lower()

    # Medical careers require medical background
    medical_careers = [
        "doctor",
        "nurse",
        "pharmacist",
        "physiotherapist"
    ]

    if career in medical_careers:

        medical_terms = [
            "medical",
            "medicine",
            "biology",
            "clinical",
            "healthcare"
        ]

        if any(
            term in profile_specialization
            or term in profile_education
            for term in medical_terms
        ):
            return 100

        return 0

    # Engineering / Technology careers
    if (
        domain == "technology"
        or domain == "engineering"
    ):

        cse_terms = [
            "computer",
            "computer science",
            "engineering",
            "information technology",
            "bachelor"
        ]

        if any(
            term in profile_specialization
            or term in profile_education
            for term in cse_terms
        ):
            return 100

    # Finance
    if domain == "finance":

        finance_terms = [
            "finance",
            "commerce",
            "accounting",
            "business"
        ]

        if any(
            term in profile_specialization
            or term in profile_education
            for term in finance_terms
        ):
            return 100

    # General domain match
    if domain and domain in profile_specialization:
        return 70

    return 0


def calculate_experience_score(row):

    if (
        not profile_experience
        or "no experience" in profile_experience
    ):
        return 0

    if "less than 1" in profile_experience:
        return 20

    if "1-2" in profile_experience:
        return 50

    if "2-5" in profile_experience:
        return 75

    if "5+" in profile_experience:
        return 100

    return 0


def calculate_project_score(row):

    career = str(row.get("career", "")).lower()

    if not profile_projects:
        return 0

    project_text = " ".join(profile_projects)

    # Web development
    web_keywords = [
        "website",
        "web",
        "ecommerce",
        "portal",
        "html",
        "javascript",
        "frontend",
        "backend"
    ]

    # AI
    ai_keywords = [
        "artificial intelligence",
        "ai",
        "machine learning",
        "deep learning",
        "automation",
        "voice-controlled",
        "voice controlled",
        "intelligent"
    ]

    # Data
    data_keywords = [
        "data analysis",
        "data science",
        "machine learning",
        "analytics"
    ]

    # Cybersecurity
    cyber_keywords = [
        "cybersecurity",
        "security",
        "network security",
        "cryptography"
    ]

    # IoT
    iot_keywords = [
        "iot",
        "internet of things",
        "sensor",
        "automation"
    ]

    keyword_map = {

        "web developer": web_keywords,

        "software developer": [
            "software",
            "website",
            "web",
            "portal",
            "application",
            "ecommerce",
            "java",
            "python"
        ],

        "ai engineer": ai_keywords,

        "data scientist": data_keywords,

        "data analyst": data_keywords,

        "cybersecurity analyst": cyber_keywords,

        "cloud engineer": [
            "cloud",
            "aws",
            "azure",
            "cloud computing"
        ],

        "electronics engineer": [
            "electronics",
            "iot",
            "sensor",
            "automation"
        ],

        "electrical engineer": [
            "electrical",
            "automation",
            "iot"
        ],

        "content creator": [
            "content",
            "video",
            "blog",
            "social media",
            "youtube"
        ],

        "journalist": [
            "journalism",
            "writing",
            "content",
            "media"
        ]
    }

    keywords = keyword_map.get(
        career,
        []
    )

    if not keywords:
        return 0

    matched = 0

    for keyword in keywords:

        if keyword in project_text:
            matched += 1

    if matched == 0:
        return 0

    return round(
        min(100, (matched / min(len(keywords), 3)) * 100),
        1
    )


def calculate_domain_score(row):

    career_domain = str(
        row.get("domain", "")
    ).lower()

    if not career_domain:
        return 0

    if career_domain == profile_domain:
        return 100

    return 0


# =========================================================
# CALCULATE COMPARISON
# =========================================================

comparison_results = []


for career_name in selected_careers:

    matching_rows = careers[
        careers["career"] == career_name
    ]

    if matching_rows.empty:
        continue

    row = matching_rows.iloc[0]

    skill_score = calculate_skill_score(row)
    interest_score = calculate_interest_score(row)
    education_score = calculate_education_score(row)
    experience_score = calculate_experience_score(row)
    project_score = calculate_project_score(row)
    domain_score = calculate_domain_score(row)

    # Official project weights from Career Path AI design
    overall_score = (
        skill_score * 0.55
        + interest_score * 0.20
        + education_score * 0.15
        + experience_score * 0.10
    )

    comparison_results.append({
        "Career": career_name,
        "Overall": round(overall_score, 1),
        "Skills": skill_score,
        "Interests": interest_score,
        "Education": education_score,
        "Experience": experience_score,
        "Projects": project_score,
        "Domain": domain_score
    })


# =========================================================
# COMPARISON TABLE
# =========================================================

st.divider()

st.subheader("Career Comparison")

comparison_df = pd.DataFrame(
    comparison_results
)

display_df = comparison_df.copy()

display_df["Overall"] = (
    display_df["Overall"].astype(str) + "%"
)

display_df["Skills"] = (
    display_df["Skills"].astype(str) + "%"
)

display_df["Interests"] = (
    display_df["Interests"].astype(str) + "%"
)

display_df["Education"] = (
    display_df["Education"].astype(str) + "%"
)

display_df["Experience"] = (
    display_df["Experience"].astype(str) + "%"
)

display_df["Projects"] = (
    display_df["Projects"].astype(str) + "%"
)

display_df["Domain"] = (
    display_df["Domain"].astype(str) + "%"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# INDIVIDUAL CAREER CARDS
# =========================================================

st.divider()

st.subheader("Detailed Comparison")


for result in comparison_results:

    career_name = result["Career"]

    st.markdown(
        f"### {career_name}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Overall Match",
            f'{result["Overall"]}%'
        )

    with col2:
        st.metric(
            "Skills",
            f'{result["Skills"]}%'
        )

    with col3:
        st.metric(
            "Interests",
            f'{result["Interests"]}%'
        )

    with col4:
        st.metric(
            "Education",
            f'{result["Education"]}%'
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Experience",
            f'{result["Experience"]}%'
        )

    with col2:
        st.metric(
            "Projects",
            f'{result["Projects"]}%'
        )

    with col3:
        st.metric(
            "Domain",
            f'{result["Domain"]}%'
        )

    st.divider()


# =========================================================
# SCORE EXPLANATION
# =========================================================

st.subheader("How the Comparison Works")

st.write(
    "The overall career compatibility score is calculated "
    "using the Career Path AI scoring model:"
)

st.write(
    "**Skills: 55%  |  Interests: 20%  |  Education: 15%  |  Experience: 10%**"
)

st.caption(
    "Projects and preferred domain are displayed as additional "
    "supporting information and are not added separately to the overall score."
)