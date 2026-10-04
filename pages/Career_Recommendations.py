import streamlit as st
import pandas as pd
import json
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Career Recommendations",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# FILE PATHS
# =========================================================

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

PROFILE_FILE = PROJECT_FOLDER / "data" / "profile.json"
CAREERS_FILE = PROJECT_FOLDER / "data" / "careers.csv"


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

            with open(
                PROFILE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                saved_profile = json.load(file)

            if isinstance(saved_profile, dict):
                default_profile.update(saved_profile)

        return default_profile

    except Exception:

        return default_profile


# =========================================================
# LOAD CAREERS
# =========================================================

def load_careers():

    try:

        return pd.read_csv(CAREERS_FILE)

    except Exception as error:

        st.error(
            f"Unable to load career database: {error}"
        )

        return pd.DataFrame()


# =========================================================
# LOAD DATA
# =========================================================

profile = load_profile()
careers = load_careers()

if careers.empty:
    st.stop()


# =========================================================
# NORMALIZE PROFILE DATA
# =========================================================

profile_skills = [
    str(x).strip().lower()
    for x in profile.get("skills", [])
]

profile_interests = [
    str(x).strip().lower()
    for x in profile.get("interests", [])
]

profile_projects = [
    str(x).strip().lower()
    for x in profile.get("projects", [])
]

profile_education = str(
    profile.get("education", "")
).strip()

profile_specialization = str(
    profile.get("specialization", "")
).strip().lower()

profile_experience = str(
    profile.get("experience", "")
).strip().lower()

profile_goal = str(
    profile.get("career_goal", "")
).strip().lower()

# IMPORTANT:
# Read preferred_domain directly from profile.json
profile_domain = str(
    profile.get("preferred_domain", "")
).strip()


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


def skill_score(row):

    required_skills = split_values(
        row.get("skills", "")
    )

    if not required_skills:
        return 0.0

    matched = 0

    for required in required_skills:

        for user_skill in profile_skills:

            if (
                required == user_skill
                or required in user_skill
                or user_skill in required
            ):
                matched += 1
                break

    return round(
        (matched / len(required_skills)) * 100,
        1
    )


def interest_score(row):

    required_interests = split_values(
        row.get("interests", "")
    )

    if not required_interests:
        return 0.0

    matched = 0

    for required in required_interests:

        for user_interest in profile_interests:

            if (
                required == user_interest
                or required in user_interest
                or user_interest in required
            ):
                matched += 1
                break

    return round(
        (matched / len(required_interests)) * 100,
        1
    )


def education_score(row):

    career = str(
        row.get("career", "")
    ).lower()

    domain = str(
        row.get("domain", "")
    ).lower()

    education = profile_education.lower()

    specialization = profile_specialization

    # Medical careers
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
            term in education
            or term in specialization
            for term in medical_terms
        ):
            return 100.0

        return 0.0

    # Computer Science / Technology
    if domain == "technology":

        technology_terms = [
            "computer",
            "computer science",
            "information technology",
            "software",
            "engineering",
            "technology"
        ]

        if any(
            term in education
            or term in specialization
            for term in technology_terms
        ):
            return 100.0

        if "bachelor" in education:
            return 70.0

    # Engineering
    if domain == "engineering":

        if (
            "engineering" in education
            or "engineering" in specialization
        ):
            return 100.0

    # Finance
    if domain == "finance":

        finance_terms = [
            "finance",
            "commerce",
            "accounting",
            "business"
        ]

        if any(
            term in education
            or term in specialization
            for term in finance_terms
        ):
            return 100.0

    # Business
    if domain == "business":

        business_terms = [
            "business",
            "management",
            "commerce",
            "mba"
        ]

        if any(
            term in education
            or term in specialization
            for term in business_terms
        ):
            return 100.0

    # Education
    if domain == "education":

        education_terms = [
            "education",
            "teaching",
            "teacher"
        ]

        if any(
            term in education
            or term in specialization
            for term in education_terms
        ):
            return 100.0

    return 0.0


def experience_score():

    if not profile_experience:
        return 0.0

    if "no experience" in profile_experience:
        return 0.0

    if "less than 1" in profile_experience:
        return 20.0

    if "1-2" in profile_experience:
        return 50.0

    if "2-5" in profile_experience:
        return 75.0

    if "5+" in profile_experience:
        return 100.0

    return 0.0


def project_score(row):

    career = str(
        row.get("career", "")
    ).lower()

    project_text = " ".join(
        profile_projects
    )

    if not project_text:
        return 0.0

    project_keywords = {

        "web developer": [
            "website",
            "web",
            "ecommerce",
            "portal",
            "html",
            "javascript"
        ],

        "software developer": [
            "software",
            "website",
            "web",
            "portal",
            "ecommerce",
            "application"
        ],

        "ai engineer": [
            "artificial intelligence",
            "ai",
            "machine learning",
            "automation",
            "voice-controlled",
            "voice controlled"
        ],

        "data analyst": [
            "data",
            "analysis",
            "analytics"
        ],

        "data scientist": [
            "data",
            "machine learning",
            "analytics",
            "artificial intelligence"
        ],

        "cybersecurity analyst": [
            "cybersecurity",
            "security",
            "cryptography",
            "network security"
        ],

        "cloud engineer": [
            "cloud",
            "aws",
            "azure"
        ],

        "content creator": [
            "content",
            "video",
            "blog",
            "social media"
        ],

        "journalist": [
            "journalism",
            "writing",
            "media",
            "content"
        ]
    }

    keywords = project_keywords.get(
        career,
        []
    )

    if not keywords:
        return 0.0

    matched = 0

    for keyword in keywords:

        if keyword in project_text:
            matched += 1

    if matched == 0:
        return 0.0

    return round(
        min(
            100,
            (matched / min(len(keywords), 3)) * 100
        ),
        1
    )


def domain_score(row):

    career_domain = str(
        row.get("domain", "")
    ).strip().lower()

    selected_domain = profile_domain.lower()

    if not career_domain or not selected_domain:
        return 0.0

    if career_domain == selected_domain:
        return 100.0

    return 0.0


def get_matching_skills(row):

    required = split_values(
        row.get("skills", "")
    )

    matched = []

    for required_skill in required:

        for user_skill in profile_skills:

            if (
                required_skill == user_skill
                or required_skill in user_skill
                or user_skill in required_skill
            ):

                matched.append(
                    required_skill.title()
                )

                break

    return list(dict.fromkeys(matched))


def get_skill_gaps(row):

    required = split_values(
        row.get("skills", "")
    )

    gaps = []

    for required_skill in required:

        found = False

        for user_skill in profile_skills:

            if (
                required_skill == user_skill
                or required_skill in user_skill
                or user_skill in required_skill
            ):
                found = True
                break

        if not found:
            gaps.append(
                required_skill.title()
            )

    return list(dict.fromkeys(gaps))


def get_matching_interests(row):

    required = split_values(
        row.get("interests", "")
    )

    matched = []

    for required_interest in required:

        for user_interest in profile_interests:

            if (
                required_interest == user_interest
                or required_interest in user_interest
                or user_interest in required_interest
            ):

                matched.append(
                    required_interest.title()
                )

                break

    return list(dict.fromkeys(matched))


# =========================================================
# CALCULATE RECOMMENDATIONS
# =========================================================

results = []

exp_score = experience_score()

for _, row in careers.iterrows():

    skills = skill_score(row)
    interests = interest_score(row)
    education = education_score(row)
    projects = project_score(row)
    domain = domain_score(row)

    overall = (
        skills * 0.55
        + interests * 0.20
        + education * 0.15
        + exp_score * 0.10
    )

    results.append({

        "career": row["career"],

        "domain": row.get(
            "domain",
            ""
        ),

        "description": row.get(
            "description",
            ""
        ),

        "skills": skills,

        "interests": interests,

        "education": education,

        "experience": exp_score,

        "projects": projects,

        "domain_score": domain,

        "overall": round(
            overall,
            1
        ),

        "matching_skills":
            get_matching_skills(row),

        "skill_gaps":
            get_skill_gaps(row),

        "matching_interests":
            get_matching_interests(row)
    })


results = sorted(
    results,
    key=lambda x: x["overall"],
    reverse=True
)

top_matches = results[:5]


# =========================================================
# HEADER
# =========================================================

st.title("🎯 Career Recommendations")

st.write(
    "Explore career paths matched to your skills, "
    "interests, education, experience, projects, "
    "and preferred professional domain."
)


# =========================================================
# CURRENT PROFILE
# =========================================================

st.subheader("Your Current Profile")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.write("**Education**")
    st.write(
        profile_education
        if profile_education
        else "Not provided"
    )

with col2:

    st.write("**Domain**")
    st.write(
        profile_domain
        if profile_domain
        else "Not provided"
    )

with col3:

    st.write("**Skills**")
    st.write(
        len(profile_skills)
    )

with col4:

    st.write("**Interests**")
    st.write(
        len(profile_interests)
    )


# =========================================================
# TOP CAREER MATCHES
# =========================================================

st.divider()

st.subheader("Top Career Matches")


for index, match in enumerate(
    top_matches,
    start=1
):

    st.markdown(
        f"### {index}. {match['career']} — {match['overall']}%"
    )

    st.write(
        match["description"]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Skills",
            f"{match['skills']}%"
        )

    with col2:

        st.metric(
            "Interests",
            f"{match['interests']}%"
        )

    with col3:

        st.metric(
            "Education",
            f"{match['education']}%"
        )

    with col4:

        st.metric(
            "Experience",
            f"{match['experience']}%"
        )

    with col5:

        st.metric(
            "Projects",
            f"{match['projects']}%"
        )

    if match["matching_skills"]:

        st.write(
            "**Matching Skills:** "
            + ", ".join(
                match["matching_skills"]
            )
        )

    if match["skill_gaps"]:

        st.write(
            "**Skill Gaps:** "
            + ", ".join(
                match["skill_gaps"]
            )
        )

    if match["matching_interests"]:

        st.write(
            "**Matching Interests:** "
            + ", ".join(
                match["matching_interests"]
            )
        )

    with st.expander(
        "🤖 AI Career Explanation"
    ):

        explanation = (
            f"{match['career']} has an overall compatibility "
            f"score of {match['overall']}%. "
            f"Your skill compatibility is {match['skills']}%, "
            f"interest compatibility is {match['interests']}%, "
            f"education compatibility is {match['education']}%, "
            f"and experience compatibility is "
            f"{match['experience']}%."
        )

        if match["skill_gaps"]:

            explanation += (
                " The main skills you can develop are: "
                + ", ".join(
                    match["skill_gaps"]
                )
                + "."
            )

        st.write(
            explanation
        )

    st.divider()


# =========================================================
# MATCHING ANALYSIS
# =========================================================

st.subheader("Matching Analysis")

chart_data = pd.DataFrame({

    "Career": [
        item["career"]
        for item in top_matches
    ],

    "Match": [
        item["overall"]
        for item in top_matches
    ]
})

st.bar_chart(
    chart_data.set_index("Career")
)


# =========================================================
# BEST CAREER MATCH
# =========================================================

if top_matches:

    best = top_matches[0]

    st.divider()

    st.subheader(
        "Best Career Match Analysis"
    )

    st.markdown(
        f"### {best['career']} — {best['overall']}%"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Skill Compatibility",
            f"{best['skills']}%"
        )

    with col2:

        st.metric(
            "Interest Compatibility",
            f"{best['interests']}%"
        )

    with col3:

        st.metric(
            "Project Compatibility",
            f"{best['projects']}%"
        )

    st.write(
        f"**Education Compatibility:** "
        f"{best['education']}%"
    )

    st.write(
        f"**Experience Compatibility:** "
        f"{best['experience']}%"
    )

    st.write(
        f"**Domain Compatibility:** "
        f"{best['domain_score']}%"
    )


# =========================================================
# NEXT ACTIONS
# =========================================================

st.divider()

st.subheader(
    "Recommended Next Actions"
)

actions = [
    "Strengthen the skill gaps identified for your top career.",
    "Build one practical project related to your target career.",
    "Follow the personalized Learning Roadmap.",
    "Practice career-specific interview questions.",
    "Improve your resume based on the recommended career.",
    "Track your progress using Progress Tracking.",
    "Compare your target career with alternative career paths."
]

for number, action in enumerate(
    actions,
    start=1
):

    st.write(
        f"**{number}.** {action}"
    )