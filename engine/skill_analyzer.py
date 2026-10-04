import re


def clean_skill(skill):
    """Clean and normalize a single skill name."""
    if skill is None:
        return ""

    skill = str(skill).strip().lower()

    # Remove brackets, quotes and unnecessary punctuation
    skill = skill.replace("[", "")
    skill = skill.replace("]", "")
    skill = skill.replace("'", "")
    skill = skill.replace('"', "")

    # Normalize separators
    skill = skill.replace("_", " ")
    skill = re.sub(r"\s+", " ", skill)

    return skill.strip()


def clean_skill_list(skills):
    """Convert skills into a clean list of normalized skill names."""
    if skills is None:
        return []

    if isinstance(skills, str):
        # Handle comma, semicolon and pipe separated values
        skills = re.split(r"[,;|]", skills)

    cleaned = []

    for skill in skills:
        value = clean_skill(skill)

        if value and value not in cleaned:
            cleaned.append(value)

    return cleaned


def get_required_skills(career):
    """Get the required skills for a career."""
    if career is None:
        return []

    if isinstance(career, dict):
        skills = career.get("skills", "")
    else:
        try:
            skills = career["skills"]
        except (KeyError, TypeError):
            return []

    return clean_skill_list(skills)


def find_matching_skills(current_skills, required_skills):
    """Find skills that exist in both the profile and career requirements."""
    current = clean_skill_list(current_skills)
    required = clean_skill_list(required_skills)

    matches = []

    for required_skill in required:
        for current_skill in current:
            if (
                required_skill == current_skill
                or required_skill in current_skill
                or current_skill in required_skill
            ):
                if required_skill not in matches:
                    matches.append(required_skill)
                break

    return matches


def find_skill_gaps(current_skills, required_skills):
    """Find career-required skills that are missing from the profile."""
    current = clean_skill_list(current_skills)
    required = clean_skill_list(required_skills)

    gaps = []

    for required_skill in required:
        found = False

        for current_skill in current:
            if (
                required_skill == current_skill
                or required_skill in current_skill
                or current_skill in required_skill
            ):
                found = True
                break

        if not found:
            gaps.append(required_skill)

    return gaps


def calculate_skill_coverage(current_skills, required_skills):
    """
    Calculate percentage of required career skills
    that are already present in the user's profile.
    """

    required = clean_skill_list(required_skills)

    if not required:
        return 0.0

    matching = find_matching_skills(current_skills, required)

    coverage = (len(matching) / len(required)) * 100

    return round(coverage, 2)


def analyze_career_skills(current_skills, career):
    """
    Analyze a user's skills against one career.
    """

    current = clean_skill_list(current_skills)
    required = get_required_skills(career)

    matching = find_matching_skills(current, required)
    gaps = find_skill_gaps(current, required)
    coverage = calculate_skill_coverage(current, required)

    return {
        "required_skills": required,
        "matching_skills": matching,
        "skill_gaps": gaps,
        "coverage": coverage
    }


def analyze_multiple_careers(current_skills, careers):
    """Analyze the user's skills against multiple careers."""

    results = []

    for career in careers:
        analysis = analyze_career_skills(current_skills, career)

        if isinstance(career, dict):
            career_name = career.get("career", "Unknown Career")
        else:
            try:
                career_name = career["career"]
            except (KeyError, TypeError):
                career_name = "Unknown Career"

        results.append({
            "career": career_name,
            "coverage": analysis["coverage"],
            "matching_skills": analysis["matching_skills"],
            "skill_gaps": analysis["skill_gaps"]
        })

    return results


def get_top_skill_analysis(current_skills, careers, top_n=5):
    """Return careers with the highest skill coverage."""

    results = analyze_multiple_careers(current_skills, careers)

    results.sort(
        key=lambda item: item["coverage"],
        reverse=True
    )

    return results[:top_n]


def print_skill_analysis(current_skills, career):
    """Print a readable skill analysis in the terminal."""

    career_name = career.get("career", "Unknown Career")

    analysis = analyze_career_skills(
        current_skills,
        career
    )

    print("\nCareer:", career_name)
    print("Required Skills:", ", ".join(analysis["required_skills"]))
    print(
        "Matching Skills:",
        ", ".join(analysis["matching_skills"])
        if analysis["matching_skills"]
        else "None"
    )
    print(
        "Skill Gaps:",
        ", ".join(analysis["skill_gaps"])
        if analysis["skill_gaps"]
        else "None"
    )
    print("Skill Coverage:", analysis["coverage"], "%")


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    test_skills = [
        "Biology",
        "Medicine",
        "Communication",
        "Clinical Skills"
    ]

    test_career = {
        "career": "Doctor",
        "skills": "Biology, Clinical Skills, Communication, Decision Making, Medicine"
    }

    print_skill_analysis(
        test_skills,
        test_career
    )