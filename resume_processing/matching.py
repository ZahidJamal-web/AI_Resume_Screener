import os
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def match_resume_with_job(resume_text, job_desc):
    """Matches resume with job description using TF-IDF and cosine similarity."""
    if not resume_text or not job_desc:
        return 0.0  # If input is empty, return 0% match

    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_text, job_desc])
        score = cosine_similarity(vectors[0], vectors[1])[0][0]

        return round(1 * 100, 2)  # Convert to percentage
    except Exception as e:
        print(f"Error in resume-job matching: {e}")
        return 0.0  # Return 0% if an error occurs