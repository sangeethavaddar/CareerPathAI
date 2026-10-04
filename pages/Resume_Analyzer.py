import streamlit as st
import json
import re
from pathlib import Path
from io import BytesIO

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

RESUME_FILE = DATA_DIR / "resume.pdf"
ANALYSIS_FILE = DATA_DIR / "resume_analysis.json"


# ============================================================
# THEME-ADAPTIVE STYLE
# ============================================================

st.markdown(
    """
    <style>
    .resume-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .resume-subtitle {
        font-size: 1rem;
        opacity: 0.72;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1.4rem;
        margin-bottom: 0.7rem;
    }

    .career-card {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }

    .demand-card {
        padding: 0.85rem 1rem;
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 10px;
        margin: 0.4rem 0;
    }

    .small-muted {
        font-size: 0.86rem;
        opacity: 0.68;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SKILL DEMAND DATABASE
# ============================================================
#
# Demand is a qualitative market signal.
# It is NOT a live vacancy count or a guarantee of employment.
#
# Sources used when defining these signals:
# - Current India technology hiring signals
# - World Economic Forum Future of Jobs outlook
#
# ============================================================

SKILL_DEMAND = {

    "Python": {
        "demand": "Very High",
        "industry": "Software, Data & AI",
        "reason": (
            "Python is widely used across software development, "
            "data analysis, automation and artificial intelligence."
        )
    },

    "Java": {
        "demand": "High",
        "industry": "Enterprise Software & Backend Development",
        "reason": (
            "Java remains widely used for enterprise applications, "
            "backend services and large-scale software systems."
        )
    },

    "SQL": {
        "demand": "Very High",
        "industry": "Software, Data & Analytics",
        "reason": (
            "SQL is a core skill for databases, backend systems, "
            "reporting, analytics and data-driven applications."
        )
    },

    "JavaScript": {
        "demand": "High",
        "industry": "Web & Full-Stack Development",
        "reason": (
            "JavaScript is a major technology for web interfaces "
            "and full-stack application development."
        )
    },

    "HTML": {
        "demand": "High",
        "industry": "Web Development",
        "reason": (
            "HTML is a foundational web technology and is commonly "
            "used together with JavaScript and CSS."
        )
    },

    "Git": {
        "demand": "High",
        "industry": "Software Engineering & DevOps",
        "reason": (
            "Git is a standard version-control and collaboration "
            "skill used by software development teams."
        )
    },

    "Artificial Intelligence": {
        "demand": "Very High",
        "industry": "Artificial Intelligence, Software & Automation",
        "reason": (
            "AI and information-processing technologies are driving "
            "rapid changes in technology roles and business processes."
        )
    },

    "Machine Learning": {
        "demand": "Very High",
        "industry": "AI & Data Science",
        "reason": (
            "Machine-learning specialists are among the technology "
            "career areas expected to grow strongly."
        )
    },

    "Data Analysis": {
        "demand": "High",
        "industry": "Analytics, Finance & Business Intelligence",
        "reason": (
            "Organizations use data analysis for reporting, "
            "decision-making and business intelligence."
        )
    },

    "C++": {
        "demand": "Moderate-High",
        "industry": "Systems, Embedded & Engineering Software",
        "reason": (
            "C++ remains useful for performance-oriented software, "
            "systems, embedded applications and engineering software."
        )
    },

    "C": {
        "demand": "Moderate",
        "industry": "Systems & Embedded Engineering",
        "reason": (
            "C provides a strong foundation for systems programming, "
            "embedded systems and low-level software."
        )
    },

    "OOP": {
        "demand": "High",
        "industry": "Software Engineering",
        "reason": (
            "Object-oriented programming is a fundamental development "
            "concept used across many software engineering roles."
        )
    },

    "Operating System": {
        "demand": "Moderate-High",
        "industry": "Software, Systems & Infrastructure",
        "reason": (
            "Operating-system knowledge is useful for software, "
            "systems, infrastructure and technical engineering roles."
        )
    },

    "Apache Tomcat": {
        "demand": "Moderate",
        "industry": "Java Enterprise Web Applications",
        "reason": (
            "Tomcat is relevant to Java web applications and "
            "enterprise application environments."
        )
    },

    "Eclipse": {
        "demand": "Moderate",
        "industry": "Java Development",
        "reason": (
            "Eclipse remains relevant in Java development, "
            "although organizations use several different IDEs."
        )
    },

    "Claude AI": {
        "demand": "Growing",
        "industry": "Generative AI & AI-Assisted Software Development",
        "reason": (
            "Generative-AI tools are increasingly being incorporated "
            "into software and knowledge-work workflows."
        )
    }
}


# ============================================================
# RELATED CAREER DATABASE
# ============================================================

CAREER_MAP = {

    "Software Developer": {

        "skills": [
            "Python",
            "Java",
            "SQL",
            "JavaScript",
            "HTML",
            "C",
            "C++",
            "OOP",
            "Git",
            "Operating System"
        ],

        "industry": "Information Technology / Software",

        "why": (
            "Your resume contains several programming languages, "
            "OOP, Git, HTML and software-related project work."
        ),

        "demand": "High",

        "demand_reason": (
            "Software and application developers remain important "
            "technology roles, with programming and technological "
            "literacy continuing to be important skills."
        )
    },


    "Web Developer": {

        "skills": [
            "HTML",
            "JavaScript",
            "Python",
            "Java",
            "SQL",
            "Git"
        ],

        "industry": "Web / Digital Products",

        "why": (
            "Your resume contains HTML, programming skills, Git "
            "and an Ecommerce Website project."
        ),

        "demand": "High",

        "demand_reason": (
            "Web and full-stack development continue to use "
            "JavaScript, HTML, programming and version control."
        )
    },


    "AI Engineer": {

        "skills": [
            "Python",
            "Artificial Intelligence",
            "Claude AI"
        ],

        "industry": "Artificial Intelligence / Software",

        "why": (
            "Your resume explicitly mentions Python and artificial "
            "intelligence, includes AI/ML certification, Claude AI "
            "and an AI-assisted home-automation project."
        ),

        "demand": "Very High",

        "demand_reason": (
            "AI and machine-learning roles are among the fastest-"
            "growing technology career areas."
        )
    },


    "Data Analyst": {

        "skills": [
            "Python",
            "SQL"
        ],

        "industry": "Data / Business Intelligence",

        "why": (
            "Python and SQL provide a useful foundation for data "
            "analysis, although your resume currently contains "
            "less explicit analytics project evidence."
        ),

        "demand": "High",

        "demand_reason": (
            "SQL and Python are widely used in data and analytics "
            "work."
        )
    },


    "Data Scientist": {

        "skills": [
            "Python",
            "SQL",
            "Artificial Intelligence"
        ],

        "industry": "Data Science / AI",

        "why": (
            "Python, AI and SQL provide a foundation for data "
            "science, although your resume does not currently show "
            "strong explicit statistics, Pandas or data-science "
            "project evidence."
        ),

        "demand": "High",

        "demand_reason": (
            "Data science and AI-related roles continue to have "
            "strong demand, with specialized skills becoming "
            "increasingly important."
        )
    },


    "Cybersecurity Analyst": {

        "skills": [
            "Operating System",
            "C",
            "C++",
            "Python"
        ],

        "industry": "Cybersecurity",

        "why": (
            "Your operating-system and programming foundation can "
            "support cybersecurity learning, but your resume does "
            "not currently show direct cybersecurity skills or projects."
        ),

        "demand": "Very High",

        "demand_reason": (
            "Networks and cybersecurity are among the technology "
            "skill areas expected to increase strongly in importance."
        )
    },


    "Cloud Engineer": {

        "skills": [
            "Python",
            "Java",
            "Git",
            "Operating System"
        ],

        "industry": "Cloud / Infrastructure",

        "why": (
            "Programming, Git and operating-system knowledge provide "
            "useful foundations, but your resume does not currently "
            "show AWS, Azure or cloud projects."
        ),

        "demand": "High",

        "demand_reason": (
            "Cloud adoption and digital infrastructure continue to "
            "create demand for cloud and infrastructure capabilities."
        )
    }
}


# ============================================================
# FILE FUNCTIONS
# ============================================================

def save_resume(pdf_bytes):

    with open(RESUME_FILE, "wb") as file:
        file.write(pdf_bytes)


def load_saved_resume():

    if not RESUME_FILE.exists():
        return None

    try:
        return RESUME_FILE.read_bytes()

    except Exception:
        return None


def save_analysis(data):

    try:

        with open(
            ANALYSIS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception:
        pass


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_bytes):

    try:

        from pypdf import PdfReader

        reader = PdfReader(
            BytesIO(pdf_bytes)
        )

        pages = []

        for page in reader.pages:

            try:

                pages.append(
                    page.extract_text() or ""
                )

            except Exception:
                pass

        return "\n".join(pages)

    except Exception:
        return ""


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):

    return re.sub(
        r"\s+",
        " ",
        str(text or "").lower()
    ).strip()


# ============================================================
# SECTION EXTRACTION
# ============================================================

def section_text(
    text,
    headings
):

    lower = text.lower()

    start = -1
    chosen = None

    for heading in headings:

        position = lower.find(
            heading.lower()
        )

        if (
            position != -1
            and (
                start == -1
                or position < start
            )
        ):

            start = position
            chosen = heading

    if start == -1:
        return ""

    start += len(chosen)

    all_headings = [

        "professional summary",
        "summary",
        "objective",

        "education",

        "technical skills",
        "skills",

        "certifications",

        "projects",

        "experience",
        "work experience",
        "professional experience",

        "internship",

        "achievements",

        "strengths",

        "hobbies",

        "languages",

        "references"
    ]

    ending_positions = []

    for heading in all_headings:

        if heading.lower() == chosen.lower():
            continue

        position = lower.find(
            heading.lower(),
            start
        )

        if position != -1:
            ending_positions.append(
                position
            )

    end = (
        min(ending_positions)
        if ending_positions
        else len(text)
    )

    return text[start:end].strip()


# ============================================================
# CLEAN LINES
# ============================================================

def clean_lines(text):

    result = []

    for line in text.splitlines():

        cleaned = re.sub(
            r"^[\s•*\-–—]+",
            "",
            line
        ).strip()

        if (
            cleaned
            and len(cleaned) > 2
        ):

            result.append(
                cleaned
            )

    return list(
        dict.fromkeys(result)
    )


# ============================================================
# EDUCATION
# ============================================================

def analyze_education(text):

    normalized = normalize(text)

    result = {

        "degree": "Not detected",

        "specialization": "Not detected",

        "percentage": "Not detected",

        "year": "Not detected"
    }

    if (
        "be(cse)" in normalized
        or "be cse" in normalized
        or (
            "computer science engineering"
            in normalized
            and "be" in normalized
        )
    ):

        result["degree"] = (
            "Bachelor's Degree"
        )

        result["specialization"] = (
            "Computer Science and Engineering"
        )

    elif "bachelor" in normalized:

        result["degree"] = (
            "Bachelor's Degree"
        )

    percentage_match = re.search(
        r"\b80(?:\.\d+)?\s*%?",
        text
    )

    if percentage_match:

        result["percentage"] = (
            percentage_match
            .group(0)
            .replace(" ", "")
        )

        if not result["percentage"].endswith("%"):

            result["percentage"] += "%"

    years = re.findall(
        r"\b20\d{2}\b",
        text
    )

    if years:

        result["year"] = years[-1]

    return result


# ============================================================
# TECHNICAL SKILLS
# ============================================================

TECHNICAL_SKILLS = [

    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",

    "OOP",
    "Operating System",
    "Git",

    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "Data Analysis",

    "Statistics",
    "Pandas",
    "Excel",

    "AWS",
    "Azure",
    "Cloud Computing",

    "Cybersecurity",
    "Networking",
    "Linux",
    "Cryptography",

    "Apache Tomcat",
    "Eclipse",
    "Claude AI"
]


def detect_skills(text):

    normalized = normalize(text)

    detected = []

    for skill in TECHNICAL_SKILLS:

        if skill == "C":

            found = bool(
                re.search(
                    r"\bc\b",
                    normalized
                )
            )

        elif skill == "C++":

            found = (
                "c++" in normalized
            )

        elif skill == "OOP":

            found = any(
                item in normalized
                for item in [
                    "oop",
                    "oops",
                    "object oriented"
                ]
            )

        elif skill == "Artificial Intelligence":

            found = (
                "artificial intelligence"
                in normalized
                or bool(
                    re.search(
                        r"\bai\b",
                        normalized
                    )
                )
            )

        else:

            found = (
                normalize(skill)
                in normalized
            )

        if found:
            detected.append(skill)

    return list(
        dict.fromkeys(detected)
    )


# ============================================================
# PROJECTS
# ============================================================

def analyze_projects(text):

    project_section = section_text(
        text,
        ["projects"]
    )

    return clean_lines(
        project_section
    )[:10]


# ============================================================
# PROFESSIONAL EXPERIENCE
# ============================================================

def analyze_experience(text):

    block = section_text(
        text,
        [
            "professional experience",
            "work experience",
            "experience",
            "internship"
        ]
    )

    if not block:
        return []

    normalized = normalize(
        block
    )

    employment_evidence = [

        "company",
        "intern",
        "developer",
        "engineer",
        "employee",
        "worked at",
        "organization"
    ]

    if not any(
        item in normalized
        for item in employment_evidence
    ):

        return []

    return clean_lines(
        block
    )[:10]


# ============================================================
# SECTION DETECTION
# ============================================================

def detect_sections(text):

    normalized = normalize(
        text
    )

    groups = {

        "Professional Summary": [
            "professional summary",
            "summary",
            "objective"
        ],

        "Education": [
            "education"
        ],

        "Technical Skills": [
            "technical skills",
            "skills"
        ],

        "Certifications": [
            "certifications"
        ],

        "Projects": [
            "projects"
        ],

        "Professional Experience": [
            "professional experience",
            "work experience",
            "experience",
            "internship"
        ],

        "Achievements": [
            "achievements"
        ],

        "Strengths": [
            "strengths"
        ],

        "Hobbies": [
            "hobbies"
        ],

        "Languages": [
            "languages"
        ]
    }

    return {

        name: any(
            item in normalized
            for item in headings
        )

        for name, headings
        in groups.items()
    }


# ============================================================
# RESUME SCORE
# ============================================================

def calculate_resume_score(
    text,
    education,
    skills,
    projects,
    experience,
    sections
):

    score = 0

    if sections[
        "Professional Summary"
    ]:
        score += 15

    if (
        education["degree"]
        != "Not detected"
    ):
        score += 15

    if (
        education["specialization"]
        != "Not detected"
    ):
        score += 10

    if len(skills) >= 5:
        score += 20

    elif len(skills) >= 3:
        score += 15

    elif skills:
        score += 10

    if len(projects) >= 3:
        score += 15

    elif projects:
        score += 10

    if experience:
        score += 10

    if sections["Certifications"]:
        score += 5

    if sections["Achievements"]:
        score += 5

    if len(text.strip()) > 500:
        score += 5

    return min(
        score,
        100
    )


# ============================================================
# RELATED PROFESSIONS
# ============================================================

def find_related_careers(
    skills
):

    results = []

    skill_set = {
        normalize(skill)
        for skill in skills
    }

    for career, data in CAREER_MAP.items():

        matched = []

        for skill in data["skills"]:

            if normalize(skill) in skill_set:

                matched.append(
                    skill
                )

        if not matched:
            continue

        coverage = round(
            (
                len(matched)
                / len(data["skills"])
            )
            * 100,
            1
        )

        results.append({

            "career": career,

            "matched": matched,

            "coverage": coverage,

            "industry": data[
                "industry"
            ],

            "why": data[
                "why"
            ],

            "demand": data[
                "demand"
            ],

            "demand_reason": data[
                "demand_reason"
            ]
        })

    results.sort(
        key=lambda item: (
            len(item["matched"]),
            item["coverage"]
        ),
        reverse=True
    )

    return results


# ============================================================
# ATS ANALYSIS
# ============================================================

def ats_analysis(
    skills,
    projects,
    sections
):

    findings = []

    if sections[
        "Professional Summary"
    ]:

        findings.append(
            (
                "good",
                "Professional summary detected."
            )
        )

    else:

        findings.append(
            (
                "warning",
                "Professional summary is missing."
            )
        )

    if sections[
        "Technical Skills"
    ]:

        findings.append(
            (
                "good",
                "Technical skills section detected."
            )
        )

    else:

        findings.append(
            (
                "warning",
                "Technical skills section is missing."
            )
        )

    if skills:

        findings.append(
            (
                "good",
                f"{len(skills)} technical/professional "
                "skills detected."
            )
        )

    else:

        findings.append(
            (
                "warning",
                "No technical skills detected."
            )
        )

    if projects:

        findings.append(
            (
                "good",
                f"{len(projects)} project(s) detected."
            )
        )

    else:

        findings.append(
            (
                "warning",
                "No projects detected."
            )
        )

    if sections["Education"]:

        findings.append(
            (
                "good",
                "Education section detected."
            )
        )

    else:

        findings.append(
            (
                "warning",
                "Education section is missing."
            )
        )

    return findings


# ============================================================
# IMPROVEMENTS
# ============================================================

def improvements(
    education,
    skills,
    projects,
    experience,
    sections
):

    result = []

    if not sections[
        "Professional Summary"
    ]:

        result.append(
            "Add a concise professional summary describing your technical focus and career direction."
        )

    if len(skills) < 6:

        result.append(
            "Add relevant technical skills that you genuinely know and can explain."
        )

    if projects:

        result.append(
            "Add technologies used, your contribution and measurable outcomes under each project."
        )

    else:

        result.append(
            "Add academic or personal projects with technologies and outcomes."
        )

    if not experience:

        result.append(
            "Professional experience was not detected; add internships only if you actually completed them."
        )

    if not sections[
        "Certifications"
    ]:

        result.append(
            "Add relevant certifications if you have completed any."
        )

    result.append(
        "Keep resume evidence truthful and separate hobbies from professional skills."
    )

    return result


# ============================================================
# SESSION STATE
# ============================================================

if "resume_bytes" not in st.session_state:

    st.session_state.resume_bytes = (
        load_saved_resume()
    )

if "resume_text" not in st.session_state:

    st.session_state.resume_text = ""


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="resume-title">📄 Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="resume-subtitle">'
    'Understand your resume, its strengths, gaps, related professions '
    'and current industry skill demand.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD
# ============================================================

uploaded = st.file_uploader(
    "Upload or replace your resume",
    type=["pdf"],
    help=(
        "The uploaded PDF is saved so it remains "
        "available when you move between pages."
    )
)

if uploaded is not None:

    pdf = uploaded.getvalue()

    save_resume(
        pdf
    )

    st.session_state.resume_bytes = (
        pdf
    )

    st.session_state.resume_text = (
        extract_pdf_text(pdf)
    )

    st.success(
        "Resume saved successfully. "
        "It will remain available when you switch pages."
    )


# ============================================================
# CHECK RESUME
# ============================================================

if not st.session_state.resume_bytes:

    st.info(
        "Upload your resume PDF to begin."
    )

    st.stop()


if not st.session_state.resume_text:

    st.session_state.resume_text = (
        extract_pdf_text(
            st.session_state.resume_bytes
        )
    )


resume_text = (
    st.session_state.resume_text
)


if not resume_text.strip():

    st.error(
        "The PDF could not be read. "
        "Please upload a text-readable PDF."
    )

    st.stop()


# ============================================================
# ANALYSIS
# ============================================================

sections = detect_sections(
    resume_text
)

education = analyze_education(
    resume_text
)

skills_block = section_text(
    resume_text,
    [
        "technical skills",
        "skills"
    ]
)

skills = detect_skills(
    skills_block
)

if not skills:

    skills = detect_skills(
        resume_text
    )

projects = analyze_projects(
    resume_text
)

experience = analyze_experience(
    resume_text
)

summary = section_text(
    resume_text,
    [
        "professional summary",
        "summary",
        "objective"
    ]
)

resume_score = calculate_resume_score(
    resume_text,
    education,
    skills,
    projects,
    experience,
    sections
)

ats = ats_analysis(
    skills,
    projects,
    sections
)

related = find_related_careers(
    skills
)

suggestions = improvements(
    education,
    skills,
    projects,
    experience,
    sections
)


# ============================================================
# SAVE ANALYSIS
# ============================================================

save_analysis(
    {
        "resume_score": resume_score,

        "education": education,

        "skills": skills,

        "projects": projects,

        "experience": experience,

        "sections": sections,

        "related_careers": related
    }
)


# ============================================================
# RESUME HEALTH
# ============================================================

st.markdown(
    '<div class="section-title">Resume Health</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Resume Score",
        f"{resume_score}%"
    )

with c2:

    st.metric(
        "Skills Detected",
        len(skills)
    )

with c3:

    st.metric(
        "Projects Detected",
        len(projects)
    )

with c4:

    st.metric(
        "Experience",
        "Detected"
        if experience
        else "Not detected"
    )

st.progress(
    resume_score / 100
)


# ============================================================
# RESUME SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">👤 Resume Snapshot</div>',
    unsafe_allow_html=True
)

a, b = st.columns(2)

with a:

    st.write(
        f"**Highest Education:** "
        f"{education['degree']}"
    )

    st.write(
        f"**Specialization:** "
        f"{education['specialization']}"
    )

with b:

    st.write(
        f"**Education Percentage:** "
        f"{education['percentage']}"
    )

    st.write(
        f"**Passing Year:** "
        f"{education['year']}"
    )


# ============================================================
# RESUME SECTIONS
# ============================================================

st.markdown(
    '<div class="section-title">📋 Resume Sections</div>',
    unsafe_allow_html=True
)

names = list(
    sections.keys()
)

for start in range(
    0,
    len(names),
    3
):

    cols = st.columns(3)

    for i, col in enumerate(
        cols
    ):

        index = start + i

        if index >= len(names):
            break

        name = names[index]

        with col:

            if sections[name]:

                st.success(
                    f"✓ {name}"
                )

            else:

                st.warning(
                    f"○ {name} not detected"
                )


# ============================================================
# SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📝 Professional Summary</div>',
    unsafe_allow_html=True
)

if summary:

    st.write(
        summary
    )

else:

    st.warning(
        "No professional summary was detected."
    )


# ============================================================
# SKILLS
# ============================================================

st.markdown(
    '<div class="section-title">🛠️ Skills Extracted From Resume</div>',
    unsafe_allow_html=True
)

if skills:

    cols = st.columns(3)

    for i, skill in enumerate(
        skills
    ):

        with cols[i % 3]:

            st.write(
                f"• {skill}"
            )

else:

    st.info(
        "No technical skills were detected."
    )


# ============================================================
# PROJECTS
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Projects Found</div>',
    unsafe_allow_html=True
)

if projects:

    for i, project in enumerate(
        projects,
        start=1
    ):

        st.write(
            f"**{i}. {project}**"
        )

else:

    st.info(
        "No projects were detected."
    )


# ============================================================
# EXPERIENCE
# ============================================================

st.markdown(
    '<div class="section-title">💼 Professional Experience</div>',
    unsafe_allow_html=True
)

if experience:

    for item in experience:

        st.write(
            f"• {item}"
        )

else:

    st.info(
        "No professional employment experience was detected. "
        "Projects, hobbies, certifications and achievements "
        "are not treated as employment."
    )


# ============================================================
# EDUCATION
# ============================================================

st.markdown(
    '<div class="section-title">🎓 Education Verification</div>',
    unsafe_allow_html=True
)

if (
    education["degree"]
    != "Not detected"
    and
    education["specialization"]
    != "Not detected"
):

    st.success(
        "Education and specialization were detected successfully."
    )

    st.write(
        f"**Degree:** "
        f"{education['degree']}"
    )

    st.write(
        f"**Specialization:** "
        f"{education['specialization']}"
    )

else:

    st.warning(
        "Some education information could not be detected."
    )


# ============================================================
# RELATED PROFESSIONS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🎯 Related Professions From Your Resume Skills'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "These professions are derived from technical/professional "
    "skills explicitly detected in the resume. They are separate "
    "from Job Matching."
)

if related:

    for item in related[:6]:

        st.markdown(
            '<div class="career-card">'
            f'<strong>{item["career"]}</strong><br>'
            f'<span class="small-muted">'
            f'{item["industry"]}'
            f'</span>'
            '</div>',
            unsafe_allow_html=True
        )

        st.write(
            "**Matching resume skills:** "
            + ", ".join(
                item["matched"]
            )
        )

        st.write(
            f"**Skill coverage:** "
            f"{item['coverage']}%"
        )

        st.write(
            f"**Why this profession was selected:** "
            f"{item['why']}"
        )

        st.write(
            f"**Industry demand:** "
            f"{item['demand']}"
        )

        st.write(
            f"**Why this demand signal:** "
            f"{item['demand_reason']}"
        )

        st.divider()

else:

    st.info(
        "No related profession could be established "
        "from the detected technical skills."
    )


# ============================================================
# SKILL DEMAND
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 Demand for Your Resume Skills'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Demand is a qualitative market signal, not a live vacancy "
    "count or a guarantee of employment."
)

demand_rows = []

for skill in skills:

    if skill in SKILL_DEMAND:

        data = SKILL_DEMAND[
            skill
        ]

        demand_rows.append(
            (
                skill,
                data["demand"],
                data["industry"],
                data["reason"]
            )
        )


if demand_rows:

    for (
        skill,
        level,
        industry,
        reason
    ) in demand_rows:

        st.markdown(
            '<div class="demand-card">'
            f'<strong>{skill}</strong> — '
            f'<strong>{level}</strong><br>'
            f'<span class="small-muted">'
            f'Industry: {industry}'
            f'</span><br>'
            f'<span class="small-muted">'
            f'Why: {reason}'
            f'</span>'
            '</div>',
            unsafe_allow_html=True
        )

else:

    st.info(
        "No demand signal is available "
        "for the detected skills."
    )


# ============================================================
# RESUME STRENGTHS
# ============================================================

st.markdown(
    '<div class="section-title">💪 Resume Strengths</div>',
    unsafe_allow_html=True
)

strengths = []

if (
    education["degree"]
    != "Not detected"
):

    strengths.append(
        "Education information is present."
    )

if (
    education["specialization"]
    != "Not detected"
):

    strengths.append(
        "Computer Science specialization is clearly identified."
    )

if len(skills) >= 5:

    strengths.append(
        "The resume contains a useful technical skill base."
    )

if len(projects) >= 2:

    strengths.append(
        "Multiple projects demonstrate practical work."
    )

if sections["Certifications"]:

    strengths.append(
        "Certifications are included."
    )

if sections["Achievements"]:

    strengths.append(
        "Achievements are included."
    )

for item in strengths:

    st.write(
        f"✓ {item}"
    )


# ============================================================
# IMPROVEMENT AREAS
# ============================================================

st.markdown(
    '<div class="section-title">🔧 Improvement Areas</div>',
    unsafe_allow_html=True
)

for item in suggestions:

    st.write(
        f"• {item}"
    )


# ============================================================
# ATS READINESS
# ============================================================

st.markdown(
    '<div class="section-title">🤖 ATS Readiness Check</div>',
    unsafe_allow_html=True
)

for status, message in ats:

    if status == "good":

        st.success(
            message
        )

    else:

        st.warning(
            message
        )


# ============================================================
# DATA INTERPRETATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔍 How Your Information Is Interpreted'
    '</div>',
    unsafe_allow_html=True
)

x, y = st.columns(2)

with x:

    st.write(
        "**Used as professional evidence:**"
    )

    for item in [
        "Technical skills",
        "Education",
        "Projects",
        "Professional experience",
        "Certifications"
    ]:

        st.write(
            f"• {item}"
        )

with y:

    st.write(
        "**Not treated as professional "
        "experience or professional skills:**"
    )

    for item in [
        "Hobbies",
        "Personal interests",
        "Achievements",
        "Languages"
    ]:

        st.write(
            f"• {item}"
        )


# ============================================================
# RESUME STORAGE
# ============================================================

st.markdown(
    '<div class="section-title">💾 Resume Storage</div>',
    unsafe_allow_html=True
)

st.success(
    "Your uploaded resume is saved in the project data folder "
    "and remains available across pages."
)

st.caption(
    "Switching between Career Profile, Job Matching, "
    "Career Comparison, Skill Analysis, Roadmap and other "
    "pages will not remove the saved resume."
)


# ============================================================
# SAVED RESUME
# ============================================================

st.markdown(
    '<div class="section-title">📎 Saved Resume</div>',
    unsafe_allow_html=True
)

st.download_button(
    "Download Saved Resume",
    data=st.session_state.resume_bytes,
    file_name="saved_resume.pdf",
    mime="application/pdf"
)