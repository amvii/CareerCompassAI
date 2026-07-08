import json


def load_jobs():

    with open("data/jobs.json", "r") as file:
        jobs = json.load(file)

    return jobs


def get_recommendations(user_input):

    jobs = load_jobs()

    user_skills = [
        skill.strip().lower()
        for skill in user_input.split(",")
    ]

    recommendations = []

    for job in jobs:

        required_skills = job["skills"]

        matched_skills = []

        for skill in user_skills:

            if skill in required_skills:
                matched_skills.append(skill)

        score = len(matched_skills)

        # 0 match wali jobs skip kar do
        if score == 0:
            continue

        total_required = len(required_skills)

        percentage = int((score / total_required) * 100)

        missing_skills = []

        for skill in required_skills:

            if skill not in user_skills:
                missing_skills.append(skill)

        recommendations.append({
            "job": job["job"],
            "score": score,
            "percentage": percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Sirf top 3 recommendations
    return recommendations[:3]