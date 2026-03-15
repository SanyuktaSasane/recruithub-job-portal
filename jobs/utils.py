from pdfminer.high_level import extract_text

def extract_resume_text(file_path):
    try:
        text = extract_text(file_path)
        return text.lower()
    except:
        return ""


def calculate_ats_score(resume_text, job_description):

    resume_words = set(resume_text.split())
    job_words = set(job_description.lower().split())

    matched_words = resume_words.intersection(job_words)

    if len(job_words) == 0:
        return 0

    score = (len(matched_words) / len(job_words)) * 100

    return round(score, 2)