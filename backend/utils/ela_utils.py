from PIL import Image, ImageChops, ImageEnhance

def perform_ela(input_path, output_path, quality=90):

    original = Image.open(input_path).convert("RGB")

    # Recompress image
    temp_path = input_path + ".temp.jpg"
    original.save(temp_path, "JPEG", quality=quality)

    recompressed = Image.open(temp_path)

    # ELA difference
    ela = ImageChops.difference(original, recompressed)

    # Scale difference for visibility
    extrema = ela.getextrema()
    max_diff = max([e[1] for e in extrema]) or 1
    scale = 255.0 / max_diff

    ela = ImageEnhance.Brightness(ela).enhance(scale)
    ela.save(output_path)

    # Simple ELA score
    return float(max_diff)
