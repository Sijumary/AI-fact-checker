import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

processor = AutoImageProcessor.from_pretrained("NYUAD-ComNets/NYUAD_AI-generated_images_detector")
model = AutoModelForImageClassification.from_pretrained("NYUAD-ComNets/NYUAD_AI-generated_images_detector")

def detect_ai_model(image_path):
    img = Image.open(image_path).convert("RGB")

    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)[0]
    class_idx = torch.argmax(probs).item()
    confidence = float(probs[class_idx])

    label = model.config.id2label[class_idx]

    # Custom labeling
    if "ai" in label.lower():
        result = "AI-generated"
    else:
        result = "Real"

    return {
        "predicted_label": label,
        "result": result,
        "confidence": round(confidence, 4)
    }