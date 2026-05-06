# GitHub Upload Steps & Proof Building Strategy

## Day-by-Day Proof Strategy

Building a portfolio piece is about showing the *process*, not just the final result.

### Day 1: Project Setup
1. Create your GitHub repository: `Automated-Resume-Screening-Pipeline`
2. Description: "End-to-End NLP Pipeline for automated resume parsing, semantic similarity scoring, and candidate ranking."
3. Tags: `python`, `nlp`, `fastapi`, `nextjs`, `machine-learning`, `resume-parser`
4. Commit: `Initial commit: Added folder structure and empty files.`

### Day 2: Ingestion & Extraction
1. Write the PyPDF2/DOCX parsing logic in `src/ingest.py`.
2. Write the fuzzy matching logic in `src/extract.py`.
3. Commit: `feat: Added PDF/DOCX ingestion and fuzzy skill extraction module.`
4. Screenshot: Take a screenshot of the terminal printing out a parsed resume's JSON structure.

### Day 3: Feature Engineering & Scoring
1. Complete `src/features.py` and `src/rank.py`.
2. Commit: `feat: Implemented Sentence-Transformer embeddings and composite ranking formula.`

### Day 4: API Development
1. Build `api/app.py`.
2. Commit: `feat: Wrapped ML pipeline in FastAPI with endpoints for jobs and resume uploads.`
3. Screenshot: Screenshot of the FastAPI Swagger UI (`http://localhost:8000/docs`).

### Day 5: Next.js Dashboard
1. Build the dashboard in `apps/web`.
2. Commit: `feat: Created Next.js dashboard with Recharts for visual analytics.`
3. Screenshot: Take a beautiful, full-screen capture of the dashboard showing the candidate rankings and bar chart. Save to `docs/dashboard.png`.

### Day 6: Documentation
1. Upload this `README.md` and the `docs/` folder.
2. Commit: `docs: Added comprehensive README, architecture diagrams, and simulation guide.`

## Git Commands to Push Code
Open your terminal in the `Automated-Resume-Screening-Tool` folder:

```bash
git init
git add .
git commit -m "feat: Completed full ML resume screening pipeline and dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Automated-Resume-Screening-Pipeline.git
git push -u origin main
```
