import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Interview Preparation",
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

PROFILE_FILE = DATA / "profile.json"
PROGRESS_FILE = DATA / "interview_progress.json"


# ============================================================
# LOAD PROFILE
# ============================================================

def load_json(path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default


profile = load_json(PROFILE_FILE, {})

# Support different profile structures
skills = profile.get("skills", [])
projects = profile.get("projects", [])
education = profile.get("education", {})
experience = profile.get("experience", [])
certifications = profile.get("certifications", [])
domain = profile.get("domain", "")
interests = profile.get("interests", [])

if isinstance(skills, str):
    skills = [skills]

if isinstance(projects, str):
    projects = [projects]

if isinstance(certifications, str):
    certifications = [certifications]

if isinstance(interests, str):
    interests = [interests]


# ============================================================
# HELPERS
# ============================================================

def text_list(value):
    if isinstance(value, list):
        return " ".join(str(x).lower() for x in value)
    if isinstance(value, dict):
        return " ".join(str(x).lower() for x in value.values())
    return str(value).lower()


def contains_any(text, keywords):
    text = text.lower()
    return any(k.lower() in text for k in keywords)


def education_text():
    return text_list(education)


def profile_domain_text():
    return text_list(domain)


def calculate_percentage(matched, total):
    if total <= 0:
        return 0
    return round((matched / total) * 100)


# ============================================================
# CAREER-SPECIFIC EVIDENCE
# ============================================================

EVIDENCE = {

    "Software Developer": {
        "skills": [
            "python", "java", "c", "c++", "javascript",
            "html", "sql", "oops", "git", "operating system"
        ],
        "projects": [
            "software", "application", "website", "portal",
            "ecommerce", "web", "automation"
        ],
        "certifications": [
            "software", "programming", "java", "python",
            "web", "development", "computer"
        ],
        "education": [
            "computer science", "computer engineering",
            "information technology", "software"
        ],
        "domains": ["technology", "software", "it"]
    },

    "Data Analyst": {
        "skills": [
            "python", "sql", "excel", "data analysis",
            "statistics", "pandas", "power bi", "tableau"
        ],
        "projects": [
            "data", "analysis", "analytics", "dashboard",
            "report", "database"
        ],
        "certifications": [
            "data", "analytics", "statistics", "power bi",
            "tableau", "excel"
        ],
        "education": [
            "computer science", "statistics", "mathematics",
            "data", "information technology"
        ],
        "domains": ["technology", "data", "analytics", "business"]
    },

    "Data Scientist": {
        "skills": [
            "python", "sql", "machine learning",
            "statistics", "data analysis", "pandas",
            "numpy", "scikit"
        ],
        "projects": [
            "machine learning", "data", "prediction",
            "analysis", "classification", "forecast"
        ],
        "certifications": [
            "machine learning", "data science",
            "artificial intelligence", "data"
        ],
        "education": [
            "computer science", "data science",
            "statistics", "mathematics"
        ],
        "domains": ["technology", "data", "artificial intelligence"]
    },

    "AI Engineer": {
        "skills": [
            "python", "artificial intelligence",
            "machine learning", "deep learning",
            "ai", "ml", "tensorflow", "pytorch",
            "api", "fastapi"
        ],
        "projects": [
            "artificial intelligence", "ai",
            "machine learning", "deep learning",
            "voice-controlled", "ai assistance",
            "automation", "prediction"
        ],
        "certifications": [
            "artificial intelligence", "ai",
            "machine learning", "deep learning",
            "data science"
        ],
        "education": [
            "computer science", "artificial intelligence",
            "machine learning", "information technology"
        ],
        "domains": ["technology", "artificial intelligence", "ai"]
    },

    "Web Developer": {
        "skills": [
            "html", "css", "javascript",
            "frontend", "backend", "sql",
            "database", "react", "node"
        ],
        "projects": [
            "website", "web", "ecommerce",
            "portal", "frontend", "backend"
        ],
        "certifications": [
            "web", "frontend", "backend",
            "javascript", "html", "css"
        ],
        "education": [
            "computer science", "information technology",
            "computer engineering"
        ],
        "domains": ["technology", "web", "software", "it"]
    },

    "Cybersecurity Analyst": {
        "skills": [
            "cybersecurity", "network security",
            "cryptography", "linux", "networking",
            "ethical hacking", "security"
        ],
        "projects": [
            "security", "cybersecurity", "cryptography",
            "network", "secure", "authentication"
        ],
        "certifications": [
            "cybersecurity", "security",
            "ethical hacking", "network security"
        ],
        "education": [
            "computer science", "cybersecurity",
            "information technology"
        ],
        "domains": ["technology", "cybersecurity", "security"]
    },

    "Cloud Engineer": {
        "skills": [
            "aws", "azure", "cloud", "docker",
            "kubernetes", "linux", "networking",
            "devops"
        ],
        "projects": [
            "cloud", "deployment", "server",
            "devops", "aws", "azure"
        ],
        "certifications": [
            "aws", "azure", "cloud",
            "devops", "kubernetes"
        ],
        "education": [
            "computer science", "information technology",
            "cloud computing"
        ],
        "domains": ["technology", "cloud", "it", "devops"]
    },

    "Mechanical Engineer": {
        "skills": [
            "mechanical", "cad", "autocad",
            "solidworks", "thermodynamics",
            "manufacturing", "design"
        ],
        "projects": [
            "mechanical", "machine", "design",
            "manufacturing", "cad"
        ],
        "certifications": [
            "mechanical", "cad", "autocad",
            "solidworks", "manufacturing"
        ],
        "education": [
            "mechanical engineering"
        ],
        "domains": ["engineering", "mechanical"]
    },

    "Civil Engineer": {
        "skills": [
            "civil", "autocad", "structural",
            "construction", "surveying",
            "structural analysis"
        ],
        "projects": [
            "civil", "construction", "building",
            "structural", "survey"
        ],
        "certifications": [
            "civil", "autocad", "construction",
            "structural"
        ],
        "education": [
            "civil engineering"
        ],
        "domains": ["engineering", "civil", "construction"]
    },

    "Electrical Engineer": {
        "skills": [
            "electrical", "circuit", "electronics",
            "power systems", "control systems",
            "matlab", "embedded"
        ],
        "projects": [
            "electrical", "circuit", "power",
            "automation", "embedded"
        ],
        "certifications": [
            "electrical", "electronics",
            "embedded", "power"
        ],
        "education": [
            "electrical engineering"
        ],
        "domains": ["engineering", "electrical"]
    },

    "Electronics Engineer": {
        "skills": [
            "electronics", "embedded", "microcontroller",
            "arduino", "esp32", "circuit",
            "iot", "embedded systems"
        ],
        "projects": [
            "electronics", "iot", "embedded",
            "sensor", "arduino", "esp32"
        ],
        "certifications": [
            "electronics", "embedded", "iot",
            "arduino"
        ],
        "education": [
            "electronics", "electronics and communication",
            "ece"
        ],
        "domains": ["engineering", "electronics", "iot"]
    },

    "Doctor": {
        "skills": [
            "medicine", "medical", "clinical",
            "diagnosis", "patient care",
            "anatomy", "pharmacology"
        ],
        "projects": [
            "medical", "healthcare", "clinical",
            "patient", "hospital"
        ],
        "certifications": [
            "medical", "medicine", "clinical",
            "healthcare"
        ],
        "education": [
            "medicine", "mbbs", "medical"
        ],
        "domains": ["healthcare", "medicine"]
    },

    "Nurse": {
        "skills": [
            "nursing", "patient care",
            "clinical", "healthcare",
            "first aid", "medical"
        ],
        "projects": [
            "nursing", "patient", "healthcare",
            "hospital", "medical"
        ],
        "certifications": [
            "nursing", "healthcare",
            "first aid", "medical"
        ],
        "education": [
            "nursing", "bsc nursing",
            "gnm"
        ],
        "domains": ["healthcare", "nursing"]
    },

    "Pharmacist": {
        "skills": [
            "pharmacy", "pharmacology",
            "drug", "medicines", "healthcare"
        ],
        "projects": [
            "pharmacy", "medicine",
            "drug", "healthcare"
        ],
        "certifications": [
            "pharmacy", "pharmacology",
            "healthcare"
        ],
        "education": [
            "pharmacy", "pharm d",
            "b pharm"
        ],
        "domains": ["healthcare", "pharmacy"]
    },

    "Physiotherapist": {
        "skills": [
            "physiotherapy", "physical therapy",
            "rehabilitation", "exercise therapy",
            "patient care"
        ],
        "projects": [
            "physiotherapy", "rehabilitation",
            "therapy", "patient"
        ],
        "certifications": [
            "physiotherapy", "rehabilitation",
            "physical therapy"
        ],
        "education": [
            "physiotherapy", "bpt"
        ],
        "domains": ["healthcare", "physiotherapy"]
    },

    "Accountant": {
        "skills": [
            "accounting", "tally", "excel",
            "taxation", "bookkeeping",
            "financial reporting"
        ],
        "projects": [
            "accounting", "finance",
            "tax", "bookkeeping"
        ],
        "certifications": [
            "accounting", "tally", "finance",
            "taxation", "ca"
        ],
        "education": [
            "commerce", "accounting",
            "finance"
        ],
        "domains": ["finance", "accounting", "business"]
    },

    "Financial Analyst": {
        "skills": [
            "finance", "financial analysis",
            "excel", "accounting",
            "valuation", "statistics"
        ],
        "projects": [
            "finance", "financial",
            "investment", "analysis"
        ],
        "certifications": [
            "finance", "financial analysis",
            "investment", "accounting"
        ],
        "education": [
            "finance", "commerce",
            "economics", "accounting"
        ],
        "domains": ["finance", "business"]
    },

    "Investment Analyst": {
        "skills": [
            "investment", "finance",
            "financial analysis", "valuation",
            "stocks", "portfolio"
        ],
        "projects": [
            "investment", "stock",
            "portfolio", "financial analysis"
        ],
        "certifications": [
            "investment", "finance",
            "cfa", "financial analysis"
        ],
        "education": [
            "finance", "economics",
            "commerce"
        ],
        "domains": ["finance", "investment", "business"]
    },

    "Marketing Manager": {
        "skills": [
            "marketing", "digital marketing",
            "seo", "social media",
            "communication", "branding",
            "market research"
        ],
        "projects": [
            "marketing", "campaign",
            "branding", "social media",
            "market research"
        ],
        "certifications": [
            "marketing", "digital marketing",
            "seo", "social media"
        ],
        "education": [
            "marketing", "business",
            "management", "commerce"
        ],
        "domains": ["marketing", "business"]
    },

    "Business Analyst": {
        "skills": [
            "business analysis", "sql",
            "data analysis", "excel",
            "communication", "requirements",
            "business"
        ],
        "projects": [
            "business", "analysis",
            "requirements", "dashboard",
            "data"
        ],
        "certifications": [
            "business analysis", "data analysis",
            "business", "analytics"
        ],
        "education": [
            "business", "management",
            "computer science", "commerce"
        ],
        "domains": ["business", "technology", "analytics"]
    },

    "Human Resources Manager": {
        "skills": [
            "human resources", "hr",
            "recruitment", "communication",
            "talent management",
            "employee relations"
        ],
        "projects": [
            "hr", "recruitment",
            "employee", "human resources"
        ],
        "certifications": [
            "human resources", "hr",
            "recruitment"
        ],
        "education": [
            "human resources", "management",
            "business", "commerce"
        ],
        "domains": ["human resources", "business", "management"]
    },

    "Entrepreneur": {
        "skills": [
            "entrepreneurship", "business",
            "leadership", "communication",
            "marketing", "finance",
            "problem solving"
        ],
        "projects": [
            "business", "startup",
            "entrepreneur", "product",
            "ecommerce"
        ],
        "certifications": [
            "entrepreneurship", "business",
            "startup", "management"
        ],
        "education": [
            "business", "management",
            "commerce"
        ],
        "domains": ["business", "entrepreneurship"]
    },

    "Teacher": {
        "skills": [
            "teaching", "communication",
            "presentation", "education",
            "training", "subject knowledge"
        ],
        "projects": [
            "teaching", "education",
            "training", "learning"
        ],
        "certifications": [
            "teaching", "education",
            "training", "ctet"
        ],
        "education": [
            "education", "teaching",
            "b ed"
        ],
        "domains": ["education", "teaching"]
    },

    "Professor": {
        "skills": [
            "teaching", "research",
            "communication", "presentation",
            "academic", "subject knowledge"
        ],
        "projects": [
            "research", "academic",
            "teaching", "education"
        ],
        "certifications": [
            "teaching", "research",
            "education", "academic"
        ],
        "education": [
            "master", "phd",
            "computer science", "engineering"
        ],
        "domains": ["education", "research", "academic"]
    },

    "Lawyer": {
        "skills": [
            "law", "legal research",
            "communication", "negotiation",
            "advocacy", "contract"
        ],
        "projects": [
            "legal", "law",
            "contract", "research"
        ],
        "certifications": [
            "law", "legal"
        ],
        "education": [
            "law", "llb", "llm"
        ],
        "domains": ["law", "legal"]
    },

    "Journalist": {
        "skills": [
            "journalism", "writing",
            "communication", "research",
            "reporting", "interviewing"
        ],
        "projects": [
            "journalism", "article",
            "news", "reporting",
            "content"
        ],
        "certifications": [
            "journalism", "media",
            "writing", "communication"
        ],
        "education": [
            "journalism", "mass communication",
            "media"
        ],
        "domains": ["journalism", "media"]
    },

    "Content Creator": {
        "skills": [
            "content creation", "writing",
            "video editing", "social media",
            "communication", "photography",
            "marketing"
        ],
        "projects": [
            "content", "youtube",
            "video", "social media",
            "blog"
        ],
        "certifications": [
            "content", "digital marketing",
            "social media", "video"
        ],
        "education": [
            "media", "communication",
            "marketing"
        ],
        "domains": ["media", "content", "marketing"]
    },

    "Graphic Designer": {
        "skills": [
            "graphic design", "photoshop",
            "illustrator", "canva",
            "design", "branding"
        ],
        "projects": [
            "graphic", "design",
            "branding", "poster"
        ],
        "certifications": [
            "graphic design", "design",
            "photoshop", "illustrator"
        ],
        "education": [
            "design", "graphic design",
            "fine arts"
        ],
        "domains": ["design", "creative"]
    },

    "UI UX Designer": {
        "skills": [
            "ui", "ux", "ui ux",
            "figma", "wireframe",
            "prototyping", "design"
        ],
        "projects": [
            "ui", "ux", "design",
            "prototype", "figma",
            "website"
        ],
        "certifications": [
            "ui", "ux", "design",
            "figma"
        ],
        "education": [
            "design", "computer science",
            "visual design"
        ],
        "domains": ["design", "technology", "ui ux"]
    },

    "Architect": {
        "skills": [
            "architecture", "autocad",
            "revit", "3d modeling",
            "design", "building"
        ],
        "projects": [
            "architecture", "building",
            "design", "construction"
        ],
        "certifications": [
            "architecture", "autocad",
            "revit", "design"
        ],
        "education": [
            "architecture", "b arch"
        ],
        "domains": ["architecture", "design"]
    },

    "Agricultural Scientist": {
        "skills": [
            "agriculture", "agronomy",
            "soil science", "crop science",
            "biology", "research"
        ],
        "projects": [
            "agriculture", "crop",
            "soil", "farming",
            "agricultural"
        ],
        "certifications": [
            "agriculture", "agronomy",
            "crop science"
        ],
        "education": [
            "agriculture", "agricultural science"
        ],
        "domains": ["agriculture", "science"]
    },

    "Environmental Scientist": {
        "skills": [
            "environmental science",
            "environment", "ecology",
            "biology", "research",
            "sustainability"
        ],
        "projects": [
            "environment", "ecology",
            "sustainability", "pollution",
            "conservation"
        ],
        "certifications": [
            "environmental", "sustainability",
            "ecology"
        ],
        "education": [
            "environmental science",
            "biology", "environment"
        ],
        "domains": ["environment", "science"]
    },

    "Hotel Manager": {
        "skills": [
            "hospitality", "hotel management",
            "customer service", "communication",
            "management", "operations"
        ],
        "projects": [
            "hotel", "hospitality",
            "event", "restaurant",
            "customer service"
        ],
        "certifications": [
            "hospitality", "hotel management",
            "management"
        ],
        "education": [
            "hotel management",
            "hospitality"
        ],
        "domains": ["hospitality", "management"]
    },

    "Chef": {
        "skills": [
            "cooking", "culinary",
            "food preparation", "kitchen",
            "food safety", "hospitality"
        ],
        "projects": [
            "cooking", "culinary",
            "food", "kitchen",
            "restaurant"
        ],
        "certifications": [
            "culinary", "cooking",
            "food safety", "hospitality"
        ],
        "education": [
            "culinary", "hotel management",
            "hospitality"
        ],
        "domains": ["hospitality", "culinary"]
    },

    "Fitness Trainer": {
        "skills": [
            "fitness", "training",
            "exercise", "nutrition",
            "personal training",
            "sports"
        ],
        "projects": [
            "fitness", "training",
            "exercise", "sports"
        ],
        "certifications": [
            "fitness", "personal training",
            "nutrition", "sports"
        ],
        "education": [
            "fitness", "sports science",
            "physical education"
        ],
        "domains": ["fitness", "sports", "health"]
    },

    "Sports Coach": {
        "skills": [
            "coaching", "sports",
            "training", "fitness",
            "leadership", "communication"
        ],
        "projects": [
            "sports", "coaching",
            "training", "team"
        ],
        "certifications": [
            "sports", "coaching",
            "fitness", "training"
        ],
        "education": [
            "sports science",
            "physical education"
        ],
        "domains": ["sports", "fitness", "education"]
    }
}


# ============================================================
# CAREER SELECTOR
# ============================================================

careers = list(EVIDENCE.keys())

if "interview_career" not in st.session_state:
    st.session_state.interview_career = careers[0]

current_index = careers.index(st.session_state.interview_career)

career = st.selectbox(
    "Select Career",
    careers,
    index=current_index,
    key="interview_career"
)

data = EVIDENCE[career]


# ============================================================
# ACCURATE INTERVIEW READINESS
# ============================================================

def skill_score():
    profile_skills = text_list(skills)

    matched = 0

    for required in data["skills"]:
        if contains_any(profile_skills, [required]):
            matched += 1

    return calculate_percentage(
        matched,
        len(data["skills"])
    )


def project_score():
    profile_projects = [
        str(x).lower()
        for x in projects
    ]

    matched_projects = 0

    for project in profile_projects:
        if contains_any(project, data["projects"]):
            matched_projects += 1

    # Practical evidence is stronger when there are multiple
    # genuinely relevant projects.
    if matched_projects == 0:
        return 0
    if matched_projects == 1:
        return 60
    if matched_projects == 2:
        return 80
    return 100


def education_score():
    text = education_text()

    if not text.strip():
        return 0

    return 100 if contains_any(
        text,
        data["education"]
    ) else 0


def domain_score():
    text = profile_domain_text()

    if not text.strip():
        return 0

    return 100 if contains_any(
        text,
        data["domains"]
    ) else 0


def certification_score():
    text = text_list(certifications)

    if not text.strip():
        return 0

    matched = 0

    for cert in data["certifications"]:
        if contains_any(text, [cert]):
            matched += 1

    # Certifications are evidence, but only 5% of readiness.
    if matched == 0:
        return 0
    if matched == 1:
        return 60
    return 100


skills_percent = skill_score()
projects_percent = project_score()
education_percent = education_score()
domain_percent = domain_score()
certification_percent = certification_score()

# IMPORTANT:
# Confidence is deliberately NOT included.
#
# Readiness represents evidence-based interview preparation.
# Confidence represents personal self-assessment.

readiness = round(
    (skills_percent * 0.40) +
    (projects_percent * 0.30) +
    (education_percent * 0.15) +
    (domain_percent * 0.10) +
    (certification_percent * 0.05)
)

readiness = max(0, min(100, readiness))


# ============================================================
# SAVE CONFIDENCE SEPARATELY
# ============================================================

saved = load_json(
    PROGRESS_FILE,
    {
        "confidence": {},
        "readiness": {}
    }
)

if "confidence" not in saved:
    saved["confidence"] = {}

if "readiness" not in saved:
    saved["readiness"] = {}

old_confidence = saved["confidence"].get(career, 50)

# Handle old dictionary format safely
if isinstance(old_confidence, dict):
    old_confidence = old_confidence.get("value", 50)

try:
    old_confidence = int(old_confidence)
except Exception:
    old_confidence = 50

old_confidence = max(0, min(100, old_confidence))

confidence = st.slider(
    "How prepared do you personally feel?",
    0,
    100,
    old_confidence,
    5,
    key=f"confidence_{career}"
)

saved["confidence"][career] = confidence

# Store the calculated readiness separately for each career.
saved["readiness"][career] = readiness

with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
    json.dump(saved, f, indent=2)


# ============================================================
# HEADER
# ============================================================

st.title("🎯 Interview Preparation")

st.caption(
    f"Career-specific interview preparation for **{career}**"
)


# ============================================================
# READINESS
# ============================================================

st.subheader("📊 Interview Readiness")

st.progress(readiness / 100)

st.metric(
    "Interview Readiness",
    f"{readiness}%"
)

st.caption(
    "Readiness is calculated from your career-specific skills, "
    "relevant projects, education, domain alignment and certifications. "
    "Your confidence does not change this score."
)


# ============================================================
# READINESS BREAKDOWN
# ============================================================

with st.expander("🔎 Why is my readiness this score?"):

    st.write(
        f"**Career:** {career}"
    )

    st.write(
        f"**Skills:** {skills_percent}% × 40%"
    )

    st.write(
        f"**Relevant Projects:** {projects_percent}% × 30%"
    )

    st.write(
        f"**Education:** {education_percent}% × 15%"
    )

    st.write(
        f"**Domain:** {domain_percent}% × 10%"
    )

    st.write(
        f"**Certifications:** {certification_percent}% × 5%"
    )

    st.divider()

    st.write(
        f"**Final Interview Readiness: {readiness}%**"
    )


# ============================================================
# CONFIDENCE
# ============================================================

st.subheader("💭 Your Personal Confidence")

st.progress(confidence / 100)

st.metric(
    "Self-Confidence",
    f"{confidence}%"
)

st.caption(
    "This is your personal self-assessment. "
    "Changing it will NOT change Interview Readiness."
)


# ============================================================
# CAREER-SPECIFIC GUIDE
# ============================================================

GUIDE = {

"Software Developer": {
"prepare": [
"Programming fundamentals",
"OOP and data structures",
"SQL and databases",
"Git and software development workflow",
"Explain your projects clearly"
],
"show": [
"Clean programming logic",
"Problem-solving ability",
"Understanding of your projects",
"Debugging approach"
],
"focus": "Coding ability, problem solving, software fundamentals and project understanding.",
"questions": [
"Explain one project you developed.",
"How do you debug a program?",
"What is OOP?",
"How do you handle database operations?"
],
"behavior": "Think aloud while solving technical problems and explain your decisions clearly.",
"mistakes": "Do not claim knowledge of technologies you cannot explain.",
"day": "Carry your resume, review projects, revise fundamentals and arrive prepared.",
"after": "Note difficult questions and revise the concepts you could not answer."
},

"Data Analyst": {
"prepare": [
"SQL",
"Excel",
"Data cleaning",
"Statistics",
"Data visualization"
],
"show": [
"Analytical thinking",
"Ability to interpret data",
"Clear explanation of findings",
"Practical project evidence"
],
"focus": "Data interpretation, SQL, analytical reasoning and business understanding.",
"questions": [
"How would you clean a dataset?",
"What SQL queries do you commonly use?",
"How do you identify trends in data?",
"Explain one data project."
],
"behavior": "Explain the reasoning behind your analysis rather than only giving the final result.",
"mistakes": "Avoid presenting charts without explaining what they mean.",
"day": "Review SQL, statistics, dashboards and your projects.",
"after": "Record the analytical questions you found difficult and practise them."
},

"Data Scientist": {
"prepare": [
"Python",
"Statistics",
"Machine learning",
"Data preprocessing",
"Model evaluation"
],
"show": [
"Understanding of ML concepts",
"Data analysis ability",
"Model reasoning",
"Project understanding"
],
"focus": "Statistics, machine learning, data preparation and model reasoning.",
"questions": [
"How do you handle missing data?",
"What is overfitting?",
"How do you evaluate a model?",
"Explain your ML project."
],
"behavior": "Explain why you selected a particular model or approach.",
"mistakes": "Do not describe ML algorithms only by memorized definitions.",
"day": "Revise statistics, ML fundamentals and project decisions.",
"after": "Review questions involving model selection and evaluation."
},

"AI Engineer": {
"prepare": [
"Python",
"Artificial intelligence",
"Machine learning",
"Deep learning",
"AI projects",
"APIs and deployment"
],
"show": [
"Understanding of AI concepts",
"Ability to explain AI projects",
"Practical implementation",
"Problem-solving"
],
"focus": "AI fundamentals, implementation decisions, projects and practical problem solving.",
"questions": [
"What is the difference between AI and machine learning?",
"Explain one AI project.",
"How would you deploy an AI model?",
"What is an API?"
],
"behavior": "Be precise about what you personally implemented.",
"mistakes": "Do not claim an AI model was built if you only used an existing tool.",
"day": "Revise Python, ML basics, APIs and your AI-related projects.",
"after": "Write down every technical question you could not answer."
},

"Web Developer": {
"prepare": [
"HTML",
"CSS",
"JavaScript",
"Frontend concepts",
"Backend concepts",
"Databases"
],
"show": [
"Website development ability",
"Frontend understanding",
"Backend understanding",
"Project implementation"
],
"focus": "Web fundamentals, frontend/backend integration and practical projects.",
"questions": [
"How does a web application work?",
"What is the difference between frontend and backend?",
"How do you connect a database?",
"Explain your website project."
],
"behavior": "Explain the complete flow from user interface to backend and database.",
"mistakes": "Do not memorize web terms without understanding how they connect.",
"day": "Review HTML, CSS, JavaScript, backend and database basics.",
"after": "Improve any weak area revealed during the interview."
},

"Cybersecurity Analyst": {
"prepare": [
"Networking",
"Cybersecurity fundamentals",
"Authentication",
"Cryptography",
"Security threats"
],
"show": [
"Security awareness",
"Analytical thinking",
"Understanding of threats",
"Security project knowledge"
],
"focus": "Threat identification, security fundamentals and analytical thinking.",
"questions": [
"What is phishing?",
"What is encryption?",
"How can an application be secured?",
"Explain a security project."
],
"behavior": "Think carefully before suggesting security controls.",
"mistakes": "Never suggest insecure practices casually.",
"day": "Revise networking, security principles and common threats.",
"after": "Review unfamiliar security terminology."
},

"Cloud Engineer": {
"prepare": [
"Cloud fundamentals",
"AWS/Azure concepts",
"Networking",
"Linux",
"Deployment"
],
"show": [
"Understanding of cloud architecture",
"Deployment knowledge",
"Troubleshooting ability",
"Infrastructure understanding"
],
"focus": "Cloud architecture, deployment, networking and infrastructure.",
"questions": [
"What is cloud computing?",
"What is the difference between IaaS and PaaS?",
"How would you deploy an application?",
"What is a virtual machine?"
],
"behavior": "Explain infrastructure decisions logically.",
"mistakes": "Do not claim cloud experience you have not actually used.",
"day": "Review cloud services, networking and deployment concepts.",
"after": "Practise architecture-based questions."
},

"Teacher": {
"prepare": [
"Subject knowledge",
"Teaching methods",
"Communication",
"Classroom management",
"Lesson planning"
],
"show": [
"Clear communication",
"Ability to explain concepts",
"Patience",
"Teaching approach"
],
"focus": "Subject knowledge, communication and ability to explain concepts clearly.",
"questions": [
"How would you explain a difficult topic?",
"How would you handle a struggling student?",
"How do you plan a lesson?",
"How do you keep students engaged?"
],
"behavior": "Speak clearly and explain ideas as if you are teaching them.",
"mistakes": "Avoid giving overly complicated explanations.",
"day": "Revise your subject and practise explaining concepts simply.",
"after": "Identify explanations that could have been clearer."
},

"Professor": {
"prepare": [
"Subject expertise",
"Research",
"Teaching",
"Presentation",
"Academic communication"
],
"show": [
"Depth of knowledge",
"Research ability",
"Teaching ability",
"Academic communication"
],
"focus": "Subject expertise, teaching ability and research orientation.",
"questions": [
"Explain your research interests.",
"How would you teach a difficult topic?",
"How do you encourage student participation?",
"How do you evaluate student understanding?"
],
"behavior": "Demonstrate depth without making explanations unnecessarily complicated.",
"mistakes": "Avoid presenting unsupported academic claims.",
"day": "Review your subject, research and teaching approach.",
"after": "Review subject-specific questions that challenged you."
},

"Doctor": {
"prepare": [
"Medical fundamentals",
"Clinical reasoning",
"Patient communication",
"Ethics",
"Relevant medical knowledge"
],
"show": [
"Clinical reasoning",
"Patient-centred thinking",
"Professional communication",
"Medical knowledge"
],
"focus": "Clinical reasoning, professional conduct and patient communication.",
"questions": [
"How would you approach a patient case?",
"How do you communicate with patients?",
"What is informed consent?",
"How do you handle uncertainty?"
],
"behavior": "Communicate carefully, professionally and ethically.",
"mistakes": "Never guess when patient safety is involved.",
"day": "Review relevant medical concepts and professional ethics.",
"after": "Review clinical reasoning questions carefully."
},

"Nurse": {
"prepare": [
"Patient care",
"Clinical fundamentals",
"Communication",
"Safety",
"Healthcare ethics"
],
"show": [
"Patient-centred care",
"Communication",
"Safety awareness",
"Clinical knowledge"
],
"focus": "Patient care, safety, communication and clinical fundamentals.",
"questions": [
"How would you communicate with a patient?",
"How do you maintain patient safety?",
"How would you respond to an emergency?",
"What is professional nursing practice?"
],
"behavior": "Show empathy while maintaining professional boundaries.",
"mistakes": "Do not ignore safety procedures.",
"day": "Review clinical basics, safety and communication.",
"after": "Review scenarios that required clinical judgement."
},

"Pharmacist": {
"prepare": [
"Pharmacology",
"Medicines",
"Drug safety",
"Patient counselling",
"Healthcare fundamentals"
],
"show": [
"Medication knowledge",
"Safety awareness",
"Patient communication",
"Professional responsibility"
],
"focus": "Medication knowledge, safety and responsible patient communication.",
"questions": [
"How do you ensure medication safety?",
"What is patient counselling?",
"How do you handle a medication-related concern?",
"Why is dosage accuracy important?"
],
"behavior": "Be precise and safety-focused.",
"mistakes": "Never guess medication-related information.",
"day": "Review pharmacology, safety and patient communication.",
"after": "Review medication-safety questions."
},

"Physiotherapist": {
"prepare": [
"Human anatomy",
"Exercise therapy",
"Rehabilitation",
"Patient assessment",
"Communication"
],
"show": [
"Clinical reasoning",
"Patient communication",
"Rehabilitation knowledge",
"Practical understanding"
],
"focus": "Assessment, rehabilitation planning and patient communication.",
"questions": [
"How do you assess a patient?",
"What is rehabilitation?",
"How do you track patient progress?",
"How do you communicate treatment plans?"
],
"behavior": "Explain treatment reasoning clearly and safely.",
"mistakes": "Avoid unsupported treatment claims.",
"day": "Review anatomy, assessment and rehabilitation concepts.",
"after": "Review scenario-based questions."
},

"Accountant": {
"prepare": [
"Accounting fundamentals",
"Financial statements",
"Excel",
"Tax basics",
"Bookkeeping"
],
"show": [
"Accuracy",
"Numerical reasoning",
"Financial knowledge",
"Attention to detail"
],
"focus": "Accounting accuracy, financial reporting and attention to detail.",
"questions": [
"What are the main financial statements?",
"What is bookkeeping?",
"How do you check accounting accuracy?",
"How do you use Excel in accounting?"
],
"behavior": "Be precise when discussing numbers and financial records.",
"mistakes": "Avoid guessing financial figures.",
"day": "Revise accounting principles and practical examples.",
"after": "Review accounting concepts that caused difficulty."
},

"Financial Analyst": {
"prepare": [
"Financial analysis",
"Excel",
"Accounting",
"Valuation",
"Business understanding"
],
"show": [
"Numerical reasoning",
"Financial interpretation",
"Analytical thinking",
"Business awareness"
],
"focus": "Financial reasoning, analysis and business decision-making.",
"questions": [
"How would you analyse a company's performance?",
"What financial ratios are useful?",
"How do you use Excel for analysis?",
"How would you evaluate an investment?"
],
"behavior": "Support conclusions with evidence and numbers.",
"mistakes": "Avoid unsupported financial recommendations.",
"day": "Review financial statements, ratios and valuation basics.",
"after": "Practise explaining financial conclusions."
},

"Investment Analyst": {
"prepare": [
"Financial markets",
"Investment analysis",
"Valuation",
"Risk",
"Portfolio concepts"
],
"show": [
"Analytical reasoning",
"Market understanding",
"Risk awareness",
"Investment knowledge"
],
"focus": "Investment reasoning, valuation, market awareness and risk analysis.",
"questions": [
"How would you evaluate an investment?",
"What is diversification?",
"What is risk?",
"How do you analyse a company?"
],
"behavior": "Clearly distinguish facts, assumptions and opinions.",
"mistakes": "Do not present uncertain market outcomes as guaranteed.",
"day": "Review markets, valuation and risk concepts.",
"after": "Review market-analysis questions."
},

"Marketing Manager": {
"prepare": [
"Marketing fundamentals",
"Digital marketing",
"Customer understanding",
"Branding",
"Market research"
],
"show": [
"Communication",
"Creative thinking",
"Customer understanding",
"Marketing strategy"
],
"focus": "Customer understanding, communication, strategy and market awareness.",
"questions": [
"How would you launch a product?",
"How do you identify a target audience?",
"What makes a marketing campaign effective?",
"How would you measure campaign performance?"
],
"behavior": "Connect ideas to customers and measurable outcomes.",
"mistakes": "Avoid describing marketing only as advertising.",
"day": "Review marketing fundamentals and campaign examples.",
"after": "Analyse which strategic questions were difficult."
},

"Business Analyst": {
"prepare": [
"Requirements analysis",
"SQL",
"Data analysis",
"Communication",
"Business processes"
],
"show": [
"Analytical thinking",
"Requirement gathering",
"Communication",
"Business understanding"
],
"focus": "Requirements, analysis, communication and business problem solving.",
"questions": [
"How do you gather requirements?",
"How do you handle conflicting requirements?",
"How can data support business decisions?",
"Explain a business problem you solved."
],
"behavior": "Clarify the problem before proposing a solution.",
"mistakes": "Do not jump to technical solutions without understanding the business need.",
"day": "Review requirements, analysis and communication techniques.",
"after": "Practise scenario-based business questions."
},

"Human Resources Manager": {
"prepare": [
"Recruitment",
"Communication",
"Employee relations",
"Talent management",
"HR fundamentals"
],
"show": [
"Communication",
"People skills",
"Professional judgement",
"Organisational understanding"
],
"focus": "People management, communication, recruitment and professional judgement.",
"questions": [
"How would you handle workplace conflict?",
"How would you evaluate a candidate?",
"How do you maintain confidentiality?",
"How would you improve employee engagement?"
],
"behavior": "Listen carefully and respond neutrally.",
"mistakes": "Avoid making personal assumptions about employees.",
"day": "Review recruitment, HR processes and workplace scenarios.",
"after": "Review scenario questions and your reasoning."
},

"Entrepreneur": {
"prepare": [
"Business fundamentals",
"Problem solving",
"Customer understanding",
"Finance",
"Leadership"
],
"show": [
"Initiative",
"Problem-solving",
"Business thinking",
"Communication"
],
"focus": "Problem identification, customer value, business thinking and execution.",
"questions": [
"What problem would you solve?",
"Who is your customer?",
"How would you validate an idea?",
"How would you generate revenue?"
],
"behavior": "Explain assumptions and how you would test them.",
"mistakes": "Avoid presenting an idea without explaining its customer value.",
"day": "Review your ideas, customers, competition and business model.",
"after": "Write down assumptions that interviewers challenged."
},

"Lawyer": {
"prepare": [
"Legal fundamentals",
"Legal research",
"Communication",
"Negotiation",
"Case analysis"
],
"show": [
"Reasoning",
"Legal knowledge",
"Communication",
"Attention to detail"
],
"focus": "Legal reasoning, research, communication and professional judgement.",
"questions": [
"How would you analyse a legal issue?",
"How do you conduct legal research?",
"How would you negotiate?",
"How do you handle conflicting evidence?"
],
"behavior": "Separate facts, assumptions and legal reasoning.",
"mistakes": "Avoid stating uncertain legal conclusions as facts.",
"day": "Review relevant legal principles and cases.",
"after": "Review legal reasoning questions."
},

"Journalist": {
"prepare": [
"Writing",
"Research",
"Reporting",
"Communication",
"Interviewing"
],
"show": [
"Research ability",
"Clear writing",
"Questioning ability",
"Fact checking"
],
"focus": "Research, factual accuracy, communication and reporting.",
"questions": [
"How do you verify information?",
"How would you interview a difficult source?",
"How do you structure a news story?",
"How do you avoid bias?"
],
"behavior": "Distinguish verified information from assumptions.",
"mistakes": "Never present unverified information as fact.",
"day": "Review writing, reporting and fact-checking principles.",
"after": "Review questions involving source verification."
},

"Content Creator": {
"prepare": [
"Content strategy",
"Writing",
"Video or media skills",
"Social media",
"Audience understanding"
],
"show": [
"Creativity",
"Communication",
"Audience awareness",
"Content planning"
],
"focus": "Audience understanding, content strategy, creativity and communication.",
"questions": [
"How would you grow an audience?",
"How do you choose content topics?",
"How do you measure content performance?",
"Explain a piece of content you created."
],
"behavior": "Explain both the creative idea and the audience purpose.",
"mistakes": "Avoid focusing only on views without explaining value.",
"day": "Review your content examples and audience strategy.",
"after": "Analyse which content-strategy questions were difficult."
},

"Graphic Designer": {
"prepare": [
"Design principles",
"Typography",
"Colour theory",
"Design tools",
"Portfolio"
],
"show": [
"Creative thinking",
"Visual communication",
"Design reasoning",
"Portfolio quality"
],
"focus": "Visual communication, design decisions and portfolio evidence.",
"questions": [
"How do you approach a design brief?",
"Why did you choose a particular design?",
"How do you respond to feedback?",
"Explain one portfolio project."
],
"behavior": "Explain the reasoning behind visual decisions.",
"mistakes": "Do not show designs without explaining the problem they solve.",
"day": "Review your portfolio and design principles.",
"after": "Improve projects based on interview feedback."
},

"UI UX Designer": {
"prepare": [
"User research",
"Wireframing",
"Prototyping",
"UI principles",
"UX principles"
],
"show": [
"User-centred thinking",
"Design reasoning",
"Problem solving",
"Portfolio evidence"
],
"focus": "User needs, design process, usability and problem solving.",
"questions": [
"How do you conduct user research?",
"What makes a good user interface?",
"How do you test a design?",
"Explain one design project."
],
"behavior": "Start with the user problem before discussing visual design.",
"mistakes": "Avoid treating UI as only visual decoration.",
"day": "Review your portfolio and UX process.",
"after": "Review design decisions questioned by interviewers."
},

"Architect": {
"prepare": [
"Design principles",
"Architecture fundamentals",
"CAD",
"Building concepts",
"Portfolio"
],
"show": [
"Design reasoning",
"Technical understanding",
"Creativity",
"Portfolio evidence"
],
"focus": "Design thinking, technical knowledge and portfolio quality.",
"questions": [
"How do you approach a design brief?",
"How do you balance aesthetics and function?",
"What tools do you use?",
"Explain a design project."
],
"behavior": "Explain both design intent and practical constraints.",
"mistakes": "Avoid presenting concepts without considering functionality.",
"day": "Review your portfolio and design fundamentals.",
"after": "Improve weak areas identified during discussion."
},

"Agricultural Scientist": {
"prepare": [
"Agricultural science",
"Research",
"Crop science",
"Soil science",
"Data interpretation"
],
"show": [
"Scientific reasoning",
"Research ability",
"Domain knowledge",
"Problem solving"
],
"focus": "Scientific reasoning, agricultural knowledge and research.",
"questions": [
"How would you study crop productivity?",
"How can technology support agriculture?",
"How do you design an experiment?",
"Explain an agricultural research problem."
],
"behavior": "Support conclusions with evidence.",
"mistakes": "Avoid making scientific claims without evidence.",
"day": "Review agricultural science and research methods.",
"after": "Review scientific reasoning questions."
},

"Environmental Scientist": {
"prepare": [
"Environmental science",
"Ecology",
"Sustainability",
"Research",
"Data interpretation"
],
"show": [
"Scientific reasoning",
"Environmental knowledge",
"Research ability",
"Problem solving"
],
"focus": "Environmental science, research and evidence-based reasoning.",
"questions": [
"How would you investigate pollution?",
"What is sustainability?",
"How can technology help environmental monitoring?",
"Explain an environmental project."
],
"behavior": "Clearly distinguish evidence from assumptions.",
"mistakes": "Avoid unsupported environmental claims.",
"day": "Review ecology, sustainability and research methods.",
"after": "Review scientific scenario questions."
},

"Hotel Manager": {
"prepare": [
"Hospitality",
"Customer service",
"Operations",
"Communication",
"Team management"
],
"show": [
"Customer focus",
"Leadership",
"Problem solving",
"Communication"
],
"focus": "Customer experience, operations, communication and leadership.",
"questions": [
"How would you handle an unhappy guest?",
"How do you manage staff?",
"How do you maintain service quality?",
"How would you handle an operational problem?"
],
"behavior": "Stay calm and customer-focused.",
"mistakes": "Avoid blaming customers or staff.",
"day": "Review hospitality operations and customer scenarios.",
"after": "Review service-related scenarios."
},

"Chef": {
"prepare": [
"Culinary fundamentals",
"Food safety",
"Kitchen operations",
"Food preparation",
"Creativity"
],
"show": [
"Practical knowledge",
"Food safety awareness",
"Creativity",
"Organisation"
],
"focus": "Culinary skill, food safety, kitchen organisation and creativity.",
"questions": [
"How do you maintain food safety?",
"How do you plan a menu?",
"How do you handle a busy kitchen?",
"Explain a dish you prepare well."
],
"behavior": "Demonstrate discipline and attention to safety.",
"mistakes": "Never ignore food-safety procedures.",
"day": "Review culinary fundamentals and practical examples.",
"after": "Review practical kitchen scenarios."
},

"Fitness Trainer": {
"prepare": [
"Exercise science",
"Training",
"Fitness assessment",
"Nutrition basics",
"Client communication"
],
"show": [
"Safety awareness",
"Training knowledge",
"Communication",
"Client understanding"
],
"focus": "Safe training, client assessment and fitness knowledge.",
"questions": [
"How do you assess a client?",
"How would you design a training plan?",
"How do you track progress?",
"How do you communicate safety?"
],
"behavior": "Prioritise safe, evidence-based guidance.",
"mistakes": "Avoid making unrealistic health claims.",
"day": "Review exercise fundamentals and client communication.",
"after": "Review scenario-based training questions."
},

"Sports Coach": {
"prepare": [
"Sports fundamentals",
"Coaching",
"Training",
"Leadership",
"Communication"
],
"show": [
"Leadership",
"Training knowledge",
"Team management",
"Communication"
],
"focus": "Coaching methodology, leadership and athlete development.",
"questions": [
"How do you motivate athletes?",
"How do you evaluate performance?",
"How do you handle team conflict?",
"How do you plan training?"
],
"behavior": "Be supportive, structured and performance-focused.",
"mistakes": "Avoid using the same approach for every athlete.",
"day": "Review coaching methods and sport-specific knowledge.",
"after": "Review scenario-based coaching questions."
}
}


guide = GUIDE.get(
    career,
    {
        "prepare": [],
        "show": [],
        "focus": "Career-specific knowledge and practical evidence.",
        "questions": [],
        "behavior": "Be clear and professional.",
        "mistakes": "Avoid claiming skills you do not have.",
        "day": "Review your skills and projects.",
        "after": "Review difficult questions."
    }
)


# ============================================================
# INTERVIEW GUIDE UI
# ============================================================

st.divider()

st.subheader("📚 What You Must Prepare")

for item in guide["prepare"]:
    st.write(f"• {item}")


st.subheader("🏆 What You Should Be Able to Show")

for item in guide["show"]:
    st.write(f"• {item}")


st.subheader("👀 What the Interviewer Will Focus On")

st.info(guide["focus"])


st.subheader("❓ Likely Questions")

for item in guide["questions"]:
    st.write(f"• {item}")


st.subheader("🗣️ How to Behave")

st.write(guide["behavior"])


st.subheader("⚠️ Mistakes to Avoid")

st.warning(guide["mistakes"])


st.subheader("📅 Interview Day")

st.write(guide["day"])


st.subheader("🔄 After the Interview")

st.write(guide["after"])


# ============================================================
# FINAL EXPLANATION
# ============================================================

st.divider()

st.caption(
    "Interview Readiness is an evidence-based score for the selected career. "
    "It uses career-specific skills (40%), relevant projects (30%), "
    "education (15%), domain alignment (10%) and certifications (5%). "
    "Personal confidence is intentionally excluded."
)