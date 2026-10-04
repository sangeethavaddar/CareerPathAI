import re


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize_text(value):
    """Convert text to clean lowercase text."""

    if value is None:
        return ""

    return str(value).strip().lower()


def split_values(value):
    """
    Convert lists or separated text into clean lowercase values.
    Supports comma and | separators.
    """

    if value is None:
        return []

    if isinstance(value, list):
        values = value
    else:
        values = re.split(r"[,|]", str(value))

    return [
        normalize_text(item)
        for item in values
        if normalize_text(item)
    ]


def text_words(value):
    """Extract useful words from text."""

    text = normalize_text(value)

    return set(
        re.findall(
            r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}",
            text
        )
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def calculate_skill_match(student_skills, required_skills):
    """
    Calculate percentage of required skills
    already present in the student's profile.
    """

    student = set(split_values(student_skills))
    required = set(split_values(required_skills))

    if not required:
        return 0.0

    matched = student.intersection(required)

    return round(
        (len(matched) / len(required)) * 100,
        2
    )


def get_matched_skills(student_skills, required_skills):

    student = set(split_values(student_skills))
    required = set(split_values(required_skills))

    return sorted(
        student.intersection(required)
    )


def get_skill_gaps(student_skills, required_skills):

    student = set(split_values(student_skills))
    required = set(split_values(required_skills))

    return sorted(
        required - student
    )


# ============================================================
# INTEREST MATCHING
# ============================================================

def calculate_interest_match(
    student_interests,
    career_interests
):
    """
    Compare student interests with career interests.
    """

    student = set(
        split_values(student_interests)
    )

    career = set(
        split_values(career_interests)
    )

    if not student or not career:
        return 0.0

    matched = student.intersection(career)

    # Direct matches
    direct_score = (
        len(matched) / len(career)
    ) * 100

    # Related-interest groups
    related_groups = [

        {
            "technology",
            "programming",
            "software",
            "computer science",
            "data",
            "artificial intelligence"
        },

        {
            "healthcare",
            "medicine",
            "biology",
            "anatomy",
            "health",
            "clinical"
        },

        {
            "business",
            "management",
            "entrepreneurship",
            "leadership",
            "marketing"
        },

        {
            "finance",
            "accounting",
            "investment",
            "economics"
        },

        {
            "design",
            "creativity",
            "arts",
            "visual",
            "graphics"
        },

        {
            "communication",
            "media",
            "journalism",
            "writing",
            "social media"
        },

        {
            "engineering",
            "technology",
            "problem solving",
            "technical"
        },

        {
            "agriculture",
            "farming",
            "environment",
            "nature",
            "sustainability"
        },

        {
            "education",
            "teaching",
            "learning",
            "research"
        },

        {
            "sports",
            "fitness",
            "health",
            "training"
        }
    ]

    related_match = 0

    for group in related_groups:

        student_group = student.intersection(group)
        career_group = career.intersection(group)

        if student_group and career_group:

            related_match += 1

    if related_match > 0:

        related_bonus = min(
            related_match * 10,
            40
        )

    else:

        related_bonus = 0

    final_score = min(
        direct_score + related_bonus,
        100
    )

    return round(
        final_score,
        2
    )


def get_matched_interests(
    student_interests,
    career_interests
):

    student = set(
        split_values(student_interests)
    )

    career = set(
        split_values(career_interests)
    )

    direct_matches = student.intersection(
        career
    )

    return sorted(
        direct_matches
    )


# ============================================================
# DOMAIN MATCHING
# ============================================================

def calculate_domain_match(
    student_domain,
    career_domain
):
    """
    Same professional domain = 100%.
    Unknown preference = neutral 50%.
    Different domain = 0%.
    """

    student = normalize_text(
        student_domain
    )

    career = normalize_text(
        career_domain
    )

    if not student or student == "not sure yet":
        return 50.0

    if student == career:
        return 100.0

    return 0.0


# ============================================================
# EDUCATION MATCHING
# ============================================================

def education_level(value):
    """
    Convert education into an approximate level.
    """

    text = normalize_text(value)

    if any(
        item in text
        for item in [
            "10th",
            "secondary school"
        ]
    ):
        return 1

    if any(
        item in text
        for item in [
            "12th",
            "higher secondary"
        ]
    ):
        return 2

    if "diploma" in text:
        return 3

    if any(
        item in text
        for item in [
            "bachelor",
            "b.tech",
            "b.e",
            "bca",
            "b.sc",
            "b.com",
            "bba"
        ]
    ):
        return 4

    if any(
        item in text
        for item in [
            "master",
            "m.tech",
            "m.e",
            "mca",
            "m.sc",
            "mba"
        ]
    ):
        return 5

    if any(
        item in text
        for item in [
            "phd",
            "doctorate"
        ]
    ):
        return 6

    return 0


def calculate_education_match(
    student_education,
    career_education
):
    """
    Compare the student's education level with
    the education requirements of the career.
    """

    student_level = education_level(
        student_education
    )

    career_options = split_values(
        career_education
    )

    if student_level == 0:
        return 0.0

    if not career_options:
        return 50.0

    career_levels = [
        education_level(option)
        for option in career_options
    ]

    career_levels = [
        level
        for level in career_levels
        if level > 0
    ]

    if not career_levels:
        return 50.0

    if student_level in career_levels:
        return 100.0

    # One education level below/above
    if any(
        abs(student_level - level) == 1
        for level in career_levels
    ):
        return 70.0

    # Student has a higher education level
    if any(
        student_level > level
        for level in career_levels
    ):
        return 80.0

    return 30.0


# ============================================================
# EXPERIENCE MATCHING
# ============================================================

def experience_level(value):
    """Convert experience text to an approximate level."""

    text = normalize_text(value)

    if (
        "no experience" in text
        or "fresher" in text
    ):
        return 0

    if "internship" in text:
        return 1

    if "1-2" in text:
        return 2

    if "3-5" in text:
        return 3

    if "5+" in text:
        return 4

    return 0


def calculate_experience_match(
    student_experience,
    career_experience
):
    """
    Compare student's experience with career requirements.
    """

    student_level = experience_level(
        student_experience
    )

    career_options = split_values(
        career_experience
    )

    if not career_options:
        return 50.0

    career_levels = [
        experience_level(option)
        for option in career_options
    ]

    if (
        student_level in career_levels
    ):
        return 100.0

    # Fresher/internship can still enter many careers
    if student_level <= 1:

        if any(
            level <= 1
            for level in career_levels
        ):
            return 90.0

        return 60.0

    # Experienced candidates
    if any(
        student_level >= level
        for level in career_levels
    ):
        return 90.0

    if any(
        abs(student_level - level) == 1
        for level in career_levels
    ):
        return 70.0

    return 40.0


# ============================================================
# PROJECT MATCHING
# ============================================================

def calculate_project_match(
    student_projects,
    career
):
    """
    Analyze the student's project description
    against the career information.
    """

    projects = normalize_text(
        student_projects
    )

    if not projects:
        return 0.0

    career_text = " ".join(
        [
            normalize_text(
                career.get("career", "")
            ),
            normalize_text(
                career.get("description", "")
            ),
            normalize_text(
                career.get("skills", "")
            ),
            normalize_text(
                career.get("interests", "")
            )
        ]
    )

    project_words = text_words(
        projects
    )

    if not project_words:
        return 0.0

    # Ignore very common words
    ignored_words = {
        "the",
        "and",
        "using",
        "used",
        "with",
        "for",
        "from",
        "this",
        "that",
        "project",
        "developed",
        "develop",
        "application",
        "system"
    }

    useful_words = (
        project_words - ignored_words
    )

    if not useful_words:
        return 0.0

    matched_words = 0

    for word in useful_words:

        if word in career_text:
            matched_words += 1

    score = (
        matched_words
        / len(useful_words)
    ) * 100

    return round(
        min(score, 100),
        2
    )


# ============================================================
# CAREER GOAL MATCHING
# ============================================================

def calculate_goal_match(
    student_goal,
    career_name
):
    """
    Compare the student's career goal
    with the career name.
    """

    goal = normalize_text(
        student_goal
    )

    career = normalize_text(
        career_name
    )

    if not goal or not career:
        return 0.0

    if goal == career:
        return 100.0

    goal_words = text_words(
        goal
    )

    career_words = text_words(
        career
    )

    if not goal_words or not career_words:
        return 0.0

    # Remove generic career words
    generic_words = {
        "career",
        "job",
        "professional",
        "developer",
        "engineer",
        "manager",
        "analyst",
        "specialist",
        "officer"
    }

    useful_goal_words = (
        goal_words - generic_words
    )

    useful_career_words = (
        career_words - generic_words
    )

    if not useful_goal_words:
        useful_goal_words = goal_words

    if not useful_career_words:
        useful_career_words = career_words

    matched = (
        useful_goal_words
        .intersection(
            useful_career_words
        )
    )

    if not matched:
        return 0.0

    return round(
        (
            len(matched)
            / len(useful_goal_words)
        ) * 100,
        2
    )


# ============================================================
# MAIN CAREER MATCH
# ============================================================

def calculate_career_match(
    profile,
    career
):
    """
    Explainable weighted career matching.

    Weights:

    Skills       = 35%
    Interests    = 20%
    Domain       = 10%
    Education    = 10%
    Experience   = 5%
    Projects     = 10%
    Career Goal  = 10%
    """

    skills_score = calculate_skill_match(
        profile.get("skills", []),
        career.get("skills", "")
    )

    interests_score = calculate_interest_match(
        profile.get("interests", []),
        career.get("interests", "")
    )

    domain_score = calculate_domain_match(
        profile.get("preferred_domain", ""),
        career.get("domain", "")
    )

    education_score = calculate_education_match(
        profile.get("education", ""),
        career.get("education", "")
    )

    experience_score = calculate_experience_match(
        profile.get("experience", ""),
        career.get("experience", "")
    )

    project_score = calculate_project_match(
        profile.get("projects", ""),
        career
    )

    goal_score = calculate_goal_match(
        profile.get("career_goal", ""),
        career.get("career", "")
    )

    # ========================================================
    # WEIGHTED FINAL SCORE
    # ========================================================

    final_score = (
        skills_score * 0.35
        + interests_score * 0.20
        + domain_score * 0.10
        + education_score * 0.10
        + experience_score * 0.05
        + project_score * 0.10
        + goal_score * 0.10
    )

    matched_skills = get_matched_skills(
        profile.get("skills", []),
        career.get("skills", "")
    )

    skill_gaps = get_skill_gaps(
        profile.get("skills", []),
        career.get("skills", "")
    )

    matched_interests = get_matched_interests(
        profile.get("interests", []),
        career.get("interests", "")
    )

    return {

        "match": round(
            final_score,
            2
        ),

        "skills": round(
            skills_score,
            2
        ),

        "interests": round(
            interests_score,
            2
        ),

        "domain": round(
            domain_score,
            2
        ),

        "education": round(
            education_score,
            2
        ),

        "experience": round(
            experience_score,
            2
        ),

        "projects": round(
            project_score,
            2
        ),

        "career_goal": round(
            goal_score,
            2
        ),

        "matched_skills": matched_skills,

        "skill_gaps": skill_gaps,

        "matched_interests": matched_interests
    }


# ============================================================
# EXPLANATION GENERATOR
# ============================================================

def generate_match_reasons(result):

    reasons = []

    if result["skills"] >= 70:

        reasons.append(
            "Your current skills strongly match "
            "the skills required for this career."
        )

    elif result["skills"] >= 40:

        reasons.append(
            "Several of your current skills are "
            "relevant to this career."
        )

    elif result["skills"] > 0:

        reasons.append(
            "Some of your existing skills are "
            "useful for this career."
        )

    if result["interests"] >= 70:

        reasons.append(
            "Your interests have strong alignment "
            "with this career."
        )

    elif result["interests"] >= 40:

        reasons.append(
            "Some of your interests are related "
            "to this career."
        )

    if result["domain"] == 100:

        reasons.append(
            "This career belongs to your selected "
            "professional domain."
        )

    if result["education"] >= 80:

        reasons.append(
            "Your education level is compatible "
            "with this career."
        )

    elif result["education"] >= 60:

        reasons.append(
            "Your education has reasonable "
            "compatibility with this career."
        )

    if result["experience"] >= 80:

        reasons.append(
            "Your experience level is suitable "
            "for this career."
        )

    elif result["experience"] >= 60:

        reasons.append(
            "Your current experience can provide "
            "a starting point for this career."
        )

    if result["projects"] >= 50:

        reasons.append(
            "Your project experience contains "
            "relevant connections to this career."
        )

    elif result["projects"] > 0:

        reasons.append(
            "Your project experience has some "
            "relevant connections."
        )

    if result["career_goal"] >= 70:

        reasons.append(
            "Your stated career goal closely "
            "matches this career."
        )

    elif result["career_goal"] >= 40:

        reasons.append(
            "Your stated career goal has some "
            "connection with this career."
        )

    if not reasons:

        reasons.append(
            "The recommendation is based on the "
            "combined information in your profile."
        )

    return reasons


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def recommend_careers(
    profile,
    careers,
    top_n=5
):
    """
    Generate career recommendations
    from the complete career database.
    """

    if hasattr(careers, "to_dict"):

        career_records = careers.to_dict(
            "records"
        )

    else:

        career_records = careers

    recommendations = []

    for career in career_records:

        result = calculate_career_match(
            profile,
            career
        )

        result["career"] = career.get(
            "career",
            "Unknown Career"
        )

        result["domain_name"] = career.get(
            "domain",
            "Unknown"
        )

        result["description"] = career.get(
            "description",
            ""
        )

        result["reasons"] = (
            generate_match_reasons(
                result
            )
        )

        recommendations.append(
            result
        )

    recommendations.sort(
        key=lambda item: item["match"],
        reverse=True
    )

    return recommendations[:top_n]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_profile = {

        "name": "Test Student",

        "education": "Bachelor's Degree",

        "preferred_domain": "Technology",

        "interests": [
            "Technology",
            "Programming",
            "Problem Solving"
        ],

        "skills": [
            "Python",
            "Java",
            "Data Analysis",
            "Communication",
            "Machine Learning"
        ],

        "experience": "No Experience",

        "projects":
            "Developed an ecommerce website "
            "using Java and SQL",

        "career_goal":
            "Software Developer"
    }

    test_career = {

        "career":
            "Software Developer",

        "domain":
            "Technology",

        "description":
            "Develops software applications "
            "and systems.",

        "skills":
            "Java|Python|SQL|Problem Solving|Git",

        "interests":
            "Technology|Programming|Problem Solving",

        "education":
            "Bachelor's Degree|Master's Degree",

        "experience":
            "No Experience|1-2 Years"
    }

    result = calculate_career_match(
        test_profile,
        test_career
    )

    print()
    print("=" * 60)
    print("        CAREERPATH AI MATCHING ENGINE")
    print("=" * 60)

    print()
    print("Career:", test_career["career"])

    print(
        "Overall Match:",
        result["match"],
        "%"
    )

    print(
        "Skills:",
        result["skills"],
        "%"
    )

    print(
        "Interests:",
        result["interests"],
        "%"
    )

    print(
        "Domain:",
        result["domain"],
        "%"
    )

    print(
        "Education:",
        result["education"],
        "%"
    )

    print(
        "Experience:",
        result["experience"],
        "%"
    )

    print(
        "Projects:",
        result["projects"],
        "%"
    )

    print(
        "Career Goal:",
        result["career_goal"],
        "%"
    )

    print()
    print("Matched Skills:")

    if result["matched_skills"]:

        print(
            ", ".join(
                result["matched_skills"]
            )
        )

    else:

        print("None")

    print()
    print("Skill Gaps:")

    if result["skill_gaps"]:

        print(
            ", ".join(
                result["skill_gaps"]
            )
        )

    else:

        print("None")

    print()
    print("Matching Interests:")

    if result["matched_interests"]:

        print(
            ", ".join(
                result["matched_interests"]
            )
        )

    else:

        print("None")

    print()
    print("Reasons:")

    for reason in generate_match_reasons(
        result
    ):

        print(
            "-",
            reason
        )

    print()
    print("=" * 60)