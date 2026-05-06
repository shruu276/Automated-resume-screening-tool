import re
from rapidfuzz import process, fuzz

SKILLS_DB = [
    "python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "sql", "power bi",
    "excel", "aws", "azure", "gcp", "react", "node", "django", "flask", "java", "spring",
    "salesforce", "nosql", "mongodb", "docker", "kubernetes", "c++", "c", "git", "linux", "html", "css", "javascript", "next.js", "tableau"
]
# Normalize list
NORM_SKILLS = {s.lower(): s.lower() for s in SKILLS_DB}

def extract_skills(text: str, cutoff=80):
    tokens = set(re.findall(r"[a-zA-Z\+\#\.]{2,}", text.lower()))
    found_skills = set()
    for token in tokens:
        match = process.extractOne(token, SKILLS_DB, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= cutoff:
            found_skills.add(NORM_SKILLS[match[0]])
    return sorted(list(found_skills))

def extract_years_experience(text: str) -> float:
    years = 0.0
    # Match patterns like "3 years", "2.5 yrs", "5+ years"
    matches = re.finditer(r'(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(years|yrs|y)\b', text.lower())
    for m in matches:
        years = max(years, float(m.group(1)))
    return years

def parse_resume_text(raw_text: str) -> dict:
    skills = extract_skills(raw_text)
    years_exp = extract_years_experience(raw_text)
    
    # Simple education check
    edu = None
    if any(keyword in raw_text.lower() for keyword in ["b.tech", "btech", "b.s", "b.sc", "bachelor"]):
        edu = "Bachelor's"
    elif any(keyword in raw_text.lower() for keyword in ["m.tech", "m.s", "master"]):
        edu = "Master's"
        
    return {
        "skills": skills,
        "years_exp": years_exp,
        "education": edu
    }
