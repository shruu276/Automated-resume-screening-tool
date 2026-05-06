import sqlite3
import json
from sentence_transformers import SentenceTransformer, util

# Load a small, fast embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_job_and_resume(db_path, job_id, candidate_id):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    jd = cur.execute("SELECT jd_text, must_have FROM jobs WHERE id=?", (job_id,)).fetchone()
    rs = cur.execute("SELECT parsed_json FROM resumes WHERE candidate_id=?", (candidate_id,)).fetchone()
    con.close()
    
    if not jd or not rs:
        return None, None
        
    jd_text = jd[0]
    must_have = json.loads(jd[1]) if isinstance(jd[1], str) else (jd[1] or [])
    parsed_resume = json.loads(rs[0])
    
    return (jd_text, must_have), parsed_resume

def compute_features(db_path, job_id, candidate_id):
    job_data, resume_data = get_job_and_resume(db_path, job_id, candidate_id)
    if not job_data:
        return None
        
    jd_text, must_have = job_data
    skills = set(resume_data.get("skills", []))
    years_exp = resume_data.get("years_exp", 0.0)
    
    # 1. Semantic Similarity
    # Compare JD text with Resume Skills + Education
    resume_text_repr = " ".join(skills) + " " + str(resume_data.get("education", ""))
    
    # Check if either string is empty to avoid errors
    if not jd_text.strip() or not resume_text_repr.strip():
        sim_score = 0.0
    else:
        embeddings1 = model.encode(jd_text, convert_to_tensor=True)
        embeddings2 = model.encode(resume_text_repr, convert_to_tensor=True)
        sim_score = float(util.cos_sim(embeddings1, embeddings2)[0][0])
    
    # 2. Rule Coverage (Must Have)
    hits = sum(1 for s in must_have if s.lower() in skills)
    must_total = len(must_have)
    
    # 3. Gap Penalty (Missing Must Haves)
    gap_penalty = 0.1 * (must_total - hits) if must_total > 0 else 0.0
    
    return {
        "sim_embedding": sim_score,
        "rule_musthave_hits": hits,
        "rule_musthave_total": must_total,
        "years_exp": years_exp,
        "gap_penalty": gap_penalty,
        "matched_skills": list(skills.intersection(set(s.lower() for s in must_have)))
    }
