import os
import uuid
import io
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.exif_utils import extract_exif
from utils.ela_utils import perform_ela
from PIL import Image, ImageChops, ImageEnhance

# Directories for storage
UPLOAD_DIR = "backend/uploads"
PROCESSED_DIR = "backend/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# FastAPI app
app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Existing endpoint: /analyze-image
# -------------------------------
@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    # Save file locally
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.jpg"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract EXIF
    exif_data = extract_exif(file_path)

    # Run simple ELA
    ela_output_path = f"{PROCESSED_DIR}/{file_id}_ela.jpg"
    ela_score = perform_ela(file_path, ela_output_path)

    return {
        "file_id": file_id,
        "exif": exif_data,
        "ela_score": ela_score,
        "ela_image_url": f"http://localhost:8000/processed/{file_id}_ela.jpg"
    }

# ------------------------------------------
# New endpoint: /upload-base64 (ELA in base64)
# ------------------------------------------
@app.post("/upload-base64")
async def upload_base64(file: UploadFile = File(...)):
    # Read image bytes
    content = await file.read()

    # Save locally (optional)
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.jpg"
    with open(file_path, "wb") as f:
        f.write(content)

    # Extract EXIF
    exif_data = extract_exif(file_path)

    # Generate ELA image
    pil_img = Image.open(io.BytesIO(content)).convert("RGB")

    # Recompress to simulate JPEG artifacts
    buffer = io.BytesIO()
    pil_img.save(buffer, "JPEG", quality=85)
    buffer.seek(0)
    recompressed = Image.open(buffer)

    # ELA difference
    ela_img = ImageChops.difference(pil_img, recompressed)
    ela_img = ImageEnhance.Brightness(ela_img).enhance(10)

    # Encode ELA image as base64
    out_buf = io.BytesIO()
    ela_img.save(out_buf, format="PNG")
    ela_base64 = base64.b64encode(out_buf.getvalue()).decode("utf-8")

    return {
        "file_id": file_id,
        "exif": exif_data,
        "ela_base64": ela_base64
    }

# -------------------------------
# Serve processed images via URL
# -------------------------------
app.mount("/processed", StaticFiles(directory="backend/processed"), name="processed")
