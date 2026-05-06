# Interview Preparation

## 1. Explain your project.
**Answer:** In this project, I built an end-to-end Python-based tool that automatically screens resumes against a job description. The system extracts text from resumes, extracts skills via NLP, computes semantic similarity using Transformer models, calculates a composite matching score, and ranks candidates. I wrapped this in a FastAPI backend and built a premium Next.js dashboard with visual analytics to help HR teams easily interpret the results.

## 2. What problem does this project solve?
**Answer:** It solves the bottleneck of manual resume screening. When hundreds of applications arrive, manually filtering them is slow and biased. My tool allows recruiters to instantly identify the candidates that best match the required skills and experience.

## 3. What technologies did you use?
**Answer:** I used Python with libraries like `scikit-learn` and `sentence-transformers` for the machine learning components. `PyPDF2` was used for text extraction. The backend was built with `FastAPI` and `SQLite`, and the frontend dashboard was built using `Next.js`, `Tailwind CSS`, and `Recharts` for graph analytics.

## 4. How does your tool screen resumes?
**Answer:** It follows a pipeline: ingestion, extraction, and scoring. First, it extracts unstructured text. Then, it uses fuzzy matching to identify specific skills and regex to find years of experience. Finally, it uses semantic embeddings and a rule-based formula to score how well the candidate matches the Job Description.

## 5. What is TF-IDF and why would you use it vs Dense Embeddings?
**Answer:** TF-IDF (Term Frequency-Inverse Document Frequency) measures how important a word is in a document. It's great for exact keyword matching. However, in my project, I utilized dense embeddings (`all-MiniLM-L6-v2`) which understand context. So if the JD says "Machine Learning" and the resume says "Deep Learning", embeddings recognize they are conceptually similar, whereas TF-IDF might miss it.

## 6. What is cosine similarity?
**Answer:** Cosine similarity measures the angle between two vectors. In my project, both the resume and the job description are converted into numerical vectors (embeddings). Cosine similarity tells us how semantically close these two text blocks are, giving a score between 0 and 1.

## 7. What kind of output does your project generate?
**Answer:** The API generates a JSON array of ranked candidates with a composite score and specific reasons (e.g., matched 3/4 must-have skills, 80% semantic match). The frontend visualizes this using a Bar Chart and a detailed list with visual flags.

## 8. What challenges did you face?
**Answer:** The main challenge was unstructured data. Resumes come in wild formats. Normalizing the text and dealing with edge cases where candidates format their experience strangely required robust regex and fuzzy string matching.

## 9. How can this project be improved further?
**Answer:** I could integrate a Large Language Model (like GPT-4 or Gemini) specifically to summarize the "Why" behind the ranking, instead of relying purely on a formulaic explanation. Additionally, integrating OCR (Tesseract) would allow parsing image-based PDFs.

## 10. How would you explain this project to a non-technical person?
**Answer:** I created a digital assistant that reads hundreds of resumes in seconds, compares them to what the manager is looking for, and provides a top 10 list with charts explaining exactly why these people are the best fit.
