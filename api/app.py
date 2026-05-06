from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import uuid
import json
import os
import sys

# Add src to python path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingest import extract_text_from_file, save_resume, init_db
from src.extract import parse_resume_text
from src.rank import rank_candidates_for_job

app = FastAPI(title="Automated Resume Screening API")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'screening.db'))

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db(DB_PATH)

class Job(BaseModel):
    title: str
    jd_text: str
    must_have: List[str] = []
    nice_to_have: List[str] = []
    min_exp_years: float = 2.0
    location: Optional[str] = None

@app.post("/api/jobs")
def create_job(job: Job):
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    con = sqlite3.connect(DB_PATH)
    con.execute("""INSERT INTO jobs(id, title, jd_text, must_have, nice_to_have, min_exp_years, location)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (job_id, job.title, job.jd_text, json.dumps(job.must_have),
                 json.dumps(job.nice_to_have), job.min_exp_years, job.location))
    con.commit()
    con.close()
    return {"status": "success", "job_id": job_id}

@app.get("/api/jobs")
def get_jobs():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    jobs = con.execute("SELECT * FROM jobs").fetchall()
    con.close()
    return [dict(j) for j in jobs]

@app.post("/api/resumes/upload")
async def upload_resume(candidate_name: str = Form(...), file: UploadFile = File(...)):
    candidate_id = f"cand_{uuid.uuid4().hex[:8]}"
    
    # Save file temporarily to extract text
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        raw_text = extract_text_from_file(temp_file)
        parsed_data = parse_resume_text(raw_text)
        
        # Save to DB
        con = sqlite3.connect(DB_PATH)
        con.execute("INSERT OR IGNORE INTO candidates(id, name) VALUES (?, ?)", (candidate_id, candidate_name))
        con.commit()
        con.close()
        
        save_resume(DB_PATH, candidate_id, file.filename, raw_text, parsed_data)
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    return {"status": "success", "candidate_id": candidate_id, "parsed_skills": parsed_data["skills"]}

@app.post("/api/rank/{job_id}")
def rank_candidates(job_id: str):
    success = rank_candidates_for_job(DB_PATH, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "success"}

@app.get("/api/rankings/{job_id}")
def get_rankings(job_id: str):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    query = """
    SELECT r.candidate_id, c.name, r.score, r.reasons 
    FROM rankings r 
    JOIN candidates c ON r.candidate_id = c.id
    WHERE r.job_id = ? 
    ORDER BY r.score DESC
    """
    rows = con.execute(query, (job_id,)).fetchall()
    con.close()
    
    results = []
    for r in rows:
        result = dict(r)
        result["reasons"] = json.loads(result["reasons"])
        results.append(result)
        
    return results

# Health check
@app.get("/api/health")
def health():
    return {"status": "ok"}
