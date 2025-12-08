import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from utils.exif_utils import extract_exif
from utils.ela_utils import perform_ela
from utils.ai_detector import detect_ai_model
from utils.video__detector import detect_deepfake_video

UPLOAD_DIR = "backend/uploads"
PROCESSED_DIR = "backend/processed"
FRAMES_DIR = "backend/frames"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

app = FastAPI()

# Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# IMAGE DETECTION
# -----------------------------
@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.jpg"

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1. EXIF extraction
    exif_data = extract_exif(file_path)

    # 2. ELA analysis
    ela_output_path = f"{PROCESSED_DIR}/{file_id}_ela.jpg"
    ela_score = perform_ela(file_path, ela_output_path)

    # 3. AI detection
    ai_result = detect_ai_model(file_path)

    return {
        "file_id": file_id,
        "exif": exif_data,
        "ela_score": ela_score,
        "ela_image_url": f"http://localhost:8000/processed/{file_id}_ela.jpg",
        "ai_detection": ai_result
    }

# -----------------------------
# VIDEO DETECTION
# -----------------------------
@app.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    video_path = f"{UPLOAD_DIR}/{file_id}.mp4"

    # Save uploaded video
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # Run AI/deepfake detection
    video_result = detect_deepfake_video(video_path)

    return {
        "video_id": file_id,
        "video_detection": video_result
    }

# -----------------------------
# Serve processed ELA images
# -----------------------------
from fastapi.staticfiles import StaticFiles
app.mount("/processed", StaticFiles(directory="backend/processed"), name="processed")
