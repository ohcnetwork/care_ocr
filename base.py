from pathlib import Path
import easyocr

# print("-"*20)
# print("Initializeds")
# print("-"*20)

ROOT_DIR = Path(__file__).resolve(strict=True).parent

MODEL_PATH = str(ROOT_DIR / "model/best.pt")

YOLO_PATH = str(ROOT_DIR / "yolov5")

reader = easyocr.Reader(['en'])