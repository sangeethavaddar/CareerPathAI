import io
import re
from pathlib import Path

import streamlit as st

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None


st.set_page_config(
    page_title="Resume Improvement | CareerPath AI",
    page_icon="✨",
    layout="wide"
)


# =========================================================
# TEXT EXTRACTION
# =========================================================

def extract_text(uploaded_file):

    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()

    if suffix == ".txt":
        return data.decode("utf-8", errors="ignore")

    if suffix == ".pdf":

        if PdfReader is None:
            raise RuntimeError(
                "Install pypdf using: pip install pypdf"
            )

        reader = PdfReader(io.BytesIO(data))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if suffix == ".docx":

        if Document is None:
            raise RuntimeError(
                "Install python-docx using: pip install python-docx"
            )

        document = Document(io.BytesIO(data))

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    raise ValueError(
        "Upload a PDF, DOCX or TXT file."
    )


def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


# =========================================================
# SECTION DETECTION
# =========================================================

SECTION_HEADERS = {
    "Objective": [
        "objective",
        "career objective",
        "professional objective",
        "summary",
        "profile"
    ],
    "Education": [
        "education",
        "academic qualification",
        "academic qualifications"
    ],
    "Skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills"
    ],
    "Experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships",
        "employment"
    ],
    "Projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],
    "Certifications": [
        "certifications",
        "certificates",
        "courses",
        "training"
    ]
}


def detect_sections(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    detected = {}

    for section, headers in SECTION_HEADERS.items():

        found = False

        for line in lines:

            clean = re.sub(
                r"[^a-zA-Z ]",
                "",
                line
            ).strip().lower()

            if clean in [
                header.lower()
                for header in headers
            ]:
                found = True
                break

        detected[section] = found

    # Detect objective even when there is no heading
    if not detected["Objective"]:

        objective_terms = [
            "seeking an entry-level",
            "seeking an entry level",
            "seeking a position",
            "looking for an opportunity",
            "career objective"
        ]

        if any(
            term in normalize(text)
            for term in objective_terms
        ):
            detected["Objective"] = True

    return detected


# =========================================================
# SAME SKILL ENGINE USED FOR THIS RESUME
# =========================================================

SKILL_ALIASES = {

    "Python": ["python"],

    "Java": [r"\bjava\b"],

    "C++": ["c++", "cpp"],

    "C": [r"\bc\b"],

    "HTML": [r"\bhtml\b"],

    "CSS": [r"\bcss\b"],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    "OOP": [
        "oops",
        "oop",
        "object oriented",
        "object-oriented"
    ],

    "Data Structures": [
        "data structures",
        "dsa"
    ],

    "Operating Systems": [
        "operating system",
        "operating systems"
    ],

    "Git": [
        r"\bgit\b"
    ],

    "Apache Tomcat": [
        "apache tomcat",
        "tomcat"
    ],

    "Eclipse": [
        r"\beclipse\b"
    ],

    "Claude AI": [
        "claude ai",
        "claude"
    ],

    "Machine Learning": [
        "machine learning"
    ],

    "Artificial Intelligence": [
        "artificial intelligence",
        r"\bai\b"
    ],

    "Communication": [
        "communication"
    ],

    "Problem Solving": [
        "problem solving",
        "problem-solving"
    ],

    "SQL": [
        r"\bsql\b"
    ],

    "Deep Learning": [
        "deep learning"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics"
    ]
}


def detect_skills(text):

    t = normalize(text)

    found = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            try:

                matched = (
                    re.search(
                        alias,
                        t,
                        flags=re.I
                    )
                    is not None
                )

            except re.error:

                matched = (
                    alias.lower()
                    in t
                )

            if matched:

                found.append(skill)

                break

    return sorted(
        found
    )


# =========================================================
# OBJECTIVE EXTRACTION
# =========================================================

def extract_objective(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    markers = [
        "seeking an entry-level",
        "seeking an entry level",
        "seeking a position",
        "looking for an opportunity",
        "career objective",
        "objective:"
    ]

    for index, line in enumerate(lines):

        lower = line.lower()

        if any(
            marker in lower
            for marker in markers
        ):

            selected = [line]

            if index + 1 < len(lines):

                next_line = lines[index + 1]

                if len(next_line) > 20:
                    selected.append(next_line)

            return " ".join(
                selected
            )

    return ""


# =========================================================
# CAREER TARGET DETECTION
# ONLY OBJECTIVE IS USED
# =========================================================

def detect_target_careers(text):

    objective = normalize(
        extract_objective(text)
    )

    careers = []

    if any(
        term in objective
        for term in [
            "software developer",
            "software engineer"
        ]
    ):
        careers.append(
            "Software Developer"
        )

    if any(
        term in objective
        for term in [
            "ai/ml",
            "ai ml",
            "ai engineer",
            "artificial intelligence",
            "machine learning"
        ]
    ):
        careers.append(
            "AI Engineer"
        )

    if "data scientist" in objective:
        careers.append(
            "Data Scientist"
        )

    if "web developer" in objective:
        careers.append(
            "Web Developer"
        )

    if "cybersecurity" in objective:
        careers.append(
            "Cybersecurity Analyst"
        )

    if "cloud engineer" in objective:
        careers.append(
            "Cloud Engineer"
        )

    return careers


# =========================================================
# RESUME READINESS SCORE
# =========================================================

def calculate_readiness(
    sections,
    skills
):

    score = 0

    if sections["Objective"]:
        score += 15

    if sections["Education"]:
        score += 20

    if sections["Skills"]:
        score += 20

    if sections["Projects"]:
        score += 20

    if sections["Experience"]:
        score += 15

    if sections["Certifications"]:
        score += 10

    # Skill bonus only for 10+ genuinely detected skills
    if len(skills) >= 10:
        score += 5

    # Do not allow a resume without experience
    # to receive an artificially high readiness score.
    if not sections["Experience"]:
        score = min(score, 85)

    return min(
        score,
        100
    )


# =========================================================
# IMPROVEMENTS
# =========================================================

def generate_improvements(
    sections,
    skills,
    careers
):

    improvements = []

    if not sections["Experience"]:

        improvements.append(
            (
                "Experience",
                "No work experience or internship section "
                "was detected. If you have an internship, training "
                "or relevant experience, add the organization, role "
                "and dates."
            )
        )

    if "Software Developer" in careers:

        missing = []

        for skill in [
            "Data Structures",
            "SQL",
            "JavaScript"
        ]:

            if skill not in skills:
                missing.append(skill)

        if missing:

            improvements.append(
                (
                    "Software Developer Skills",
                    "Consider strengthening: "
                    + ", ".join(missing)
                    + "."
                )
            )

    if "AI Engineer" in careers:

        missing = []

        for skill in [
            "Deep Learning",
            "Data Structures",
            "SQL"
        ]:

            if skill not in skills:
                missing.append(skill)

        if missing:

            improvements.append(
                (
                    "AI Engineer Skills",
                    "Consider strengthening: "
                    + ", ".join(missing)
                    + "."
                )
            )

    if not sections["Projects"]:

        improvements.append(
            (
                "Projects",
                "Add 2–3 relevant projects with the problem, "
                "technologies used, your contribution and result."
            )
        )

    else:

        improvements.append(
            (
                "Project Descriptions",
                "For every project, clearly mention the problem, "
                "technology used, your contribution and result."
            )
        )

    if not sections["Certifications"]:

        improvements.append(
            (
                "Certifications",
                "Add relevant certifications or completed courses "
                "if you have them."
            )
        )

    improvements.append(
        (
            "ATS Keywords",
            "Use job-relevant keywords naturally and keep them "
            "consistent with the skills you actually know."
        )
    )

    improvements.append(
        (
            "Formatting",
            "Keep headings, dates, bullet points, spacing and "
            "technology names consistent."
        )
    )

    improvements.append(
        (
            "Proofreading",
            "Check spelling, grammar and capitalization before "
            "submitting the resume."
        )
    )

    return improvements


# =========================================================
# OBJECTIVE SUGGESTION
# =========================================================

def objective_suggestion(careers):

    if (
        "Software Developer" in careers
        and "AI Engineer" in careers
    ):

        return (
            "Final-year Computer Science Engineering student "
            "with skills in Python, Java, C++ and machine learning, "
            "seeking an entry-level Software Developer or AI Engineer "
            "role to apply programming, problem-solving and analytical "
            "skills while continuing professional growth."
        )

    if "AI Engineer" in careers:

        return (
            "Final-year Computer Science Engineering student with "
            "skills in Python, Java and machine learning, seeking an "
            "entry-level AI Engineer role to apply technical and "
            "problem-solving skills while developing expertise in "
            "artificial intelligence."
        )

    if "Software Developer" in careers:

        return (
            "Final-year Computer Science Engineering student with "
            "skills in Python, Java and C++, seeking an entry-level "
            "Software Developer role to apply programming and "
            "problem-solving skills."
        )

    return (
        "Final-year Computer Science Engineering student seeking "
        "an entry-level technology role to apply programming, "
        "analytical and problem-solving skills."
    )


# =========================================================
# USER INTERFACE
# =========================================================

st.title(
    "✨ Resume Improvement"
)

st.caption(
    "CareerPath AI • Improve your resume using detected content and career targets"
)

uploaded = st.file_uploader(
    "Upload your resume",
    type=[
        "pdf",
        "docx",
        "txt"
    ]
)

if not uploaded:

    st.info(
        "Upload the same resume used in Resume Analyzer."
    )

    st.stop()


try:

    resume_text = extract_text(
        uploaded
    )

except Exception as error:

    st.error(
        f"Unable to read resume: {error}"
    )

    st.stop()


if not resume_text.strip():

    st.error(
        "No readable text was found in the uploaded resume."
    )

    st.stop()


sections = detect_sections(
    resume_text
)

skills = detect_skills(
    resume_text
)

careers = detect_target_careers(
    resume_text
)

readiness = calculate_readiness(
    sections,
    skills
)

improvements = generate_improvements(
    sections,
    skills,
    careers
)


st.success(
    "Resume improvement analysis completed."
)


# =========================================================
# SUMMARY
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Resume Readiness",
        f"{readiness}%"
    )

with c2:

    st.metric(
        "Skills Detected",
        len(skills)
    )

with c3:

    st.metric(
        "Target Careers",
        len(careers)
    )


st.divider()


# =========================================================
# TARGET CAREERS
# =========================================================

st.subheader(
    "🎯 Detected Career Targets"
)

if careers:

    for career in careers:

        st.success(
            career
        )

else:

    st.info(
        "No specific career target was detected from the objective."
    )


# =========================================================
# RESUME STRUCTURE
# =========================================================

st.subheader(
    "📋 Resume Structure"
)

for section, detected in sections.items():

    if detected:

        st.write(
            f"✅ {section}"
        )

    else:

        st.write(
            f"⚠️ {section} — needs attention"
        )


st.divider()


# =========================================================
# SKILLS
# =========================================================

st.subheader(
    "🛠 Detected Skills"
)

if skills:

    st.write(
        ", ".join(skills)
    )

else:

    st.warning(
        "No recognized skills detected."
    )


st.divider()


# =========================================================
# IMPROVEMENTS
# =========================================================

st.subheader(
    "🚀 Recommended Improvements"
)

for title, description in improvements:

    with st.container(
        border=True
    ):

        st.markdown(
            f"### {title}"
        )

        st.write(
            description
        )


st.divider()


# =========================================================
# SUGGESTED OBJECTIVE
# =========================================================

st.subheader(
    "✍️ Suggested Career Objective"
)

st.write(
    objective_suggestion(
        careers
    )
)


st.divider()


# =========================================================
# IMPORTANT NOTE
# =========================================================

st.info(
    "Suggestions are based only on information detected from "
    "the uploaded resume. Add only skills, experience and "
    "qualifications that are genuinely true."
)


# =========================================================
# EXTRACTED TEXT
# =========================================================

with st.expander(
    "🔎 View Extracted Resume Text"
):

    st.text_area(
        "Resume text",
        resume_text,
        height=350,
        label_visibility="collapsed"
    )