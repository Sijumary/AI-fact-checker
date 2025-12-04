import os
from uuid import uuid4

UPLOAD_DIR = "uploads"
ANALYSIS_DIR = "analysis"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

def save_upload_file(file):
    ext = file.filename.split(".")[-1]
    file_id = str(uuid4())
    path = f"{UPLOAD_DIR}/{file_id}.{ext}"

    with open(path, "wb") as f:
        f.write(file.file.read())

    return file_id, path
