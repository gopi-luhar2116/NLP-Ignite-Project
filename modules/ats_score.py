def calculate_ats_score(matched, job):

    if len(job) == 0:
        return 0

    score = (len(matched) / len(job)) * 100

    return round(score, 2)