from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_semantic_similarity(text1, text2):
    """Calculates TF-IDF Cosine Similarity between resume and job description."""
    if not text1 or not text2:
        return 0.0
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return round(similarity * 100, 1)

def compare_skills(resume_skills, job_skills):
    """Finds matched and missing skills."""
    matched = list(set(resume_skills).intersection(set(job_skills)))
    missing = list(set(job_skills) - set(resume_skills))
    return matched, missing