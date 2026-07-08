import json


def extract_skills(text):

    with open("data/skills.json", "r") as file:
        skills_database = json.load(file)

    text = text.lower()

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text:

            found_skills.append(skill)

    return list(set(found_skills))