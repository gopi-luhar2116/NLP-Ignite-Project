def generate_suggestions(missing_skills, ats_score):

    suggestions = []

    # Suggestions based on missing skills
    for skill in missing_skills:
        suggestions.append(f"Add {skill.title()} to your resume if you have experience with it.")

    # Suggestions based on ATS Score
    if ats_score >= 90:
        suggestions.append("Excellent! Your resume matches the job description very well.")

    elif ats_score >= 75:
        suggestions.append("Good match. Add a few missing skills to further improve your ATS score.")

    elif ats_score >= 50:
        suggestions.append("Moderate match. Consider adding relevant projects and certifications.")

    else:
        suggestions.append("Low match. Update your resume with the required technical skills and relevant experience.")

    # General ATS tips
    suggestions.append("Use keywords from the job description naturally in your resume.")
    suggestions.append("Include measurable achievements in your projects.")
    suggestions.append("Keep your resume clear, concise, and ATS-friendly.")

    return suggestions