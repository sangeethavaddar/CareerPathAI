import streamlit as st
import pandas as pd
import json
import re
from pathlib import Path
import plotly.express as px


# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parent.parent
CAREERS_FILE = BASE / "data" / "careers.csv"
PROFILE_FILE = BASE / "data" / "profile.json"


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Job Matching",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Job Matching")
st.caption(
    "Explainable career matching based on evidence from your profile."
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_careers():
    return pd.read_csv(CAREERS_FILE)


def load_profile():
    if not PROFILE_FILE.exists():
        return {}

    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


careers_df = load_careers()
profile = load_profile()

if careers_df.empty:
    st.error("Career database is empty.")
    st.stop()


# ============================================================
# TEXT / LIST HELPERS
# ============================================================

def as_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return [
            str(x).strip()
            for x in value
            if str(x).strip()
        ]

    text = str(value).strip()

    if not text:
        return []

    if "," in text:
        return [
            x.strip()
            for x in text.split(",")
            if x.strip()
        ]

    if ";" in text:
        return [
            x.strip()
            for x in text.split(";")
            if x.strip()
        ]

    return [text]


def normalize(text):
    text = str(text).lower().strip()

    text = text.replace("&", " and ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)

    aliases = {
        "js": "javascript",
        "py": "python",
        "ml": "machine learning",
        "ai": "artificial intelligence",
        "powerbi": "power bi",
        "power bi": "power bi",
        "ui/ux": "ui ux",
        "ux/ui": "ui ux",
        "data analytics": "data analysis",
        "web development": "web development",
        "software development": "software development",
    }

    return aliases.get(text, text)


def normalized_list(values):
    return [
        normalize(x)
        for x in values
        if str(x).strip()
    ]


def exact_or_alias_match(user_value, required_value):
    user = normalize(user_value)
    required = normalize(required_value)

    if user == required:
        return True

    aliases = {
        ("web development", "web developer"),
        ("software development", "software developer"),
        ("data analysis", "data analyst"),
        ("data science", "data scientist"),
        ("artificial intelligence", "ai engineer"),
        ("machine learning", "ai engineer"),
        ("ui ux", "ui ux designer"),
        ("graphic design", "graphic designer"),
        ("human resources", "human resources manager"),
        ("digital marketing", "marketing manager"),
        ("finance", "financial analyst"),
        ("accounting", "accountant"),
    }

    if (user, required) in aliases:
        return True

    return False


def contains_term(text, term):
    text = normalize(text)
    term = normalize(term)

    if not term:
        return False

    if text == term:
        return True

    return re.search(
        r"(?<!\w)" + re.escape(term) + r"(?!\w)",
        text
    ) is not None


def score_from_fraction(matched, total):
    if total <= 0:
        return 0.0

    return round(
        (matched / total) * 100,
        1
    )


# ============================================================
# USER PROFILE
# ============================================================

user_skills = normalized_list(
    as_list(profile.get("skills", []))
)

user_interests = normalized_list(
    as_list(profile.get("interests", []))
)

user_projects = as_list(
    profile.get("projects", [])
)

education = normalize(
    profile.get("education", "")
)

specialization = normalize(
    profile.get("specialization", "")
)

experience = normalize(
    profile.get("experience", "")
)

preferred_domain = normalize(
    profile.get("preferred_domain", "")
)

career_goal = normalize(
    profile.get("career_goal", "")
)


# ============================================================
# CAREER-SPECIFIC SKILL IMPORTANCE
#
# core = skills that are central to the profession
# support = useful but less central skills
# ============================================================

SKILL_RULES = {

    "Software Developer": {
        "core": [
            "programming",
            "python",
            "java",
            "data structures",
            "oop"
        ],
        "support": [
            "sql",
            "git",
            "problem solving"
        ]
    },

    "Web Developer": {
        "core": [
            "html",
            "css",
            "javascript",
            "web development"
        ],
        "support": [
            "sql",
            "git"
        ]
    },

    "Data Analyst": {
        "core": [
            "data analysis",
            "sql",
            "excel",
            "statistics"
        ],
        "support": [
            "power bi",
            "data visualization"
        ]
    },

    "Data Scientist": {
        "core": [
            "python",
            "statistics",
            "machine learning",
            "data analysis"
        ],
        "support": [
            "sql",
            "pandas",
            "data visualization"
        ]
    },

    "AI Engineer": {
        "core": [
            "python",
            "machine learning",
            "deep learning",
            "artificial intelligence"
        ],
        "support": [
            "sql",
            "data analysis",
            "git"
        ]
    },

    "Cybersecurity Analyst": {
        "core": [
            "cybersecurity",
            "networking",
            "security",
            "linux"
        ],
        "support": [
            "python",
            "cryptography",
            "risk analysis"
        ]
    },

    "Cloud Engineer": {
        "core": [
            "cloud computing",
            "aws",
            "azure",
            "linux"
        ],
        "support": [
            "networking",
            "docker",
            "git"
        ]
    },

    "Mechanical Engineer": {
        "core": [
            "mechanical engineering",
            "cad",
            "mechanics",
            "machine design"
        ],
        "support": [
            "thermodynamics",
            "manufacturing"
        ]
    },

    "Civil Engineer": {
        "core": [
            "civil engineering",
            "autocad",
            "construction",
            "structural analysis"
        ],
        "support": [
            "surveying",
            "project management"
        ]
    },

    "Electrical Engineer": {
        "core": [
            "electrical engineering",
            "circuit design",
            "power systems",
            "control systems"
        ],
        "support": [
            "matlab",
            "electrical machines"
        ]
    },

    "Electronics Engineer": {
        "core": [
            "electronics",
            "circuit design",
            "embedded systems",
            "microcontrollers"
        ],
        "support": [
            "arduino",
            "esp32",
            "iot"
        ]
    },

    "Doctor": {
        "core": [
            "medicine",
            "biology",
            "anatomy",
            "clinical skills"
        ],
        "support": [
            "diagnosis",
            "patient care"
        ]
    },

    "Nurse": {
        "core": [
            "nursing",
            "patient care",
            "clinical skills"
        ],
        "support": [
            "biology",
            "first aid",
            "communication"
        ]
    },

    "Pharmacist": {
        "core": [
            "pharmacy",
            "pharmacology",
            "medicines",
            "pharmaceutical science"
        ],
        "support": [
            "chemistry",
            "patient counseling"
        ]
    },

    "Physiotherapist": {
        "core": [
            "physiotherapy",
            "anatomy",
            "rehabilitation"
        ],
        "support": [
            "exercise therapy",
            "patient care",
            "clinical skills"
        ]
    },

    "Accountant": {
        "core": [
            "accounting",
            "bookkeeping",
            "financial reporting"
        ],
        "support": [
            "excel",
            "tally",
            "taxation"
        ]
    },

    "Financial Analyst": {
        "core": [
            "financial analysis",
            "finance",
            "financial modeling"
        ],
        "support": [
            "excel",
            "accounting",
            "data analysis"
        ]
    },

    "Investment Analyst": {
        "core": [
            "investment analysis",
            "financial modeling",
            "valuation"
        ],
        "support": [
            "excel",
            "economics",
            "financial markets"
        ]
    },

    "Marketing Manager": {
        "core": [
            "marketing",
            "digital marketing",
            "market research"
        ],
        "support": [
            "communication",
            "social media",
            "analytics"
        ]
    },

    "Business Analyst": {
        "core": [
            "business analysis",
            "requirements analysis",
            "data analysis"
        ],
        "support": [
            "sql",
            "excel",
            "communication"
        ]
    },

    "Human Resources Manager": {
        "core": [
            "human resources",
            "recruitment",
            "employee relations"
        ],
        "support": [
            "communication",
            "leadership",
            "conflict resolution"
        ]
    },

    "Entrepreneur": {
        "core": [
            "business planning",
            "leadership",
            "problem solving"
        ],
        "support": [
            "marketing",
            "communication",
            "financial management"
        ]
    },

    "Teacher": {
        "core": [
            "teaching",
            "communication",
            "subject knowledge"
        ],
        "support": [
            "lesson planning",
            "presentation",
            "classroom management"
        ]
    },

    "Professor": {
        "core": [
            "teaching",
            "research",
            "academic writing"
        ],
        "support": [
            "presentation",
            "communication",
            "subject expertise"
        ]
    },

    "Lawyer": {
        "core": [
            "law",
            "legal research",
            "legal writing"
        ],
        "support": [
            "communication",
            "argumentation",
            "critical thinking"
        ]
    },

    "Journalist": {
        "core": [
            "journalism",
            "writing",
            "news reporting"
        ],
        "support": [
            "communication",
            "research",
            "interviewing"
        ]
    },

    "Content Creator": {
        "core": [
            "content creation",
            "writing",
            "creativity"
        ],
        "support": [
            "video editing",
            "social media",
            "communication"
        ]
    },

    "Graphic Designer": {
        "core": [
            "graphic design",
            "creativity",
            "typography"
        ],
        "support": [
            "adobe photoshop",
            "illustrator",
            "color theory"
        ]
    },

    "UI UX Designer": {
        "core": [
            "ui design",
            "ux design",
            "user research",
            "prototyping"
        ],
        "support": [
            "figma",
            "wireframing"
        ]
    },

    "Architect": {
        "core": [
            "architecture",
            "building design",
            "technical drawing"
        ],
        "support": [
            "autocad",
            "revit",
            "3d modeling"
        ]
    },

    "Agricultural Scientist": {
        "core": [
            "agriculture",
            "plant science",
            "soil science"
        ],
        "support": [
            "research",
            "biology",
            "data analysis"
        ]
    },

    "Environmental Scientist": {
        "core": [
            "environmental science",
            "ecology",
            "sustainability"
        ],
        "support": [
            "research",
            "data analysis",
            "gis"
        ]
    },

    "Hotel Manager": {
        "core": [
            "hotel management",
            "hospitality",
            "operations"
        ],
        "support": [
            "customer service",
            "communication",
            "leadership"
        ]
    },

    "Chef": {
        "core": [
            "cooking",
            "food preparation",
            "food safety"
        ],
        "support": [
            "menu planning",
            "kitchen management",
            "creativity"
        ]
    },

    "Fitness Trainer": {
        "core": [
            "fitness training",
            "exercise science",
            "workout planning"
        ],
        "support": [
            "nutrition",
            "anatomy",
            "communication"
        ]
    },

    "Sports Coach": {
        "core": [
            "coaching",
            "sports",
            "training"
        ],
        "support": [
            "leadership",
            "communication",
            "performance analysis"
        ]
    }
}


# ============================================================
# CAREER INTERESTS
# ============================================================

INTEREST_RULES = {

    "Software Developer": [
        "programming",
        "software development",
        "technology",
        "problem solving"
    ],

    "Web Developer": [
        "web development",
        "web design",
        "technology",
        "programming"
    ],

    "Data Analyst": [
        "data analysis",
        "analytics",
        "statistics",
        "business"
    ],

    "Data Scientist": [
        "data science",
        "machine learning",
        "statistics",
        "artificial intelligence"
    ],

    "AI Engineer": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "technology"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity",
        "networking",
        "security",
        "ethical hacking"
    ],

    "Cloud Engineer": [
        "cloud computing",
        "devops",
        "networking",
        "technology"
    ],

    "Mechanical Engineer": [
        "mechanical engineering",
        "machines",
        "manufacturing",
        "design"
    ],

    "Civil Engineer": [
        "civil engineering",
        "construction",
        "infrastructure",
        "design"
    ],

    "Electrical Engineer": [
        "electrical engineering",
        "electronics",
        "circuits",
        "power"
    ],

    "Electronics Engineer": [
        "electronics",
        "embedded systems",
        "iot",
        "robotics"
    ],

    "Doctor": [
        "medicine",
        "biology",
        "anatomy",
        "healthcare"
    ],

    "Nurse": [
        "nursing",
        "healthcare",
        "medicine",
        "patient care"
    ],

    "Pharmacist": [
        "pharmacy",
        "medicine",
        "healthcare",
        "chemistry"
    ],

    "Physiotherapist": [
        "physiotherapy",
        "healthcare",
        "anatomy",
        "fitness"
    ],

    "Accountant": [
        "accounting",
        "finance",
        "taxation",
        "business"
    ],

    "Financial Analyst": [
        "finance",
        "financial analysis",
        "business",
        "data analysis"
    ],

    "Investment Analyst": [
        "investment",
        "finance",
        "stock market",
        "economics"
    ],

    "Marketing Manager": [
        "marketing",
        "advertising",
        "social media",
        "business"
    ],

    "Business Analyst": [
        "business",
        "analytics",
        "problem solving",
        "management"
    ],

    "Human Resources Manager": [
        "human resources",
        "people",
        "communication",
        "management"
    ],

    "Entrepreneur": [
        "entrepreneurship",
        "business",
        "innovation",
        "leadership"
    ],

    "Teacher": [
        "teaching",
        "education",
        "learning",
        "communication"
    ],

    "Professor": [
        "education",
        "research",
        "teaching",
        "academics"
    ],

    "Lawyer": [
        "law",
        "legal studies",
        "justice",
        "communication"
    ],

    "Journalist": [
        "journalism",
        "news",
        "writing",
        "media"
    ],

    "Content Creator": [
        "content creation",
        "social media",
        "video",
        "writing"
    ],

    "Graphic Designer": [
        "graphic design",
        "art",
        "design",
        "creativity"
    ],

    "UI UX Designer": [
        "ui ux",
        "design",
        "user experience",
        "creativity"
    ],

    "Architect": [
        "architecture",
        "design",
        "buildings",
        "construction"
    ],

    "Agricultural Scientist": [
        "agriculture",
        "biology",
        "plants",
        "environment"
    ],

    "Environmental Scientist": [
        "environment",
        "ecology",
        "sustainability",
        "science"
    ],

    "Hotel Manager": [
        "hospitality",
        "hotels",
        "travel",
        "customer service"
    ],

    "Chef": [
        "cooking",
        "food",
        "hospitality",
        "culinary arts"
    ],

    "Fitness Trainer": [
        "fitness",
        "health",
        "exercise",
        "sports"
    ],

    "Sports Coach": [
        "sports",
        "coaching",
        "fitness",
        "athletics"
    ]
}


# ============================================================
# EDUCATION REQUIREMENTS
# ============================================================

EDUCATION_RULES = {

    "Software Developer": {
        "acceptable": [
            "computer science",
            "computer engineering",
            "information technology",
            "software engineering"
        ],
        "preferred": [
            "computer science",
            "computer engineering",
            "information technology"
        ],
        "regulated": False
    },

    "Web Developer": {
        "acceptable": [
            "computer science",
            "computer engineering",
            "information technology",
            "software engineering"
        ],
        "preferred": [
            "computer science",
            "information technology"
        ],
        "regulated": False
    },

    "Data Analyst": {
        "acceptable": [
            "computer science",
            "information technology",
            "statistics",
            "mathematics",
            "data science",
            "business",
            "commerce",
            "economics",
            "engineering"
        ],
        "preferred": [
            "statistics",
            "mathematics",
            "data science",
            "computer science"
        ],
        "regulated": False
    },

    "Data Scientist": {
        "acceptable": [
            "computer science",
            "data science",
            "statistics",
            "mathematics",
            "information technology",
            "engineering"
        ],
        "preferred": [
            "data science",
            "statistics",
            "mathematics",
            "computer science"
        ],
        "regulated": False
    },

    "AI Engineer": {
        "acceptable": [
            "computer science",
            "artificial intelligence",
            "machine learning",
            "information technology",
            "engineering",
            "data science"
        ],
        "preferred": [
            "computer science",
            "artificial intelligence",
            "machine learning"
        ],
        "regulated": False
    },

    "Cybersecurity Analyst": {
        "acceptable": [
            "computer science",
            "cybersecurity",
            "information technology",
            "computer engineering"
        ],
        "preferred": [
            "cybersecurity",
            "computer science",
            "information technology"
        ],
        "regulated": False
    },

    "Cloud Engineer": {
        "acceptable": [
            "computer science",
            "information technology",
            "computer engineering",
            "engineering"
        ],
        "preferred": [
            "computer science",
            "information technology"
        ],
        "regulated": False
    },

    "Mechanical Engineer": {
        "acceptable": [
            "mechanical engineering"
        ],
        "preferred": [
            "mechanical engineering"
        ],
        "regulated": True
    },

    "Civil Engineer": {
        "acceptable": [
            "civil engineering"
        ],
        "preferred": [
            "civil engineering"
        ],
        "regulated": True
    },

    "Electrical Engineer": {
        "acceptable": [
            "electrical engineering"
        ],
        "preferred": [
            "electrical engineering"
        ],
        "regulated": True
    },

    "Electronics Engineer": {
        "acceptable": [
            "electronics",
            "electronics and communication",
            "electrical engineering"
        ],
        "preferred": [
            "electronics",
            "electronics and communication"
        ],
        "regulated": True
    },

    "Doctor": {
        "acceptable": [
            "mbbs",
            "medicine",
            "medical"
        ],
        "preferred": [
            "mbbs",
            "medicine"
        ],
        "regulated": True
    },

    "Nurse": {
        "acceptable": [
            "nursing",
            "bsc nursing",
            "gnm"
        ],
        "preferred": [
            "nursing",
            "bsc nursing"
        ],
        "regulated": True
    },

    "Pharmacist": {
        "acceptable": [
            "pharmacy",
            "b pharma",
            "d pharma",
            "pharmaceutical"
        ],
        "preferred": [
            "pharmacy",
            "b pharma"
        ],
        "regulated": True
    },

    "Physiotherapist": {
        "acceptable": [
            "physiotherapy",
            "bpt"
        ],
        "preferred": [
            "physiotherapy",
            "bpt"
        ],
        "regulated": True
    },

    "Accountant": {
        "acceptable": [
            "commerce",
            "accounting",
            "finance",
            "business",
            "economics"
        ],
        "preferred": [
            "commerce",
            "accounting",
            "finance"
        ],
        "regulated": False
    },

    "Financial Analyst": {
        "acceptable": [
            "finance",
            "commerce",
            "economics",
            "business",
            "accounting",
            "mathematics"
        ],
        "preferred": [
            "finance",
            "economics",
            "commerce"
        ],
        "regulated": False
    },

    "Investment Analyst": {
        "acceptable": [
            "finance",
            "economics",
            "commerce",
            "business",
            "accounting"
        ],
        "preferred": [
            "finance",
            "economics"
        ],
        "regulated": False
    },

    "Marketing Manager": {
        "acceptable": [
            "marketing",
            "business",
            "management",
            "commerce",
            "communication"
        ],
        "preferred": [
            "marketing",
            "business",
            "management"
        ],
        "regulated": False
    },

    "Business Analyst": {
        "acceptable": [
            "business",
            "management",
            "commerce",
            "computer science",
            "information technology",
            "engineering"
        ],
        "preferred": [
            "business",
            "computer science",
            "information technology"
        ],
        "regulated": False
    },

    "Human Resources Manager": {
        "acceptable": [
            "human resources",
            "business",
            "management",
            "psychology",
            "commerce"
        ],
        "preferred": [
            "human resources",
            "business",
            "management"
        ],
        "regulated": False
    },

    "Entrepreneur": {
        "acceptable": [
            "business",
            "management",
            "commerce",
            "computer science",
            "engineering",
            "any"
        ],
        "preferred": [
            "business",
            "management"
        ],
        "regulated": False
    },

    "Teacher": {
        "acceptable": [
            "education",
            "teaching",
            "computer science",
            "mathematics",
            "science",
            "english",
            "arts"
        ],
        "preferred": [
            "education",
            "teaching"
        ],
        "regulated": False
    },

    "Professor": {
        "acceptable": [
            "master",
            "phd",
            "computer science",
            "engineering",
            "science",
            "arts"
        ],
        "preferred": [
            "master",
            "phd"
        ],
        "regulated": False
    },

    "Lawyer": {
        "acceptable": [
            "law",
            "llb",
            "llm"
        ],
        "preferred": [
            "llb",
            "llm"
        ],
        "regulated": True
    },

    "Journalist": {
        "acceptable": [
            "journalism",
            "mass communication",
            "media",
            "communication"
        ],
        "preferred": [
            "journalism",
            "mass communication"
        ],
        "regulated": False
    },

    "Content Creator": {
        "acceptable": [
            "media",
            "communication",
            "journalism",
            "arts",
            "design",
            "any"
        ],
        "preferred": [
            "media",
            "communication",
            "design"
        ],
        "regulated": False
    },

    "Graphic Designer": {
        "acceptable": [
            "graphic design",
            "design",
            "fine arts",
            "arts"
        ],
        "preferred": [
            "graphic design",
            "design"
        ],
        "regulated": False
    },

    "UI UX Designer": {
        "acceptable": [
            "design",
            "graphic design",
            "computer science",
            "information technology",
            "arts"
        ],
        "preferred": [
            "design",
            "graphic design"
        ],
        "regulated": False
    },

    "Architect": {
        "acceptable": [
            "architecture",
            "b arch"
        ],
        "preferred": [
            "architecture",
            "b arch"
        ],
        "regulated": True
    },

    "Agricultural Scientist": {
        "acceptable": [
            "agriculture",
            "agricultural science",
            "biology",
            "botany"
        ],
        "preferred": [
            "agriculture",
            "agricultural science"
        ],
        "regulated": True
    },

    "Environmental Scientist": {
        "acceptable": [
            "environmental science",
            "environment",
            "ecology",
            "biology",
            "science"
        ],
        "preferred": [
            "environmental science",
            "ecology"
        ],
        "regulated": False
    },

    "Hotel Manager": {
        "acceptable": [
            "hotel management",
            "hospitality",
            "tourism",
            "business",
            "management"
        ],
        "preferred": [
            "hotel management",
            "hospitality"
        ],
        "regulated": False
    },

    "Chef": {
        "acceptable": [
            "culinary",
            "hotel management",
            "hospitality",
            "food"
        ],
        "preferred": [
            "culinary",
            "hotel management"
        ],
        "regulated": False
    },

    "Fitness Trainer": {
        "acceptable": [
            "fitness",
            "sports science",
            "exercise science",
            "physical education"
        ],
        "preferred": [
            "sports science",
            "exercise science"
        ],
        "regulated": False
    },

    "Sports Coach": {
        "acceptable": [
            "sports",
            "physical education",
            "sports science"
        ],
        "preferred": [
            "sports science",
            "physical education"
        ],
        "regulated": False
    }
}


# ============================================================
# PROJECT KEYWORDS
#
# STRICT terms only.
# Generic words such as "application", "project",
# "website" are intentionally avoided where possible.
# ============================================================

PROJECT_RULES = {

    "Software Developer": [
        "software",
        "programming",
        "course feedback portal",
        "ecommerce website",
        "voice controlled home automation"
    ],

    "Web Developer": [
        "ecommerce website",
        "website",
        "web application",
        "frontend",
        "backend"
    ],

    "Data Analyst": [
        "data analysis",
        "dashboard",
        "analytics",
        "reporting",
        "excel"
    ],

    "Data Scientist": [
        "data science",
        "machine learning",
        "prediction",
        "classification",
        "data analysis"
    ],

    "AI Engineer": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "ai assistance",
        "voice controlled home automation"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity",
        "security",
        "cryptography",
        "encryption",
        "network security"
    ],

    "Cloud Engineer": [
        "cloud",
        "aws",
        "azure",
        "devops",
        "deployment"
    ],

    "Mechanical Engineer": [
        "mechanical",
        "cad",
        "machine design",
        "manufacturing"
    ],

    "Civil Engineer": [
        "civil",
        "construction",
        "structural",
        "building",
        "surveying"
    ],

    "Electrical Engineer": [
        "electrical",
        "circuit",
        "power",
        "control system"
    ],

    "Electronics Engineer": [
        "electronics",
        "arduino",
        "esp32",
        "iot",
        "embedded",
        "sensor"
    ],

    "Doctor": [
        "medical",
        "medicine",
        "clinical",
        "patient"
    ],

    "Nurse": [
        "nursing",
        "patient care",
        "clinical"
    ],

    "Pharmacist": [
        "pharmacy",
        "pharmaceutical",
        "medicine",
        "drug"
    ],

    "Physiotherapist": [
        "physiotherapy",
        "rehabilitation",
        "exercise therapy"
    ],

    "Accountant": [
        "accounting",
        "billing",
        "bookkeeping",
        "tax"
    ],

    "Financial Analyst": [
        "financial analysis",
        "financial modeling",
        "finance",
        "budget"
    ],

    "Investment Analyst": [
        "investment",
        "stock",
        "portfolio",
        "financial analysis"
    ],

    "Marketing Manager": [
        "marketing",
        "campaign",
        "advertising",
        "social media"
    ],

    "Business Analyst": [
        "business analysis",
        "requirements",
        "business process",
        "dashboard"
    ],

    "Human Resources Manager": [
        "human resources",
        "recruitment",
        "employee",
        "training"
    ],

    "Entrepreneur": [
        "startup",
        "business",
        "product",
        "ecommerce"
    ],

    "Teacher": [
        "teaching",
        "education",
        "course",
        "training"
    ],

    "Professor": [
        "research",
        "academic",
        "publication",
        "teaching"
    ],

    "Lawyer": [
        "legal",
        "law",
        "case",
        "court"
    ],

    "Journalist": [
        "journalism",
        "news",
        "article",
        "reporting"
    ],

    "Content Creator": [
        "content",
        "video",
        "blog",
        "youtube",
        "social media"
    ],

    "Graphic Designer": [
        "graphic",
        "poster",
        "logo",
        "branding"
    ],

    "UI UX Designer": [
        "ui",
        "ux",
        "figma",
        "prototype",
        "wireframe"
    ],

    "Architect": [
        "architecture",
        "building design",
        "autocad",
        "revit"
    ],

    "Agricultural Scientist": [
        "agriculture",
        "crop",
        "plant",
        "soil"
    ],

    "Environmental Scientist": [
        "environment",
        "ecology",
        "climate",
        "sustainability"
    ],

    "Hotel Manager": [
        "hotel",
        "hospitality",
        "tourism",
        "restaurant"
    ],

    "Chef": [
        "cooking",
        "culinary",
        "recipe",
        "food preparation"
    ],

    "Fitness Trainer": [
        "fitness",
        "workout",
        "exercise",
        "training"
    ],

    "Sports Coach": [
        "sports",
        "coaching",
        "athletics",
        "training"
    ]
}


# ============================================================
# EXPERIENCE
# ============================================================

def extract_years(text):

    text = normalize(text)

    if not text:
        return 0.0

    no_experience = [
        "no experience",
        "no professional experience",
        "fresher",
        "fresh graduate",
        "student",
        "none"
    ]

    if any(
        term in text
        for term in no_experience
    ):
        return 0.0

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)",
        text
    )

    if match:
        return float(match.group(1))

    if "internship" in text or "intern" in text:
        return 0.5

    return 0.0


def experience_score():

    years = extract_years(
        experience
    )

    # This represents actual experience evidence.
    # It intentionally does NOT give a fresher 100%.

    if years <= 0:
        return 0.0

    if years >= 2:
        return 100.0

    return round(
        years / 2 * 100,
        1
    )


# ============================================================
# SKILL SCORE
# ============================================================

def skill_score(career, csv_skills):

    rules = SKILL_RULES.get(
        career,
        {}
    )

    core = rules.get(
        "core",
        []
    )

    support = rules.get(
        "support",
        []
    )

    # If the career is not explicitly defined,
    # use the career CSV as the requirement source.
    if not core and not support:

        csv_skills = as_list(csv_skills)

        core = csv_skills

    matching_core = []
    missing_core = []

    matching_support = []
    missing_support = []

    for required in core:

        found = any(
            exact_or_alias_match(
                user_skill,
                required
            )
            for user_skill in user_skills
        )

        if found:
            matching_core.append(required)
        else:
            missing_core.append(required)

    for required in support:

        found = any(
            exact_or_alias_match(
                user_skill,
                required
            )
            for user_skill in user_skills
        )

        if found:
            matching_support.append(required)
        else:
            missing_support.append(required)

    core_score = score_from_fraction(
        len(matching_core),
        len(core)
    )

    support_score = score_from_fraction(
        len(matching_support),
        len(support)
    )

    if core and support:

        final_score = round(
            core_score * 0.70
            + support_score * 0.30,
            1
        )

    elif core:

        final_score = core_score

    else:

        final_score = support_score

    matching = (
        matching_core
        + matching_support
    )

    missing = (
        missing_core
        + missing_support
    )

    return (
        final_score,
        matching,
        missing
    )


# ============================================================
# INTEREST SCORE
# ============================================================

def interest_score(career):

    required = INTEREST_RULES.get(
        career,
        []
    )

    if not required:
        return 0.0, []

    matching = []

    for required_interest in required:

        for user_interest in user_interests:

            if exact_or_alias_match(
                user_interest,
                required_interest
            ):
                matching.append(
                    required_interest
                )
                break

    score = score_from_fraction(
        len(matching),
        len(required)
    )

    return score, matching


# ============================================================
# EDUCATION SCORE
# ============================================================

def education_score(career):

    rules = EDUCATION_RULES.get(
        career
    )

    education_text = (
        education
        + " "
        + specialization
    ).strip()

    if not education_text:
        return 0.0

    if not rules:
        return 50.0

    acceptable = rules["acceptable"]
    preferred = rules["preferred"]
    regulated = rules["regulated"]

    # Exact specialist qualification
    for requirement in preferred:

        if requirement == "any":
            continue

        if contains_term(
            education_text,
            requirement
        ):
            return 100.0

    # Acceptable qualification
    for requirement in acceptable:

        if requirement == "any":
            continue

        if contains_term(
            education_text,
            requirement
        ):
            return 85.0

    # Generic degree without field evidence
    generic_degree = any(
        term in education_text
        for term in [
            "bachelor",
            "degree",
            "graduation",
            "be",
            "b.e",
            "btech",
            "b.tech"
        ]
    )

    if generic_degree:

        if regulated:
            return 0.0

        return 50.0

    return 0.0


# ============================================================
# PROJECT SCORE
# ============================================================

def project_score(career):

    projects = [
        str(project).strip()
        for project in user_projects
        if str(project).strip()
    ]

    if not projects:
        return 0.0, []

    keywords = PROJECT_RULES.get(
        career,
        []
    )

    if not keywords:
        return 0.0, []

    project_scores = []
    relevant_projects = []

    for project in projects:

        project_text = normalize(
            project
        )

        matched_keywords = 0

        for keyword in keywords:

            if contains_term(
                project_text,
                keyword
            ):
                matched_keywords += 1

        if matched_keywords == 0:

            project_scores.append(0)

        else:

            # One project cannot become 100% merely
            # because one generic keyword matched.
            #
            # 1 strong matching concept = 50
            # 2 = 75
            # 3+ = 100

            if matched_keywords == 1:
                score = 50.0
            elif matched_keywords == 2:
                score = 75.0
            else:
                score = 100.0

            project_scores.append(score)

            relevant_projects.append(
                project
            )

    # Average relevance across ALL projects.
    final_score = round(
        sum(project_scores)
        / len(project_scores),
        1
    )

    return (
        final_score,
        relevant_projects
    )


# ============================================================
# DOMAIN SCORE
# ============================================================

def domain_score(career_domain):

    if not preferred_domain:
        return 0.0

    career_domain = normalize(
        career_domain
    )

    if preferred_domain == career_domain:
        return 100.0

    # Related domain groups
    related_domains = {

        "technology": {
            "technology",
            "engineering"
        },

        "engineering": {
            "engineering",
            "technology"
        },

        "business": {
            "business",
            "finance",
            "hospitality"
        },

        "finance": {
            "finance",
            "business"
        },

        "media": {
            "media",
            "arts"
        },

        "arts": {
            "arts",
            "media",
            "architecture"
        },

        "healthcare": {
            "healthcare",
            "fitness",
            "sports"
        },

        "sports": {
            "sports",
            "fitness",
            "healthcare"
        }
    }

    if career_domain in related_domains.get(
        preferred_domain,
        set()
    ):
        return 50.0

    return 0.0


# ============================================================
# CAREER GOAL SCORE
# ============================================================

def goal_score(career):

    if not career_goal:
        return 0.0

    career_text = normalize(
        career
    )

    goal = normalize(
        career_goal
    )

    if career_text in goal:
        return 100.0

    career_words = [
        word
        for word in career_text.split()
        if len(word) >= 5
    ]

    matches = sum(
        1
        for word in career_words
        if word in goal
    )

    if matches:
        return 50.0

    return 0.0


# ============================================================
# CALCULATE ALL CAREERS
# ============================================================

results = []

for _, row in careers_df.iterrows():

    career = str(
        row["career"]
    ).strip()

    career_domain = str(
        row.get("domain", "")
    ).strip()

    description = str(
        row.get("description", "")
    ).strip()

    csv_skills = row.get(
        "skills",
        ""
    )

    # --------------------------------------------------------
    # COMPONENTS
    # --------------------------------------------------------

    skills, matching_skills, missing_skills = (
        skill_score(
            career,
            csv_skills
        )
    )

    interests, matching_interests = (
        interest_score(
            career
        )
    )

    education_match = education_score(
        career
    )

    experience_match = experience_score()

    projects, matching_projects = (
        project_score(
            career
        )
    )

    domain_match = domain_score(
        career_domain
    )

    goal_match = goal_score(
        career
    )

    # --------------------------------------------------------
    # CORE SCORE
    #
    # Project specification:
    # Skills      55%
    # Interests   20%
    # Education  15%
    # Experience 10%
    #
    # Projects, Domain and Goal are displayed separately
    # as supporting evidence and are NOT secretly inserted
    # into the core score.
    # --------------------------------------------------------

    overall = (
        skills * 0.55
        + interests * 0.20
        + education_match * 0.15
        + experience_match * 0.10
    )

    results.append({

        "Career": career,

        "Domain": career_domain,

        "Description": description,

        "Match": round(
            overall,
            1
        ),

        "Skills": skills,

        "Interests": interests,

        "Education": education_match,

        "Experience": experience_match,

        "Projects": projects,

        "Domain Score": domain_match,

        "Goal": goal_match,

        "Matching Skills": matching_skills,

        "Missing Skills": missing_skills,

        "Matching Interests": matching_interests,

        "Matching Projects": matching_projects
    })


results_df = pd.DataFrame(
    results
)

results_df = (
    results_df
    .sort_values(
        by="Match",
        ascending=False
    )
    .reset_index(drop=True)
)


# ============================================================
# TOP 5
# ============================================================

st.subheader(
    "🏆 Top 5 Career Matches"
)

top5 = results_df.head(5)

for position, result in top5.iterrows():

    st.markdown(
        f"### {position + 1}. "
        f"{result['Career']} — "
        f"{result['Match']}%"
    )

    st.write(
        result["Description"]
        or "Career compatibility calculated from your profile."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Skills",
            f"{result['Skills']}%"
        )

    with c2:
        st.metric(
            "Interests",
            f"{result['Interests']}%"
        )

    with c3:
        st.metric(
            "Education",
            f"{result['Education']}%"
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric(
            "Experience",
            f"{result['Experience']}%"
        )

    with c5:
        st.metric(
            "Projects",
            f"{result['Projects']}%"
        )

    with c6:
        st.metric(
            "Domain",
            f"{result['Domain Score']}%"
        )

    if result["Matching Skills"]:

        st.write(
            "**Matching skills:** "
            + ", ".join(
                x.title()
                for x in result["Matching Skills"]
            )
        )

    if result["Missing Skills"]:

        st.write(
            "**Skills to develop:** "
            + ", ".join(
                x.title()
                for x in result["Missing Skills"]
            )
        )

    if result["Matching Interests"]:

        st.write(
            "**Matching interests:** "
            + ", ".join(
                x.title()
                for x in result["Matching Interests"]
            )
        )

    if result["Matching Projects"]:

        st.write(
            "**Relevant projects:** "
            + ", ".join(
                result["Matching Projects"]
            )
        )

    st.divider()


# ============================================================
# CHART
# ============================================================

st.subheader(
    "📊 Career Match Comparison"
)

chart = px.bar(
    top5,
    x="Career",
    y="Match",
    text="Match",
    title="Top 5 Career Compatibility"
)

chart.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

chart.update_layout(
    yaxis_title="Compatibility (%)",
    xaxis_title="Career",
    yaxis_range=[0, 100]
)

st.plotly_chart(
    chart,
    use_container_width=True
)


# ============================================================
# BEST MATCH
# ============================================================

best = results_df.iloc[0]

st.subheader(
    "🥇 Best Career Match Analysis"
)

st.success(
    f"{best['Career']} is currently your strongest "
    f"career match with a compatibility of "
    f"{best['Match']}%."
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Skills",
        f"{best['Skills']}%"
    )

with c2:
    st.metric(
        "Interests",
        f"{best['Interests']}%"
    )

with c3:
    st.metric(
        "Education",
        f"{best['Education']}%"
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Experience",
        f"{best['Experience']}%"
    )

with c5:
    st.metric(
        "Projects",
        f"{best['Projects']}%"
    )

with c6:
    st.metric(
        "Domain",
        f"{best['Domain Score']}%"
    )


# ============================================================
# SKILL DEVELOPMENT
# ============================================================

st.subheader(
    "🛠️ Skill Development Opportunities"
)

for _, result in top5.iterrows():

    missing = result[
        "Missing Skills"
    ]

    if missing:

        st.write(
            f"**{result['Career']}:** "
            + ", ".join(
                x.title()
                for x in missing
            )
        )


# ============================================================
# NEXT ACTIONS
# ============================================================

st.subheader(
    "🚀 Recommended Next Actions"
)

actions = []

if best["Missing Skills"]:
    actions.append(
        "Develop the missing skills identified for your strongest career."
    )

if best["Projects"] < 50:
    actions.append(
        f"Build a practical project related to {best['Career']}."
    )

if best["Education"] < 70:
    actions.append(
        f"Review the educational requirements for {best['Career']}."
    )

if best["Experience"] < 50:
    actions.append(
        "Gain relevant internship, training or practical experience."
    )

if best["Interests"] < 50:
    actions.append(
        f"Explore {best['Career']} through practical activities."
    )

if best["Domain Score"] < 100:
    actions.append(
        "Consider whether your preferred domain matches this career."
    )

actions.append(
    "Use Career Roadmap and Learning Roadmap for the next preparation steps."
)

for number, action in enumerate(
    actions[:7],
    1
):

    st.write(
        f"{number}. {action}"
    )


# ============================================================
# SCORING EXPLANATION
# ============================================================

with st.expander(
    "ℹ️ How the score is calculated"
):

    st.write(
        "Core Career Match:"
    )

    st.write(
        "Skills — 55%"
    )

    st.write(
        "Interests — 20%"
    )

    st.write(
        "Education — 15%"
    )

    st.write(
        "Experience — 10%"
    )

    st.write(
        "Projects and Domain are displayed separately as "
        "supporting evidence. They are not secretly added "
        "to the core score."
    )

    st.write(
        "A 100% component is only produced when the "
        "available profile evidence fully satisfies that "
        "specific component's defined requirements."
    )