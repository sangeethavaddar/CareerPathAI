"""
CareerPath AI - Career Explanation Engine

Generates clear, personalized explanations from the
existing career matching results.
"""


def generate_career_explanation(profile, career, result):
    """Generate a personalized explanation for a career recommendation."""

    career_name = career.get("career", "this career")
    domain = career.get("domain", "Professional")
    description = career.get("description", "")

    matched_skills = result.get("matched_skills", [])
    skill_gaps = result.get("skill_gaps", [])
    matched_interests = result.get("matched_interests", [])

    skills_score = result.get("skills", 0)
    interests_score = result.get("interests", 0)
    education_score = result.get("education", 0)
    experience_score = result.get("experience", 0)
    domain_score = result.get("domain", 0)
    projects_score = result.get("projects", 0)
    goal_score = result.get("career_goal", 0)
    overall_score = result.get("match", 0)

    strengths = []
    improvements = []

    # Strength analysis
    if skills_score >= 70:
        strengths.append(
            f"Your current skills show a strong connection with {career_name}."
        )
    elif skills_score >= 40:
        strengths.append(
            f"You already have some useful skills for {career_name}."
        )

    if interests_score >= 70:
        strengths.append(
            "Your interests strongly align with this career area."
        )
    elif interests_score >= 40:
        strengths.append(
            "Some of your interests are related to this career."
        )

    if education_score >= 70:
        strengths.append(
            "Your educational background is well aligned with this career."
        )
    elif education_score >= 40:
        strengths.append(
            "Your education provides some foundation for this career."
        )

    if experience_score >= 70:
        strengths.append(
            "Your experience provides useful preparation for this career."
        )

    if domain_score >= 70:
        strengths.append(
            f"Your preferred professional domain matches {domain}."
        )

    if projects_score >= 70:
        strengths.append(
            "Your projects provide relevant practical exposure."
        )

    if goal_score >= 70:
        strengths.append(
            "Your career goal is closely related to this career."
        )

    # Improvement analysis
    if skill_gaps:
        improvements.append(
            "Develop these skills: " + ", ".join(skill_gaps[:5]) + "."
        )

    if skills_score < 50:
        improvements.append(
            "Build stronger career-specific technical or professional skills."
        )

    if interests_score < 50:
        improvements.append(
            "Explore this career through introductory activities or projects."
        )

    if education_score < 50:
        improvements.append(
            "Check the educational requirements and plan the required qualifications."
        )

    if experience_score < 50:
        improvements.append(
            "Gain practical exposure through projects, internships, volunteering, or relevant activities."
        )

    if projects_score < 50:
        improvements.append(
            "Build practical projects related to this career."
        )

    if goal_score < 50:
        improvements.append(
            "Define a clearer career goal related to this profession."
        )

    if not strengths:
        strengths.append(
            "Your profile has some initial connections with this career."
        )

    if not improvements:
        improvements.append(
            "Continue developing your skills and gaining practical experience."
        )

    # Overall interpretation
    if overall_score >= 75:
        level = "strong alignment"
    elif overall_score >= 50:
        level = "moderate alignment"
    elif overall_score >= 30:
        level = "developing alignment"
    else:
        level = "early-stage alignment"

    explanation = {
        "career": career_name,
        "domain": domain,
        "description": description,
        "overall_score": overall_score,
        "alignment": level,
        "summary": (
            f"Your profile currently shows {level} with {career_name}, "
            f"with an overall match of {overall_score:.2f}%."
        ),
        "strengths": strengths,
        "improvements": improvements,
        "matched_skills": matched_skills,
        "skill_gaps": skill_gaps,
        "matched_interests": matched_interests,
    }

    return explanation


def print_career_explanation(explanation):
    """Display an explanation in the terminal."""

    print("\n" + "=" * 60)
    print("CAREERPATH AI - CAREER EXPLANATION")
    print("=" * 60)

    print(f"\nCareer: {explanation['career']}")
    print(f"Domain: {explanation['domain']}")
    print(f"Match: {explanation['overall_score']:.2f}%")
    print(f"Alignment: {explanation['alignment']}")

    print("\nSummary:")
    print(explanation["summary"])

    print("\nStrengths:")
    for item in explanation["strengths"]:
        print(" - " + item)

    print("\nAreas to Improve:")
    for item in explanation["improvements"]:
        print(" - " + item)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Simple test
    profile = {
        "skills": [
            "Biology",
            "Medicine",
            "Communication",
            "Clinical Skills"
        ],
        "interests": [
            "Biology",
            "Medicine"
        ]
    }

    career = {
        "career": "Doctor",
        "domain": "Healthcare",
        "description": "Diagnoses and treats patients and manages health conditions"
    }

    result = {
        "match": 51.67,
        "skills": 80.0,
        "interests": 43.33,
        "education": 50.0,
        "experience": 100.0,
        "domain": 100.0,
        "projects": 0.0,
        "career_goal": 0.0,
        "matched_skills": [
            "Biology",
            "Medicine",
            "Communication",
            "Clinical Skills"
        ],
        "skill_gaps": [
            "Decision Making"
        ],
        "matched_interests": [
            "Biology"
        ]
    }

    explanation = generate_career_explanation(
        profile,
        career,
        result
    )

    print_career_explanation(explanation)