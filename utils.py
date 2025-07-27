import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def compute_similarity(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    return round(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100, 2)

def extract_keywords(text, top_n=20):
    words = text.split()
    keywords = Counter(words)
    return [word for word, freq in keywords.most_common(top_n)]

def find_missing_keywords(resume_keywords, jd_keywords):
    return [word for word in jd_keywords if word not in resume_keywords]
