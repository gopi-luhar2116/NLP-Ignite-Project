import pandas as pd

def extract_skills(processed_words):

    skills_df = pd.read_csv("skills.csv")

    skill_list = skills_df["Skill"].str.lower().tolist()

    found_skills = []

    resume_text = " ".join(processed_words)

    processed_set = set(processed_words)

    for skill in skill_list:

        skill_words = skill.lower().split()

        if all(word in processed_set for word in skill_words):
            found_skills.append(skill.title())

    return sorted(list(set(found_skills)))