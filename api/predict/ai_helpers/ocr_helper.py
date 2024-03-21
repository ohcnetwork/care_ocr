import os
import io

from PIL import Image

from config import ROOT_DIR, READER


def get_ocr_data(image_content, filename):
    image_content = io.BytesIO(image_content)
    save_path = ROOT_DIR / "image"
    if not save_path.exists():
        save_path.mkdir()
    save_path = str(save_path) + "/" + filename
    Image.open(image_content).save(save_path)

    data = READER.readtext(save_path)
    data = [{"bounding_box": d[0], "text": d[1], "confidence": d[2]} for d in data]
    for d in data:
        d["bounding_box"] = [[int(x), int(y)] for x, y in d["bounding_box"]]
    os.remove(save_path)

    return data
