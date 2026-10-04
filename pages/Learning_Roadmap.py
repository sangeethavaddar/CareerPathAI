import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Learning Roadmap",
    page_icon="🗺️",
    layout="wide"
)

# ============================================================
# FILES
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

ROADMAP_FILE = DATA / "roadmap.json"


# ============================================================
# CAREER ROADMAPS
# ============================================================

ROADMAPS = {

    "Software Developer": [
        ("Programming Fundamentals", "Python, Java, C/C++ and programming logic"),
        ("Data Structures", "Arrays, strings, stacks, queues, trees and graphs"),
        ("Object-Oriented Programming", "Classes, inheritance, abstraction and polymorphism"),
        ("Database Skills", "SQL, relational databases and database design"),
        ("Web Development", "Frontend, backend and API development"),
        ("Git & GitHub", "Version control and collaborative development"),
        ("Software Engineering", "Testing, debugging and clean code"),
        ("Build Projects", "Develop practical software applications"),
        ("Interview Preparation", "Coding and technical interview practice"),
        ("Job Readiness", "Resume, portfolio and job preparation")
    ],

    "Data Analyst": [
        ("Excel", "Formulas, pivot tables, charts and data cleaning"),
        ("SQL", "Queries, joins, grouping and filtering"),
        ("Statistics", "Statistics and probability fundamentals"),
        ("Python for Data", "Python, Pandas and NumPy"),
        ("Data Cleaning", "Prepare real-world datasets"),
        ("Data Visualization", "Charts, dashboards and reporting"),
        ("Business Analysis", "Convert data into useful insights"),
        ("Data Projects", "Build practical analysis projects"),
        ("Portfolio", "Document dashboards and analysis"),
        ("Job Readiness", "SQL and analytical interview preparation")
    ],

    "Data Scientist": [
        ("Python", "Python programming for data science"),
        ("Statistics", "Probability and statistical reasoning"),
        ("Data Analysis", "Pandas, NumPy and exploratory analysis"),
        ("Visualization", "Communicate data through charts"),
        ("Machine Learning", "Supervised and unsupervised learning"),
        ("Model Evaluation", "Metrics, validation and overfitting"),
        ("Feature Engineering", "Prepare useful model features"),
        ("ML Projects", "Build practical machine-learning projects"),
        ("Portfolio", "Document models and results"),
        ("Job Readiness", "Machine-learning interview preparation")
    ],

    "AI Engineer": [
        ("Python", "Strong Python programming and problem solving"),
        ("Artificial Intelligence", "AI concepts and intelligent systems"),
        ("Machine Learning", "Machine-learning fundamentals"),
        ("Deep Learning", "Neural networks and deep learning"),
        ("Generative AI", "Modern AI and LLM concepts"),
        ("APIs", "Build and consume APIs"),
        ("AI Applications", "Develop AI-powered applications"),
        ("Model Integration", "Integrate AI models into applications"),
        ("AI Projects", "Build portfolio-quality AI projects"),
        ("Job Readiness", "AI and ML interview preparation")
    ],

    "Web Developer": [
        ("HTML", "Build structured web pages"),
        ("CSS", "Layouts, styling and responsive design"),
        ("JavaScript", "Interactive web development"),
        ("Frontend", "Build modern user interfaces"),
        ("Backend", "Server-side development and APIs"),
        ("Databases", "SQL and database integration"),
        ("Authentication", "Login and secure application access"),
        ("Web Projects", "Build complete web applications"),
        ("GitHub Portfolio", "Publish and document projects"),
        ("Job Readiness", "Frontend and backend interview preparation")
    ],

    "Cybersecurity Analyst": [
        ("Computer Fundamentals", "Operating systems and computer basics"),
        ("Networking", "TCP/IP, DNS, HTTP, ports and networks"),
        ("Linux", "Linux commands and system administration"),
        ("Cybersecurity Fundamentals", "Threats, vulnerabilities and controls"),
        ("Cryptography", "Encryption, hashing and authentication"),
        ("Security Monitoring", "Logs, alerts and incident analysis"),
        ("Ethical Security", "Security testing principles"),
        ("Security Projects", "Build safe cybersecurity projects"),
        ("Security Portfolio", "Document cybersecurity learning"),
        ("Job Readiness", "Security and scenario interview preparation")
    ],

    "Cloud Engineer": [
        ("Cloud Fundamentals", "Cloud computing and service models"),
        ("Linux", "Linux administration"),
        ("Networking", "Cloud networking and DNS"),
        ("AWS / Azure", "Core cloud services"),
        ("Cloud Storage", "Storage and cloud databases"),
        ("Docker", "Container fundamentals"),
        ("Deployment", "Deploy applications to cloud platforms"),
        ("Monitoring", "Logs and troubleshooting"),
        ("Cloud Project", "Build and deploy a cloud project"),
        ("Job Readiness", "Cloud interview preparation")
    ],

    "Mechanical Engineer": [
        ("Engineering Fundamentals", "Core mechanical engineering concepts"),
        ("CAD", "Technical drawings and modelling"),
        ("Manufacturing", "Manufacturing processes"),
        ("Materials", "Engineering materials"),
        ("Thermodynamics", "Thermodynamic principles"),
        ("Machine Design", "Machine elements and design"),
        ("Simulation", "Engineering simulation tools"),
        ("Practical Project", "Complete a mechanical project"),
        ("Portfolio", "Document designs and projects"),
        ("Job Readiness", "Technical interview preparation")
    ],

    "Civil Engineer": [
        ("Civil Fundamentals", "Core civil engineering concepts"),
        ("AutoCAD", "Technical drawing and drafting"),
        ("Surveying", "Surveying methods and instruments"),
        ("Construction", "Construction methods and materials"),
        ("Structural Concepts", "Structural engineering fundamentals"),
        ("Estimation", "Quantity estimation and costing"),
        ("Project Planning", "Construction planning"),
        ("Civil Project", "Complete a civil engineering project"),
        ("Portfolio", "Document project work"),
        ("Job Readiness", "Technical interview preparation")
    ],

    "Electrical Engineer": [
        ("Electrical Fundamentals", "Circuits and electrical basics"),
        ("Circuit Analysis", "Electrical circuit analysis"),
        ("Power Systems", "Power generation and distribution"),
        ("Control Systems", "Control-system fundamentals"),
        ("Electrical Machines", "Motors and generators"),
        ("MATLAB", "Engineering calculations and simulation"),
        ("Automation", "Industrial automation"),
        ("Electrical Project", "Build an electrical project"),
        ("Portfolio", "Document technical work"),
        ("Job Readiness", "Technical interview preparation")
    ],

    "Electronics Engineer": [
        ("Electronics Fundamentals", "Electronic circuits"),
        ("Digital Electronics", "Digital logic and systems"),
        ("Microcontrollers", "Microcontroller programming"),
        ("Sensors", "Sensors and data acquisition"),
        ("Embedded Systems", "Embedded-system architecture"),
        ("IoT", "Internet of Things"),
        ("Arduino / ESP32", "Practical hardware development"),
        ("Electronics Project", "Build an electronics project"),
        ("Portfolio", "Document hardware and software"),
        ("Job Readiness", "Embedded and electronics interviews")
    ],

    "Doctor": [
        ("Medical Fundamentals", "Core medical knowledge"),
        ("Anatomy", "Human anatomy"),
        ("Physiology", "Human body functions"),
        ("Clinical Reasoning", "Structured clinical reasoning"),
        ("Patient Communication", "Professional patient communication"),
        ("Medical Ethics", "Professional medical ethics"),
        ("Clinical Practice", "Appropriate supervised clinical learning"),
        ("Case Analysis", "Case-based learning"),
        ("Professional Development", "Continue medical learning"),
        ("Career Preparation", "Relevant examination and interview preparation")
    ],

    "Nurse": [
        ("Nursing Fundamentals", "Core nursing knowledge"),
        ("Patient Care", "Safe patient-care practices"),
        ("Clinical Skills", "Essential clinical skills"),
        ("Communication", "Professional patient communication"),
        ("Healthcare Safety", "Safety and infection control"),
        ("Emergency Care", "Emergency-care fundamentals"),
        ("Clinical Practice", "Supervised practical experience"),
        ("Case Learning", "Clinical scenarios"),
        ("Professional Development", "Continuous nursing education"),
        ("Career Preparation", "Nursing interview preparation")
    ],

    "Pharmacist": [
        ("Pharmacy Fundamentals", "Core pharmacy concepts"),
        ("Pharmacology", "Medicines and their effects"),
        ("Drug Safety", "Safe medication practices"),
        ("Pharmaceutical Science", "Pharmaceutical concepts"),
        ("Patient Counselling", "Responsible patient communication"),
        ("Prescription Knowledge", "Prescription handling"),
        ("Practical Training", "Supervised pharmacy experience"),
        ("Case Learning", "Pharmacy scenarios"),
        ("Professional Development", "Current pharmacy practices"),
        ("Career Preparation", "Pharmacy interview preparation")
    ],

    "Physiotherapist": [
        ("Anatomy", "Human anatomy"),
        ("Physiology", "Human body functions"),
        ("Assessment", "Patient assessment"),
        ("Exercise Therapy", "Therapeutic exercises"),
        ("Rehabilitation", "Rehabilitation planning"),
        ("Patient Communication", "Professional communication"),
        ("Clinical Practice", "Supervised practical learning"),
        ("Case Studies", "Rehabilitation scenarios"),
        ("Portfolio", "Document academic and practical work"),
        ("Career Preparation", "Professional interview preparation")
    ],

    "Accountant": [
        ("Accounting Fundamentals", "Accounting principles"),
        ("Financial Statements", "Balance sheet, income statement and cash flow"),
        ("Excel", "Spreadsheet skills"),
        ("Bookkeeping", "Bookkeeping processes"),
        ("Taxation", "Taxation fundamentals"),
        ("Accounting Software", "Accounting tools"),
        ("Financial Analysis", "Analyse financial information"),
        ("Accounting Project", "Practical accounting case study"),
        ("Portfolio", "Document practical work"),
        ("Career Preparation", "Accounting interview preparation")
    ],

    "Financial Analyst": [
        ("Finance Fundamentals", "Core finance concepts"),
        ("Accounting", "Financial statements"),
        ("Excel", "Financial spreadsheet analysis"),
        ("Financial Ratios", "Important financial ratios"),
        ("Valuation", "Company valuation"),
        ("Financial Modelling", "Build financial models"),
        ("Business Analysis", "Financial decision making"),
        ("Finance Project", "Financial-analysis case study"),
        ("Portfolio", "Document financial analysis"),
        ("Career Preparation", "Financial interview preparation")
    ],

    "Investment Analyst": [
        ("Finance Fundamentals", "Financial concepts"),
        ("Financial Markets", "Equity and financial markets"),
        ("Company Analysis", "Fundamental analysis"),
        ("Valuation", "Investment valuation"),
        ("Risk Analysis", "Investment risk"),
        ("Portfolio Management", "Portfolio concepts"),
        ("Investment Research", "Research and analysis"),
        ("Investment Project", "Investment case study"),
        ("Portfolio", "Document research"),
        ("Career Preparation", "Investment interview preparation")
    ],

    "Marketing Manager": [
        ("Marketing Fundamentals", "Marketing principles"),
        ("Consumer Behaviour", "Understand customers"),
        ("Market Research", "Research methods"),
        ("Digital Marketing", "Digital marketing channels"),
        ("SEO", "Search-engine optimization"),
        ("Social Media", "Social-media strategy"),
        ("Campaign Planning", "Plan marketing campaigns"),
        ("Marketing Project", "Create a campaign"),
        ("Portfolio", "Document marketing work"),
        ("Career Preparation", "Marketing interview preparation")
    ],

    "Business Analyst": [
        ("Business Fundamentals", "Business processes"),
        ("Requirements", "Requirements gathering"),
        ("Data Analysis", "Analytical skills"),
        ("SQL", "Database querying"),
        ("Excel", "Spreadsheet analysis"),
        ("Process Mapping", "Business-process modelling"),
        ("Communication", "Stakeholder communication"),
        ("Business Project", "Business-analysis case study"),
        ("Portfolio", "Document solutions"),
        ("Career Preparation", "Business-analysis interviews")
    ],

    "Human Resources Manager": [
        ("HR Fundamentals", "Human-resource functions"),
        ("Recruitment", "Recruitment processes"),
        ("Interviewing", "Candidate evaluation"),
        ("Employee Relations", "Workplace relationships"),
        ("Performance Management", "Performance management"),
        ("HR Analytics", "Data-driven HR"),
        ("Communication", "Professional communication"),
        ("HR Project", "HR case study"),
        ("Portfolio", "Document HR work"),
        ("Career Preparation", "HR interview preparation")
    ],

    "Entrepreneur": [
        ("Problem Identification", "Identify meaningful problems worth solving"),
        ("Customer Research", "Understand customer needs"),
        ("Business Model", "Create a practical business model"),
        ("Market Research", "Study competitors and opportunities"),
        ("Product Development", "Create and test an MVP"),
        ("Marketing", "Customer acquisition and branding"),
        ("Finance", "Pricing, costs, revenue and cash flow"),
        ("Business Project", "Build and validate a business idea"),
        ("Pitch & Portfolio", "Prepare a professional business pitch"),
        ("Career Preparation", "Business and entrepreneurship preparation")
    ],

    "Teacher": [
        ("Subject Knowledge", "Strengthen your teaching subject"),
        ("Teaching Methods", "Effective teaching approaches"),
        ("Lesson Planning", "Create structured lessons"),
        ("Communication", "Explain concepts clearly"),
        ("Classroom Management", "Manage classroom situations"),
        ("Educational Technology", "Use digital teaching tools"),
        ("Assessment", "Evaluate student understanding"),
        ("Teaching Practice", "Practise teaching"),
        ("Teaching Portfolio", "Document teaching work"),
        ("Career Preparation", "Teaching interview preparation")
    ],

    "Professor": [
        ("Subject Expertise", "Advanced subject knowledge"),
        ("Research Methods", "Academic research methodology"),
        ("Academic Writing", "Research writing"),
        ("Teaching", "Higher-education teaching"),
        ("Presentation", "Academic presentations"),
        ("Research Project", "Conduct meaningful research"),
        ("Publication Skills", "Academic publication basics"),
        ("Academic Portfolio", "Research and teaching portfolio"),
        ("Professional Development", "Continue academic development"),
        ("Career Preparation", "Academic interview preparation")
    ],

    "Lawyer": [
        ("Legal Fundamentals", "Core legal principles"),
        ("Legal Research", "Structured legal research"),
        ("Case Analysis", "Analyse legal cases"),
        ("Legal Writing", "Professional legal writing"),
        ("Negotiation", "Negotiation skills"),
        ("Communication", "Legal communication"),
        ("Practical Training", "Supervised legal experience"),
        ("Case Portfolio", "Document case analysis"),
        ("Professional Development", "Continue legal learning"),
        ("Career Preparation", "Legal interview preparation")
    ],

    "Journalist": [
        ("Journalism Fundamentals", "Journalism principles"),
        ("Research", "Reliable research"),
        ("Writing", "Journalistic writing"),
        ("Reporting", "Reporting techniques"),
        ("Interviewing", "Interview skills"),
        ("Fact Checking", "Information verification"),
        ("Digital Journalism", "Digital publishing"),
        ("Portfolio", "Build journalistic work"),
        ("Media Skills", "Multimedia communication"),
        ("Career Preparation", "Journalism interview preparation")
    ],

    "Content Creator": [
        ("Content Strategy", "Plan content around a specific audience"),
        ("Audience Research", "Understand audience interests and behaviour"),
        ("Content Pillars", "Create consistent content themes"),
        ("Content Calendar", "Plan and schedule content"),
        ("Writing & Storytelling", "Create engaging scripts and captions"),
        ("Visual & Video Skills", "Improve design and video skills"),
        ("Social Media", "Develop platform-specific strategies"),
        ("Analytics", "Use audience data to improve content"),
        ("Creator Portfolio", "Build a strong collection of work"),
        ("Career Preparation", "Prepare pitches and portfolio presentations")
    ],

    "Graphic Designer": [
        ("Design Fundamentals", "Composition, balance and hierarchy"),
        ("Typography", "Typography and readability"),
        ("Colour Theory", "Effective colour combinations"),
        ("Design Tools", "Practise design software"),
        ("Branding", "Visual identity"),
        ("Digital Design", "Create digital graphics"),
        ("Design Projects", "Build practical design projects"),
        ("Client Communication", "Understand design briefs"),
        ("Portfolio", "Build a professional portfolio"),
        ("Career Preparation", "Portfolio and design interviews")
    ],

    "UI UX Designer": [
        ("UX Fundamentals", "User-centred design"),
        ("User Research", "Understand user needs"),
        ("Information Architecture", "Organise content and navigation"),
        ("Wireframing", "Create effective wireframes"),
        ("UI Design", "Interface design principles"),
        ("Prototyping", "Build interactive prototypes"),
        ("Usability Testing", "Test designs"),
        ("UX Project", "Complete a UX case study"),
        ("Portfolio", "Build a design portfolio"),
        ("Career Preparation", "Design interview preparation")
    ],

    "Architect": [
        ("Architecture Fundamentals", "Architectural principles"),
        ("Design", "Architectural design"),
        ("CAD", "Computer-aided design"),
        ("Building Systems", "Building systems"),
        ("Materials", "Construction materials"),
        ("3D Modelling", "3D modelling"),
        ("Design Projects", "Complete architectural projects"),
        ("Portfolio", "Build an architecture portfolio"),
        ("Presentation", "Design presentation"),
        ("Career Preparation", "Architecture interview preparation")
    ],

    "Agricultural Scientist": [
        ("Agricultural Science", "Agricultural fundamentals"),
        ("Crop Science", "Crop production"),
        ("Soil Science", "Soil properties"),
        ("Agricultural Research", "Research methods"),
        ("Data Analysis", "Analyse agricultural data"),
        ("Sustainable Agriculture", "Sustainable farming"),
        ("Field Work", "Practical agricultural experience"),
        ("Research Project", "Agricultural research project"),
        ("Portfolio", "Document research"),
        ("Career Preparation", "Agricultural science preparation")
    ],

    "Environmental Scientist": [
        ("Environmental Science", "Environmental fundamentals"),
        ("Ecology", "Ecosystems"),
        ("Sustainability", "Sustainable practices"),
        ("Environmental Monitoring", "Environmental measurements"),
        ("Data Analysis", "Environmental data"),
        ("Research Methods", "Scientific research"),
        ("Conservation", "Conservation approaches"),
        ("Research Project", "Environmental project"),
        ("Portfolio", "Document research"),
        ("Career Preparation", "Environmental science preparation")
    ],

    "Hotel Manager": [
        ("Hospitality Fundamentals", "Hospitality operations"),
        ("Customer Service", "Guest service"),
        ("Hotel Operations", "Front office and operations"),
        ("Food & Beverage", "Hospitality food service"),
        ("Team Management", "Leadership"),
        ("Communication", "Professional communication"),
        ("Problem Solving", "Handle customer situations"),
        ("Hospitality Project", "Practical hospitality project"),
        ("Portfolio", "Document experience"),
        ("Career Preparation", "Hospitality interview preparation")
    ],

    "Chef": [
        ("Culinary Fundamentals", "Cooking fundamentals"),
        ("Food Safety", "Food-safety practices"),
        ("Kitchen Skills", "Practical kitchen skills"),
        ("Menu Planning", "Menu development"),
        ("Nutrition", "Basic nutrition"),
        ("Kitchen Management", "Kitchen organisation"),
        ("Creativity", "Dish creation and presentation"),
        ("Culinary Project", "Create culinary work"),
        ("Portfolio", "Document dishes"),
        ("Career Preparation", "Culinary interview preparation")
    ],

    "Fitness Trainer": [
        ("Fitness Fundamentals", "Exercise fundamentals"),
        ("Human Anatomy", "Basic anatomy"),
        ("Exercise Science", "Exercise principles"),
        ("Fitness Assessment", "Client assessment"),
        ("Training Plans", "Structured training"),
        ("Nutrition Basics", "General nutrition"),
        ("Client Communication", "Professional communication"),
        ("Practical Training", "Supervised practical experience"),
        ("Portfolio", "Document training work"),
        ("Career Preparation", "Fitness interview preparation")
    ],

    "Sports Coach": [
        ("Sports Fundamentals", "Sport-specific knowledge"),
        ("Coaching Principles", "Effective coaching"),
        ("Training", "Structured training plans"),
        ("Performance Analysis", "Evaluate performance"),
        ("Team Management", "Leadership"),
        ("Communication", "Athlete communication"),
        ("Motivation", "Positive performance support"),
        ("Coaching Project", "Create coaching plans"),
        ("Portfolio", "Document coaching activities"),
        ("Career Preparation", "Coaching interview preparation")
    ]
}


# ============================================================
# CAREER SELECTION
# ============================================================

careers = list(ROADMAPS.keys())

if "learning_career" not in st.session_state:
    st.session_state.learning_career = "Content Creator"

career = st.selectbox(
    "🎯 Target Career",
    careers,
    key="learning_career"
)


# ============================================================
# PREVIOUS-STYLE HEADER
# ============================================================

st.title("🗺️ Personalized Career Journey")

st.write(
    f"Structured learning path for **{career}**"
)

st.divider()

st.subheader(f"🚀 {career} — Career Journey")


# ============================================================
# ROADMAP STEPS
# ============================================================

steps = ROADMAPS[career]

for number, (title, description) in enumerate(steps, start=1):

    col1, col2 = st.columns([0.08, 0.92])

    with col1:
        st.info(str(number))

    with col2:
        st.markdown(f"### {title}")
        st.write(description)

    if number < len(steps):
        st.divider()


# ============================================================
# QUICK ACTION PLAN
# ============================================================

st.divider()

st.subheader("⚡ Quick Action Plan")

st.write(
    f"**Step 1:** Start with {steps[0][0]}."
)

st.write(
    f"**Step 2:** Build your knowledge through {steps[1][0]}."
)

st.write(
    f"**Step 3:** Continue with {steps[2][0]}."
)

st.write(
    f"**Step 4:** Complete practical work related to {career}."
)

st.write(
    f"**Step 5:** Finish with {steps[-1][0]}."
)


# ============================================================
# SAVE SELECTED CAREER / ROADMAP
# ============================================================

try:
    existing = {}

    if ROADMAP_FILE.exists():
        with open(ROADMAP_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)

            if isinstance(loaded, dict):
                existing = loaded

    existing["selected_career"] = career
    existing["career"] = career

    with open(ROADMAP_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)

except Exception:
    pass