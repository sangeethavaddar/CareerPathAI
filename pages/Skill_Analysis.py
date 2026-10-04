import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parent.parent

CAREERS_FILE = BASE / "data" / "careers.csv"
PROFILE_FILE = BASE / "data" / "profile.json"
SAVE_FILE = BASE / "data" / "skill_analysis.json"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Skill Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Skill Analysis")
st.caption(
    "Identify your current skills, required skills and skill gaps for your selected career."
)


# ============================================================
# LOAD CAREERS
# ============================================================

try:
    careers_df = pd.read_csv(CAREERS_FILE)
except Exception as error:
    st.error("Unable to load careers.csv")
    st.code(str(error))
    st.stop()


if "career" not in careers_df.columns:
    st.error("careers.csv must contain a 'career' column.")
    st.stop()


careers = (
    careers_df["career"]
    .dropna()
    .astype(str)
    .str.strip()
    .tolist()
)

careers = list(dict.fromkeys(careers))


if not careers:
    st.error("No careers found.")
    st.stop()


# ============================================================
# LOAD PROFILE
# ============================================================

profile = {}

if PROFILE_FILE.exists():

    try:
        with open(
            PROFILE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            profile = json.load(file)

    except Exception:
        profile = {}


# ============================================================
# GET USER CURRENT SKILLS
# ============================================================

profile_skills = profile.get("skills", [])

if isinstance(profile_skills, str):

    current_skills = [
        item.strip()
        for item in profile_skills.split(",")
        if item.strip()
    ]

elif isinstance(profile_skills, list):

    current_skills = [
        str(item).strip()
        for item in profile_skills
        if str(item).strip()
    ]

else:

    current_skills = []


# ============================================================
# LOAD SAVED CAREER
# ============================================================

saved_career = ""

if SAVE_FILE.exists():

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            saved_data = json.load(file)

            saved_career = str(
                saved_data.get("career", "")
            ).strip()

    except Exception:

        saved_career = ""


# ============================================================
# DETERMINE DEFAULT CAREER
# ============================================================

if saved_career in careers:

    default_career = saved_career

else:

    default_career = careers[0]


# ============================================================
# CAREER SELECTOR
# ============================================================

selected_career = st.selectbox(
    "🎯 Select Career",
    careers,
    index=careers.index(default_career),
    key="skill_analysis_career"
)


# ============================================================
# SAVE CAREER IMMEDIATELY
# ============================================================

# This is the important fix.
# Every time the user selects another career,
# the selection is written to skill_analysis.json.

try:

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "career": selected_career
            },
            file,
            indent=4
        )

except Exception as error:

    st.warning(
        "The selected career could not be saved."
    )


# ============================================================
# CAREER-SPECIFIC REQUIRED SKILLS
# ============================================================

REQUIRED_SKILLS = {

    "Software Developer": [
        "Python",
        "Java",
        "SQL",
        "Git",
        "Data Structures"
    ],

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "SQL",
        "Git"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Pandas",
        "Machine Learning"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Statistics",
        "Data Analysis"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "SQL",
        "Git"
    ],

    "Cybersecurity Analyst": [
        "Networking",
        "Linux",
        "Cybersecurity",
        "Cryptography",
        "Python"
    ],

    "Cloud Engineer": [
        "Linux",
        "Networking",
        "Cloud Computing",
        "Git",
        "Python"
    ],

    "Mechanical Engineer": [
        "Engineering Mathematics",
        "CAD",
        "Machine Design",
        "Thermodynamics",
        "Manufacturing"
    ],

    "Civil Engineer": [
        "Engineering Mathematics",
        "AutoCAD",
        "Structural Engineering",
        "Surveying",
        "Construction"
    ],

    "Electrical Engineer": [
        "Circuit Analysis",
        "Electrical Machines",
        "Power Systems",
        "Control Systems",
        "Electrical Design"
    ],

    "Electronics Engineer": [
        "Digital Electronics",
        "Analog Electronics",
        "Microcontrollers",
        "Embedded Systems",
        "IoT"
    ],

    "Doctor": [
        "Medicine",
        "Anatomy",
        "Biology",
        "Clinical Skills",
        "Patient Care"
    ],

    "Nurse": [
        "Nursing",
        "Anatomy",
        "Patient Care",
        "Clinical Skills",
        "Communication"
    ],

    "Pharmacist": [
        "Pharmacology",
        "Pharmaceutics",
        "Chemistry",
        "Drug Safety",
        "Patient Care"
    ],

    "Physiotherapist": [
        "Anatomy",
        "Physiology",
        "Exercise Therapy",
        "Rehabilitation",
        "Patient Care"
    ],

    "Accountant": [
        "Accounting",
        "Excel",
        "Taxation",
        "Auditing",
        "Financial Analysis"
    ],

    "Financial Analyst": [
        "Excel",
        "Financial Analysis",
        "Accounting",
        "Statistics",
        "Financial Modeling"
    ],

    "Investment Analyst": [
        "Financial Analysis",
        "Accounting",
        "Valuation",
        "Investment Research",
        "Excel"
    ],

    "Marketing Manager": [
        "Marketing",
        "Communication",
        "Digital Marketing",
        "Market Research",
        "Analytics"
    ],

    "Business Analyst": [
        "Business Analysis",
        "SQL",
        "Excel",
        "Data Analysis",
        "Communication"
    ],

    "Human Resources Manager": [
        "Human Resources",
        "Communication",
        "Recruitment",
        "Leadership",
        "HR Analytics"
    ],

    "Entrepreneur": [
        "Business Strategy",
        "Communication",
        "Leadership",
        "Marketing",
        "Financial Management"
    ],

    "Teacher": [
        "Communication",
        "Teaching",
        "Lesson Planning",
        "Classroom Management",
        "Presentation"
    ],

    "Professor": [
        "Research",
        "Teaching",
        "Academic Writing",
        "Communication",
        "Presentation"
    ],

    "Lawyer": [
        "Legal Research",
        "Legal Writing",
        "Communication",
        "Negotiation",
        "Critical Thinking"
    ],

    "Journalist": [
        "Journalism",
        "Writing",
        "Communication",
        "Research",
        "Interviewing"
    ],

    "Content Creator": [
        "Content Creation",
        "Communication",
        "Video Editing",
        "Writing",
        "Social Media"
    ],

    "Graphic Designer": [
        "Graphic Design",
        "Typography",
        "Visual Design",
        "Creativity",
        "Design Software"
    ],

    "UI UX Designer": [
        "UI Design",
        "UX Design",
        "User Research",
        "Wireframing",
        "Prototyping"
    ],

    "Architect": [
        "Architecture",
        "CAD",
        "Design",
        "Drawing",
        "Building Technology"
    ],

    "Agricultural Scientist": [
        "Agriculture",
        "Crop Science",
        "Soil Science",
        "Research",
        "Data Analysis"
    ],

    "Environmental Scientist": [
        "Environmental Science",
        "Ecology",
        "Research",
        "Data Analysis",
        "Sustainability"
    ],

    "Hotel Manager": [
        "Hospitality",
        "Communication",
        "Customer Service",
        "Leadership",
        "Hotel Management"
    ],

    "Chef": [
        "Cooking",
        "Food Safety",
        "Menu Planning",
        "Kitchen Management",
        "Food Preparation"
    ],

    "Fitness Trainer": [
        "Fitness Training",
        "Exercise Science",
        "Anatomy",
        "Communication",
        "Exercise Programming"
    ],

    "Sports Coach": [
        "Coaching",
        "Sports Training",
        "Communication",
        "Leadership",
        "Performance Analysis"
    ]
}


# ============================================================
# GET REQUIRED SKILLS
# ============================================================

if selected_career in REQUIRED_SKILLS:

    required_skills = REQUIRED_SKILLS[selected_career]

else:

    career_row = careers_df[
        careers_df["career"].astype(str).str.strip()
        == selected_career
    ]

    if not career_row.empty:

        raw_skills = str(
            career_row.iloc[0].get("skills", "")
        )

        required_skills = [
            item.strip()
            for item in raw_skills.split(",")
            if item.strip()
        ]

    else:

        required_skills = []


# ============================================================
# NORMALIZE SKILLS FOR COMPARISON
# ============================================================

def normalize_skill(skill):

    return (
        str(skill)
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )


normalized_current = {
    normalize_skill(skill)
    for skill in current_skills
}

normalized_required = {
    normalize_skill(skill)
    for skill in required_skills
}


# ============================================================
# FIND MATCHING SKILLS
# ============================================================

matching_skills = []

missing_skills = []

for skill in required_skills:

    if normalize_skill(skill) in normalized_current:

        matching_skills.append(skill)

    else:

        missing_skills.append(skill)


# ============================================================
# SKILL COVERAGE
# ============================================================

if required_skills:

    coverage = (
        len(matching_skills)
        / len(required_skills)
    ) * 100

else:

    coverage = 0


coverage = round(coverage, 1)


# ============================================================
# CAREER INFORMATION
# ============================================================

career_row = careers_df[
    careers_df["career"].astype(str).str.strip()
    == selected_career
]

if not career_row.empty:

    row = career_row.iloc[0]

    domain = str(
        row.get("domain", "")
    )

    education = str(
        row.get("education", "")
    )

else:

    domain = ""

    education = ""


# ============================================================
# SUMMARY
# ============================================================

st.subheader(
    f"🎯 {selected_career}"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Skill Coverage",
        f"{coverage}%"
    )

with col2:

    st.metric(
        "Required Skills",
        len(required_skills)
    )

with col3:

    st.metric(
        "Matching Skills",
        len(matching_skills)
    )


# ============================================================
# PROGRESS BAR
# ============================================================

st.progress(
    int(coverage)
)


# ============================================================
# CURRENT SKILLS
# ============================================================

st.subheader("💼 Your Current Skills")

if current_skills:

    st.write(
        ", ".join(current_skills)
    )

else:

    st.info(
        "No skills have been added to your Career Profile yet."
    )


# ============================================================
# REQUIRED SKILLS
# ============================================================

st.subheader(
    "📚 Skills Required for This Career"
)

if required_skills:

    st.write(
        ", ".join(required_skills)
    )

else:

    st.info(
        "Required skills are not available for this career yet."
    )


# ============================================================
# MATCHING SKILLS
# ============================================================

st.subheader("✅ Matching Skills")

if matching_skills:

    for skill in matching_skills:

        st.write(
            f"✅ {skill}"
        )

else:

    st.info(
        "No matching skills found yet."
    )


# ============================================================
# SKILL GAPS
# ============================================================

st.subheader("⚠️ Skill Gaps")

if missing_skills:

    for skill in missing_skills:

        st.write(
            f"⚠️ {skill}"
        )

else:

    st.success(
        "Excellent! You currently have all the listed required skills."
    )


# ============================================================
# RECOMMENDED DEVELOPMENT
# ============================================================

st.subheader(
    "🚀 Recommended Skills to Develop"
)

if missing_skills:

    for skill in missing_skills:

        st.write(
            f"📌 Focus on learning **{skill}** next."
        )

else:

    st.success(
        "Continue strengthening your existing skills through projects and practical experience."
    )


# ============================================================
# CAREER DETAILS
# ============================================================

st.subheader("🎓 Career Details")

detail_col1, detail_col2 = st.columns(2)

with detail_col1:

    st.write(
        f"**Domain:** "
        f"{domain if domain else 'Not specified'}"
    )

with detail_col2:

    st.write(
        f"**Education:** "
        f"{education if education else 'Not specified'}"
    )


# ============================================================
# FINAL STATUS
# ============================================================

if coverage >= 80:

    st.success(
        f"Your current skill profile is strongly aligned "
        f"with {selected_career}."
    )

elif coverage >= 50:

    st.info(
        f"You have a good starting foundation for "
        f"{selected_career}, but some important skills "
        f"still need development."
    )

else:

    st.warning(
        f"You are at an early stage for {selected_career}. "
        f"Focus on the listed skill gaps step by step."
    )


st.caption(
    f"Selected career is saved automatically. "
    f"Available careers: {len(careers)}"
)