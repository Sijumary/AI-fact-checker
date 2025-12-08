import cv2
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import numpy as np

# Choose a lightweight deepfake model
VIDEO_MODEL_NAME = "sarvansh/NotUrFace-AI"

video_processor = AutoImageProcessor.from_pretrained(VIDEO_MODEL_NAME)
video_model = AutoModelForImageClassification.from_pretrained(VIDEO_MODEL_NAME)

def detect_deepfake_frame(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    inputs = video_processor(images=img, return_tensors="pt")
    with torch.no_grad():
        outputs = video_model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)[0]
    class_idx = torch.argmax(probs).item()
    confidence = float(probs[class_idx])
    label = video_model.config.id2label[class_idx]

    return label, confidence


def detect_deepfake_video(video_path, frame_interval=15):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {"error": "Could not open video"}

    frame_count = 0
    fake_count = 0
    real_count = 0
    scores = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process every nth frame
        if frame_count % frame_interval == 0:
            label, confidence = detect_deepfake_frame(frame)
            scores.append(confidence)

            if "fake" in label.lower() or "ai" in label.lower():
                fake_count += 1
            else:
                real_count += 1

        frame_count += 1

    cap.release()

    if fake_count > real_count:
        result = "AI-generated / Deepfake"
    else:
        result = "Real Video"

    overall_confidence = round(float(np.mean(scores)), 4) if scores else 0.0

    return {
        "result": result,
        "fake_frames": fake_count,
        "real_frames": real_count,
        "confidence": overall_confidence,
        "frames_checked": len(scores)
    }
