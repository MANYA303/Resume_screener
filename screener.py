import docx
import fitz  # PyMuPDF for PDFs
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(path):
    text = ""
    try:
        with fitz.open(path) as pdf:
            for page in pdf:
                text += page.get_text("text")
    except Exception as e:
        print("PDF Error:", e)
    return text

def extract_text_from_docx(path):
    text = ""
    try:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + " "
    except Exception as e:
        print("DOCX Error:", e)
    return text

def extract_text_from_txt(path):
    text = ""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except Exception as e:
        print("TXT Error:", e)
    return text

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    elif ext == '.docx':
        return extract_text_from_docx(path)
    elif ext == '.txt':
        return extract_text_from_txt(path)
    else:
        return ""

def screen_resumes(job_description, resume_paths):
    resume_texts = []
    resume_names = []

    for path in resume_paths:
        text = extract_text(path)
        if text.strip():
            resume_texts.append(text)
            resume_names.append(os.path.basename(path))

    if not resume_texts:
        return [{"name": "No readable resumes found", "score": 0}]

    docs = [job_description] + resume_texts
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(docs)

    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    results = [
        {"name": name, "score": round(float(score) * 100, 2)}
        for name, score in zip(resume_names, similarity)
    ]

    results.sort(key=lambda x: x['score'], reverse=True)
    return results

