import sqlite3
import json
import datetime as dt
from .features import compute_features

def rank_candidates_for_job(db_path, job_id, default_min_req_years=2.0):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    job = cur.execute("SELECT must_have, min_exp_years FROM jobs WHERE id=?", (job_id,)).fetchone()
    if not job:
        print(f"Job {job_id} not found.")
        return
        
    must_have_raw = job[0]
    must_total = len(json.loads(must_have_raw) if isinstance(must_have_raw, str) else (must_have_raw or []))
    min_req_years = job[1] if job[1] is not None else default_min_req_years
    
    candidates = cur.execute("SELECT candidate_id FROM resumes").fetchall()
    
    rows = []
    for (cid,) in candidates:
        f = compute_features(db_path, job_id, cid)
        if not f:
            continue
            
        # Composite Scoring Formula
        sim_weight = 0.55
        rule_weight = 0.35
        exp_weight = 0.10
        
        rule_score = f["rule_musthave_hits"] / max(1, f["rule_musthave_total"])
        exp_score = min(1.0, f["years_exp"] / max(1, min_req_years))
        
        score = (sim_weight * f["sim_embedding"]) + (rule_weight * rule_score) + (exp_weight * exp_score) - f["gap_penalty"]
        
        reasons = {
            "top_skills_matched": f"Matched {f['rule_musthave_hits']}/{f['rule_musthave_total']} must-haves.",
            "matched_skills_list": f["matched_skills"],
            "similarity": round(f["sim_embedding"], 3),
            "experience_ok": f["years_exp"] >= min_req_years,
            "years_exp": f["years_exp"]
        }
        
        rows.append((job_id, cid, float(score), json.dumps(reasons), dt.datetime.utcnow().isoformat()))
        
    cur.executemany("INSERT OR REPLACE INTO rankings(job_id, candidate_id, score, reasons, created_at) VALUES (?,?,?,?,?)", rows)
    con.commit()
    con.close()
    print(f"Ranked {len(rows)} candidates for job {job_id}")
    return True
