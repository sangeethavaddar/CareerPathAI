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
SAVE_FILE = BASE / "data" / "roadmap.json"


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Career Roadmap",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Career Roadmap")
st.caption(
    "A complete journey from education and learning to career and interview preparation."
)


# ============================================================
# LOAD CAREERS
# ============================================================

try:
    careers_df = pd.read_csv(CAREERS_FILE)
except Exception as error:
    st.error("Unable to load data/careers.csv")
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
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            profile = json.load(file)
    except Exception:
        profile = {}

preferred_domain = str(
    profile.get("preferred_domain", "")
).strip()


# ============================================================
# LOAD SAVED CAREER
# ============================================================

saved_career = ""

if SAVE_FILE.exists():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            saved_career = str(
                json.load(file).get("career", "")
            ).strip()
    except Exception:
        saved_career = ""


# ============================================================
# DEFAULT CAREER
# ============================================================

if saved_career in careers:

    default_career = saved_career

else:

    domain_matches = []

    for _, row in careers_df.iterrows():

        row_domain = str(
            row.get("domain", "")
        ).strip()

        row_career = str(
            row.get("career", "")
        ).strip()

        if (
            row_domain.lower() == preferred_domain.lower()
            and row_career in careers
        ):
            domain_matches.append(row_career)

    default_career = (
        domain_matches[0]
        if domain_matches
        else careers[0]
    )


# ============================================================
# SELECT CAREER
# ============================================================

selected_career = st.selectbox(
    "🎯 Select Career",
    careers,
    index=careers.index(default_career)
)


# ============================================================
# SAVE CAREER
# ============================================================

try:
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"career": selected_career},
            file,
            indent=4
        )
except Exception:
    pass


# ============================================================
# CAREER DATA
# ============================================================

career_rows = careers_df[
    careers_df["career"].astype(str).str.strip()
    == selected_career
]

if career_rows.empty:
    st.error("Selected career was not found.")
    st.stop()

career_data = career_rows.iloc[0]

domain = str(
    career_data.get("domain", "")
).strip()

csv_skills = str(
    career_data.get("skills", "")
).strip()

csv_education = str(
    career_data.get("education", "")
).strip()

csv_experience = str(
    career_data.get("experience", "")
).strip()

csv_description = str(
    career_data.get("description", "")
).strip()


# ============================================================
# DETAILED CAREER GUIDANCE
# ============================================================

GUIDANCE = {

# ------------------------------------------------------------
# TECHNOLOGY
# ------------------------------------------------------------

"Software Developer": {
    "education":
        "A degree or diploma in Computer Science, Computer Engineering, Information Technology or a related field is a common pathway.",
    "learn":
        "Programming, Object-Oriented Programming, Data Structures, Algorithms, SQL, databases, Git, APIs, debugging, testing and software engineering.",
    "subjects":
        "Programming, Data Structures, Algorithms, Database Management, Operating Systems, Computer Networks and Software Engineering.",
    "skills":
        "Python/Java, SQL, Git, problem solving, debugging, API development and application development.",
    "practice":
        "Build applications such as a complaint management system, e-commerce application, student portal or career guidance system.",
    "entry_role":
        "Software Developer Intern, Junior Software Developer, Graduate Developer or Associate Software Engineer.",
    "advanced":
        "Learn system design, cloud deployment, security, scalable architecture and advanced backend/frontend development.",
    "interview":
        "Prepare programming problems, DSA, OOP, SQL, project explanation, debugging questions, Git and behavioral questions."
},

"Data Analyst": {
    "education":
        "A degree in Computer Science, Statistics, Mathematics, Economics, Business or another data-related field can provide a suitable foundation.",
    "learn":
        "Excel, SQL, statistics, Python, Pandas, data cleaning, data visualization, dashboards and business analysis.",
    "subjects":
        "Statistics, Mathematics, Database Management, Business Analytics and Programming.",
    "skills":
        "Excel, SQL, Python, Pandas, visualization, analytical thinking and communication.",
    "practice":
        "Analyze sales, student, finance, customer or other real datasets and create dashboards.",
    "entry_role":
        "Data Analyst Intern, Junior Data Analyst, Reporting Analyst or Business Data Analyst.",
    "advanced":
        "Learn advanced statistics, predictive analytics, automation and machine learning.",
    "interview":
        "Prepare SQL queries, Excel tasks, statistics, dashboard questions, data interpretation and case studies."
},

"Data Scientist": {
    "education":
        "A degree in Computer Science, Data Science, Statistics, Mathematics, Engineering or a related quantitative field is useful.",
    "learn":
        "Python, statistics, probability, SQL, Pandas, NumPy, visualization, machine learning and model evaluation.",
    "subjects":
        "Statistics, Probability, Mathematics, Programming, Databases and Machine Learning.",
    "skills":
        "Python, SQL, statistics, Pandas, machine learning, data visualization and analytical thinking.",
    "practice":
        "Work with real datasets and build prediction, classification, clustering or recommendation projects.",
    "entry_role":
        "Data Science Intern, Junior Data Scientist, Data Analyst or Machine Learning Intern.",
    "advanced":
        "Learn deep learning, NLP, computer vision, MLOps and advanced machine learning.",
    "interview":
        "Prepare statistics, ML algorithms, SQL, Python, model evaluation, case studies and project discussions."
},

"AI Engineer": {
    "education":
        "A degree in Computer Science, Artificial Intelligence, Data Science, Engineering or a related technical field is a common pathway.",
    "learn":
        "Python, mathematics, statistics, machine learning, deep learning, NLP, computer vision, generative AI and model deployment.",
    "subjects":
        "Programming, Mathematics, Statistics, Machine Learning, Deep Learning and Artificial Intelligence.",
    "skills":
        "Python, SQL, machine learning, deep learning, data analysis, Git and AI application development.",
    "practice":
        "Build AI applications such as prediction systems, recommendation systems, computer vision or AI assistants.",
    "entry_role":
        "AI/ML Intern, Junior AI Engineer, Machine Learning Engineer or AI Application Developer.",
    "advanced":
        "Learn transformers, LLMs, RAG, model evaluation, MLOps, cloud AI and production AI systems.",
    "interview":
        "Prepare Python, ML concepts, neural networks, AI system design, projects, model evaluation and behavioral questions."
},

"Web Developer": {
    "education":
        "A degree or diploma in Computer Science, IT, Web Development or a related field can be useful, although strong projects can also demonstrate practical ability.",
    "learn":
        "HTML, CSS, JavaScript, frontend development, backend development, APIs, databases and deployment.",
    "subjects":
        "Web Technology, Programming, Databases, Computer Networks and Software Engineering.",
    "skills":
        "HTML, CSS, JavaScript, backend programming, SQL, Git and API development.",
    "practice":
        "Build responsive websites and complete full-stack applications.",
    "entry_role":
        "Web Developer Intern, Frontend Developer, Backend Developer or Junior Full-Stack Developer.",
    "advanced":
        "Learn React or another frontend framework, advanced backend development, cloud and application security.",
    "interview":
        "Prepare HTML, CSS, JavaScript, APIs, SQL, debugging, projects and frontend/backend practical questions."
},

"Cybersecurity Analyst": {
    "education":
        "A degree or diploma in Cybersecurity, Computer Science, Information Technology or a related field is a common pathway.",
    "learn":
        "Networking, operating systems, security fundamentals, authentication, vulnerabilities, monitoring and incident response.",
    "subjects":
        "Computer Networks, Operating Systems, Cryptography, Cybersecurity and Information Security.",
    "skills":
        "Networking, Linux, security analysis, log analysis, vulnerability assessment and problem solving.",
    "practice":
        "Build safe cybersecurity labs, analyze logs and practice defensive security techniques in authorized environments.",
    "entry_role":
        "Cybersecurity Intern, SOC Analyst, Junior Security Analyst or Security Operations Trainee.",
    "advanced":
        "Learn cloud security, application security, threat detection, security automation and incident response.",
    "interview":
        "Prepare networking, security concepts, authentication, vulnerabilities, incident scenarios and project questions."
},

"Cloud Engineer": {
    "education":
        "A degree or diploma in Computer Science, IT, Computer Engineering or a related technical field is a common pathway.",
    "learn":
        "Linux, networking, cloud computing, storage, databases, virtualization, containers and automation.",
    "subjects":
        "Computer Networks, Operating Systems, Cloud Computing, Databases and Distributed Systems.",
    "skills":
        "Linux, networking, cloud platforms, Git, scripting, containers and deployment.",
    "practice":
        "Deploy applications, configure cloud resources and create small cloud infrastructure projects.",
    "entry_role":
        "Cloud Intern, Junior Cloud Engineer, Cloud Support Associate or DevOps Trainee.",
    "advanced":
        "Learn Kubernetes, infrastructure automation, CI/CD, cloud architecture and cloud security.",
    "interview":
        "Prepare networking, Linux, cloud concepts, deployment scenarios, troubleshooting and project questions."
},

# ------------------------------------------------------------
# ENGINEERING
# ------------------------------------------------------------

"Mechanical Engineer": {
    "education":
        "A bachelor's degree in Mechanical Engineering or an appropriate engineering qualification is a common pathway.",
    "learn":
        "Engineering mechanics, thermodynamics, materials, machine design, manufacturing, CAD and engineering analysis.",
    "subjects":
        "Engineering Mathematics, Mechanics, Thermodynamics, Fluid Mechanics, Machine Design and Manufacturing.",
    "skills":
        "CAD, mechanical design, problem solving, engineering analysis and technical documentation.",
    "practice":
        "Create CAD models, mechanical designs, simulations and manufacturing-related projects.",
    "entry_role":
        "Graduate Mechanical Engineer, Design Engineer, Production Engineer or Quality Engineer.",
    "advanced":
        "Develop specialization in design, manufacturing, automotive, robotics, thermal systems or other areas.",
    "interview":
        "Prepare engineering fundamentals, CAD, design problems, projects, manufacturing and behavioral questions."
},

"Civil Engineer": {
    "education":
        "A bachelor's degree in Civil Engineering or an appropriate civil engineering qualification is a common pathway.",
    "learn":
        "Structural concepts, construction, surveying, materials, CAD, estimation and project management.",
    "subjects":
        "Engineering Mechanics, Structural Engineering, Surveying, Construction, Geotechnical Engineering and Transportation.",
    "skills":
        "AutoCAD/CAD, surveying, estimation, structural understanding and project coordination.",
    "practice":
        "Work on drawings, surveying exercises, structural projects and construction planning.",
    "entry_role":
        "Graduate Civil Engineer, Site Engineer, Design Engineer or Project Engineer.",
    "advanced":
        "Specialize in structural engineering, transportation, construction, environmental or geotechnical engineering.",
    "interview":
        "Prepare core civil subjects, drawings, project experience, site scenarios and technical questions."
},

"Electrical Engineer": {
    "education":
        "A bachelor's degree in Electrical Engineering or an appropriate electrical engineering qualification is a common pathway.",
    "learn":
        "Circuit analysis, electrical machines, power systems, control systems and electrical safety.",
    "subjects":
        "Circuit Theory, Electrical Machines, Power Systems, Control Systems and Power Electronics.",
    "skills":
        "Circuit analysis, electrical design, simulation, troubleshooting and technical documentation.",
    "practice":
        "Build circuit projects, simulations and electrical system designs.",
    "entry_role":
        "Graduate Electrical Engineer, Design Engineer, Maintenance Engineer or Electrical Project Engineer.",
    "advanced":
        "Specialize in power systems, automation, renewable energy, control or electrical design.",
    "interview":
        "Prepare circuits, machines, power systems, control concepts, projects and troubleshooting scenarios."
},

"Electronics Engineer": {
    "education":
        "A bachelor's degree in Electronics, Electronics and Communication Engineering or a related field is a common pathway.",
    "learn":
        "Electronic circuits, digital electronics, microcontrollers, embedded systems, communication and IoT.",
    "subjects":
        "Analog Electronics, Digital Electronics, Microprocessors, Embedded Systems and Communication Systems.",
    "skills":
        "Circuit design, microcontrollers, embedded programming, sensors and troubleshooting.",
    "practice":
        "Build embedded systems, sensor projects, IoT projects and microcontroller applications.",
    "entry_role":
        "Embedded Intern, Electronics Engineer, Hardware Engineer or IoT Developer.",
    "advanced":
        "Learn embedded Linux, robotics, advanced IoT, automation and edge AI.",
    "interview":
        "Prepare electronics fundamentals, microcontrollers, circuits, projects and troubleshooting questions."
},

# ------------------------------------------------------------
# HEALTHCARE
# ------------------------------------------------------------

"Doctor": {
    "education":
        "Follow the medical education pathway required in your country. In India, this normally involves the appropriate medical degree and required professional registration.",
    "learn":
        "Anatomy, physiology, biochemistry, pathology, pharmacology, microbiology, medicine, surgery and clinical practice.",
    "subjects":
        "Pre-clinical, para-clinical and clinical medical subjects.",
    "skills":
        "Clinical knowledge, communication, patient assessment, teamwork, ethics and decision-making.",
    "practice":
        "Complete required supervised clinical training, rotations and practical experience as part of medical education.",
    "entry_role":
        "After completing the required qualification and registration, pursue an appropriate medical role or further specialization.",
    "advanced":
        "Choose a medical specialty and continue professional education and clinical development.",
    "interview":
        "Prepare medical fundamentals, clinical reasoning, communication, ethics, professional scenarios and career motivation."
},

"Nurse": {
    "education":
        "Complete an approved nursing education pathway and the professional registration or licensing requirements applicable to your location.",
    "learn":
        "Anatomy, physiology, nursing fundamentals, patient care, medical-surgical nursing and healthcare ethics.",
    "subjects":
        "Nursing fundamentals, anatomy, physiology, pharmacology, medical-surgical nursing and community health.",
    "skills":
        "Patient care, communication, observation, teamwork, documentation and professional responsibility.",
    "practice":
        "Complete supervised clinical training and develop practical nursing skills in appropriate healthcare environments.",
    "entry_role":
        "Nursing graduate, staff nurse or another entry-level nursing role appropriate to your qualification and registration.",
    "advanced":
        "Explore critical care, pediatric nursing, community health or other nursing specializations.",
    "interview":
        "Prepare nursing fundamentals, patient-care scenarios, communication, ethics and situation-based questions."
},

"Pharmacist": {
    "education":
        "Complete an approved pharmacy qualification and the registration or licensing requirements applicable to your location.",
    "learn":
        "Pharmaceutical chemistry, pharmacology, pharmaceutics, drug safety and clinical pharmacy.",
    "subjects":
        "Pharmaceutics, pharmacology, pharmaceutical chemistry, microbiology and clinical pharmacy.",
    "skills":
        "Medication knowledge, accuracy, communication, documentation and patient-focused practice.",
    "practice":
        "Complete required practical or supervised training and gain experience in an appropriate pharmacy environment.",
    "entry_role":
        "Pharmacy graduate, pharmacist or suitable entry-level pharmacy role according to qualification and registration.",
    "advanced":
        "Explore clinical pharmacy, hospital pharmacy, pharmaceutical industry, research or other specializations.",
    "interview":
        "Prepare pharmacology, medicine safety, patient communication, professional ethics and practical scenarios."
},

"Physiotherapist": {
    "education":
        "Complete an approved physiotherapy education pathway and meet the applicable professional registration requirements.",
    "learn":
        "Anatomy, physiology, biomechanics, kinesiology, assessment, exercise therapy and rehabilitation.",
    "subjects":
        "Anatomy, physiology, biomechanics, exercise therapy, rehabilitation and clinical practice.",
    "skills":
        "Patient assessment, exercise instruction, communication, observation and treatment planning.",
    "practice":
        "Complete supervised clinical training and gain practical rehabilitation experience.",
    "entry_role":
        "Physiotherapy graduate or entry-level physiotherapy role according to qualification requirements.",
    "advanced":
        "Specialize in areas such as sports, orthopedic, neurological or rehabilitation practice.",
    "interview":
        "Prepare anatomy, assessment, rehabilitation concepts, patient scenarios, communication and professional ethics."
},

# ------------------------------------------------------------
# FINANCE
# ------------------------------------------------------------

"Accountant": {
    "education":
        "A degree or appropriate accounting qualification in commerce, accounting, finance or a related field is a common starting point.",
    "learn":
        "Accounting principles, financial statements, taxation, auditing, Excel and accounting software.",
    "subjects":
        "Financial Accounting, Cost Accounting, Taxation, Auditing, Business Law and Financial Management.",
    "skills":
        "Excel, accounting software, financial reporting, attention to detail and analytical thinking.",
    "practice":
        "Practice preparing financial statements, recording transactions and analyzing financial information.",
    "entry_role":
        "Accounts Intern, Junior Accountant, Accounts Executive or Finance Assistant.",
    "advanced":
        "Develop expertise in taxation, auditing, financial analysis or professional accounting qualifications.",
    "interview":
        "Prepare accounting fundamentals, journal entries, financial statements, Excel, taxation and practical scenarios."
},

"Financial Analyst": {
    "education":
        "A degree in Finance, Commerce, Economics, Mathematics, Business or a related field can provide a suitable foundation.",
    "learn":
        "Financial statements, Excel, financial modeling, valuation, financial ratios and data analysis.",
    "subjects":
        "Accounting, Financial Management, Economics, Statistics and Investment Analysis.",
    "skills":
        "Excel, financial modeling, analysis, research and communication.",
    "practice":
        "Analyze companies, build financial models and prepare financial research reports.",
    "entry_role":
        "Finance Intern, Junior Financial Analyst, Research Analyst or Financial Planning Assistant.",
    "advanced":
        "Learn valuation, investment analysis, forecasting and advanced financial modeling.",
    "interview":
        "Prepare accounting, valuation, financial ratios, Excel, case studies and market-related questions."
},

"Investment Analyst": {
    "education":
        "A degree in Finance, Economics, Commerce, Mathematics or a related field can provide a suitable foundation.",
    "learn":
        "Financial markets, accounting, company analysis, valuation, investment research and risk.",
    "subjects":
        "Financial Markets, Accounting, Economics, Investment Analysis and Statistics.",
    "skills":
        "Financial modeling, valuation, research, analytical thinking and communication.",
    "practice":
        "Create company research reports, valuation models and investment analysis projects.",
    "entry_role":
        "Investment Research Intern, Junior Research Analyst or Investment Analyst trainee.",
    "advanced":
        "Develop advanced valuation, portfolio analysis, risk analysis and investment research skills.",
    "interview":
        "Prepare financial concepts, valuation, accounting, market questions, case studies and analytical reasoning."
},

# ------------------------------------------------------------
# BUSINESS
# ------------------------------------------------------------

"Marketing Manager": {
    "education":
        "A degree in Marketing, Business Administration, Commerce, Communications or a related field is a common foundation.",
    "learn":
        "Marketing principles, consumer behavior, branding, digital marketing, market research and analytics.",
    "subjects":
        "Marketing, Business Management, Consumer Behavior, Market Research and Digital Marketing.",
    "skills":
        "Communication, content strategy, analytics, campaign planning, creativity and leadership.",
    "practice":
        "Create marketing campaigns, analyze audiences, develop content strategies and measure campaign results.",
    "entry_role":
        "Marketing Intern, Marketing Executive, Digital Marketing Associate or Marketing Coordinator.",
    "advanced":
        "Develop expertise in brand management, growth marketing, performance marketing or strategic marketing.",
    "interview":
        "Prepare marketing concepts, campaign case studies, KPIs, communication questions and problem-solving scenarios."
},

"Business Analyst": {
    "education":
        "A degree in Business, Computer Science, Economics, Engineering, Finance or a related field can be useful.",
    "learn":
        "Business processes, requirements analysis, Excel, SQL, data analysis, process modeling and communication.",
    "subjects":
        "Business Management, Statistics, Databases, Business Analytics and Project Management.",
    "skills":
        "Analytical thinking, communication, requirements gathering, Excel, SQL and presentation.",
    "practice":
        "Analyze business problems, document requirements, create process diagrams and develop data-driven recommendations.",
    "entry_role":
        "Business Analyst Intern, Junior Business Analyst, Process Analyst or Business Operations Analyst.",
    "advanced":
        "Learn strategic analysis, product analysis, process improvement and advanced analytics.",
    "interview":
        "Prepare case studies, requirements questions, SQL/Excel, process analysis and stakeholder scenarios."
},

"Human Resources Manager": {
    "education":
        "A degree in Human Resources, Business Administration, Psychology, Commerce or a related field is a common pathway.",
    "learn":
        "Recruitment, employee relations, training, performance management, HR policies and HR analytics.",
    "subjects":
        "Human Resource Management, Organizational Behavior, Business Management, Employment Practices and HR Analytics.",
    "skills":
        "Communication, interviewing, conflict resolution, organization, data analysis and leadership.",
    "practice":
        "Practice recruitment workflows, interview planning, employee engagement activities and HR reporting.",
    "entry_role":
        "HR Intern, HR Executive, Recruitment Coordinator or HR Assistant.",
    "advanced":
        "Develop expertise in talent management, HR analytics, organizational development and HR leadership.",
    "interview":
        "Prepare recruitment scenarios, employee relations, communication, conflict management and behavioral questions."
},

"Entrepreneur": {
    "education":
        "There is no single mandatory educational route for entrepreneurship. Business, technology, finance, marketing or industry knowledge can be useful.",
    "learn":
        "Problem identification, market research, business models, finance, marketing, sales and operations.",
    "subjects":
        "Business Management, Finance, Marketing, Economics and Entrepreneurship.",
    "skills":
        "Communication, leadership, decision-making, financial thinking, creativity and problem solving.",
    "practice":
        "Identify a real problem, validate customer needs and develop a small product or service.",
    "entry_role":
        "Founder, co-founder, startup project lead or entrepreneur.",
    "advanced":
        "Learn business scaling, leadership, investment, operations and strategic management.",
    "interview":
        "Prepare your business idea, customer problem, solution, market, business model, competition and growth plan."
},

# ------------------------------------------------------------
# EDUCATION
# ------------------------------------------------------------

"Teacher": {
    "education":
        "Choose the teacher-education pathway required for the subject and school level you want to teach. In India, this commonly involves an appropriate bachelor's degree and teacher-education qualification such as B.Ed., depending on the role and eligibility requirements.",
    "learn":
        "Your teaching subject, pedagogy, lesson planning, classroom management, educational psychology, assessment and communication.",
    "subjects":
        "First develop strong subject knowledge. Then study teaching methods, educational psychology, classroom management, assessment and educational technology.",
    "skills":
        "Clear communication, explanation, patience, classroom management, lesson planning, assessment and presentation.",
    "practice":
        "Prepare lesson plans, practice explaining topics, conduct supervised teaching practice and create teaching materials.",
    "entry_role":
        "Teacher trainee, teaching intern, assistant teacher or eligible school-teaching role depending on your qualification and local requirements.",
    "advanced":
        "Develop specialization in a subject, educational technology, curriculum development, mentoring or academic leadership.",
    "interview":
        "Prepare self-introduction, subject questions, lesson-plan questions, classroom situations, student-management scenarios and why you want to become a teacher."
},

"Professor": {
    "education":
        "Higher-education teaching generally requires advanced qualifications in the relevant subject and may require additional eligibility, research or professional requirements depending on the institution and country.",
    "learn":
        "Advanced subject knowledge, research methods, academic writing, teaching methods, assessment and presentation.",
    "subjects":
        "Your specialization, research methodology, statistics or analytical methods where applicable, pedagogy and academic writing.",
    "skills":
        "Teaching, research, presentation, academic writing, mentoring and communication.",
    "practice":
        "Conduct research, write academic work, participate in seminars and develop teaching or mentoring experience.",
    "entry_role":
        "Teaching assistant, lecturer or other academic role depending on qualification and institutional requirements.",
    "advanced":
        "Develop research specialization, publications, academic leadership and advanced teaching expertise.",
    "interview":
        "Prepare subject expertise, teaching demonstration, research interests, academic projects, publications and professional goals."
},

# ------------------------------------------------------------
# LAW
# ------------------------------------------------------------

"Lawyer": {
    "education":
        "Complete the law education pathway and professional qualification or licensing requirements applicable to your location.",
    "learn":
        "Constitutional principles, contracts, civil law, criminal law, legal research, legal writing and professional ethics.",
    "subjects":
        "Core legal subjects followed by specialization in an area of law.",
    "skills":
        "Legal research, analysis, writing, communication, negotiation and presentation.",
    "practice":
        "Analyze cases, prepare legal documents, conduct legal research and gain appropriate supervised practical exposure.",
    "entry_role":
        "Legal intern, trainee or entry-level legal role according to your qualification and local professional requirements.",
    "advanced":
        "Specialize in corporate, criminal, civil, technology, intellectual property or another area of law.",
    "interview":
        "Prepare legal concepts, case analysis, reasoning, communication, ethics and questions about your chosen specialization."
},

# ------------------------------------------------------------
# MEDIA
# ------------------------------------------------------------

"Journalist": {
    "education":
        "A degree or diploma in Journalism, Mass Communication, Media Studies or a related field can provide a strong foundation.",
    "learn":
        "Reporting, research, interviewing, news writing, media ethics, fact checking and digital journalism.",
    "subjects":
        "Journalism, Mass Communication, Media Ethics, Writing, Reporting and Digital Media.",
    "skills":
        "Writing, interviewing, research, communication, fact checking and storytelling.",
    "practice":
        "Create news reports, conduct interviews, write articles and build a portfolio of responsible journalism work.",
    "entry_role":
        "Journalism Intern, Reporter, Content Writer, Editorial Assistant or Digital Journalist.",
    "advanced":
        "Develop investigative journalism, specialized reporting, multimedia journalism or editorial leadership.",
    "interview":
        "Prepare writing samples, current-affairs discussion, reporting scenarios, ethics questions and portfolio explanation."
},

"Content Creator": {
    "education":
        "There is no single mandatory degree. Education in Media, Communication, Design, Marketing or a related field can be useful.",
    "learn":
        "Storytelling, scripting, photography, video, editing, social media, audience research and content strategy.",
    "subjects":
        "Communication, Media, Marketing, Design, Video Production and Digital Media.",
    "skills":
        "Writing, video editing, design, communication, creativity, audience analysis and consistency.",
    "practice":
        "Create videos, articles, social posts, educational content or other portfolio pieces and measure audience response.",
    "entry_role":
        "Content Intern, Social Media Assistant, Content Creator, Video Content Assistant or Digital Content Executive.",
    "advanced":
        "Develop personal branding, content strategy, analytics, monetization and professional collaborations.",
    "interview":
        "Prepare your portfolio, explain content decisions, audience strategy, performance metrics and creative process."
},

# ------------------------------------------------------------
# DESIGN
# ------------------------------------------------------------

"Graphic Designer": {
    "education":
        "A degree or diploma in Graphic Design, Visual Communication, Fine Arts or a related field can be useful.",
    "learn":
        "Design principles, typography, color, composition, branding, digital design and professional design software.",
    "subjects":
        "Graphic Design, Typography, Visual Communication, Illustration and Digital Design.",
    "skills":
        "Visual design, creativity, typography, layout, software proficiency and communication.",
    "practice":
        "Create logos, posters, social media designs, brand identities and other portfolio projects.",
    "entry_role":
        "Graphic Design Intern, Junior Graphic Designer, Visual Designer or Design Assistant.",
    "advanced":
        "Develop expertise in branding, UI design, motion graphics, illustration or art direction.",
    "interview":
        "Prepare your portfolio, explain design decisions, handle feedback and discuss your design process."
},

"UI UX Designer": {
    "education":
        "A degree or diploma in Design, Computer Science, Human-Computer Interaction, Visual Communication or a related field can be useful.",
    "learn":
        "User research, information architecture, wireframing, prototyping, usability testing and visual design.",
    "subjects":
        "Design, Human-Computer Interaction, User Research, Visual Design and Interaction Design.",
    "skills":
        "Figma or similar tools, user research, wireframing, prototyping and communication.",
    "practice":
        "Redesign existing interfaces, conduct user research and create complete UX case studies.",
    "entry_role":
        "UI/UX Intern, Junior UX Designer, UI Designer or Product Design Intern.",
    "advanced":
        "Learn design systems, accessibility, product strategy and advanced user research.",
    "interview":
        "Prepare portfolio case studies, design challenges, user research questions and explain your design decisions."
},

# ------------------------------------------------------------
# ARCHITECTURE
# ------------------------------------------------------------

"Architect": {
    "education":
        "Complete the recognized architecture education and professional requirements applicable to your location.",
    "learn":
        "Architectural design, drawing, building technology, materials, CAD/BIM, structures and sustainable design.",
    "subjects":
        "Architectural Design, Building Construction, Architectural Graphics, Structures and Environmental Design.",
    "skills":
        "Drawing, design thinking, CAD/BIM, visualization, communication and project documentation.",
    "practice":
        "Create design projects, architectural drawings, models and portfolio presentations.",
    "entry_role":
        "Architecture Intern, Junior Architectural Designer or trainee role according to qualification requirements.",
    "advanced":
        "Specialize in sustainable design, urban design, interiors, BIM, landscape or another architectural area.",
    "interview":
        "Prepare your portfolio, explain design concepts, drawings, software skills, projects and design decisions."
},

# ------------------------------------------------------------
# AGRICULTURE / ENVIRONMENT
# ------------------------------------------------------------

"Agricultural Scientist": {
    "education":
        "A degree in Agricultural Science, Agronomy, Horticulture, Soil Science or a related agricultural field can provide a foundation.",
    "learn":
        "Crop science, soil science, plant biology, agricultural technology, research methods and data analysis.",
    "subjects":
        "Agronomy, Soil Science, Plant Science, Agricultural Economics and Agricultural Technology.",
    "skills":
        "Research, field observation, data analysis, scientific writing and agricultural technology.",
    "practice":
        "Conduct field studies, agricultural experiments, crop analysis or technology-based agriculture projects.",
    "entry_role":
        "Agricultural Research Intern, Field Assistant, Research Assistant or suitable entry-level agricultural role.",
    "advanced":
        "Specialize in crop science, soil science, agricultural technology, biotechnology or sustainable agriculture.",
    "interview":
        "Prepare agricultural fundamentals, project work, research methods, field scenarios and scientific reasoning."
},

"Environmental Scientist": {
    "education":
        "A degree in Environmental Science, Environmental Engineering, Biology, Chemistry or a related field can provide a foundation.",
    "learn":
        "Ecology, environmental monitoring, pollution, conservation, sustainability, data analysis and environmental assessment.",
    "subjects":
        "Environmental Science, Ecology, Chemistry, Biology, Statistics and Environmental Management.",
    "skills":
        "Research, data analysis, field observation, scientific reporting and environmental assessment.",
    "practice":
        "Work on environmental monitoring, pollution analysis, biodiversity or sustainability projects.",
    "entry_role":
        "Environmental Intern, Research Assistant, Environmental Analyst or Field Assistant.",
    "advanced":
        "Develop specialization in conservation, climate, pollution control, environmental assessment or sustainability.",
    "interview":
        "Prepare environmental concepts, project explanation, data interpretation and field-based scenarios."
},

# ------------------------------------------------------------
# HOSPITALITY
# ------------------------------------------------------------

"Hotel Manager": {
    "education":
        "A degree or diploma in Hotel Management, Hospitality Management, Tourism or a related field can provide a suitable foundation.",
    "learn":
        "Front office, housekeeping, food and beverage, customer service, hotel operations, finance and leadership.",
    "subjects":
        "Hospitality Management, Food and Beverage, Front Office, Housekeeping and Hotel Operations.",
    "skills":
        "Communication, customer service, organization, leadership, problem solving and financial awareness.",
    "practice":
        "Gain practical hospitality experience through training, internships and supervised hotel operations.",
    "entry_role":
        "Hotel Management Intern, Front Office Executive, Guest Relations Executive or Operations Trainee.",
    "advanced":
        "Develop expertise in hotel operations, revenue management, food and beverage or hospitality leadership.",
    "interview":
        "Prepare customer-service scenarios, conflict handling, hotel operations, leadership and hospitality questions."
},

"Chef": {
    "education":
        "A culinary arts or hospitality qualification can provide a structured pathway, although practical culinary training is also important.",
    "learn":
        "Food safety, kitchen techniques, ingredients, cuisines, menu planning, costing and kitchen management.",
    "subjects":
        "Culinary Arts, Food Safety, Nutrition, Kitchen Operations and Menu Planning.",
    "skills":
        "Cooking, food presentation, time management, hygiene, creativity and teamwork.",
    "practice":
        "Practice cooking techniques and gain supervised experience in professional kitchen environments.",
    "entry_role":
        "Kitchen Trainee, Commis Chef or other appropriate entry-level culinary role.",
    "advanced":
        "Specialize in a cuisine or develop expertise in pastry, restaurant management or culinary leadership.",
    "interview":
        "Prepare practical cooking questions, food safety, menu planning, teamwork and portfolio/work-experience discussion."
},

# ------------------------------------------------------------
# SPORTS
# ------------------------------------------------------------

"Fitness Trainer": {
    "education":
        "Relevant fitness, exercise science, sports science or recognized professional training can provide a foundation. Follow applicable certification requirements.",
    "learn":
        "Anatomy, exercise science, fitness assessment, exercise programming, strength, endurance and mobility.",
    "subjects":
        "Anatomy, Exercise Science, Fitness Training, Nutrition basics and Sports Science.",
    "skills":
        "Exercise instruction, communication, observation, planning and client management.",
    "practice":
        "Develop safe exercise programs and gain supervised practical coaching experience.",
    "entry_role":
        "Fitness Trainer Intern, Gym Trainer, Fitness Coach or suitable entry-level role.",
    "advanced":
        "Specialize in strength and conditioning, sports fitness, rehabilitation support or another area within your qualifications.",
    "interview":
        "Prepare exercise principles, client scenarios, communication, safety and professional certification questions."
},

"Sports Coach": {
    "education":
        "Build education or recognized training in your chosen sport and follow the relevant coaching requirements.",
    "learn":
        "Sport-specific techniques, training principles, athlete development, performance analysis and coaching methods.",
    "subjects":
        "Sports Science, Coaching, Exercise Physiology, Sport Psychology and sport-specific knowledge.",
    "skills":
        "Leadership, communication, observation, training planning and performance analysis.",
    "practice":
        "Coach athletes under appropriate supervision and develop training sessions and performance plans.",
    "entry_role":
        "Assistant Coach, Sports Coach Trainee or other entry-level coaching role.",
    "advanced":
        "Develop advanced coaching strategy, performance analysis and specialization in your chosen sport.",
    "interview":
        "Prepare coaching scenarios, athlete development plans, leadership questions and sport-specific knowledge."
}

}


# ============================================================
# GET CAREER GUIDANCE
# ============================================================

guidance = GUIDANCE.get(selected_career)


# ============================================================
# FALLBACK
# ============================================================

if guidance is None:

    guidance = {
        "education":
            csv_education if csv_education else
            "Identify the recognized education or qualification required for this career in your location.",

        "learn":
            "Study the fundamental knowledge, technical skills and professional concepts required for this career.",

        "subjects":
            "Identify the major subjects related to this career and build strong fundamentals in each one.",

        "skills":
            csv_skills if csv_skills else
            "Develop communication, problem solving, technical and professional skills relevant to the career.",

        "practice":
            "Build practical projects, complete training and gain supervised experience related to the career.",

        "entry_role":
            f"Look for internships, trainee positions and entry-level opportunities related to {selected_career}.",

        "advanced":
            f"After gaining the fundamentals, specialize in an advanced area of {selected_career}.",

        "interview":
            f"Prepare technical questions, project explanations, behavioral questions and career-specific scenarios for {selected_career}."
    }


# ============================================================
# CAREER OVERVIEW
# ============================================================

st.subheader(f"🎯 {selected_career}")

if csv_description:
    st.info(csv_description)

overview_col1, overview_col2 = st.columns(2)

with overview_col1:
    st.write(
        f"**Domain:** {domain if domain else 'Not specified'}"
    )

    st.write(
        f"**Education in database:** "
        f"{csv_education if csv_education else 'Not specified'}"
    )

with overview_col2:
    st.write(
        f"**Skills in database:** "
        f"{csv_skills if csv_skills else 'Not specified'}"
    )

    st.write(
        f"**Experience:** "
        f"{csv_experience if csv_experience else 'Not specified'}"
    )


# ============================================================
# COMPLETE JOURNEY
# ============================================================

st.subheader("🚀 Complete Career Journey")

st.write(
    f"Follow these stages from the beginning of your journey "
    f"toward becoming a **{selected_career}**."
)


st.markdown("### 1️⃣ Understand the Career")

st.write(
    f"Before starting, understand what a **{selected_career}** "
    f"actually does, what type of workplace they work in, "
    f"what responsibilities they have and what employers "
    f"normally expect."
)


st.markdown("### 2️⃣ 🎓 Education and Qualification")

st.write(
    guidance["education"]
)

st.markdown(
    "**Your action:** Identify the appropriate course or "
    "qualification, check the entry requirements and create "
    "a realistic education plan."
)


st.markdown("### 3️⃣ 📚 What You Need to Study")

st.write(
    guidance["subjects"]
)

st.write(
    f"**Main learning areas:** {guidance['learn']}"
)


st.markdown("### 4️⃣ 🧠 Skills You Need to Develop")

st.write(
    guidance["skills"]
)

st.write(
    "**Your action:** Learn one skill at a time, practice it "
    "regularly and keep evidence of your progress through "
    "projects, assignments or practical work."
)


st.markdown("### 5️⃣ 🛠️ Practical Experience")

st.write(
    guidance["practice"]
)

st.write(
    "**Your action:** Do practical work instead of studying "
    "only theory. Build projects, complete training or gain "
    "appropriate supervised experience."
)


st.markdown("### 6️⃣ 💼 First Job / Entry-Level Role")

st.write(
    guidance["entry_role"]
)

st.write(
    "**Your action:** Search for internships, trainee positions "
    "and entry-level opportunities after meeting the required "
    "qualification or eligibility."
)


st.markdown("### 7️⃣ 📈 Grow Your Career")

st.write(
    guidance["advanced"]
)

st.write(
    "**Your action:** Choose a specialization, improve your "
    "professional skills and continue learning as the industry changes."
)


st.markdown("### 8️⃣ 📄 Resume and Portfolio")

st.write(
    f"Create a resume focused on **{selected_career}**. "
    "Include your education, relevant skills, projects, "
    "training, certifications and practical experience."
)

st.write(
    "Create a portfolio where appropriate. Show what you "
    "built, researched, designed, analyzed or accomplished "
    "instead of only listing skills."
)


st.markdown("### 9️⃣ 🎤 Interview Preparation")

st.write(
    guidance["interview"]
)

st.write(
    "**Practice these areas:** self-introduction, education, "
    "skills, projects, strengths, weaknesses, career goals, "
    "technical questions and real-world situations."
)


st.markdown("### 🔟 🏆 Career Ready")

st.write(
    f"You are moving toward being career-ready for "
    f"**{selected_career}** when you have the required "
    "qualification, strong foundational knowledge, relevant "
    "skills, practical experience, a professional resume/"
    "portfolio and interview preparation."
)


# ============================================================
# QUICK ACTION PLAN
# ============================================================

st.subheader("📌 What You Should Do First")

st.write(
    f"**Step 1:** Understand the {selected_career} role."
)

st.write(
    f"**Step 2:** Check the education and qualification requirements."
)

st.write(
    f"**Step 3:** Start learning: {guidance['learn']}"
)

st.write(
    "**Step 4:** Practice through projects or practical training."
)

st.write(
    "**Step 5:** Build your resume and portfolio."
)

st.write(
    "**Step 6:** Start applying for suitable internships or entry-level roles."
)

st.write(
    "**Step 7:** Prepare for career-specific interviews."
)


# ============================================================
# FINAL MESSAGE
# ============================================================

st.success(
    f"Your complete roadmap for {selected_career} is ready — "
    "from education and learning to practical experience, "
    "job preparation and interviews."
)

st.caption(
    f"CareerPath AI currently provides {len(careers)} career options."
)