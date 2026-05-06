# Automated Resume Screening Tool

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Machine Learning](https://img.shields.io/badge/NLP-TF--IDF%20%7C%20Transformers-blue)
![Python](https://img.shields.io/badge/Python-3.11-yellow)

## 📌 Project Overview
The **Automated Resume Screening Tool** is an intelligent, end-to-end Machine Learning pipeline that ingests resumes, compares them against job descriptions, and automatically ranks candidates based on their relevance. It reduces the time recruiters spend manually reading resumes by up to 70% and standardizes the screening process using data-driven metrics.

## 🎯 Problem Statement & Industry Relevance
Recruiters receive thousands of resumes for a single job opening. Manually parsing through them is time-consuming, prone to human bias, and inefficient. Modern HR Tech platforms and ATS (Applicant Tracking Systems) vendors use automated screening to enforce fair skills matching and standardize shortlists. 
This project bridges the gap by building a robust ML pipeline involving text ingestion, information extraction, vector search (embeddings), and ranking algorithms, topped with an intuitive Next.js dashboard.

## ✨ Features
- **Multi-format Ingestion:** Extracts text from PDF, DOCX, and TXT files.
- **NLP Skill Extraction:** Uses fuzzy matching and regular expressions to extract skills, experience years, and education from unstructured text.
- **Semantic Matching:** Uses `all-MiniLM-L6-v2` embeddings to measure the semantic similarity between a resume and a job description.
- **Rule-based Scoring:** Enforces "Must Have" skills and calculates gap penalties.
- **REST API:** FastAPI backend for job creation, resume uploading, and candidate ranking.
- **Analytics Dashboard:** Premium Next.js UI using glassmorphism, Recharts, and Tailwind CSS.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLite
- **Machine Learning:** Scikit-Learn, Sentence-Transformers, RapidFuzz, PyPDF2
- **Frontend:** Next.js (App Router), Tailwind CSS, Recharts, Lucide-React

## 📂 Folder Structure
```text
Automated-Resume-Screening-Tool/
│
├── api/
│   └── app.py                  # FastAPI Backend Server
├── apps/web/                   # Next.js Frontend Dashboard
├── data/                       # Sample Resumes and Job Descriptions
├── db/                         # SQLite Database
├── docs/                       # Project Guides & Interview Prep
├── src/
│   ├── extract.py              # NLP Text parsing & Skill extraction
│   ├── features.py             # Feature Engineering & Embeddings
│   ├── ingest.py               # File reading and Database interactions
│   └── rank.py                 # Composite scoring and candidate ranking
├── requirements.txt            # Python Dependencies
├── upload_demo.py              # Script to simulate uploading resumes
└── README.md
```

## 🚀 How to Run

### 1. Backend Setup
```bash
# Create a virtual environment
python -m venv venv
venv\Scripts\activate # On Windows
source venv/bin/activate # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn api.app:app --reload
```
API runs on `http://localhost:8000`.

### 2. Upload Demo Data
Open a new terminal, activate the environment, and upload sample data:
```bash
python upload_demo.py
```

### 3. Frontend Setup
```bash
cd apps/web
npm install
npm run dev
```
Dashboard runs on `http://localhost:3000`.

## 📸 Screenshots
*(Add screenshots of your UI, API docs, and terminal output here!)*

## 🎓 Learning Outcomes
- Designing and implementing an end-to-end ML application.
- Applying Natural Language Processing for text extraction and semantic similarity.
- Developing robust APIs using FastAPI.
- Building modern, interactive web dashboards using Next.js and Tailwind CSS.
