def compare_skills(resume_skills, job_skills):

    resume_set = set(skill.lower() for skill in resume_skills)

    job_set = set(skill.lower() for skill in job_skills)

    matched = list(resume_set & job_set)

    missing = list(job_set - resume_set)

    return matched, missing