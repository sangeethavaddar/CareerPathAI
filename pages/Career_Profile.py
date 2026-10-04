import streamlit as st
import json
from pathlib import Path


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Career Profile",
    page_icon="👤",
    layout="wide"
)


# ---------------------------------------------------------
# FILE PATH
# ---------------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
PROFILE_FILE = PROJECT_FOLDER / "data" / "profile.json"


# ---------------------------------------------------------
# LOAD PROFILE
# ---------------------------------------------------------

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

        return default_profile

    except Exception:
        return default_profile


# ---------------------------------------------------------
# SAVE PROFILE
# ---------------------------------------------------------

def save_profile(profile):
    PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profile, file, indent=4)


# ---------------------------------------------------------
# LOAD SAVED DATA
# ---------------------------------------------------------

profile = load_profile()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("👤 Career Profile")
st.write("Create and update your personal career profile.")


# ---------------------------------------------------------
# PERSONAL INFORMATION
# ---------------------------------------------------------

st.subheader("Personal Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Full Name",
        value=str(profile.get("name", "")),
        key="career_profile_name"
    )

with col2:
    age = st.text_input(
        "Age",
        value=str(profile.get("age", "")),
        key="career_profile_age"
    )


# ---------------------------------------------------------
# EDUCATION
# ---------------------------------------------------------

st.subheader("Education")

col1, col2 = st.columns(2)

with col1:
    education_options = [
        "10th",
        "12th / PUC",
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
        index=education_options.index(saved_education),
        key="career_profile_education"
    )


with col2:
    specialization = st.text_input(
        "Specialization",
        value=str(profile.get("specialization", "")),
        key="career_profile_specialization"
    )


# ---------------------------------------------------------
# EXPERIENCE
# ---------------------------------------------------------

st.subheader("Experience")

experience_options = [
    "No Experience",
    "Less than 1 Year",
    "1-2 Years",
    "2-5 Years",
    "5+ Years"
]

saved_experience = profile.get(
    "experience",
    "No Experience"
)

if saved_experience not in experience_options:
    saved_experience = "No Experience"

experience = st.selectbox(
    "Experience Level",
    experience_options,
    index=experience_options.index(saved_experience),
    key="career_profile_experience"
)


# ---------------------------------------------------------
# CAREER GOAL
# ---------------------------------------------------------

st.subheader("Career Goal")

career_goal = st.text_input(
    "What career role are you interested in?",
    value=str(profile.get("career_goal", "")),
    key="career_profile_goal"
)


# ---------------------------------------------------------
# PROFESSIONAL DOMAIN
# ---------------------------------------------------------

st.subheader("Preferred Professional Domain")

domain_options = [
    "Technology",
    "Engineering",
    "Healthcare",
    "Finance",
    "Business",
    "Education",
    "Law",
    "Media",
    "Arts & Design",
    "Architecture",
    "Agriculture",
    "Environment",
    "Hospitality",
    "Sports"
]

saved_domain = profile.get(
    "preferred_domain",
    "Technology"
)

if saved_domain not in domain_options:
    saved_domain = "Technology"

preferred_domain = st.selectbox(
    "Preferred Domain",
    domain_options,
    index=domain_options.index(saved_domain),
    key="career_profile_domain"
)


# ---------------------------------------------------------
# SKILLS
# ---------------------------------------------------------

st.subheader("Skills")

skill_options = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Data Analysis",
    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "Cybersecurity",
    "Cloud Computing",
    "Communication",
    "Leadership",
    "Problem Solving",
    "Project Management",
    "Accounting",
    "Finance",
    "Marketing",
    "Sales",
    "Teaching",
    "Research",
    "Writing",
    "Graphic Design",
    "UI UX Design",
    "Architecture",
    "Biology",
    "Medicine",
    "Clinical Skills",
    "Agriculture",
    "Environmental Science",
    "Hospitality Management",
    "Cooking",
    "Fitness",
    "Sports Management"
]

saved_skills = profile.get("skills", [])

if not isinstance(saved_skills, list):
    saved_skills = []

valid_saved_skills = [
    skill for skill in saved_skills
    if skill in skill_options
]

skills = st.multiselect(
    "Select your skills",
    skill_options,
    default=valid_saved_skills,
    key="career_profile_skills"
)


# ---------------------------------------------------------
# INTERESTS
# ---------------------------------------------------------

st.subheader("Interests")

interest_options = [
    "Programming",
    "Artificial Intelligence",
    "Machine Learning",
    "Web Development",
    "Data Science",
    "Cybersecurity",
    "Cloud Computing",
    "Engineering",
    "Healthcare",
    "Medicine",
    "Biology",
    "Finance",
    "Business",
    "Entrepreneurship",
    "Marketing",
    "Teaching",
    "Research",
    "Law",
    "Journalism",
    "Writing",
    "Content Creation",
    "Graphic Design",
    "UI UX Design",
    "Architecture",
    "Agriculture",
    "Environment",
    "Hospitality",
    "Cooking",
    "Fitness",
    "Sports"
]

saved_interests = profile.get("interests", [])

if not isinstance(saved_interests, list):
    saved_interests = []

valid_saved_interests = [
    interest for interest in saved_interests
    if interest in interest_options
]

interests = st.multiselect(
    "Select your interests",
    interest_options,
    default=valid_saved_interests,
    key="career_profile_interests"
)


# ---------------------------------------------------------
# PROJECTS
# ---------------------------------------------------------

st.subheader("Projects")

project_options = [
    "Course Feedback Portal",
    "Ecommerce Website",
    "Voice-Controlled Home Automation using AI Assistance",
    "Machine Learning Project",
    "Deep Learning Project",
    "Web Development Project",
    "Mobile Application",
    "Cybersecurity Project",
    "Data Analysis Project",
    "IoT Project",
    "Cloud Computing Project",
    "Other"
]

saved_projects = profile.get("projects", [])

if not isinstance(saved_projects, list):
    saved_projects = []

valid_saved_projects = [
    project for project in saved_projects
    if project in project_options
]

projects = st.multiselect(
    "Select your projects",
    project_options,
    default=valid_saved_projects,
    key="career_profile_projects"
)


# ---------------------------------------------------------
# SAVE BUTTON
# ---------------------------------------------------------

st.divider()

if st.button(
    "🔄 Update Career Profile",
    type="primary",
    use_container_width=True
):

    updated_profile = {
        "name": name,
        "age": age,
        "education": education,
        "specialization": specialization,
        "experience": experience,
        "career_goal": career_goal,
        "preferred_domain": preferred_domain,
        "skills": skills,
        "interests": interests,
        "projects": projects
    }

    try:
        save_profile(updated_profile)

        st.success(
            "Career Profile updated successfully!"
        )

        st.info(
            "Your profile is permanently saved. "
            "You can now move between pages without losing the saved information."
        )

    except Exception as error:
        st.error(
            f"Unable to save your profile: {error}"
        )


# ---------------------------------------------------------
# CURRENT SAVED PROFILE
# ---------------------------------------------------------

st.divider()

st.subheader("Current Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"**Name:** {name}")
    st.write(f"**Education:** {education}")
    st.write(f"**Experience:** {experience}")

with col2:
    st.write(f"**Domain:** {preferred_domain}")
    st.write(f"**Career Goal:** {career_goal}")

with col3:
    st.write(f"**Skills:** {len(skills)}")
    st.write(f"**Interests:** {len(interests)}")
    st.write(f"**Projects:** {len(projects)}")