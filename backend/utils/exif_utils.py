from PIL import Image
import piexif

def extract_exif(filepath):
    try:
        img = Image.open(filepath)
        exif_dict = piexif.load(img.info.get("exif", b""))
        cleaned = {}

        for ifd in exif_dict:
            for tag in exif_dict[ifd]:
                try:
                    cleaned[str(tag)] = str(exif_dict[ifd][tag])
                except:
                    pass

        return cleaned

    except Exception as e:
        return {"error": str(e)}
