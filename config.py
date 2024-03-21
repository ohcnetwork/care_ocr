import os

from pathlib import Path
from dotenv import dotenv_values
import easyocr


config = dotenv_values(".env")

ROOT_DIR = Path(__file__).resolve(strict=True).parent
OPENAI_API_KEY = config.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))

READER: easyocr.Reader = easyocr.Reader(["en"])
