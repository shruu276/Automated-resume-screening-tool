import sqlite3
import json
import re
import os
from pathlib import Path
import PyPDF2
# Ensure you have installed: PyPDF2, python-docx
try:
    import docx
except ImportError:
    docx = None

def init_db(db_path="db/screening.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    con = sqlite3.connect(db_path)
    
    con.execute('''CREATE TABLE IF NOT EXISTS jobs(
        id TEXT PRIMARY KEY,
        title TEXT,
        jd_text TEXT,
        must_have TEXT,
        nice_to_have TEXT,
        min_exp_years REAL,
        location TEXT
    )''')

    con.execute('''CREATE TABLE IF NOT EXISTS candidates(
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        location TEXT
    )''')

    con.execute('''CREATE TABLE IF NOT EXISTS resumes(
        candidate_id TEXT REFERENCES candidates(id),
        source TEXT,
        raw_text TEXT,
        parsed_json TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(candidate_id)
    )''')

    con.execute('''CREATE TABLE IF NOT EXISTS rankings(
        job_id TEXT,
        candidate_id TEXT,
        score REAL,
        reasons TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(job_id, candidate_id)
    )''')
    
    con.commit()
    con.close()

def extract_text_from_file(file_path: str) -> str:
    path = Path(file_path)
    text = ""
    if path.suffix.lower() == ".pdf":
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
    elif path.suffix.lower() == ".docx":
        if docx:
            try:
                doc = docx.Document(path)
                text = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                print(f"Error reading DOCX: {e}")
        else:
            print("python-docx is not installed.")
    else:
        # Default text read
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading text file: {e}")
            
    # Clean up whitespace
    return re.sub(r'\s+', ' ', text).strip()

def save_resume(db_path, candidate_id, source, raw_text, parsed_data):
    con = sqlite3.connect(db_path)
    con.execute("""INSERT OR REPLACE INTO resumes(candidate_id, source, raw_text, parsed_json, updated_at)
                   VALUES(?, ?, ?, ?, datetime('now'))""",
                (candidate_id, source, raw_text, json.dumps(parsed_data)))
    con.commit()
    con.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
