from pathlib import Path
import easyocr
from dotenv import dotenv_values
import os

config = dotenv_values(".env")


# print("-"*20)
# print("Initializeds")
# print("-"*20)

ROOT_DIR = Path(__file__).resolve(strict=True).parent

MODEL_PATH = str(ROOT_DIR / "model/best.pt")

YOLO_PATH = str(ROOT_DIR / "yolov5")

reader = easyocr.Reader(['en'])

OPENAI_API_KEY = config.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))