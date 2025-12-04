# AI Fact Checker

A proof-of-concept application to analyze images for authenticity.  
Built with **FastAPI** (backend) and **React + Vite** (frontend).  
Detects image manipulations via **EXIF metadata**, **Error Level Analysis (ELA)**, and includes a **Deepfake / AI-generated image detection stub**.

---

## Features

- Upload images via frontend
- Extract EXIF metadata (camera, timestamp, software)
- Perform **Error Level Analysis (ELA)** to highlight edits
- Detect whether an image is **Real / AI-generated / Deepfake** (stub logic for now)
- Fully local, no cloud storage required

---

## Folder Structure

ai-fact-checker/
│
├─ backend/
│ ├─ main.py # FastAPI backend
│ ├─ utils/
│ │ ├─ exif_utils.py # EXIF extraction
│ │ └─ ela_utils.py # ELA computation
│ ├─ uploads/ # Uploaded images (ignored in git)
│ └─ processed/ # Processed ELA images (ignored in git)
│
├─ frontend/
│ ├─ package.json
│ ├─ vite.config.js
│ └─ src/
│ ├─ main.jsx
│ └─ App.jsx # React frontend UI
│
└─ .gitignore


---

## Prerequisites

- Python 3.10+  
- Node.js 18+  
- npm 9+  

---

## Setup & Run

### 1️⃣ Backend (FastAPI)

```bash
cd backend
python -m venv .venv           # optional but recommended
source .venv/Scripts/activate  # Windows
# OR on Git Bash / Linux: source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000


API will run at: http://localhost:8000

Swagger docs: http://localhost:8000/docs

2️⃣ Frontend (React + Vite)
cd frontend
npm install
npm run dev


Frontend runs at: http://localhost:3000

Open in browser and upload an image to see results

Usage

Open frontend: http://localhost:3000

Select an image to upload

Click Upload

View:

EXIF metadata (camera info, timestamp, software)

ELA heatmap highlighting edits

AI / Deepfake detection result
