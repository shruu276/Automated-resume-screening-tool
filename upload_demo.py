import requests
import os
import glob

API_URL = "http://localhost:8000/api/resumes/upload"
RESUME_DIR = os.path.join(os.path.dirname(__file__), "data", "sample_resumes")

def upload_resumes():
    files = glob.glob(os.path.join(RESUME_DIR, "*.txt"))
    if not files:
        print(f"No text files found in {RESUME_DIR}")
        return

    for file_path in files:
        filename = os.path.basename(file_path)
        # Extract candidate name from filename (e.g., resume1.txt -> Candidate 1)
        candidate_name = filename.replace(".txt", "").capitalize()
        
        with open(file_path, "rb") as f:
            files_data = {"file": (filename, f, "text/plain")}
            data = {"candidate_name": candidate_name}
            
            try:
                print(f"Uploading {filename}...")
                response = requests.post(API_URL, files=files_data, data=data)
                response.raise_for_status()
                print(f"Success: {response.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to upload {filename}: {e}")

if __name__ == "__main__":
    upload_resumes()
