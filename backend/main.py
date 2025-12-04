import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from utils.exif_utils import extract_exif
from utils.ela_utils import perform_ela
from utils.ai_detector import detect_ai_model

UPLOAD_DIR = "backend/uploads"
PROCESSED_DIR = "backend/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.jpg"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1. EXIF extraction
    exif_data = extract_exif(file_path)

    # 2. ELA analysis
    ela_output_path = f"{PROCESSED_DIR}/{file_id}_ela.jpg"
    ela_score = perform_ela(file_path, ela_output_path)

    # 3. AI detection (REAL MODEL)
    ai_result = detect_ai_model(file_path)

    return {
        "file_id": file_id,
        "exif": exif_data,
        "ela_score": ela_score,
        "ela_image_url": f"http://localhost:8000/processed/{file_id}_ela.jpg",
        "ai_detection": ai_result
    }

# Serve processed ELA images
from fastapi.staticfiles import StaticFiles
app.mount("/processed", StaticFiles(directory="backend/processed"), name="processed")
